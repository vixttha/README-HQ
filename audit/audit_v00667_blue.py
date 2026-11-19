"""Blue audit of diagnostic, retry, and evidence behavior on a pinned candidate."""
import argparse
from contextlib import redirect_stderr
from hashlib import sha256
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.error import HTTPError

ROOT = Path.cwd()
CANDIDATE = "8d50caec2bc6fcb998994a1fd302294a029325f9"
KIT = ROOT / "graphify-hq/template/v0.0.8"


def git(directory, *args):
    return subprocess.check_output(["git", "-C", str(directory), *args], text=True).strip()


def commit(directory):
    git(directory, "add", "--all")
    git(directory, "-c", "user.email=fixture@example.invalid", "-c", "user.name=Fixture", "commit", "-qm", "Blue fixture")
    return git(directory, "rev-parse", "HEAD")


def command(program, *args):
    return subprocess.run(
        [sys.executable, str(program), *map(str, args)],
        encoding="utf-8", errors="replace", capture_output=True, timeout=90,
    )


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def adopter(base):
    repo = base / "adopter"
    repo.mkdir()
    git(repo, "init", "--quiet")
    git(repo, "config", "core.autocrlf", "false")
    git(repo, "remote", "add", "origin", "https://github.com/example/blue-readme-fixture.git")
    (repo / "README.md").write_text("# Blue fixture\n\nThe fixture checks first-action reporting.\n", encoding="utf-8")
    (repo / "first_action.py").write_text(
        'from pathlib import Path\nimport sys\n'
        'mode = Path("fixture-state.txt").read_text().strip()\n'
        'if mode == "ready":\n    print("READY")\nelse:\n'
        '    print(mode, file=sys.stderr)\n    sys.exit(7)\n',
        encoding="utf-8",
    )
    return repo


def run_smoke(base, repo, name, spec):
    entry = base / f"{name}-spec.json"
    receipt = base / f"{name}-receipt.json"
    write_json(entry, spec)
    result = command(ROOT / "tools/check_readme_hq.py", "--repo", repo, "--profile", "reference",
                     "--smoke", entry, "--receipt", receipt)
    data = json.loads(receipt.read_bytes())
    return {"exit": result.returncode, "stderr": result.stderr.splitlines(), "overall": data["result"],
            "smoke": data["cases"]["first_action"], "unchecked": data["unchecked"]}


def smoke_cases(base, repo):
    args = [sys.executable, "first_action.py"]
    marker = repo / "fixture-state.txt"
    outcomes = []
    for index, mode in enumerate(("ready", "fixture input missing", "fixture option unsupported")):
        marker.write_text(mode + "\n", encoding="utf-8")
        revision = commit(repo)
        result = run_smoke(base, repo, f"local-{index}", {"commit": revision, "argv": args,
                           "expected": {"exit": 0, "contains": "READY"}})
        outcomes.append(result)
    revision = git(repo, "rev-parse", "HEAD")
    unchecked = run_smoke(base, repo, "network-disabled", {
        "commit": revision, "url": "https://example.invalid/readme-hq-blue",
        "expected": {"http_status": 200, "contains": "READY"},
    })
    ok, missing, unsupported = outcomes
    assert (ok["exit"], ok["overall"], ok["smoke"]["result"]) == (0, "passed", "passed"), ok
    assert (unchecked["exit"], unchecked["overall"], unchecked["smoke"]["result"]) == (0, "passed", "unchecked"), unchecked
    assert missing["exit"] == unsupported["exit"] == 1, outcomes
    assert missing["stderr"] == unsupported["stderr"] == ["first action failed its expected result"], outcomes
    for trial, hidden in ((missing, "fixture input missing"), (unsupported, "fixture option unsupported")):
        expected = sha256((hidden + os.linesep).encode()).hexdigest()
        output_sha = trial["smoke"]["observed"]["output_sha256"]
        # Native subprocess output may follow Python's default platform newline.
        assert output_sha in {expected, sha256((hidden + "\n").encode()).hexdigest()}, trial
        assert hidden not in json.dumps(trial), trial
        del trial["smoke"]["argv"]
    del ok["smoke"]["argv"]
    return {"successful_control": ok, "network_disabled": unchecked, "failure_a": missing, "failure_b": unsupported}


def partition_retry(base):
    reference = {"path": "README.md", "anchor": "# README HQ", "line": 1}
    feature = {relation: [reference] for relation in ("documented_in", "changed_in", "tested_by")}
    rows = [{"id": f"checkpoint-{i}", "label": f"Checkpoint {i}", **feature} for i in range(1, 34)]
    request = base / "partition.json"
    output = base / "partitions"
    good = {"repository": "vixttha/README-HQ", "source_commit": CANDIDATE, "features": rows}
    invalid = [*rows[:-1], {key: value for key, value in rows[-1].items() if key != "tested_by"}]
    write_json(request, {**good, "features": invalid})
    program = ROOT / "tools/verify_plan.py"
    partial = command(program, "--partition", request, "--output", output)
    files = sorted(path.relative_to(output).as_posix() for path in output.rglob("manifest.json"))
    write_json(request, good)
    blocked = command(program, "--partition", request, "--output", output)
    fresh = command(program, "--partition", request, "--output", base / "fresh")
    assert partial.returncode != 0 and "tested_by" in partial.stderr, partial.stderr
    assert files == ["part-001/manifest.json"], files
    existing_diagnostic = any(message in blocked.stderr.lower() for message in ("file exists", "file already exists"))
    assert blocked.returncode != 0 and existing_diagnostic, blocked.stderr
    assert fresh.returncode == 0 and "33 ordered checkpoints in 2 manifests" in fresh.stdout, fresh.stdout
    return {"bad_input_exit": partial.returncode, "first_error": "missing tested_by",
            "partial_manifests": files, "same_path_retry_exit": blocked.returncode,
            "same_path_retry_error": "destination already exists", "fresh_path_retry_exit": fresh.returncode}


def intake_triage(base, repo):
    sys.path.insert(0, str(ROOT / "learning"))
    import intake

    path = base / "intake.json"
    output = base / "intake-receipts"
    revision = git(repo, "rev-parse", "HEAD")
    source = {"checkout": str(repo), "repository": "example/blue-readme-fixture", "ref": revision,
              "path": "README.md", "line": 1, "anchor": "# Blue fixture", "visibility": "public"}
    spec = {"visibility": "public", "sources": [{"id": "source", **source}], "selected": ["source"],
            "target": {**source, "audience": "readers", "capability": "first action"}, "findings": []}
    record = intake.record_intake

    def public(route):
        return {"sha": revision} if "/commits/" in route else {"visibility": "public", "private": False}

    def limited(route):
        raise HTTPError("https://api.github.com/repos/" + route, 429, "Too Many Requests", None, None)

    def invoke(data, fetch, dest):
        write_json(path, data)
        captured = io.StringIO()
        with patch.object(sys, "argv", ["intake.py", str(path), str(dest)]), redirect_stderr(captured), \
                patch.object(intake, "record_intake", side_effect=lambda item, directory: record(item, directory, fetch=fetch)):
            try:
                intake.main()
            except SystemExit as error:
                return {"exit": error.code, "stderr": captured.getvalue().splitlines()}
        return {"exit": 0, "stderr": captured.getvalue().splitlines()}

    bad_anchor = {**spec, "sources": [{**spec["sources"][0], "anchor": "No fixture anchor"}]}
    transient = invoke(spec, limited, output)
    invalid = invoke(bad_anchor, public, output)
    control = invoke(spec, public, output)
    assert transient == invalid and transient["exit"] == 2 and control["exit"] == 0
    return {"simulated_http_429": transient, "invalid_pinned_anchor": invalid, "valid_control": control}


def crash_at_promotion(staged, destination):
    sys.path.insert(0, str(KIT))
    from evidence_map import publish_directory

    original_replace = os.replace

    def interrupt(source, target):
        if Path(source) == staged:
            os._exit(91)
        return original_replace(source, target)

    with patch("evidence_map.os.replace", side_effect=interrupt):
        publish_directory(staged, destination)


def graphify_recovery(base, source):
    published = base / "published"
    staged = base / "staged"
    shutil.copytree(source, published)
    shutil.copytree(source, staged)
    receipt = (published / "receipt.json").read_bytes()
    graph = (published / "graph.json").read_bytes()
    result = command(Path(__file__).resolve(), "--crash-at-promotion", staged, published)
    lock = base / ".published.publish-lock"
    previous = lock / "previous"
    assert result.returncode == 91 and not published.exists(), result
    assert receipt == (previous / "receipt.json").read_bytes() and graph == (previous / "graph.json").read_bytes()
    sys.path.insert(0, str(KIT))
    from evidence_map import publish_directory

    try:
        publish_directory(staged, published)
    except FileExistsError:
        replay_blocked = True
    else:
        raise AssertionError("Expected stale-lock retry to fail")
    previous.replace(published)
    lock.rmdir()
    assert (published / "receipt.json").read_bytes() == receipt
    assert (published / "graph.json").read_bytes() == graph
    return {"first_attempt_exit": result.returncode, "publication_missing_after_interruption": True,
            "same_target_retry_blocked": replay_blocked, "prior_pair_recovered_from_lock": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, nargs="?")
    parser.add_argument("--graph-source", type=Path)
    parser.add_argument("--crash-at-promotion", type=Path, nargs=2)
    args = parser.parse_args()
    if args.crash_at_promotion:
        crash_at_promotion(*args.crash_at_promotion)
        return
    assert git(ROOT, "rev-parse", "HEAD") == CANDIDATE
    with TemporaryDirectory(prefix="readme-hq-blue-") as tmp:
        base = Path(tmp)
        if args.graph_source:
            findings = {"graphify_interrupted_publication": graphify_recovery(base, args.graph_source)}
        else:
            repo = adopter(base)
            findings = {"smoke": smoke_cases(base, repo), "partition_retry": partition_retry(base),
                        "learning_diagnostics": intake_triage(base, repo)}
    data = {"candidate": CANDIDATE, "platform": sys.platform, "run": os.getenv("GITHUB_RUN_ID"),
            "attempt": os.getenv("GITHUB_RUN_ATTEMPT"), "job": os.getenv("GITHUB_JOB"), "findings": findings}
    write_json(args.output, data)
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
