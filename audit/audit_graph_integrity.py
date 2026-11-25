"""Compare README HQ and Graphify evidence against controlled Git fixtures."""

import asyncio
from contextlib import contextmanager
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "f50e3749dab90ddfe35894284d1660097a1fb1a8"
MAP = Path("graphify-hq/maps/v0.0.6")
TEMPLATE = Path("graphify-hq/template/v0.0.8/evidence_map.py")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def run(directory, *args):
    result = subprocess.run(args, cwd=directory, capture_output=True, text=True)
    require(result.returncode == 0, result.stdout + result.stderr)
    return result.stdout


def git(directory, *args):
    return run(directory, "git", *args).strip()


def check(worktree):
    return run(worktree, sys.executable, "tools/check_readme_hq.py")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


@contextmanager
def replace(path, data):
    original = path.read_bytes()
    path.write_bytes(data)
    try:
        yield
    finally:
        path.write_bytes(original)


async def neighbor_paths(file, feature):
    params = StdioServerParameters(command=sys.executable, args=["-m", "graphify.serve", str(file)])
    async with asyncio.timeout(30), stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            response = await session.call_tool("get_neighbors", {"node_id": feature, "token_budget": 8000})
            require(not response.is_error, "Graphify MCP neighbor query failed")
    lines = [line for content in response.content if content.type == "text" for line in content.text.splitlines()]
    return [line for line in lines if "[documented_in]" in line and "-->" in line]


def check_mcp_destinations(worktree, temporary, template):
    graph_path = worktree / MAP / "graph.json"
    data = read_json(graph_path)
    receipt = read_json(worktree / MAP / "receipt.json")
    feature = "feature:standalone-hq-v0-0-6"
    links = data["links"]
    old = next(x for x in links if x["source"] == feature and x["relation"] == "documented_in")
    other = next(x for x in links if x["source"] != feature and x["relation"] == "documented_in")
    expected_path, replacement_path = old["source_file"], other["source_file"]
    before = asyncio.run(neighbor_paths(graph_path, feature))
    require(len(before) == 1 and expected_path in before[0], str(before))
    for field in ("target", "source_file", "source_location"):
        old[field] = other[field]
    changed = temporary / "rerouted-document-edge.json"
    changed.write_text(json.dumps(data), encoding="utf-8")
    after = asyncio.run(neighbor_paths(changed, feature))
    require(len(after) == 1 and replacement_path in after[0] and expected_path not in after[0], str(after))
    asyncio.run(template.verify_mcp(changed, receipt))
    print("G34: Graphify MCP returned the substituted document, and the existing readback verifier still passed.")


def check_repository_identity(worktree, temporary):
    original = read_json(worktree / MAP / "manifest.json")
    changed = {**original, "repository": "example/other-repository"}
    manifest = temporary / "repository-label.json"
    dest = temporary / "wrong-repository-output"
    manifest.write_text(json.dumps(changed), encoding="utf-8")
    run(worktree, sys.executable, str(TEMPLATE), str(manifest), str(dest))
    observed = read_json(dest / "receipt.json")
    require(observed["repository"] == changed["repository"] and observed["mcp_verified"], str(observed))
    require(observed["source_commit"] == original["source_commit"], "Source unexpectedly changed")
    print("G35: The normal Graphify build issued MCP-verified evidence under an unrelated repository label.")


def check_git_source_type(worktree, template):
    directory = worktree / "fixture-docs"
    directory.mkdir()
    (directory / "intro.md").write_text("# Actual introduction\n", encoding="utf-8")
    link = worktree / "fixture-symlink.md"
    link.symlink_to("fixture-docs/intro.md")
    git(worktree, "add", "fixture-symlink.md", "fixture-docs/intro.md")
    git(worktree, "-c", "user.name=Audit fixture", "-c", "user.email=audit@example.invalid",
        "commit", "--quiet", "-m", "Create a synthetic Git symlink")
    sha = git(worktree, "rev-parse", "HEAD")
    mode = git(worktree, "ls-tree", sha, "fixture-symlink.md").split()[0]
    require(mode == "120000", f"Expected a Git symlink, saw {mode}")
    body, _ = template.source_lines(sha, "fixture-symlink.md")
    require(body == ["fixture-docs/intro.md"], str(body))
    print("G36: Graphify treated the symlink pointer as line content instead of rejecting it or resolving its document target.")


def check_json_ambiguity(worktree, temporary):
    registry = worktree / "techniques/registry.json"
    original = registry.read_bytes()
    require(b'"schema": 1,' in original, "Missing baseline schema")
    with replace(registry, original.replace(b'"schema": 1,', b'"schema": 999, "schema": 1,', 1)):
        check(worktree)
    data = (worktree / MAP / "manifest.json").read_text(encoding="utf-8")
    first = data.find("{")
    ambiguous = temporary / "duplicate-repository.json"
    dest = temporary / "duplicate-repository-output"
    ambiguous.write_text(data[:first + 1] + '\n  "repository": "example/other-repository",' + data[first + 1:], encoding="utf-8")
    run(worktree, sys.executable, str(TEMPLATE), str(ambiguous), str(dest))
    actual = read_json(dest / "receipt.json")
    require(actual["repository"] == "vixttha/README-HQ" and actual["mcp_verified"], str(actual))
    print("G37: The README registry and Graphify manifest both accepted duplicate object keys and silently kept the last value.")


def check_source_line_range(worktree):
    filename = "tools/check_readme_hq.py"
    actual_lines = len((worktree / filename).read_text(encoding="utf-8").splitlines())
    require(actual_lines < 99999, "Out-of-range fixture is unexpectedly in range")
    readme = worktree / "README.md"
    original = readme.read_bytes()
    with replace(readme, original + f"\n[Source proof]({filename}#L99999)\n".encode()):
        check(worktree)
    print(f"G38: The README checker accepted a link to line 99999 in a {actual_lines}-line tracked source file.")


def check_archive_coverage(worktree):
    manifest = worktree / "history/sources.json"
    data = read_json(manifest)
    directory = "history/aldervale/published-v0.0.4"
    filename = "assets/breeze-campus.webp"
    path = worktree / directory / filename
    asset = path.read_bytes()
    archive = next(x for x in data["snapshots"] if x["directory"] == directory)
    before = len(archive["files"])
    archive["files"] = [x for x in archive["files"] if x["path"] != filename]
    require(len(archive["files"]) == before - 1, "Asset missing in original manifest")
    require(filename in (worktree / directory / "README.md").read_text(encoding="utf-8"), "Archived homepage does not link asset")
    with replace(manifest, (json.dumps(data, indent=2) + "\n").encode()):
        path.unlink()
        try:
            output = check(worktree)
            require("158 imported files" in output, output)
        finally:
            path.write_bytes(asset)
    print("G39: Deleting an archived homepage image and its matching manifest entry reduced coverage to 158 and still passed.")


def check_empty_version_coverage(worktree, temporary):
    catalog_path = worktree / "graphify-hq/catalog.json"
    input_data = read_json(catalog_path)
    require(len(input_data["versions"]["v0.0.6"]) == 2, "Unexpected baseline record count")
    input_data["versions"]["v0.0.6"] = []
    catalog_path.write_text(json.dumps(input_data, indent=2) + "\n", encoding="utf-8")
    git(worktree, "add", "graphify-hq/catalog.json")
    git(worktree, "-c", "user.name=Audit fixture", "-c", "user.email=audit@example.invalid",
        "commit", "--quiet", "-m", "Create a synthetic empty version catalog entry")
    pin = git(worktree, "rev-parse", "HEAD")
    (worktree / "graphify-hq/source-commit.txt").write_text(pin + "\n", encoding="utf-8")
    dest = temporary / "empty-version-output"
    output = run(worktree, sys.executable, "graphify-hq/version_maps.py", "--output", str(dest))
    receipt = read_json(dest / "v0.0.6/receipt.json")
    require(receipt["feature_links"] == {} and receipt["mcp_verified"], str(receipt))
    require("6 maps covering 15 version records" in output, output)
    require("| v0.0.6 |" in (worktree / "versions/README.md").read_text(encoding="utf-8"), "v0.0.6 index row absent")
    print("G40: The normal version-map builder succeeded with zero mapped records at v0.0.6 while the version remained advertised.")


def main():
    with TemporaryDirectory(prefix="readme-hq-graph-integrity-") as tmp:
        temporary = Path(tmp)
        worktree = temporary / "baseline"
        git(ROOT, "worktree", "add", "--quiet", "--detach", str(worktree), BASELINE)
        previous = Path.cwd()
        try:
            os.chdir(worktree)
            sys.path.insert(0, str(worktree / TEMPLATE.parent))
            import evidence_map

            check(worktree)
            check_mcp_destinations(worktree, temporary, evidence_map)
            check_repository_identity(worktree, temporary)
            check_json_ambiguity(worktree, temporary)
            check_source_line_range(worktree)
            check_archive_coverage(worktree)
            check_git_source_type(worktree, evidence_map)
            check_empty_version_coverage(worktree, temporary)
        finally:
            os.chdir(previous)
            git(ROOT, "worktree", "remove", "--force", str(worktree))


if __name__ == "__main__":
    main()
