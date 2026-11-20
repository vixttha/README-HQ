"""Build or verify a deterministic feature evidence graph from a pinned Git commit."""

import argparse
import asyncio
from collections import Counter
from contextlib import contextmanager
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from importlib.metadata import version
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

from graphify.build import build_from_json
from graphify.export import to_json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from github_provenance import COMMIT, REPOSITORY, github_json, verify_pull_request

TEMPLATE_VERSION = "v0.0.8"
RELATIONS = ("documented_in", "changed_in", "tested_by")
OPTIONAL_RELATION = "implemented_in"
FEATURE_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
MAX_SOURCE_BYTES = 1_000_000


def flex_text(value):
    return all(char.isprintable() or (
        char == "\u200d" and 0 < index < len(value) - 1
        and ord(value[index - 1]) >= 0x2300 and ord(value[index + 1]) >= 0x2300
    ) for index, char in enumerate(value))


def valid_branch(value):
    return isinstance(value, str) and bool(value) and subprocess.run(
        ["git", "check-ref-format", f"refs/heads/{value}"], capture_output=True, check=False,
    ).returncode == 0


def read_manifest(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{path}: duplicate object key {key!r}")
            result[key] = value
        return result

    return json.loads(path.read_bytes(), object_pairs_hook=unique)


def valid_path(path):
    if not isinstance(path, str) or not 0 < len(path) <= 240 or not path.isprintable():
        return False
    candidate = PurePosixPath(path)
    return (
        not candidate.is_absolute() and candidate.as_posix() == path
        and not any(part in {".", "..", ".git"} for part in path.split("/"))
        and not any(char in path for char in "\\:")
    )


def validate_manifest(data):
    required = {"repository", "source_commit", "title", "features"}
    if not isinstance(data, dict) or set(data) - {"pull_request", "source_files"} != required:
        raise ValueError("Expected repository, source_commit, title, features and optional pull_request and source_files")
    if not isinstance(data["repository"], str) or not REPOSITORY.fullmatch(data["repository"]):
        raise ValueError("Expected a GitHub owner/repository")
    if not isinstance(data["source_commit"], str) or not COMMIT.fullmatch(data["source_commit"]):
        raise ValueError("Expected a full Git commit SHA")
    title = data["title"]
    if not isinstance(title, str) or not title.strip() or len(title) > 120 or not flex_text(title):
        raise ValueError("Invalid map title")
    inventory = data.get("source_files", [])
    if (
        not isinstance(inventory, list) or len(inventory) > 64
        or not all(valid_path(path) for path in inventory)
        or len(inventory) != len(set(inventory))
    ):
        raise ValueError("Expected up to 64 unique source file paths")
    if "pull_request" in data:
        pr = data["pull_request"]
        if (
            not isinstance(pr, dict) or set(pr) != {"number", "source_branch"}
            or type(pr["number"]) is not int or pr["number"] < 1
            or not valid_branch(pr["source_branch"])
        ):
            raise ValueError("Expected a positive PR number and a plain source branch name")
    features = data["features"]
    if not isinstance(features, list) or len(features) > 32:
        raise ValueError("Expected at most 32 features")
    ids = set()
    for feature in features:
        if not isinstance(feature, dict) or set(feature) - {OPTIONAL_RELATION} != {"id", "label", *RELATIONS}:
            raise ValueError("Expected an ID, label and reference lists")
        identity, label = feature["id"], feature["label"]
        if (
            not isinstance(identity, str) or len(identity) > 80 or not FEATURE_ID.fullmatch(identity)
            or identity in ids
            or not isinstance(label, str) or not label.strip() or len(label) > 120 or not flex_text(label)
        ):
            raise ValueError("Invalid or duplicate feature")
        ids.add(identity)
        for relation in (*RELATIONS, OPTIONAL_RELATION):
            if relation not in feature:
                continue
            refs = feature[relation]
            if not isinstance(refs, list) or not 1 <= len(refs) <= 12:
                raise ValueError(f"{identity}: {relation} requires one to twelve references")
            seen = set()
            for ref in refs:
                if not isinstance(ref, dict) or set(ref) - {"line"} != {"path", "anchor"}:
                    raise ValueError("Expected a path and source anchor")
                path, anchor = ref["path"], ref["anchor"]
                if (
                    not valid_path(path)
                    or not isinstance(anchor, str) or not 0 < len(anchor) <= 500
                    or not flex_text(anchor) or anchor.strip() != anchor
                    or ("line" in ref and (type(ref["line"]) is not int or ref["line"] < 1))
                    or (path, anchor, ref.get("line")) in seen
                ):
                    raise ValueError("Invalid or duplicate source link")
                seen.add((path, anchor, ref.get("line")))
    return data


def git(*args):
    return subprocess.check_output(["git", "--no-replace-objects", *args])


def source_blob(commit, path):
    entries = git("--literal-pathspecs", "ls-tree", "-z", commit, "--", path).split(b"\0")
    header, _, name = entries[0].partition(b"\t")
    if name.decode("utf-8") != path or not header:
        raise ValueError(f"{path}: no entry at the pinned source commit")
    mode, _, blob = header.decode().split()
    if mode not in {"100644", "100755"}:
        raise ValueError(f"{path}: expected regular Git blob, got mode {mode}")
    size = int(git("cat-file", "-s", blob))
    if not 0 <= size <= MAX_SOURCE_BYTES:
        raise ValueError(f"{path}: source blob size exceeds limit")
    return git("cat-file", "blob", blob)


def source_lines(commit, path):
    body = source_blob(commit, path)
    try:
        return body.decode("utf-8").split("\n"), hashlib.sha256(body).hexdigest()
    except UnicodeError as error:
        raise ValueError(f"{path}: source anchors require UTF-8 text") from error


def locate(lines, anchor, path, coordinate=None):
    if coordinate is not None:
        if coordinate <= len(lines) and lines[coordinate - 1].strip() == anchor:
            return coordinate
        raise ValueError(f"{path}: reviewed anchor does not match line {coordinate}")
    matches = [i for i, line in enumerate(lines, 1) if line.strip() == anchor]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one match in {path}, found {len(matches)}: {anchor}")
    return matches[0]


def origin_repository():
    origin = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
    if origin.returncode:
        return None
    value = origin.stdout.strip()
    if value.startswith("git@github.com:"):
        return value.split(":", 1)[1].removesuffix(".git")
    url = urlsplit(value)
    return url.path.strip("/").removesuffix(".git") if url.hostname == "github.com" else None


def publication_path(destination):
    return destination.with_name(f".{destination.name}.publish-lock")


@contextmanager
def publication_guard(destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    state = publication_path(destination)
    state.mkdir(exist_ok=True)
    mutex = state / "writer"
    with mutex.open("a+b") as handle:
        handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            raise ValueError(f"{destination}: a publisher is already active") from error
        previous = state / "previous"
        if destination.is_symlink() or (destination.exists() and not destination.is_dir()):
            raise ValueError(f"{destination}: expected an output directory")
        if previous.exists():
            if destination.exists():
                shutil.rmtree(previous)
            else:
                os.replace(previous, destination)
        yield previous


def replace_directory(staged, destination, previous):
    if destination.exists():
        os.replace(destination, previous)
    try:
        os.replace(staged, destination)
    except OSError:
        if previous.exists():
            os.replace(previous, destination)
        raise
    if previous.exists():
        shutil.rmtree(previous)


def publish_directory(staged, destination):
    with publication_guard(destination) as previous:
        replace_directory(staged, destination, previous)


def publish_pair(output, files):
    with publication_guard(output) as previous:
        with tempfile.TemporaryDirectory(dir=output.parent) as staging:
            folder = Path(staging) / "pair"
            if output.exists():
                shutil.copytree(output, folder, symlinks=True)
            else:
                folder.mkdir()
            for name, data in files.items():
                target = folder / name
                if target.is_symlink() or (target.exists() and not target.is_file()):
                    raise ValueError(f"{name}: cannot replace a non-regular output")
                target.write_bytes(data)
            replace_directory(folder, output, previous)


def read_published_pair(output):
    folders = (output, publication_path(output) / "previous")
    for _ in range(4):
        for folder in folders:
            try:
                graph = (folder / "graph.json").read_bytes()
                receipt = (folder / "receipt.json").read_bytes()
            except FileNotFoundError:
                continue
            data = json.loads(receipt)
            if hashlib.sha256(graph).hexdigest() == data.get("graph_sha256"):
                return {"graph.json": graph, "receipt.json": receipt}
    raise ValueError(f"{output}: no complete Graphify generation could be read")


def build(manifest, folder):
    commit = manifest["source_commit"]
    if git("cat-file", "-t", commit).strip() != b"commit":
        raise ValueError("Pinned SHA must identify a commit")
    nodes, edges = {}, []
    cache, inventory_hashes, evidence, destinations = {}, {}, {}, {}
    inventory = set(manifest.get("source_files", []))
    linked_refs = set()
    root = "source:" + commit

    def add_node(identity, label, kind, path="", line=None):
        nodes[identity] = {
            "id": identity, "label": label, "file_type": kind,
            "source_file": path, "source_location": f"L{line}" if line else None,
        }

    def add_edge(start, end, relation, path="", line=None):
        edges.append({
            "source": start, "target": end, "relation": relation, "source_file": path,
            "source_location": f"L{line}" if line else None, "confidence": "EXTRACTED",
            "confidence_score": 1.0, "weight": 1.0,
        })

    add_node(root, manifest["title"], "concept")
    for path in sorted(inventory):
        inventory_hashes[path] = hashlib.sha256(source_blob(commit, path)).hexdigest()
        add_node("file:" + path, path, "file", path)
        add_edge(root, "file:" + path, "contains_source", path)
    for feature in sorted(manifest["features"], key=lambda feature: feature["id"]):
        feature_id = "feature:" + feature["id"]
        evidence[feature_id] = {}
        destinations[feature_id] = []
        add_node(feature_id, feature["label"], "concept")
        add_edge(root, feature_id, "contains_feature")
        for relation in (*RELATIONS, OPTIONAL_RELATION):
            if relation not in feature:
                continue
            refs = sorted(feature[relation], key=lambda ref: (ref["path"], ref["anchor"], ref.get("line", 0)))
            evidence[feature_id][relation] = len(refs)
            resolved_destinations = set()
            for ref in refs:
                path, anchor = ref["path"], ref["anchor"]
                if path not in cache:
                    cache[path] = source_lines(commit, path)
                lines, _ = cache[path]
                line = locate(lines, anchor, path, ref.get("line"))
                ref_id = f"{relation}:{path}:L{line}"
                if ref_id in resolved_destinations:
                    raise ValueError(f"{feature_id} {relation}: duplicate resolved destination {path}:L{line}")
                resolved_destinations.add(ref_id)
                kind = "code" if relation in ("tested_by", OPTIONAL_RELATION) else "document"
                add_node(ref_id, f"{path} L{line}", kind, path, line)
                add_edge(feature_id, ref_id, relation, path, line)
                destinations[feature_id].append([relation, ref_id, path, f"L{line}"])
                if path in inventory and ref_id not in linked_refs:
                    add_edge(ref_id, "file:" + path, "located_in", path, line)
                    linked_refs.add(ref_id)

    graph = build_from_json(
        {"nodes": list(nodes.values()), "edges": edges}, directed=True, dedup=False,
    )
    graph.graph.update(template_version=TEMPLATE_VERSION, scope="feature-evidence")
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "graph.json"
    to_json(graph, {0: list(graph)}, str(path), built_at_commit=commit)
    receipt = {
        "schema_version": 1,
        "template_version": TEMPLATE_VERSION,
        "repository": manifest["repository"],
        "source_commit": commit,
        "pull_request": manifest.get("pull_request"),
        "scope": "feature-evidence",
        "repository_provenance": "unverified-local-source",
        "graphify_version": version("graphifyy"),
        "graph_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "feature_links": evidence,
        "feature_destinations": destinations,
        "source_files": sorted(inventory),
        "source_sha256": dict(sorted({**inventory_hashes, **{key: value[1] for key, value in cache.items()}}.items())),
    }
    return path, receipt


async def verify_mcp(graph, receipt):
    if hashlib.sha256(graph.read_bytes()).hexdigest() != receipt["graph_sha256"]:
        raise ValueError("Graph digest differs from the expected receipt")
    saved = json.loads(graph.read_bytes())
    actual = {}
    for edge in saved["links"]:
        if edge["source"] in receipt["feature_destinations"]:
            actual.setdefault(edge["source"], []).append([
                edge["relation"], edge["target"], edge["source_file"], edge["source_location"],
            ])
    if {key: sorted(items) for key, items in actual.items()} != {
        key: sorted(items) for key, items in receipt["feature_destinations"].items()
    }:
        raise ValueError("Graph evidence destinations differ from the pinned manifest")

    params = StdioServerParameters(command=sys.executable, args=["-m", "graphify.serve", str(graph)])
    async with asyncio.timeout(120), stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()

            async def query(tool, args):
                result = await session.call_tool(tool, args)
                if result.is_error:
                    raise ValueError("Graphify MCP call failed: " + tool)
                return "\n".join(item.text for item in result.content if item.type == "text")

            stats = await query("graph_stats", {})
            expected = {
                f"Nodes: {receipt['nodes']}", f"Edges: {receipt['edges']}",
                f"Built at commit: {receipt['source_commit']}",
            }
            if not expected <= set(stats.splitlines()):
                raise ValueError("Graphify MCP returned different graph statistics or source SHA")
            for node, targets in receipt["feature_destinations"].items():
                for relation in sorted({item[0] for item in targets}):
                    response = await query("get_neighbors", {
                        "node_id": node, "relation_filter": relation, "token_budget": 16000,
                    })
                    if any(token.startswith("... (truncated") for token in response.splitlines()):
                        raise ValueError(f"Graphify MCP readback was truncated for {node}")
                    expected_rows = Counter(
                        (f"{path} {line}", path, line)
                        for relationship, _, path, line in targets if relationship == relation
                    )
                    actual_rows = Counter()
                    pattern = re.compile(r"^  --> (.+) \[" + re.escape(relation) + r"\] \[[^\]]+\] at=(.+):(L[0-9]+)$")
                    for row in response.splitlines():
                        if match := pattern.fullmatch(row):
                            actual_rows[match.groups()] += 1
                    if actual_rows != expected_rows:
                        raise ValueError(f"Graphify MCP {node} {relation}: evidence target mismatch")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--verify-repository", action="store_true", help="Verify the source SHA against the GitHub repository")
    parser.add_argument("--verify-pr", action="store_true", help="Print a separate live GitHub observation")
    parser.add_argument("--check", action="store_true", help="Rebuild and compare the existing output bytes")
    args = parser.parse_args()
    manifest = validate_manifest(read_manifest(args.manifest))
    provenance = "unverified-local-source"
    origin = origin_repository()
    if origin is not None and origin.casefold() != manifest["repository"].casefold():
        parser.error("manifest repository disagrees with the GitHub origin")
    if args.verify_repository:
        commit = manifest["source_commit"]
        observation = github_json(manifest["repository"], f"commits/{commit}")
        if observation.get("sha") != commit:
            parser.error("GitHub did not establish the claimed repository source")
        provenance = "github-commit-observed"
    if args.verify_pr:
        if "pull_request" not in manifest:
            parser.error("--verify-pr requires pull_request in the manifest")
        observation = verify_pull_request(
            manifest["repository"], manifest["source_commit"], manifest["pull_request"],
        )
        print("GitHub pull request provenance:\n" + json.dumps(observation, indent=2))

    with tempfile.TemporaryDirectory() as temporary:
        path, receipt = build(manifest, Path(temporary))
        asyncio.run(verify_mcp(path, receipt))
        receipt["mcp_verified"] = True
        receipt["repository_provenance"] = provenance
        files = {"graph.json": path.read_bytes(), "receipt.json": (json.dumps(receipt, indent=2) + "\n").encode()}
        if args.check:
            published = read_published_pair(args.output)
            for name, expected in files.items():
                if published[name] != expected:
                    raise ValueError("Deterministic rebuild differs: " + name)
        else:
            publish_pair(args.output, files)
    print(f"Graphify MCP verified {receipt['nodes']} nodes and {receipt['edges']} edges at {receipt['source_commit']}")


if __name__ == "__main__":
    main()
