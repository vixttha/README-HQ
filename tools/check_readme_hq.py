"""Check README HQ or audit the selected README in another Git repository."""

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import parse_qs, unquote, urlsplit

from hq_data import GitTree, REPOSITORY, SHA, parse_json, read_json
from hq_navigation import MARKDOWN, check_document, parse_markdown, readme_path, suffix


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "f50e3749dab90ddfe35894284d1660097a1fb1a8"
INVENTORY_SHA256 = "d628a1c29fea09fff6063bdb85368a6b2d6969025161b1928d82838a2980cfbb"
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
VERSION = re.compile(r"v[0-9]+(?:\.[0-9]+){2,}")
SOURCE_SPAN = re.compile(r"L[1-9]\d*(?:-L[1-9]\d*)?")
MAX_README_BYTES = 500 * 1024


def normalize(value):
    return "".join(char for char in unicodedata.normalize("NFKC", value).casefold() if char.isalnum())


def evidence_identity(item):
    if not isinstance(item, dict) or not isinstance(item.get("url"), str):
        raise ValueError("evidence requires a source URL")
    if item.get("visibility", "public") != "public":
        raise ValueError("only public evidence belongs in the shared registry")
    url = urlsplit(item["url"])
    parts = unquote(url.path).strip("/").split("/", 4)
    repo = "/".join(parts[:2])
    if (url.scheme != "https" or url.netloc.lower() != "github.com" or len(parts) != 5
            or not REPOSITORY.fullmatch(repo) or parts[2] != "blob" or not SHA.fullmatch(parts[3])
            or any(x in {"", ".", ".."} for x in parts[4].split("/"))):
        raise ValueError("evidence requires an immutable public GitHub blob URL")
    if url.fragment and not SOURCE_SPAN.fullmatch(url.fragment):
        raise ValueError("invalid evidence source span")
    return repo.lower(), parts[3], parts[4]


def check_evidence(item, tree):
    identity = evidence_identity(item)
    if item.get("status") == "observed":
        return identity
    if item.get("status") != "verified":
        raise ValueError("invalid evidence status")
    receipt_path = item.get("receipt")
    if not isinstance(receipt_path, str) or not receipt_path.startswith("evidence/public/"):
        raise ValueError("verified evidence requires a durable reviewed run receipt")
    receipt = parse_json(tree.read(receipt_path), receipt_path)
    fields = ("source_repository", "source_commit", "source_path", "source_span",
              "environment", "run_url", "source_sha256", "expected", "observed")
    if (
        any(not isinstance(receipt.get(key), str) or not receipt[key].strip() for key in fields)
        or receipt.get("result") != "pass" or receipt.get("visibility") != "public"
        or (receipt["source_repository"].lower(), receipt["source_commit"], receipt["source_path"]) != identity
        or receipt["source_span"] != urlsplit(item["url"]).fragment
        or not re.fullmatch(r"[0-9a-f]{64}", receipt["source_sha256"])
        or not re.fullmatch(r"https://github\.com/[^/]+/[^/]+/actions/runs/\d+(?:/job/\d+)?", receipt["run_url"])
        or receipt["expected"] != receipt["observed"]
    ):
        raise ValueError("run receipt does not establish the stated source and result")
    return identity


def check_registry(errors, tree=None):
    tree = tree or GitTree(ROOT)
    path = "techniques/registry.json"
    data = parse_json(tree.read(path), path)
    records = data.get("techniques")
    if type(data.get("schema")) is not int or data["schema"] != 1 or not isinstance(records, list) or not records:
        errors.append("technique registry must use integer schema 1 and a non-empty record array")
        return []
    checked_sources = {
        tuple(item[:3]) for item in parse_json(
            tree.read("techniques/public-source-inventory.json"), "public source inventory"
        )
    }
    keys = ("title", "problem", "practice", "outcome")
    names, mechanisms, ids = {}, {}, set()
    for record in records:
        slug = record.get("id") if isinstance(record, dict) else None
        if not isinstance(slug, str) or not SLUG.fullmatch(slug) or slug in ids:
            errors.append(f"invalid or duplicate technique ID: {slug!r}")
            continue
        ids.add(slug)
        outcome_key, status = record.get("outcome_key"), record.get("status")
        aliases, items = record.get("aliases"), record.get("evidence")
        if (
            not isinstance(outcome_key, str) or not SLUG.fullmatch(outcome_key)
            or status not in ("active", "retired")
            or any(not isinstance(record.get(key), str) or not record[key].strip() for key in keys)
            or not isinstance(aliases, list) or not all(isinstance(a, str) and a.strip() for a in aliases)
            or not isinstance(items, list) or not items
        ):
            errors.append(f"{slug}: invalid technique fields, aliases, or evidence array")
            continue
        for value in [slug, record["title"], outcome_key, record["outcome"], *aliases]:
            key = normalize(value)
            previous = names.setdefault(key, slug)
            if not key or previous != slug:
                errors.append(f"{slug}: lookup key collision for {value!r} with {previous}")
        signature = tuple(normalize(record[key]) for key in ("problem", "practice"))
        previous = mechanisms.setdefault(signature, slug)
        if previous != slug:
            errors.append(f"{slug}: mechanism duplicates {previous}")
        seen = set()
        for item in items:
            try:
                identity = check_evidence(item, tree)
                if identity not in checked_sources:
                    raise ValueError("evidence is absent from the independently reviewed public source inventory")
                if identity in seen:
                    raise ValueError("duplicate evidence source, regardless of query or span")
                seen.add(identity)
            except (KeyError, TypeError, ValueError) as error:
                errors.append(f"{slug}: {error}")
    return records


def check_history(errors, tree=None):
    tree = tree or GitTree(ROOT)
    path = "history/source-inventory.json"
    content = tree.read(path)
    if hashlib.sha256(content).hexdigest() != INVENTORY_SHA256:
        errors.append("historical inventory differs from the independently checked original trees")
        return 0
    expected = parse_json(content, path)["snapshots"]
    sources = parse_json(tree.read("history/sources.json"), "history/sources.json")["snapshots"]
    expected_sources = [
        {**item, "files": [{"path": row["path"], "blob": row["blob"]} for row in item["files"]]}
        for item in expected
    ]
    if expected_sources != sources:
        errors.append("history source manifest differs from independently pinned repositories, commits, and paths")
    entries = tree.entries()
    archived = set()
    for snapshot in expected:
        for file in snapshot["files"]:
            path = f'{snapshot["directory"]}/{file["path"]}'
            archived.add(path)
            if entries.get(path) != (file["mode"], file["blob"]):
                errors.append(f"{path}: tracked archive blob or mode differs from the original")
                continue
            if tree.draft:
                content = tree.read(path)
                digest = hashlib.sha1(f"blob {len(content)}\0".encode() + content).hexdigest()
                if digest != file["blob"]:
                    errors.append(f"{path}: working-tree archive bytes differ from the original")
    permitted = {"history/README.md", "history/sources.json", "history/source-inventory.json"}
    for path in sorted(set(name for name in entries if name.startswith("history/")) - archived - permitted):
        errors.append(f"{path}: untracked archive provenance")
    return len(archived)


def check_versions(errors, tree=None):
    tree = tree or GitTree(ROOT)
    entries = tree.entries()
    index = tree.read("versions/README.md").decode("utf-8")
    readme = tree.read("README.md").decode("utf-8")
    original = tree.entries(BASELINE)
    for path in sorted(name for name in original if re.fullmatch(r"versions/v[^/]+/(README|CHANGELOG)\.md", name)):
        if entries.get(path) != original[path] or (tree.draft and tree.read(path) != tree.read(path, BASELINE)):
            errors.append(f"{path}: frozen standalone snapshot differs from v0.0.6 baseline")
    rows = re.findall(r"^\| (v[0-9.]+) \| [^\n]+$", index, re.M)
    for version, count in Counter(rows).items():
        matching = [line for line in index.splitlines() if line.startswith(f"| {version} |")]
        if count != 1 or not matching[0].endswith(f"| [Map](../graphify-hq/maps/{version}/README.md) |"):
            errors.append(f"{version}: expected one release row linking to its own map")
    current = re.findall(r"\*\*Current version\*\*[^\n]*\]\((?:versions/)?(v[0-9.]+)/README\.md\)", index)
    home = re.findall(r"\*\*Current version\*\*[^\n]*\]\(versions/(v[0-9.]+)/README\.md\)", readme)
    if len(current) != 1 or current != home or not set(current) <= set(rows):
        errors.append("homepage and index must agree on exactly one listed current version")
    dirs = sorted({path.split("/")[1] for path in entries if path.startswith("versions/") and path.count("/") >= 2})
    if not dirs:
        errors.append("missing standalone versions")
    for version in dirs:
        if not VERSION.fullmatch(version) or not all(f"versions/{version}/{x}.md" in entries for x in ("README", "CHANGELOG")):
            errors.append(f"{version}: incomplete standalone version directory")
        if f"]({version}/README.md)" not in index:
            errors.append(f"{version}: standalone README is missing from the index")
    return len(dirs)


def check_navigation(errors, tree=None, gaps=None):
    tree = tree or GitTree(ROOT)
    gaps = gaps if gaps is not None else []
    entries = tree.entries()
    documents = {"README.md", "README-GUIDE.md", "AGENTS.md", "history/README.md",
                 "techniques/README.md", "graphify-hq/README.md"}
    documents.update(name for name in ("REUSE.md", "learning/README.md") if name in entries)
    documents.update(name for name in entries if suffix(name) in MARKDOWN and
                     name.startswith(("audits/", "versions/", "graphify-hq/maps/")))
    count = sum(check_document(tree, path, errors, gaps) for path in sorted(documents))
    for name in sorted(entries):
        if re.fullmatch(r"history/[^/]+/(?:published-v[^/]+|main-rebrand-v[^/]+)/README\.md", name):
            count += check_document(tree, name, errors, gaps, archive_scope=name.rsplit("/", 1)[0])
    return count


def target_readme(tree, subproject, errors, gaps, profile):
    prefix = Path(subproject).as_posix().removeprefix("./")
    if Path(subproject).is_absolute() or ".." in Path(subproject).parts or "\\" in subproject:
        raise ValueError("subproject must be relative to the selected repository")
    source = readme_path(tree.entries(), "" if prefix == "." else prefix, homepage=prefix == ".")
    if not source:
        errors.append("no supported README found at the selected entry point")
        return None, 0
    body = tree.read(source)
    if len(body) > MAX_README_BYTES:
        errors.append(f"{source}: exceeds GitHub's 500 KiB rendered README limit")
    if suffix(source) not in MARKDOWN:
        gaps.append(f"{source}: editorial and first-use checks for this format require review")
        return source, 0
    text = body.decode("utf-8")
    _, links, blocks = parse_markdown(text)
    paragraphs = [blocks[i+1].content for i, token in enumerate(blocks)
                  if token.type == "paragraph_open" and blocks[i+1].type == "inline"]
    if not any(len(value.strip()) >= 20 for value in paragraphs):
        errors.append(f"{source}: README needs a meaningful project description")
    if any(re.search(r"^\s*(?:TODO|TBD|FIXME)(?:\b|:)", value, re.I) for value in paragraphs):
        errors.append(f"{source}: unresolved reader-facing placeholder")
    if profile != "reference":
        first_action = re.compile(r"\b(quick.?start|getting started|install|run|try|play|build|use|setup)\b", re.I)
        first_screen = "\n".join(t.content for t in blocks[:35] if t.type == "inline")
        if not first_action.search(first_screen) or not (links or any(t.type == "fence" for t in blocks)):
            errors.append(f"{source}: no discoverable first action for {profile}")
    gaps.append(f"{source}: editorial quality and material claims require human or agent review")
    return source, check_document(tree, source, errors, gaps)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="print the technique index after HQ validation")
    parser.add_argument("--repo", type=Path, help="audit a consumer Git repository instead of HQ")
    parser.add_argument("--ref", default="HEAD", help="local ref or commit to validate")
    parser.add_argument("--subproject", default=".", help="repository-relative monorepo directory")
    parser.add_argument("--profile", choices=("application", "library", "reference"), default="application")
    parser.add_argument("--draft", action="store_true", help="inspect tracked working-tree bytes instead of the published tree")
    parser.add_argument("--receipt", type=Path, help="write a machine-readable check receipt")
    parser.add_argument("--smoke", type=Path, help="an explicit local first-action specification to execute")
    parser.add_argument("--allow-network", action="store_true", help="allow the explicit remote first-action probe")
    args = parser.parse_args()
    errors, gaps, records = [], [], []
    cases = {}
    try:
        if args.draft and args.ref != "HEAD":
            raise ValueError("--draft applies to the current checkout only")
        tree = GitTree(args.repo or ROOT, args.ref, draft=args.draft)
        if args.repo:
            entry, count = target_readme(tree, args.subproject, errors, gaps, args.profile)
            cases.update(entrypoint=entry, local_links=count)
            if args.smoke:
                from hq_smoke import verify_first_action
                outcome = verify_first_action(tree, args.smoke, allow_network=args.allow_network)
                cases["first_action"] = outcome
                if outcome["result"] == "failed":
                    errors.append("first action failed its expected result")
                elif outcome["result"] != "passed":
                    gaps.append(f"first action {outcome['result']}: {outcome['detail']}")
            else:
                gaps.append("first action execution not checked: no explicit smoke spec")
        else:
            if args.smoke:
                raise ValueError("--smoke requires an explicit --repo")
            records = check_registry(errors, tree)
            cases.update(standalone_versions=check_versions(errors, tree), techniques=len(records),
                         local_links=check_navigation(errors, tree, gaps), imported_files=check_history(errors, tree))
    except (KeyError, OSError, TypeError, ValueError) as error:
        errors.append(str(error))
    if args.receipt:
        from hq_smoke import write_receipt
        write_receipt(args.receipt, locals().get("tree"), cases, errors, gaps)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.repo:
        print(f"Selected {tree.repository or 'local repository'} at {tree.commit} ({'draft' if args.draft else 'Git tree'})")
        print(f"README: {cases['entrypoint']}; checked {cases['local_links']} local links")
        for gap in gaps:
            print(f"Unchecked: {gap}")
    else:
        print(f"Validated {cases['standalone_versions']} standalone version(s), {cases['techniques']} techniques, "
              f"{cases['local_links']} local links, and {cases['imported_files']} imported files.")
        if gaps:
            print(f"{len(gaps)} observations remain unchecked. Use --receipt for details.")
    if args.list:
        for record in sorted(records, key=lambda item: item["id"]):
            print(f"{record['id']} [{record['status']}] - {record['title']}")
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    sys.exit(main())
