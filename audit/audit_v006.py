"""Exercise README HQ v0.0.6 using disposable worktrees."""

import argparse
import asyncio
from contextlib import contextmanager
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


TARGET = "f50e3749dab90ddfe35894284d1660097a1fb1a8"
LANDING = "a7a989ffb6b664df86aae0ea01053ea2fc0a4405"
SOURCE = "d8c4517c7e43fce02b132c3abd82b8da93e75e3e"
ROOT = Path(__file__).resolve().parents[1]


def git(directory, *args):
    return subprocess.check_output(["git", "-C", str(directory), *args], text=True)


def python(directory, *args):
    return subprocess.run([sys.executable, *args], cwd=directory, text=True, capture_output=True)


def passed(result):
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


def marker(key, evidence):
    print(f"{key}: {evidence}", flush=True)


@contextmanager
def replace(file, new):
    original = file.read_bytes()
    file.write_bytes(new)
    try:
        yield
    finally:
        file.write_bytes(original)


def load_module(path):
    spec = spec_from_file_location(path.stem, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


async def read_evidence(graph):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    args = ["-m", "graphify.serve", str(graph)]
    params = StdioServerParameters(command=sys.executable, args=args)
    async with asyncio.timeout(30), stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            data = await session.call_tool("get_neighbors", {
                "node_id": "feature:standalone-hq-v0-0-6", "token_budget": 8000,
            })
    assert not data.is_error
    return "\n".join(block.text for block in data.content if block.type == "text")


def check_landing(worktree):
    default = git(worktree, "show", LANDING + ":README.md")
    assert "readme-hq" not in default and "](https://" not in default
    assert "versions/v0.0.6/README.md" in (worktree / "README.md").read_text(encoding="utf-8")
    marker("R01", "The initial main README has no link to the active branch, versions, or instructions.")


def check_archive_navigation(worktree):
    paths = {
        "history/bart/published-v0.0.3": [
            "CHANGELOG.md", "docs/ARCHITECTURE.md", "docs/HARNESS.md", "SECURITY.md", "CONTRIBUTING.md"
        ],
        "history/bart/main-rebrand-v0.0.4": [
            "CHANGELOG.md", "docs/ARCHITECTURE.md", "docs/HARNESS.md", "SECURITY.md", "CONTRIBUTING.md"
        ],
    }
    for directory, targets in paths.items():
        readme = (worktree / directory / "README.md").read_text(encoding="utf-8")
        for target in targets:
            assert f"]({target})" in readme and not (worktree / directory / target).exists(), target
    marker("R02", "Two indexed BART homepage snapshots each expose five confirmed missing relative destinations.")


def check_markdown(worktree):
    readme = worktree / "README.md"
    original = readme.read_bytes()
    variants = {
        "titled inline": b'\n[Example](missing-audit-file.md "Example title")\n',
        "reference-style": b'\n[Example][audit-ref]\n\n[audit-ref]: missing-audit-file.md\n',
        "HTML anchor": b'\n<a href="missing-audit-file.md">Example</a>\n',
    }
    for label, text in variants.items():
        with replace(readme, original + text):
            passed(python(worktree, "tools/check_readme_hq.py"))
            marker("R03", f"Broken {label} link passed validation.")
    with replace(readme, original + b"\n[Example](#version-audit-heading)\n\nVersion audit heading\n---------------------\n"):
        result = python(worktree, "tools/check_readme_hq.py")
        assert result.returncode == 1 and "missing local heading" in result.stderr, result.stderr
        marker("R03", "The valid link to a Setext heading was rejected.")
    with replace(readme, original + b"\nInline example: `[Example](missing-audit-file.md)`\n"):
        result = python(worktree, "tools/check_readme_hq.py")
        assert result.returncode == 1 and "missing local target" in result.stderr, result.stderr
        marker("R03", "Literal Markdown syntax inside inline code was reported as a broken link.")


def check_archive_provenance(worktree):
    manifest = worktree / "history/sources.json"
    data = json.loads(manifest.read_bytes())
    data["snapshots"][0]["commit"] = "0" * 40
    with replace(manifest, json.dumps(data).encode()):
        passed(python(worktree, "tools/check_readme_hq.py"))
        marker("R04", "The archive verifier accepted an all-zero source commit for an existing snapshot.")
    item = data["snapshots"][0]
    relative = item["directory"] + "/" + item["files"][0]["path"]
    assert git(worktree, "ls-files", "--stage", "--", relative).startswith("100644")
    git(worktree, "update-index", "--chmod=+x", "--", relative)
    try:
        assert git(worktree, "ls-files", "--stage", "--", relative).startswith("100755")
        passed(python(worktree, "tools/check_readme_hq.py"))
        marker("R04", "The archive verifier accepted tracked file-mode drift with identical bytes.")
    finally:
        git(worktree, "update-index", "--chmod=-x", "--", relative)


def check_standalone_version_drift(worktree):
    path = worktree / "versions/v0.0.6/CHANGELOG.md"
    assert path.read_bytes() == git(worktree, "show", SOURCE + ":versions/v0.0.6/CHANGELOG.md").encode()
    with replace(path, path.read_bytes() + b"\nAudit fixture text after the version source was pinned.\n"):
        passed(python(worktree, "tools/check_readme_hq.py"))
        passed(python(worktree, "graphify-hq/version_maps.py", "--check"))
        marker("R05", "Both checks stayed green after the live v0.0.6 changelog diverged from the graph's pinned source.")


def check_index_mapping(worktree):
    index = worktree / "versions/README.md"
    root_readme = worktree / "README.md"
    old = b"[Map](../graphify-hq/maps/v0.0.6/README.md)"
    new = old.replace(b"v0.0.6", b"v0.0.5")
    value = index.read_bytes()
    assert value.count(old) == 1
    current = b"[README HQ v0.0.6](versions/v0.0.6/README.md)"
    readme = root_readme.read_bytes()
    assert readme.count(current) == 1
    with replace(index, value.replace(old, new)), replace(root_readme, readme.replace(current, current.replace(b"v0.0.6", b"v0.0.1"))):
        passed(python(worktree, "tools/check_readme_hq.py"))
        passed(python(worktree, "graphify-hq/version_maps.py", "--check"))
        marker("R06", "Both checks accepted the v0.0.6 row linking to the v0.0.5 map and the homepage advertising v0.0.1.")


def check_graph_evidence(worktree):
    graph = worktree / "graphify-hq/maps/v0.0.6/graph.json"
    response = asyncio.run(read_evidence(graph))
    assert "[tested_by]" in response and "tools/check_readme_hq.py" in response, response
    data = json.loads(graph.read_bytes())
    edge = next(x for x in data["links"] if x["source"] == "feature:standalone-hq-v0-0-6" and x["relation"] == "tested_by")
    line = int(edge["source_location"][1:])
    checker = git(worktree, "show", SOURCE + ":" + edge["source_file"]).splitlines()
    assert checker[line - 1] == "def check_history(errors):"
    source = "\n".join(checker[line - 1:line + 31])
    assert "history/sources.json" in source and "versions/v0.0.6" not in source
    marker("R07", f"Graphify MCP links the standalone version's tested_by relation to the imported-history verifier at line {line}.")


def check_registry_shape(worktree):
    path = worktree / "techniques/registry.json"
    data = json.loads(path.read_bytes())
    data["schema"] = True
    data["techniques"][0]["aliases"] = "xy"
    with replace(path, json.dumps(data).encode()):
        passed(python(worktree, "tools/check_readme_hq.py", "--list"))
        marker("R08", "Public CLI accepted a Boolean schema field and a string in place of an alias array.")


def check_graph_output_retry(worktree, temporary):
    from unittest.mock import patch

    version_maps = load_module(worktree / "graphify-hq/version_maps.py")
    target = temporary / "partial-map-output"
    sys_path = ["version_maps.py", "--output", str(target)]
    run = subprocess.run
    calls = 0

    def fail_second(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise subprocess.CalledProcessError(1, args[0])
        return run(*args, **kwargs)

    with patch.object(sys, "argv", sys_path), patch.object(version_maps.subprocess, "run", side_effect=fail_second):
        try:
            version_maps.main()
        except subprocess.CalledProcessError:
            assert calls == 2
        else:
            raise AssertionError("The simulated build error was not delivered.")
    assert (target / "v0.0.1/receipt.json").is_file()
    assert (target / "v0.0.2/manifest.json").is_file()
    assert not (target / "v0.0.2/receipt.json").exists()
    retry = python(worktree, "graphify-hq/version_maps.py", "--output", str(target))
    assert retry.returncode == 2 and "output directory must be empty" in retry.stderr, retry.stderr
    marker("R09", "A controlled second-map failure leaves a partial archive and blocks immediate retry.")


def check_outline_rendering(worktree):
    version_maps = load_module(worktree / "graphify-hq/version_maps.py")
    entry = {"title": "Public | preview", "summary": "Old | new"}
    source = {"path": "README.md"}
    receipt = {"source_commit": SOURCE, "nodes": 1, "edges": 0}
    body = version_maps.render_outline("v0.0.6", "vixttha/README-HQ", receipt, [(entry, [(source, 1)], (source, 1))])
    row = body.splitlines()[-1]
    assert row.count("|") == 6 and "\\|" not in row, row
    marker("R10", "A pipe in a catalog title or summary creates extra Markdown table cells in the map outline.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--baseline-only", action="store_true")
    args = parser.parse_args()
    with TemporaryDirectory(prefix="readme-hq-audit-") as tmp:
        temporary = Path(tmp)
        worktree = temporary / "baseline"
        git(args.repo, "worktree", "add", "--quiet", "--detach", str(worktree), TARGET)
        try:
            marker("BASELINE", passed(python(worktree, "tools/check_readme_hq.py")).strip())
            if not args.baseline_only:
                assert git(worktree, "rev-parse", "HEAD").strip() == TARGET
                marker("GRAPHIFY", passed(python(worktree, "graphify-hq/version_maps.py", "--check")).splitlines()[-1])
                check_landing(worktree)
                check_archive_navigation(worktree)
                check_markdown(worktree)
                check_archive_provenance(worktree)
                check_standalone_version_drift(worktree)
                check_index_mapping(worktree)
                check_graph_evidence(worktree)
                check_registry_shape(worktree)
                check_graph_output_retry(worktree, temporary)
                check_outline_rendering(worktree)
        finally:
            git(args.repo, "worktree", "remove", "--force", str(worktree))


if __name__ == "__main__":
    main()
