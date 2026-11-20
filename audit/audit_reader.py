"""Exercise reader outcomes, Graphify capacity, and learning evidence on pinned sources."""

import asyncio
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT = Path(__file__).resolve().parents[1]
BASE = "f50e3749dab90ddfe35894284d1660097a1fb1a8"
LEARNING = "a8d97d0559853538d4d814edf5c998e42cfec3d2"
KIT = Path("graphify-hq/template/v0.0.8")
SOURCE = "audit-fixture/source.md"
ASSET = "history/aldervale/published-v0.0.4/assets/breeze-campus.webp"
RELATIONS = ("documented_in", "changed_in", "tested_by", "implemented_in")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def command(directory, *args):
    return subprocess.run(args, cwd=directory, capture_output=True, text=True)


def run(directory, *args):
    result = command(directory, *args)
    require(result.returncode == 0, result.stdout + result.stderr)
    return result.stdout


def git(directory, *args):
    return run(directory, "git", *args).strip()


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evidence_ref(path, anchor):
    return {"path": path, "anchor": anchor}


def template_manifest(commit):
    return {
        "repository": "vixttha/README-HQ", "source_commit": commit, "title": "Reader audit fixture",
        "features": [{
            "id": "reader", "label": "Reader",
            "documented_in": [evidence_ref(SOURCE, "# Reader evidence")],
            "changed_in": [evidence_ref(SOURCE, "- Record a change")],
            "tested_by": [evidence_ref(SOURCE, "def evidence_test():")],
        }],
    }


def save_manifest(temporary, name, manifest):
    path = temporary / (name + ".json")
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path


def compile_graph(worktree, manifest_path, out):
    return command(worktree, sys.executable, str(KIT / "evidence_map.py"), str(manifest_path), str(out))


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_unicode_line_coordinates(worktree, temporary, commit):
    result = git(worktree, "grep", "-n", "-F", "# Reader evidence", commit, "--", SOURCE)
    require(f":{SOURCE}:2:" in result, result)
    manifest = save_manifest(temporary, "line-coordinates", template_manifest(commit))
    output = temporary / "unicode-output"
    result = compile_graph(worktree, manifest, output)
    require(result.returncode == 0, result.stderr)
    graph = read_json(output / "graph.json")
    link = next(x for x in graph["links"] if x["relation"] == "documented_in")
    require(link["source_location"] == "L3" and read_json(output / "receipt.json")["mcp_verified"], str(link))
    print("P41: git grep locates the pinned evidence at line 2; the Graphify CLI and MCP accepted line 3.", flush=True)


def check_binary_file_inventory(worktree, temporary, commit):
    manifest = template_manifest(commit)
    manifest["source_files"] = [ASSET]
    path = save_manifest(temporary, "binary-inventory", manifest)
    require(git(worktree, "cat-file", "-t", f"{commit}:{ASSET}") == "blob", "Missing tracked WebP")
    result = compile_graph(worktree, path, temporary / "binary-output")
    require(result.returncode != 0 and "UnicodeDecodeError" in result.stderr, result.stdout + result.stderr)
    print("P42: The compiler rejects an existing tracked WebP that is listed for inventory only.", flush=True)


def check_pair_publication(worktree, temporary, commit):
    original = template_manifest(commit)
    first = save_manifest(temporary, "pair-original", original)
    output = temporary / "pair-output"
    result = compile_graph(worktree, first, output)
    require(result.returncode == 0, result.stderr)
    graph, receipt = output / "graph.json", output / "receipt.json"
    prior_graph = graph.read_bytes()
    prior_receipt = receipt.read_bytes()
    receipt.unlink()
    receipt.mkdir()
    (receipt / "prior.json").write_bytes(prior_receipt)
    modified = {**original, "title": "Revised candidate"}
    updated = save_manifest(temporary, "pair-modified", modified)
    result = compile_graph(worktree, updated, output)
    require(result.returncode != 0 and "IsADirectoryError" in result.stderr, result.stdout + result.stderr)
    require(graph.read_bytes() != prior_graph, "Old graph survived, so there was no partial write")
    require(hashlib.sha256(graph.read_bytes()).hexdigest() != json.loads(prior_receipt)["graph_sha256"],
            "New graph unexpectedly matches the old receipt")
    print("P43: Failed receipt publication overwrote an existing graph, leaving incompatible evidence.", flush=True)


def check_bounded_pr_history(provenance):
    head = "f" * 40
    commits = [{"sha": f"{index:040x}"} for index in range(1, 253)]
    reported = commits[:250]
    source = commits[250]["sha"]
    route = "pulls/7"
    repository = "vixttha/README-HQ"
    expected = {"number": 7, "source_branch": "docs/reader"}

    def fetch(path):
        if path == route:
            return {"number": 7, "state": "open", "draft": False, "merged": False, "commits": 252,
                    "base": {"repo": {"full_name": repository}, "ref": "main", "sha": "c" * 40},
                    "head": {"repo": {"full_name": repository}, "ref": expected["source_branch"], "sha": head}}
        if path.startswith(route + "/commits?"):
            page = int(path.rsplit("=", 1)[1])
            return reported[(page - 1) * 100:page * 100]
        if path == route + "/reviews?per_page=100&page=1":
            return []
        raise ValueError(f"Unexpected fixture route: {path}")

    require(provenance.verify_pull_request(repository, reported[-1]["sha"], expected, fetch)["source_relation"]
            == "historical PR commit", "Visible historical SHA was not accepted")
    try:
        provenance.verify_pull_request(repository, source, expected, fetch)
    except ValueError as error:
        require("absent from the GitHub commit list" in str(error), str(error))
    else:
        raise ValueError("The verifier unexpectedly handled the bounded history")
    print("P44: A valid historical commit after the documented 250-result cap is reported as absent.", flush=True)


def check_external_reader_route(worktree):
    path = worktree / "README.md"
    original = path.read_bytes()
    trial = original.replace(
        b"**Current version**",
        b"**First action**: [Play now](https://launch.example.invalid/play)\n\n**Current version**",
        1,
    )
    require(trial != original, "Missing root version line")
    path.write_bytes(trial)
    try:
        result = run(worktree, sys.executable, "tools/check_readme_hq.py")
    finally:
        path.write_bytes(original)
    require("Validated" in result and "unverified" not in result.lower(), result)
    print("P45: The README checker passed a declared browser entry point on reserved .invalid without reporting it unchecked.", flush=True)


def check_learning_line_coordinates(temporary, pilot_module):
    directory = temporary / "learning-sources"
    project = directory / "learning-example"
    project.mkdir(parents=True)
    git(project, "init", "-q")
    (project / "README.md").write_text("First line\nObserved pattern on last line\n", encoding="utf-8")
    git(project, "add", "README.md")
    git(project, "-c", "user.name=Audit Fixture", "-c", "user.email=audit@example.invalid",
        "commit", "-qm", "Add synthetic learning source")
    commit = git(project, "rev-parse", "HEAD")
    fixture = {"repository": project.name, "commit": commit, "blob": git(project, "rev-parse", "HEAD:README.md"),
               "line": 0, "anchor": "Observed pattern", "status": "observed"}
    pilot_module.verify_sources({"example": fixture}, directory)
    fixture.update(line=1, anchor="")
    pilot_module.verify_sources({"example": fixture}, directory)
    print("P46: Learning verified a line-zero source coordinate and a separate empty anchor.", flush=True)


def check_retired_technique(worktree, pilot_module):
    pilot = json.loads(git(worktree, "show", f"{LEARNING}:learning/pilot.json"))
    target = pilot["targets"]["Lydite"]
    selected = set(pilot["sources"])
    before = pilot_module.recommendations(pilot, target, selected)
    registry = worktree / "techniques/registry.json"
    original = registry.read_bytes()
    changed = json.loads(original)
    entry = next(x for x in changed["techniques"] if x["id"] == "clean-consumer-adoption")
    require(entry["status"] == "active", "The baseline technique was already retired")
    entry["status"] = "retired"
    registry.write_text(json.dumps(changed), encoding="utf-8")
    try:
        validation = run(worktree, sys.executable, "tools/check_readme_hq.py", "--list")
        after = pilot_module.recommendations(pilot, target, selected)
    finally:
        registry.write_bytes(original)
    require("clean-consumer-adoption [retired]" in validation, validation)
    require(after == before and [x["technique"] for x in after] == [entry["id"]], str(after))
    print("P47: The learning pilot still recommends an existing technique after its canonical registry record is retired.", flush=True)


async def query_neighbors(graph, budget):
    params = StdioServerParameters(command=sys.executable, args=["-m", "graphify.serve", str(graph)])
    async with asyncio.timeout(30), stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            result = await session.call_tool("get_neighbors", {"node_id": "feature:reader", "token_budget": budget})
            require(not result.is_error, "Graphify MCP neighbor tool failed")
            return "\n".join(x.text for x in result.content if x.type == "text")


def check_documented_neighbor_capacity(worktree, temporary, commit, paths, template):
    manifest = template_manifest(commit)
    for index, relation in enumerate(RELATIONS):
        manifest["features"][0][relation] = [evidence_ref(path, "# Fixture") for path in paths[index * 12:(index + 1) * 12]]
    manifest["source_files"] = paths
    graph, _ = template.build(template.validate_manifest(manifest), temporary / "capacity-output")
    before = asyncio.run(query_neighbors(graph, 8000))
    after = asyncio.run(query_neighbors(graph, 16000))
    require("truncated" in before and sum("  -->" in row for row in after.splitlines()) == 48, before)
    fixture = save_manifest(temporary, "supported-reference-capacity", manifest)
    result = compile_graph(worktree, fixture, temporary / "capacity-cli-output")
    require(result.returncode != 0 and "expected 12, found" in result.stderr, result.stdout + result.stderr)
    print("P48: A valid 48-edge feature failed MCP validation at the hard-coded budget and returned all edges at a larger budget.", flush=True)


def check_git_valid_branch_names(worktree, template, commit):
    name = "_docs/fix"
    run(worktree, "git", "check-ref-format", "refs/heads/" + name)
    manifest = template_manifest(commit)
    manifest["pull_request"] = {"number": 1, "source_branch": name}
    try:
        template.validate_manifest(manifest)
    except ValueError as error:
        require("plain source branch name" in str(error), str(error))
    else:
        raise ValueError("The verifier unexpectedly accepted the Git-valid branch")
    print("P49: Git accepts _docs/fix, while the Graphify manifest rejects the otherwise valid pull-request source branch.", flush=True)


def main():
    with TemporaryDirectory(prefix="readme-hq-reader-audit-") as directory:
        temporary = Path(directory)
        worktree = temporary / "baseline"
        git(ROOT, "worktree", "add", "--quiet", "--detach", str(worktree), BASE)
        previous = Path.cwd()
        try:
            os.chdir(worktree)
            sys.path.insert(0, str(worktree / KIT))
            import evidence_map
            import github_provenance

            pilot_path = temporary / "learning.py"
            pilot_path.write_text(git(worktree, "show", f"{LEARNING}:learning/audit_learning.py"), encoding="utf-8")
            pilot = load_module(pilot_path, "learning_pilot")
            check_external_reader_route(worktree)
            check_learning_line_coordinates(temporary, pilot)
            check_retired_technique(worktree, pilot)
            check_bounded_pr_history(github_provenance)
            source = worktree / SOURCE
            source.parent.mkdir()
            source.write_text("# Introduction\nOrdinary text\u2028# Reader evidence\n- Record a change\ndef evidence_test():\n", encoding="utf-8")
            paths = [f"audit-fixture/{index:02d}-{('x' * 216)}.md" for index in range(48)]
            for path in paths:
                (worktree / path).write_text("# Fixture\n", encoding="utf-8")
            git(worktree, "add", "audit-fixture")
            git(worktree, "-c", "user.name=Audit Fixture", "-c", "user.email=audit@example.invalid",
                "commit", "-qm", "Add controlled Graphify reader fixtures")
            commit = git(worktree, "rev-parse", "HEAD")
            check_unicode_line_coordinates(worktree, temporary, commit)
            check_binary_file_inventory(worktree, temporary, commit)
            check_pair_publication(worktree, temporary, commit)
            check_documented_neighbor_capacity(worktree, temporary, commit, paths, evidence_map)
            check_git_valid_branch_names(worktree, evidence_map, commit)
        finally:
            os.chdir(previous)
            git(ROOT, "worktree", "remove", "--force", str(worktree))


if __name__ == "__main__":
    main()
