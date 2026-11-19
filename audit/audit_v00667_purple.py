"""Correlate README validation, first-action execution, and Graphify receipts."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.request import Request, urlopen

ROOT = Path.cwd()
CANDIDATE = "8d50caec2bc6fcb998994a1fd302294a029325f9"
ORG_REPOSITORY = "alphapapa/org-super-agenda"
ORG_COMMIT = "fb20ad9c8a9705aa05d40751682beae2d094e0fe"


def git(directory, *args):
    return subprocess.check_output(["git", "-C", str(directory), *args], text=True, timeout=90).strip()


def commit(directory, *paths):
    git(directory, "add", "--", *paths)
    git(directory, "-c", "user.name=Audit Fixture", "-c", "user.email=fixture@example.invalid",
        "commit", "-qm", "Disposable audit fixture")
    return git(directory, "rev-parse", "HEAD")


def command(script, *args):
    return subprocess.run([sys.executable, str(script), *map(str, args)], capture_output=True,
                          encoding="utf-8", errors="replace", timeout=180)


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def readme_result(repo, receipt, *args):
    result = command(ROOT / "tools/check_readme_hq.py", "--repo", repo, "--receipt", receipt, *args)
    return result.returncode, json.loads(receipt.read_bytes())


def first_action_binding(base):
    repo = base / "adopter"
    repo.mkdir()
    git(repo, "init", "--quiet")
    git(repo, "config", "core.autocrlf", "false")
    (repo / "README.md").write_text(
        "# Purple fixture\n\nThis example demonstrates one documented first action.\n\n"
        "## Quickstart\n\n```sh\npython first_action.py\n```\n", encoding="utf-8",
    )
    script = repo / "first_action.py"
    script.write_text('raise SystemExit(7)\n', encoding="utf-8")
    broken_commit = commit(repo, "README.md", "first_action.py")
    broken_direct = command(script)
    assert broken_direct.returncode == 7
    smoke_path, receipt = base / "smoke.json", base / "receipt.json"
    expected = {"exit": 0, "contains": "READY"}

    def trial(spec):
        write_json(smoke_path, spec)
        code, data = readme_result(repo, receipt, "--smoke", smoke_path)
        return {"exit": code, "overall": data["result"], "first_action": data["cases"]["first_action"]["result"],
                "readme_sha256": data["sources"]["README.md"]}

    unrelated = trial({"commit": broken_commit, "argv": [sys.executable, "-c", "print('READY')"],
                       "expected": expected})
    documented = trial({"commit": broken_commit, "argv": [sys.executable, "first_action.py"],
                        "expected": expected})
    assert (unrelated["exit"], unrelated["overall"], unrelated["first_action"]) == (0, "passed", "passed"), unrelated
    assert (documented["exit"], documented["overall"], documented["first_action"]) == (1, "failed", "failed"), documented

    blocked_receipts = []
    for path in ("/first", "/second"):
        write_json(smoke_path, {"commit": broken_commit, "url": "https://example.invalid" + path,
                               "expected": {"http_status": 200}})
        code, result = readme_result(repo, receipt, "--smoke", smoke_path)
        assert code == 0 and result["cases"]["first_action"]["result"] == "unchecked"
        blocked_receipts.append(receipt.read_bytes())
    assert blocked_receipts[0] == blocked_receipts[1]

    script.write_text('print("READY")\n', encoding="utf-8")
    fixed_commit = commit(repo, "first_action.py")
    working = trial({"commit": fixed_commit, "argv": [sys.executable, "first_action.py"], "expected": expected})
    assert (working["exit"], working["overall"], working["first_action"]) == (0, "passed", "passed"), working
    assert unrelated["readme_sha256"] == documented["readme_sha256"] == working["readme_sha256"]
    return {
        "broken_fixture_commit": broken_commit, "documented_command_direct_exit": broken_direct.returncode,
        "unrelated_command": unrelated, "documented_command": documented, "working_documented_control": working,
        "unchecked_distinct_urls": {"network_requests": 0, "receipts_byte_identical": True,
                                     "sha256": hashlib.sha256(blocked_receipts[0]).hexdigest()},
    }


def org_homepage(base):
    checkout = base / "org-project"
    checkout.mkdir()
    git(checkout, "init", "--quiet")
    git(checkout, "remote", "add", "origin", f"https://github.com/{ORG_REPOSITORY}.git")
    git(checkout, "fetch", "--quiet", "--depth=1", "origin", ORG_COMMIT)
    revision = git(checkout, "rev-parse", "FETCH_HEAD")
    blob = git(checkout, "rev-parse", f"{revision}:README.org")
    url = f"https://api.github.com/repos/{ORG_REPOSITORY}/readme?ref={revision}"
    request = Request(url, headers={"User-Agent": "README-HQ-public-audit", "Accept": "application/vnd.github+json"})
    with urlopen(request, timeout=20) as response:
        selected = json.load(response)
    assert revision == ORG_COMMIT and (selected["path"], selected["sha"]) == ("README.org", blob), selected
    code, result = readme_result(checkout, base / "org-receipt.json", "--ref", revision, "--profile", "library")
    assert code == 1 and result["cases"]["entrypoint"] is None
    assert "no supported README found at the selected entry point" in result["errors"]
    return {"repository": ORG_REPOSITORY, "commit": revision, "published_readme": selected["path"],
            "published_blob": blob, "validator_exit": code, "validator_errors": result["errors"]}


def graph_controls():
    index = ROOT / "graphify-hq/README.md"
    original = index.read_text(encoding="utf-8")
    before, after = "maps/v0.0.6/README.md", "maps/v0.0.5/README.md"
    assert original.count("](" + before + ")") == original.count("](" + after + ")") == 1
    changed = original.replace("](" + before + ")", "](audit-placeholder)", 1)
    changed = changed.replace("](" + after + ")", "](" + before + ")", 1)
    changed = changed.replace("](audit-placeholder)", "](" + after + ")", 1)
    index.write_text(changed, encoding="utf-8")
    fixture_commit = commit(ROOT, "graphify-hq/README.md")
    nav = command(ROOT / "tools/check_readme_hq.py")
    graph = command(ROOT / "graphify-hq/version_maps.py", "--check")
    plan = command(ROOT / "tools/verify_plan.py", "--mcp")
    assert nav.returncode == graph.returncode == plan.returncode == 0, [x.stderr for x in (nav, graph, plan)]
    assert "6 maps covering 17 version records" in graph.stdout and "67 repair checkpoints" in plan.stdout
    catalog = json.loads((ROOT / "graphify-hq/catalog.json").read_bytes())
    version = next(iter(catalog["versions"]))
    receipt = ROOT / "graphify-hq/maps" / version / "receipt.json"
    previous = receipt.read_bytes()
    changed_receipt = json.loads(previous)
    changed_receipt["graph_sha256"] = "0" * 64
    try:
        write_json(receipt, changed_receipt)
        rejected = command(ROOT / "graphify-hq/version_maps.py", "--check")
    finally:
        receipt.write_bytes(previous)
    assert rejected.returncode != 0 and "Deterministic rebuild differs: receipt.json" in rejected.stderr, rejected.stderr
    return {"fixture_commit": fixture_commit, "index_wrong_destination": after, "reader_exit": nav.returncode,
            "graphify_exit": graph.returncode, "plan_exit": plan.returncode,
            "corrupt_graph_receipt_exit": rejected.returncode,
            "graphify_report": graph.stdout.splitlines()[-1], "plan_report": plan.stdout.splitlines()[-1]}


def main():
    assert git(ROOT, "rev-parse", "HEAD") == CANDIDATE
    mode = sys.argv[1]
    with TemporaryDirectory(prefix="readme-hq-purple-") as tmp:
        base = Path(tmp)
        if mode == "graph":
            cases = {"graphify_navigation": graph_controls()}
        else:
            cases = {"first_action_binding": first_action_binding(base)}
            if sys.platform == "linux":
                cases["rendered_org_readme"] = org_homepage(base)
    data = {"candidate": CANDIDATE, "platform": sys.platform, "run": os.getenv("GITHUB_RUN_ID"),
            "attempt": os.getenv("GITHUB_RUN_ATTEMPT"), "job": os.getenv("GITHUB_JOB"), "observations": cases}
    write_json(Path(sys.argv[2]), data)
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
