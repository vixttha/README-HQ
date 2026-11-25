"""Replay open defects and test source identity against exact README HQ revisions."""

from contextlib import contextmanager
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
BASE = "f50e3749dab90ddfe35894284d1660097a1fb1a8"
LEARNING = "a8d97d0559853538d4d814edf5c998e42cfec3d2"
PLAN = "7b3cf8b569f20474152e134f23c5d56f538f089d"
KIT = ROOT / "graphify-hq/template/v0.0.8/evidence_map.py"
MAP = Path("graphify-hq/plans/v0.0.6-repairs")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def command(directory, *args):
    return subprocess.run(args, cwd=directory, text=True, capture_output=True)


def run(directory, *args):
    result = command(directory, *args)
    require(result.returncode == 0, result.stdout + result.stderr)
    return result.stdout


def git(directory, *args):
    return run(directory, "git", *args).strip()


def commit(directory, message):
    git(directory, "add", "-A")
    git(directory, "-c", "user.name=Audit fixture", "-c", "user.email=audit@example.invalid",
        "commit", "--quiet", "-m", message)
    return git(directory, "rev-parse", "HEAD")


def initialize(directory):
    directory.mkdir()
    git(directory, "init", "-q")


@contextmanager
def worktree(folder, sha):
    git(ROOT, "worktree", "add", "--quiet", "--detach", str(folder), sha)
    try:
        yield folder
    finally:
        git(ROOT, "worktree", "remove", "--force", str(folder))


@contextmanager
def restore(paths):
    original = [(path, path.read_bytes()) for path in paths]
    try:
        yield
    finally:
        for path, body in original:
            path.write_bytes(body)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, body):
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")


def check_live_plan(worktree_path):
    workflow = (worktree_path / ".github/workflows/verify-repair-plan.yml").read_text(encoding="utf-8")
    marker = "      - name: Check checkpoint order and verify both Graphify maps over MCP\n"
    step = workflow.split(marker, 1)[1]
    shell = dedent(step.split("        run: |\n", 1)[1])
    result = run(worktree_path, "bash", "-e", "-o", "pipefail", "-c", shell)
    require("Verified all 49 unique, ordered issue checkpoints" in result, result)
    require(result.count("Graphify MCP verified") == 2, result)


def check_checkpoint_evidence(worktree_path):
    directory = worktree_path / MAP
    manifest = directory / "manifest.json"
    files = [manifest, directory / "graph.json", directory / "receipt.json"]
    with restore(files):
        data = read_json(manifest)
        feature = data["features"][0]
        require(feature["id"] == "v0-0-6-1", "Unexpected checkpoint order")
        feature["label"] = "Unrelated plan label"
        feature["changed_in"] = [{"path": "README.md", "anchor": "# README HQ"}]
        feature["tested_by"] = [{"path": "audit/audit_v006.py", "anchor": "def check_archive_navigation(worktree):"}]
        write_json(manifest, data)
        run(worktree_path, sys.executable, str(KIT), str(manifest), str(directory))
        check_live_plan(worktree_path)
    print("I50: Exact 49-checkpoint verification passed an unrelated Graphify label, change, and test fixture.", flush=True)


def check_plan_index(worktree_path):
    index = worktree_path / MAP / "README.md"
    with restore([index]):
        content = index.read_text(encoding="utf-8")
        updated = content.replace("[Graph JSON](graph.json)", "[Graph JSON](missing-audit-graph.json)", 1)
        require(updated != content and not (index.parent / "missing-audit-graph.json").exists(),
                "Broken plan link was not installed")
        index.write_text(updated, encoding="utf-8")
        run(worktree_path, sys.executable, "tools/check_readme_hq.py")
        check_live_plan(worktree_path)
    print("I51: A dead Graphify plan-index link passed both the README checker and exact plan verification.", flush=True)


def check_checkout_conversion(temporary):
    directory = temporary / "autocrlf"
    initialize(directory)
    git(directory, "config", "core.autocrlf", "true")
    git(directory, "fetch", "--quiet", str(ROOT), BASE)
    git(directory, "checkout", "--quiet", "--detach", "FETCH_HEAD")
    require(git(directory, "status", "--porcelain") == "", "Checkout has reported drift")
    attribute = git(directory, "ls-files", "--eol", "graphify-hq/catalog.json")
    require("i/lf" in attribute and "w/crlf" in attribute, attribute)
    run(directory, sys.executable, "tools/check_readme_hq.py")
    result = command(directory, sys.executable, "graphify-hq/version_maps.py", "--check")
    require(result.returncode == 2 and "catalog differs from the pinned source commit" in result.stderr, result.stderr)
    print("I52: A clean autocrlf checkout passes README validation but fails the Graphify catalog byte comparison.", flush=True)


def manifest(commit_id, document="guide.md"):
    return {
        "repository": "vixttha/README-HQ",
        "source_commit": commit_id,
        "title": "Synthetic pinned evidence",
        "features": [{
            "id": "proof", "label": "Proof fixture",
            "documented_in": [{"path": document, "anchor": "# Evidence"}],
            "changed_in": [{"path": "change.md", "anchor": "- Change"}],
            "tested_by": [{"path": "test.py", "anchor": "def test_fixture():"}],
        }],
    }


def graph_input_files(directory):
    (directory / "guide.md").write_text("# Evidence\nOriginal content.\n", encoding="utf-8")
    (directory / "change.md").write_text("- Change\n", encoding="utf-8")
    (directory / "test.py").write_text("def test_fixture():\n    return True\n", encoding="utf-8")


def check_replacement_object(temporary):
    directory = temporary / "git-replacement-fixture"
    initialize(directory)
    graph_input_files(directory)
    original = commit(directory, "Original evidence")
    fixture = temporary / "replacement-manifest.json"
    output = temporary / "replacement-output"
    write_json(fixture, manifest(original))
    run(directory, sys.executable, str(KIT), str(fixture), str(output))
    first = read_json(output / "receipt.json")
    (directory / "guide.md").write_text("Replacement content.\n# Evidence\n", encoding="utf-8")
    replacement = commit(directory, "Alternate source tree")
    git(directory, "replace", original, replacement)
    try:
        exact = git(directory, "--no-replace-objects", "show", f"{original}:guide.md")
        effective = git(directory, "show", f"{original}:guide.md")
        require(exact.startswith("# Evidence") and effective.startswith("Replacement content."), effective)
        run(directory, sys.executable, str(KIT), str(fixture), str(output))
        second = read_json(output / "receipt.json")
        graph = read_json(output / "graph.json")
        link = next(x for x in graph["links"] if x["relation"] == "documented_in")
        digest = sha256((directory / "guide.md").read_bytes()).hexdigest()
        require(first["source_sha256"]["guide.md"] != digest, str(first))
        require(second["source_sha256"]["guide.md"] == digest and link["source_location"] == "L2", str(second))
        require(second["source_commit"] == original and second["mcp_verified"], str(second))
    finally:
        git(directory, "replace", "-d", original)
    print("I53: A normal Git replacement ref changes the evidence and digest while Graphify reports the original SHA and MCP success.", flush=True)


def check_mcp_relation_field(temporary):
    directory = temporary / "relation-label-fixture"
    initialize(directory)
    graph_input_files(directory)
    bracket_path = "guide [tested_by].md"
    (directory / bracket_path).write_bytes((directory / "guide.md").read_bytes())
    source = commit(directory, "Include bracketed Markdown paths")
    before = temporary / "plain-path.json"
    write_json(before, manifest(source))
    run(directory, sys.executable, str(KIT), str(before), str(temporary / "plain-path-output"))
    after = temporary / "bracket-path.json"
    write_json(after, manifest(source, bracket_path))
    result = command(directory, sys.executable, str(KIT), str(after), str(temporary / "bracket-path-output"))
    require(result.returncode != 0 and "tested_by: expected 1, found 2" in result.stderr, result.stdout + result.stderr)
    print("I54: The same source contents compile under a plain filename, while bracketed text in a legal filename is counted as a test edge.", flush=True)


def check_learning_mutable_ref(temporary):
    location = temporary / "learning_source.py"
    location.write_text(git(ROOT, "show", f"{LEARNING}:learning/audit_learning.py"), encoding="utf-8")
    spec = importlib.util.spec_from_file_location("learning_source", location)
    pilot = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pilot)
    directory = temporary / "learning-with-local-sources"
    directory.mkdir()
    repo = directory / "fixture"
    initialize(repo)
    (repo / "README.md").write_text("# Verified source line\n", encoding="utf-8")
    first = commit(repo, "Initial source commit")
    blob = git(repo, "rev-parse", "HEAD:README.md")
    source = {"repository": "fixture", "commit": "HEAD", "blob": blob,
              "line": 1, "anchor": "# Verified source line", "status": "observed"}
    pilot.verify_sources({"source": source}, directory)
    (repo / "unrelated.txt").write_text("A change outside README.md\n", encoding="utf-8")
    second = commit(repo, "Advance the branch without changing the README")
    require(first != second and git(repo, "rev-parse", "HEAD:README.md") == blob, "Invalid mutable-ref fixture")
    pilot.verify_sources({"source": source}, directory)
    require(source["commit"] == "HEAD", "Pilot changed the input into a concrete commit")
    print("I55: The normal learning verifier reports exact evidence against symbolic HEAD for two different source revisions.", flush=True)


def main():
    global KIT
    with TemporaryDirectory(prefix="readme-hq-provenance-fixtures-") as directory:
        temporary = Path(directory)
        with worktree(temporary / "plan", PLAN) as plan:
            check_live_plan(plan)
            check_checkpoint_evidence(plan)
            check_plan_index(plan)
        check_checkout_conversion(temporary)
        with worktree(temporary / "historical-compiler", BASE) as historical:
            KIT = historical / "graphify-hq/template/v0.0.8/evidence_map.py"
            check_replacement_object(temporary)
            check_mcp_relation_field(temporary)
        check_learning_mutable_ref(temporary)


if __name__ == "__main__":
    main()
