"""Read live governance metadata and replay policy-boundary controls on a pinned tree."""
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.request import Request, urlopen

ROOT = Path.cwd()
CANDIDATE = "8d50caec2bc6fcb998994a1fd302294a029325f9"
PLAN_COMMIT = "4457fc1e82f2cff0225536ff1c43e3e565fb46db"
PLAN = "plans/v0.0.6.78-to-v0.0.6.128/checkpoints.json"
REPO = "vixttha/README-HQ"


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], timeout=90).decode().strip()


def run(script, *args):
    return subprocess.run([sys.executable, str(ROOT / script), *args], timeout=220,
                          capture_output=True, encoding="utf-8", errors="replace")


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def approval_observation():
    sys.path.insert(0, str(ROOT / "graphify-hq/template/v0.0.8"))
    from github_provenance import Page, verify_pull_request

    pr = {"number": 68, "state": "open", "draft": True, "merged": False, "merge_commit_sha": None,
          "head": {"sha": CANDIDATE, "ref": "repair/v0.0.6", "repo": {"full_name": REPO}},
          "base": {"repo": {"full_name": REPO}, "ref": "main"}}
    expectation = {"number": 68, "source_branch": "repair/v0.0.6"}

    def observe(association, state, seen_commit):
        calls = []

        def fetch(path):
            calls.append(path)
            if path == "pulls/68":
                return pr
            if path == "pulls/68/reviews?per_page=100&page=1":
                return Page([{"state": state, "commit_id": seen_commit,
                              "user": {"id": 17}, "author_association": association}], False)
            raise AssertionError(path)

        outcome = verify_pull_request(REPO, CANDIDATE, expectation, fetch=fetch)
        return {"count": outcome["exact_commit_approvals"], "draft": outcome["pr_state"] == "draft",
                "queries": calls}

    external = observe("NONE", "APPROVED", CANDIDATE)
    owner = observe("OWNER", "APPROVED", CANDIDATE)
    stale = observe("OWNER", "APPROVED", "a" * 40)
    assert external == owner and owner["count"] == 1 and owner["draft"]
    assert stale["count"] == 0
    return {"synthetic_external_review": external, "synthetic_owner_review": owner,
            "stale_review_control": stale, "authority_lookup_performed": False}


def live_repository():
    base = f"https://api.github.com/repos/{REPO}"

    def fetch(path):
        req = Request(base + path, headers={"User-Agent": "README-HQ-white-audit",
                                            "Accept": "application/vnd.github+json"})
        with urlopen(req, timeout=20) as response:
            assert response.status == 200
            return json.load(response)

    branch = fetch("/branches/main")
    rules = fetch("/rules/branches/main")
    pr = fetch("/pulls/68")
    return {"name": branch["name"], "commit": branch["commit"]["sha"], "protected": branch["protected"],
            "required_check_contexts": branch.get("protection", {}).get("required_status_checks", {}).get("contexts", []),
            "active_rule_types": sorted(rule["type"] for rule in rules),
            "draft": pr["draft"], "head_commit": pr["head"]["sha"], "base_commit": pr["base"]["sha"]}


def check_later_ledger():
    ledger = json.loads(git("show", f"{PLAN_COMMIT}:{PLAN}"))
    numbers = list(range(78, 129))
    checkpoints = ledger["checkpoints"]
    assert [item["issue"] for item in checkpoints] == numbers
    assert [item["version"] for item in checkpoints] == [f"v0.0.6.{n}" for n in numbers]
    assert [item["after"] for item in checkpoints] == [f"v0.0.6.{n-1}" for n in numbers]
    assert all(item["debug"]["reproduce"] and item["debug"]["acceptance"] for item in checkpoints)
    assert ledger["status"] == "awaiting_approval" and ledger["debug_before_merge"] is True
    assert ledger["implementation_authorized"] is ledger["merge_authorized"] is False

    path = ROOT / PLAN
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists()
    checkpoints[0]["issue"] = checkpoints[1]["issue"]
    del checkpoints[0]["debug"]
    ledger["debug_before_merge"] = False
    write_json(path, ledger)
    git("add", "--", PLAN)
    git("-c", "user.name=White Fixture", "-c", "user.email=fixture@example.invalid",
        "commit", "-qm", "Disposable later-plan drift fixture")
    fixture_commit = git("rev-parse", "HEAD")
    reader = run("tools/check_readme_hq.py")
    plan = run("tools/verify_plan.py", "--mcp")
    assert reader.returncode == plan.returncode == 0, (reader.stderr, plan.stderr)
    assert "Verified 67 repair checkpoints" in plan.stdout
    return {"observed_planning_commit": PLAN_COMMIT, "real_checkpoints": len(numbers),
            "real_status": "awaiting_approval", "real_post_fix_debug": True,
            "fixture_commit": fixture_commit, "fixture_duplicate_issue": checkpoints[0]["issue"],
            "fixture_missing_debug_acceptance": True, "fixture_debug_gate_disabled": True,
            "candidate_reader_exit": reader.returncode, "original_ledger_graphify_exit": plan.returncode,
            "original_ledger_graphify_scope": plan.stdout.splitlines()[-1]}


def archive_membership():
    original = ROOT / "versions/v0.0.6/README.md"
    extra = original.parent / "audit-fixture-extra.txt"
    assert original.is_file() and not extra.exists()
    extra.write_text("Disposable archive inventory test.\n", encoding="utf-8")
    git("add", "--", extra.relative_to(ROOT).as_posix())
    git("-c", "user.name=White Fixture", "-c", "user.email=fixture@example.invalid",
        "commit", "-qm", "Disposable new archive member fixture")
    clean_with_extra = run("tools/check_readme_hq.py")
    graph = run("graphify-hq/version_maps.py", "--check")
    old = original.read_bytes()
    try:
        original.write_bytes(old + b"\nDisposable frozen-file change.\n")
        changed_readme = run("tools/check_readme_hq.py", "--draft")
    finally:
        original.write_bytes(old)
    assert clean_with_extra.returncode == graph.returncode == 0, (clean_with_extra.stderr, graph.stderr)
    assert changed_readme.returncode != 0 and "frozen standalone snapshot differs" in changed_readme.stderr
    return {"extra_file": extra.relative_to(ROOT).as_posix(), "reader_exit": clean_with_extra.returncode,
            "graphify_exit": graph.returncode, "edited_frozen_readme_control_exit": changed_readme.returncode,
            "map_report": graph.stdout.splitlines()[-1]}


def main():
    assert git("rev-parse", "HEAD") == CANDIDATE
    output = Path(sys.argv[2])
    if sys.argv[1] == "graph":
        observed = {"approval_observation": approval_observation(),
                    "later_ledger": check_later_ledger(), "archive_membership": archive_membership()}
    else:
        observed = {"approval_observation": approval_observation()}
        if sys.platform == "linux":
            observed["live_repository"] = live_repository()
    data = {"candidate": CANDIDATE, "platform": sys.platform, "workflow_run_id": os.getenv("GITHUB_RUN_ID"),
            "workflow_attempt": os.getenv("GITHUB_RUN_ATTEMPT"), "observations": observed}
    write_json(output, data)
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
