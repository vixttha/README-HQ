"""Reproduce README HQ rendering, learning, and diagnostic findings on a pinned tree."""
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
import json
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.error import HTTPError

ROOT = Path.cwd()
CANDIDATE = "8d50caec2bc6fcb998994a1fd302294a029325f9"
CHECKER = ROOT / "tools/check_readme_hq.py"
sys.path[:0] = [str(ROOT / directory) for directory in ("tools", "learning")]
from hq_data import GitTree
from hq_navigation import PARSER, check_document
import intake


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE, text=True).strip()


def commit(root):
    git(root, "add", ".")
    git(root, "-c", "user.name=README HQ Audit", "-c", "user.email=audit@example.invalid", "commit", "-qm", "Fixture")
    return git(root, "rev-parse", "HEAD")


@contextmanager
def fixture(files, origin=None):
    with TemporaryDirectory() as temp:
        root = Path(temp)
        git(root, "init", "-qb", "main")
        if origin:
            git(root, "remote", "add", "origin", origin)
        for name, body in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
        yield root, commit(root)


@contextmanager
def candidate_checkout():
    with TemporaryDirectory() as temp:
        checkout = Path(temp) / "candidate"
        git(ROOT, "worktree", "add", "--detach", str(checkout), CANDIDATE)
        try:
            yield checkout
        finally:
            git(ROOT, "worktree", "remove", "--force", str(checkout))


def run(script, *args, cwd=ROOT):
    return subprocess.run([sys.executable, str(script), *map(str, args)], cwd=cwd, capture_output=True, text=True)


def hide_table(path, marker):
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    start = next(i for i, line in enumerate(lines) if line.startswith(marker))
    end = next(i for i in range(start, len(lines)) if not lines[i].startswith("| "))
    def rendered_tables(content):
        return sum(token.type == "table_open" for token in PARSER.parse(content))
    old = "".join(lines)
    new = "".join(lines[:start] + ["```text\n"] + lines[start:end] + ["```\n"] + lines[end:])
    assert rendered_tables(old) - rendered_tables(new) == 1
    path.write_text(new, encoding="utf-8")
    return sum(line.startswith("| ") for line in lines[start + 2:end])


def fenced_plan_table():
    with candidate_checkout() as root:
        rows = hide_table(root / "plans/v0.0.6-repairs/README.md", "| Checkpoint | GitHub issue |")
        checked = run(root / "tools/verify_plan.py", "--mcp", cwd=root)
        assert checked.returncode == 0 and "Verified 67 repair checkpoints" in checked.stdout, checked.stderr
        assert rows == 67
        return {"rows_hidden_in_code_fence": rows, "rendered_tables_removed": 1, "plan_verifier_exit": checked.returncode}


def fenced_version_table():
    with candidate_checkout() as root:
        rows = hide_table(root / "versions/README.md", "| Version | README HQ guide")
        commit(root)
        reader = run(root / "tools/check_readme_hq.py", cwd=root)
        maps = run(root / "graphify-hq/version_maps.py", "--check", cwd=root)
        assert rows == 6 and reader.returncode == 0 and maps.returncode == 0, (reader.stderr, maps.stderr)
        assert "Graphify verified 6 maps" in maps.stdout
        return {"version_rows_hidden_in_code_fence": rows, "rendered_tables_removed": 1,
                "reader_exit": reader.returncode, "graphify_exit": maps.returncode}


def repeated_public_metadata():
    repository = "example/readme-hq-audit-fixture"
    body = "".join(f"Observation {number:02}\n" for number in range(1, 34))
    with fixture({"README.md": body}, "https://github.com/" + repository + ".git") as (root, sha):
        location = {"repository": repository, "checkout": str(root), "visibility": "public",
                    "ref": sha, "path": "README.md"}
        sources = [{**location, "id": f"source-{number:02}", "line": number, "anchor": f"Observation {number:02}"}
                   for number in range(1, 33)]
        request = {"visibility": "public", "sources": sources, "target": {
            **location, "line": 33, "anchor": "Observation 33", "audience": "Readers", "capability": "Example"},
            "selected": [row["id"] for row in sources], "findings": []}
        calls = []
        def reply(route):
            calls.append(route)
            return {"visibility": "public", "private": False} if route == repository else {"sha": sha}
        output = intake.record_intake(request, root / "unlimited", fetch=reply)
        assert len(json.loads(output.read_bytes())["sources"]) == 32
        counts = sorted(Counter(calls).values())
        total = len(calls)
        assert counts == [33, 33] and total == 66
        calls.clear()
        def budget(route):
            if len(calls) >= 60:
                calls.append(route)
                raise HTTPError("https://example.invalid/audit-fixture", 403, "Fixture request budget", {}, None)
            return reply(route)
        try:
            intake.record_intake(request, root / "limited", fetch=budget)
        except HTTPError as error:
            assert error.code == 403 and len(calls) == 61 and not (root / "limited").exists()
        else:
            raise AssertionError("expected the fixture's 60-request budget to fail")
        return {"distinct_readme_observations": 32, "calls_to_each_of_two_endpoints": counts,
                "successful_fixture_call_count": total, "limited_fixture_failed_on_call": len(calls)}


def raw_route_heading():
    repo = "vixttha/README-HQ"
    base = "https://github.com/" + repo
    readme = f"[Raw]({base}/raw/main/guide.md#guide)\n\n[Rendered]({base}/blob/main/guide.md#guide)\n"
    with fixture({"README.md": readme, "guide.md": "# Guide\n"}, base + ".git") as (root, _):
        errors, gaps = [], []
        checked = check_document(GitTree(root), "README.md", errors, gaps)
        assert checked == 2 and not errors and not gaps
        return {"raw_markdown_heading_counted_as_checked": True,
                "rendered_blob_heading_control_passed": True, "checked": checked}


def receipt_sink_hides_errors():
    readme = "# Project\n\nThis project has a descriptive and reproducible reference guide.\n\n[Missing](missing.md)\n"
    with fixture({"README.md": readme}) as (root, _):
        sink = root / "receipt-directory"
        sink.mkdir()
        args = ("--repo", root, "--profile", "reference")
        control = run(CHECKER, *args)
        failed = run(CHECKER, *args, "--receipt", sink)
        assert control.returncode == failed.returncode == 1 and "missing tracked local target" in control.stderr
        assert "IsADirectoryError" in failed.stderr and "missing tracked local target" not in failed.stderr
        return {"ordinary_exit": control.returncode, "bad_sink_exit": failed.returncode,
                "bad_sink_traceback": True, "bad_sink_hides_original_diagnostic": True}


def draft_ancestor_symlink():
    readme = "# Project\n\nThis fixture has a reference guide maintained with the project.\n\n[Section](docs/guide.md#draft-only)\n"
    files = {"README.md": readme, "docs/guide.md": "# Original\n", "other/guide.md": "# Draft only\n"}
    with fixture(files) as (root, _):
        assert "Draft only" not in GitTree(root).read("docs/guide.md").decode()
        shutil.rmtree(root / "docs")
        (root / "docs").symlink_to("other", target_is_directory=True)
        assert not (root / "docs/guide.md").is_symlink()
        args = ("--repo", root, "--profile", "reference")
        published = run(CHECKER, *args)
        draft = run(CHECKER, *args, "--draft")
        assert published.returncode == 1 and draft.returncode == 0, draft.stderr
        assert "missing local heading" in published.stderr and "checked 1 local links" in draft.stdout
        return {"published_commit_exit": published.returncode, "draft_mode_exit": draft.returncode,
                "tracked_candidate_path": "docs/guide.md", "read_through_symlink_to": "other/guide.md"}


def disjoint_same_file_spans():
    with candidate_checkout() as root:
        path = root / "techniques/registry.json"
        data = json.loads(path.read_bytes())
        evidence = data["techniques"][0]["evidence"]
        source = evidence[0]["url"].split("#")[0]
        evidence[0]["url"] = source + "#L1-L2"
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        commit(root)
        control = run(root / "tools/check_readme_hq.py", cwd=root)
        evidence.append({"status": "observed", "url": source + "#L8-L9"})
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        commit(root)
        rejected = run(root / "tools/check_readme_hq.py", cwd=root)
        assert control.returncode == 0 and rejected.returncode == 1
        assert "duplicate evidence content" in rejected.stderr
        return {"accepted_source_span": "L1-L2", "rejected_disjoint_span": "L8-L9",
                "single_span_exit": control.returncode, "two_span_exit": rejected.returncode}


def unresolved_run_reference():
    with candidate_checkout() as root:
        path = root / "techniques/registry.json"
        data = json.loads(path.read_bytes())
        evidence = data["techniques"][0]["evidence"][0]
        parts = evidence["url"].split("/blob/", 1)
        repository = parts[0].removeprefix("https://github.com/")
        sha, name = parts[1].split("/", 1)
        source = next(row for row in json.loads((root / "techniques/public-source-inventory.json").read_bytes())
                      if row[:3] == [repository.lower(), sha, name])
        identifier = "evidence/public/synthetic-missing-run.json"
        rec = root / identifier
        rec.parent.mkdir(parents=True)
        rec.write_text(json.dumps({"source_repository": repository, "source_commit": sha, "source_path": name,
                                   "source_span": "L1", "source_sha256": source[4], "environment": "Synthetic fixture",
                                   "run_url": "https://github.com/vixttha/README-HQ/actions/runs/0",
                                   "expected": "fixture result", "observed": "fixture result",
                                   "visibility": "public", "result": "pass"}) + "\n", encoding="utf-8")
        evidence.update(status="verified", url=evidence["url"] + "#L1", receipt=identifier)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        commit(root)
        result = run(root / "tools/check_readme_hq.py", cwd=root)
        assert result.returncode == 0, result.stderr
        return {"claimed_run_id": 0, "source_identity_in_pinned_inventory": True, "catalog_validator_exit": result.returncode}


def main():
    assert git(ROOT, "rev-parse", "HEAD") == CANDIDATE
    cases = (fenced_plan_table, fenced_version_table, repeated_public_metadata, raw_route_heading,
             receipt_sink_hides_errors, draft_ancestor_symlink, disjoint_same_file_spans, unresolved_run_reference)
    results = {}
    for case in cases:
        results[case.__name__] = case()
        print("Observed", case.__name__, flush=True)
    Path(sys.argv[1]).write_text(json.dumps({"candidate": CANDIDATE, "observations": results}, indent=2) + "\n",
                                encoding="utf-8")


if __name__ == "__main__":
    main()
