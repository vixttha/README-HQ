"""Verify the documentation-only technique library and export its navigation graph."""

import argparse
import asyncio
import hashlib
import json
import os
import posixpath
import re
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt


FILES = {"README.md", "RESEARCH.md", "TEMPLATES.md"}
PARSER = MarkdownIt("commonmark").enable("table")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args]).decode().strip()


def load(root, expected_commit):
    require(git(root, "rev-parse", "HEAD") == expected_commit, "Checkout commit mismatch")
    paths = set(git(root, "ls-tree", "-r", "--name-only", "HEAD").splitlines())
    require(paths == FILES, f"Unexpected documentation inventory: {sorted(paths)}")
    return {path: (root / path).read_text(encoding="utf-8") for path in sorted(paths)}


def scan(documents):
    headings, document_links, literals = {}, [], {}
    for path, text in documents.items():
        blocks = PARSER.parse(text)
        anchors, codes = set(), []
        for i, token in enumerate(blocks):
            if token.type == "heading_open":
                title = blocks[i + 1].content
                anchor = re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")
                require(anchor and anchor not in anchors, f"{path}: ambiguous heading {title}")
                anchors.add(anchor)
            if token.type == "inline":
                for child in token.children:
                    if child.type == "link_open":
                        document_links.append((path, token.map[0] + 1, child.attrGet("href")))
                    if child.type == "code_inline":
                        codes.append(child.content)
        headings[path] = anchors
        literals[path] = codes
    return headings, document_links, literals


def navigation(documents):
    headings, document_links, _ = scan(documents)
    routes = []
    for source, line, href in document_links:
        url = urlsplit(href)
        if url.scheme in {"https", "http"} and url.netloc:
            continue
        require(not url.scheme and not url.netloc and not url.path.startswith("/"), f"{source}:{line}: use a relative link")
        target = posixpath.normpath(posixpath.join(posixpath.dirname(source), unquote(url.path))) if url.path else source
        require(target in documents, f"{source}:{line}: missing link target {target}")
        anchor = unquote(url.fragment)
        require(not anchor or anchor in headings[target], f"{source}:{line}: missing anchor {anchor}")
        routes.append((source, line, target + ("#" + anchor if anchor else "")))
    return routes


def controlled_record_trial(documents):
    _, _, literals = scan(documents)
    examples = [literal for literal in literals["TEMPLATES.md"] if literal.startswith("[Relative navigation]")]
    require(len(examples) == 2, "Expected both index and combination link examples")
    fixture = dict(documents)
    fixture["README.md"] += "\n\n" + examples[0] + "\n"
    fixture["techniques/relative-navigation.md"] = "# Relative navigation\n"
    fixture["combinations/quickstart.md"] = "# Quickstart\n\n" + examples[1] + "\n"
    routes = navigation(fixture)
    linked_from = {source for source, _, target in routes if target == "techniques/relative-navigation.md"}
    require(linked_from == {"README.md", "combinations/quickstart.md"}, "Template examples did not share a target")
    for substitution, diagnostic in (("README.md#missing-heading", "missing anchor"), ("MISSING.md", "missing link target")):
        broken = {**documents, "README.md": documents["README.md"].replace("(RESEARCH.md)", f"({substitution})", 1)}
        try:
            navigation(broken)
        except ValueError as error:
            require(diagnostic in str(error), str(error))
        else:
            raise ValueError(f"Missing expected {diagnostic} diagnostic")


async def verify_graph(root, commit, routes, directory):
    from graphify.build import build_from_json
    from graphify.detect import detect
    from graphify.export import to_json
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    detected = {Path(path).name for path in detect(root.resolve())["files"]["document"]}
    require(detected == FILES, f"Graphify found a different document set: {detected}")
    node_ids = FILES | {target for _, _, target in routes}
    nodes = [
        {"id": name, "label": name, "file_type": "document", "source_file": name.split("#", 1)[0]}
        for name in sorted(node_ids)
    ]
    edges = {}
    for source, line, target in routes:
        edges.setdefault((source, target), {
            "source": source, "target": target, "relation": "links_to",
            "source_file": source, "source_location": f"L{line}",
            "confidence": "EXTRACTED", "confidence_score": 1.0, "weight": 1.0,
        })
    graph = build_from_json({"nodes": nodes, "edges": list(edges.values())}, directed=True, dedup=False)
    path = directory / "graphify-navigation.json"
    to_json(graph, {0: list(graph)}, str(path), built_at_commit=commit)
    saved = json.loads(path.read_bytes())
    actual = {(edge["source"], edge["target"]) for edge in saved["links"]}
    require(actual == set(edges), "Graphify export changed the document routes")

    params = StdioServerParameters(command=sys.executable, args=["-m", "graphify.serve", str(path)])
    async with asyncio.timeout(45), stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            stats = await session.call_tool("graph_stats", {})
            output = "\n".join(block.text for block in stats.content if block.type == "text")
            expected = {f"Nodes: {len(nodes)}", f"Edges: {len(edges)}", f"Built at commit: {commit}"}
            require(not stats.is_error and expected <= set(output.splitlines()), f"Unexpected Graphify MCP stats: {output}")
            for source in sorted(FILES):
                result = await session.call_tool("get_neighbors", {"node_id": source, "relation_filter": "links_to"})
                output = "\n".join(block.text for block in result.content if block.type == "text")
                found = set(re.findall(r"^  --> (.+?) \[links_to\]", output, re.MULTILINE))
                targets = {target for start, target in edges if start == source}
                require(not result.is_error and found == targets, f"Graphify MCP routes differ for {source}: {output}")
    return {
        "version": version("graphifyy"), "nodes": len(nodes), "edges": len(edges),
        "mcp_verified": True, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("baseline_sha")
    parser.add_argument("candidate_sha")
    parser.add_argument("output", type=Path)
    parser.add_argument("--graphify", action="store_true")
    args = parser.parse_args()

    baseline = load(args.baseline, args.baseline_sha)
    candidate = load(args.candidate, args.candidate_sha)
    require("The catalog is empty." not in baseline["README.md"], "Baseline no longer reproduces the empty-state gap")
    require("The catalog is empty." in candidate["README.md"], "Reader cannot identify the empty catalog")
    require("Use a populated library" in candidate["README.md"], "Catalog use needs an explicit state")
    require("pass or fail" in candidate["TEMPLATES.md"], "Evidence records must show the check result")
    require("discovery, execution, and handoff separately" in candidate["RESEARCH.md"], "Evidence scope is not explicit")
    baseline_routes = navigation(baseline)
    candidate_routes = navigation(candidate)
    require(len(baseline_routes) == len(candidate_routes) == 7, "Unexpected standalone route coverage")
    controlled_record_trial(candidate)

    args.output.mkdir(parents=True, exist_ok=True)
    result = {
        "candidate": args.candidate_sha, "baseline": args.baseline_sha,
        "run_id": os.environ.get("GITHUB_RUN_ID"), "attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "runner_os": os.environ.get("RUNNER_OS"), "documents": sorted(FILES),
        "relative_links": len(candidate_routes), "template_link_trials": 2, "broken_link_controls": 2,
        "document_sha256": {path: hashlib.sha256(subprocess.check_output(["git", "-C", str(args.candidate), "show", f"HEAD:{path}"])).hexdigest() for path in sorted(FILES)},
        "git_blob": {path: git(args.candidate, "rev-parse", f"HEAD:{path}") for path in sorted(FILES)},
        "graphify": asyncio.run(verify_graph(args.candidate, args.candidate_sha, candidate_routes, args.output)) if args.graphify else None,
    }
    (args.output / "verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
