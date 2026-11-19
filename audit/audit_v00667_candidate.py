"""Reproduce the README HQ post-repair audit against the pinned candidate."""
from contextlib import contextmanager
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

ROOT = Path.cwd()
CANDIDATE = "8d50caec2bc6fcb998994a1fd302294a029325f9"
STABLE = "f50e3749dab90ddfe35894284d1660097a1fb1a8"
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "learning"), str(ROOT / "graphify-hq/template/v0.0.8")]

from hq_data import GitTree
from hq_navigation import check_document
from intake import record_intake
from verify_plan import stage_partitions
import evidence_map


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def command(*args, cwd=ROOT):
    return subprocess.run([sys.executable, *map(str, args)], cwd=cwd, text=True, capture_output=True)


def commit(root):
    git(root, "add", ".")
    git(root, "-c", "user.email=audit@example.invalid", "-c", "user.name=README HQ Audit", "commit", "-qm", "Add audit fixture")
    return git(root, "rev-parse", "HEAD")


@contextmanager
def fixture(files, github=False):
    with TemporaryDirectory() as name:
        root = Path(name)
        git(root, "init", "-qb", "main")
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        if github:
            git(root, "remote", "add", "origin", "https://github.com/example/readme-hq-audit-fixture.git")
        yield root, commit(root)


def observe_readme(tree):
    errors, unchecked = [], []
    count = check_document(tree, "README.md", errors, unchecked)
    return {"links": count, "errors": errors, "unchecked": unchecked}


def agent_route():
    current = git(ROOT, "show", f"{CANDIDATE}:AGENTS.md")
    old_cli = git(ROOT, "show", f"{STABLE}:tools/check_readme_hq.py")
    paths = git(ROOT, "ls-tree", "-r", "--name-only", STABLE, "learning/intake.py")
    published = git(ROOT, "ls-remote", "origin", "refs/heads/readme-hq").split()[0]
    assert published == STABLE and "branch" in current and "`readme-hq`" in current
    assert '"--repo"' not in old_cli and not paths
    return {"agent_route": "readme-hq", "public_branch": published, "has_adopter_cli": False, "has_learning_intake": False}


def remote_ref():
    readme = "[Guide](https://github.com/example/readme-hq-audit-fixture/blob/release/next/guide.md#setup)\n"
    with fixture({"README.md": readme, "guide.md": "# Setup\n"}, github=True) as (root, sha):
        git(root, "update-ref", "refs/remotes/origin/release/next", sha)
        before = observe_readme(GitTree(root))
        git(root, "branch", "release/next", sha)
        after = observe_readme(GitTree(root))
        assert before["links"] == 0 and "unresolved same-repository ref" in before["unchecked"][0]
        assert after == {"links": 1, "errors": [], "unchecked": []}
        return {"remote_tracking_only": before, "with_local_branch": after}


def picture():
    readme = ('<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="missing-dark.svg">\n'
              '  <img src="logo.svg" alt="Project logo">\n</picture>\n')
    with fixture({"README.md": readme, "logo.svg": '<svg xmlns="http://www.w3.org/2000/svg" />'}) as (root, _):
        result = observe_readme(GitTree(root))
        assert result == {"links": 1, "errors": [], "unchecked": []}
        return {"missing_asset": "missing-dark.svg", **result}


def smoke_file():
    with fixture({"README.md": "# Example\n\nA detailed description of this reference project.\n", "result.txt": "already tracked\n"}) as (root, sha):
        spec = root / "smoke.json"
        receipt = root / "receipt.json"
        spec.write_text(json.dumps({"commit": sha, "argv": [sys.executable, "-c", "pass"], "expected": {"exit": 0, "file": "result.txt"}}), encoding="utf-8")
        completed = command(ROOT / "tools/check_readme_hq.py", "--repo", root, "--profile", "reference", "--smoke", spec, "--receipt", receipt)
        outcome = json.loads(receipt.read_bytes())["cases"]["first_action"]
        assert completed.returncode == 0 and outcome["result"] == "passed"
        return {"command_writes_file": False, "file_in_base_tree": True, "smoke_result": outcome["result"]}


def receipt_error():
    with fixture({"README.md": "# Example\n\nA detailed description of the reference project.\n"}) as (root, _):
        (root / "README.md").unlink()
        receipt = root / "receipt.json"
        completed = command(ROOT / "tools/check_readme_hq.py", "--repo", root, "--profile", "reference", "--draft", "--receipt", receipt)
        assert completed.returncode != 0 and not receipt.exists() and "Traceback" in completed.stderr
        return {"error": completed.stderr.splitlines()[-1], "receipt_written": receipt.exists(), "exit": completed.returncode}


def inventory():
    registry_path = ROOT / "techniques/registry.json"
    inventory_path = ROOT / "techniques/public-source-inventory.json"
    registry = json.loads(registry_path.read_bytes())
    reviewed = json.loads(inventory_path.read_bytes())
    first = registry["techniques"][0]
    example = ["example/readme-hq-audit-placeholder", "0" * 40, "README.md", "1" * 40, "2" * 64, 20]
    first["evidence"].append({"url": f"https://github.com/{example[0]}/blob/{example[1]}/{example[2]}#L3", "status": "observed"})
    with TemporaryDirectory() as name:
        checkout = Path(name) / "checkout"
        git(ROOT, "worktree", "add", "--detach", str(checkout), CANDIDATE)
        try:
            (checkout / registry_path.relative_to(ROOT)).write_text(json.dumps(registry), encoding="utf-8")
            commit(checkout)
            # The validator opens its own repository, so run the checker in the fixture checkout.
            bad = command(checkout / "tools/check_readme_hq.py")
            (checkout / inventory_path.relative_to(ROOT)).write_text(json.dumps([*reviewed, example]), encoding="utf-8")
            commit(checkout)
            accepted = command(checkout / "tools/check_readme_hq.py")
            assert bad.returncode == 1 and "absent from the independently reviewed public source inventory" in bad.stderr
            assert accepted.returncode == 0
            return {"registry_only_exit": bad.returncode, "registry_and_inventory_exit": accepted.returncode, "validator": accepted.stdout.splitlines()[0]}
        finally:
            git(ROOT, "worktree", "remove", "--force", str(checkout))


def learning_aliases():
    with fixture({"README.md": "# Source\n"}, github=True) as (root, sha), TemporaryDirectory() as name:
        out = Path(name)
        repo = "example/readme-hq-audit-fixture"
        evidence = {"repository": repo, "visibility": "public", "checkout": str(root), "ref": sha,
                    "path": "README.md", "line": 1, "anchor": "Source"}
        def fetch(route):
            return {"private": False, "visibility": "public"} if route == repo else {"sha": sha}
        draft = {"problem": "Confusing setup", "practice": "Show a setup command", "outcome": "Clear entry point"}
        def learn(alias):
            return record_intake({"visibility": "public", "sources": [{"id": alias, **evidence}],
                                  "selected": [alias], "target": {**evidence, "audience": "Readers", "capability": "Setup"},
                                  "findings": [{"source": alias, "candidate": draft}]}, out, fetch=fetch)
        first, repeat, renamed = learn("source-a"), learn("source-a"), learn("source-b")
        assert first == repeat and first != renamed and len(list(out.glob("*.json"))) == 2
        one, two = (json.loads(p.read_bytes()) for p in (first, renamed))
        assert set(k for k in one if one[k] != two[k]) == {"selected"}
        return {"literal_repeat_is_idempotent": True, "alias_only_change_creates_new_history": True, "changed_fields": ["selected"]}


def publish_gap():
    with TemporaryDirectory() as name:
        root = Path(name)
        output = root / "output"
        output.mkdir()
        (output / "graph.json").write_text("old graph", encoding="utf-8")
        (output / "receipt.json").write_text("old receipt", encoding="utf-8")
        rename = evidence_map.os.replace
        observed = []
        def observe(source, dest):
            if Path(dest) == output:
                observed.append({path: (output / path).exists() for path in ("graph.json", "receipt.json")})
            return rename(source, dest)
        with patch.object(evidence_map.os, "replace", side_effect=observe):
            evidence_map.publish_pair(output, {"graph.json": b"new graph", "receipt.json": b"new receipt"})
        assert observed == [{"graph.json": False, "receipt.json": False}]
        assert (output / "graph.json").read_bytes() == b"new graph"
        return {"reader_between_renames": observed[0], "final_output_replaced": True}


def partition_file_capacity():
    with TemporaryDirectory() as name:
        features = []
        for number in range(1, 26):
            feature = {"id": f"checkpoint-{number}", "label": f"Checkpoint {number}"}
            for relation in evidence_map.RELATIONS:
                feature[relation] = [{"path": f"{relation}/{number}.md", "anchor": "# Evidence"}]
            features.append(feature)
        paths = stage_partitions(features, Path(name) / "manifest", CANDIDATE, "vixttha/README-HQ")
        assert len(paths) == 1
        manifest = evidence_map.read_manifest(paths[0])
        assert len(manifest["source_files"]) == 75
        try:
            evidence_map.validate_manifest(manifest)
        except ValueError as error:
            assert "64 unique source file paths" in str(error)
            return {"features": len(manifest["features"]), "files": len(manifest["source_files"]),
                    "compiler": str(error)}
        raise AssertionError("expected the compiler to reject the generated manifest")


def named_anchor_control():
    readme = '<a name="custom-route"></a>\n\n[Route](#custom-route)\n'
    with fixture({"README.md": readme}) as (root, _):
        result = observe_readme(GitTree(root))
        assert result == {"links": 1, "errors": [], "unchecked": []}
        return result


def release_row():
    original = (ROOT / "versions/README.md").read_text(encoding="utf-8")
    wrong = original.replace("history/aldervale/readme-hq/readme-hq/versions/v0.0.5/README.md", "history/aldervale/readme-hq/readme-hq/versions/v0.0.4/README.md")
    assert original != wrong
    with TemporaryDirectory() as name:
        checkout = Path(name) / "checkout"
        git(ROOT, "worktree", "add", "--detach", str(checkout), CANDIDATE)
        try:
            (checkout / "versions/README.md").write_text(wrong, encoding="utf-8")
            commit(checkout)
            check = command(checkout / "tools/check_readme_hq.py")
            assert check.returncode == 0
            return {"version_row": "v0.0.5", "linked_guide_version": "v0.0.4", "checker_exit": check.returncode}
        finally:
            git(ROOT, "worktree", "remove", "--force", str(checkout))


def main():
    assert git(ROOT, "rev-parse", "HEAD") == CANDIDATE
    results = {}
    for reproduce in (agent_route, remote_ref, picture, smoke_file, receipt_error, inventory, learning_aliases, publish_gap, partition_file_capacity, release_row, named_anchor_control):
        results[reproduce.__name__] = reproduce()
        print(f"Observed {reproduce.__name__}", flush=True)
    Path(sys.argv[1]).write_text(json.dumps({"commit": CANDIDATE, "observations": results}, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
