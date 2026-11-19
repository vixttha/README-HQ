"""Audit functional behavior of the pinned README HQ candidate with disposable fixtures."""
import asyncio
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

CANDIDATE = "8d50caec2bc6fcb998994a1fd302294a029325f9"
ROOT = Path.cwd()
CHECKER = ROOT / "tools/check_readme_hq.py"
DESCRIPTION = "This toolkit converts example input into a readable report."
RESULTS = {}


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def commit(root):
    git(root, "add", "--all")
    git(root, "-c", "user.email=fixture@example.invalid", "-c", "user.name=Fixture", "commit", "-qm", "Fixture")
    return git(root, "rev-parse", "HEAD")


def run(*args):
    result = subprocess.run([sys.executable, str(CHECKER), *map(str, args)], text=True,
                            encoding="utf-8", errors="replace", capture_output=True)
    return {"exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def assert_exit(results, *expected):
    exits = tuple(row["exit"] for row in results)
    if exits != expected:
        raise AssertionError(results)


def check_fixtures(base):
    repo = base / "adopter"
    repo.mkdir()
    git(repo, "init", "--quiet")
    git(repo, "config", "core.autocrlf", "false")
    readme = repo / "README.md"
    license_path = repo / "LICENSE"
    license_path.write_text("Example license placeholder for synthetic fixtures.\n", encoding="utf-8")
    image = repo / "overview.svg"
    image.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>', encoding="utf-8")
    intro = f"# Example\n\n{DESCRIPTION}\n\n"
    readme.write_text(intro + "## Quickstart\n\nRun the verified example:\n\n```sh\nexample --version\n```\n", encoding="utf-8")
    commit(repo)
    quickstart = run("--repo", repo, "--profile", "application")
    readme.write_text(intro + "## Quickstart\n\nInstructions are coming later.\n\n## Terms\n\n[License](LICENSE)\n", encoding="utf-8")
    commit(repo)
    false_first_action = run("--repo", repo, "--profile", "application")
    readme.write_text(intro + "## Status\n\nThe example has been archived.\n\n## Terms\n\n[License](LICENSE)\n", encoding="utf-8")
    commit(repo)
    no_first_action = run("--repo", repo, "--profile", "application")
    assert_exit((quickstart, false_first_action, no_first_action), 0, 0, 1)
    RESULTS["unrelated_link_first_action"] = [quickstart, false_first_action, no_first_action]

    image_results = []
    for attributes in ('alt="Report preview"', 'alt=""', ''):
        readme.write_text(intro + f'<img src="overview.svg" {attributes}>\n', encoding="utf-8")
        commit(repo)
        image_results.append(run("--repo", repo, "--profile", "reference"))
    assert_exit(image_results, 0, 0, 0)
    if any("checked 1 local links" not in case["stdout"] for case in image_results):
        raise AssertionError(image_results)
    RESULTS["missing_html_alt"] = image_results

    scope_results = [run("--subproject", "nonexistent-module", "--profile", "reference"),
                     run("--repo", ROOT, "--subproject", "nonexistent-module", "--profile", "reference")]
    assert_exit(scope_results, 0, 1)
    RESULTS["ignored_adopter_flags"] = scope_results

    plan_input = base / "malformed-plan.json"
    plan_input.write_text("[]\n", encoding="utf-8")
    learning_command = subprocess.run(
        [sys.executable, str(ROOT / "learning/intake.py"), str(plan_input), str(base / "receipts")],
        text=True, capture_output=True,
    )
    if learning_command.returncode != 1 or "AttributeError" not in learning_command.stderr:
        raise AssertionError(learning_command.stderr)
    RESULTS["learning_malformed_request"] = {"exit": learning_command.returncode, "traceback": True}


def check_self_homepage(base):
    clone = base / "self-check"
    git(ROOT, "clone", "--quiet", "--no-hardlinks", str(ROOT), str(clone))
    git(clone, "switch", "--quiet", "--detach", CANDIDATE)
    directory = clone / ".github"
    directory.mkdir(exist_ok=True)
    group = directory / "README.md"
    group.write_text(f"# Fixture\n\n{DESCRIPTION}\n\n[Missing setup guide](missing-guide.md)\n", encoding="utf-8")
    revision = commit(clone)
    command = subprocess.run([sys.executable, str(clone / "tools/check_readme_hq.py"), "--ref", revision],
                             text=True, capture_output=True)
    adopter = run("--repo", clone, "--ref", revision, "--profile", "reference")
    if command.returncode != 0 or adopter["exit"] != 1 or "missing-guide.md" not in adopter["stderr"]:
        raise AssertionError((command.stdout, command.stderr, adopter))
    RESULTS["self_homepage_selection"] = {"standalone_exit": command.returncode, "adopter": adopter}


def check_graphify(base):
    sys.path.insert(0, str(ROOT / "graphify-hq/template/v0.0.8"))
    from evidence_map import build, validate_manifest, verify_mcp

    manifest = validate_manifest({"repository": "vixttha/README-HQ", "source_commit": CANDIDATE,
                                  "title": "Inventory readback fixture", "source_files": ["README.md", "AGENTS.md"],
                                  "features": []})
    graph, receipt = build(manifest, base / "graph")
    asyncio.run(verify_mcp(graph, receipt))
    data = json.loads(graph.read_bytes())
    if sum(link["relation"] == "contains_source" for link in data["links"]) != 2:
        raise AssertionError("Expected two compiled inventory edges")
    altered = next(link for link in data["links"] if link["target"] == "file:README.md")
    altered["source_file"] = "notes.txt"
    graph.write_text(json.dumps(data), encoding="utf-8")
    receipt["graph_sha256"] = hashlib.sha256(graph.read_bytes()).hexdigest()
    asyncio.run(verify_mcp(graph, receipt))
    RESULTS["graphify_inventory_readback"] = {
        "baseline_verified": True, "modified_edge_verified": True,
        "node_count": receipt["nodes"], "edge_count": receipt["edges"],
        "expected_edge_source_file": "README.md", "observed_edge_source_file": "notes.txt",
    }


def main():
    if git(ROOT, "rev-parse", "HEAD") != CANDIDATE:
        raise AssertionError("The audit must run against the candidate checkout")
    with TemporaryDirectory(prefix="readme-hq-review-") as temporary:
        base = Path(temporary)
        check_fixtures(base)
        check_self_homepage(base)
        if "--graphify" in sys.argv:
            check_graphify(base)
    payload = {"candidate": CANDIDATE, "platform": sys.platform,
               "workflow_run_id": os.getenv("GITHUB_RUN_ID"), "workflow_run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
               "job": os.getenv("GITHUB_JOB"), "observations": RESULTS}
    Path(sys.argv[1]).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("Confirmed observations: " + ", ".join(RESULTS))


if __name__ == "__main__":
    main()
