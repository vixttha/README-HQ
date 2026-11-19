"""Audit README HQ evidence scope, Git isolation, navigation, media, and graph completeness."""
from contextlib import contextmanager
from io import BytesIO
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch
from xml.etree import ElementTree

ROOT = Path.cwd()
CANDIDATE = "8d50caec2bc6fcb998994a1fd302294a029325f9"
CHECKER = ROOT / "tools/check_readme_hq.py"
COMPILER = ROOT / "graphify-hq/template/v0.0.8/evidence_map.py"
sys.path.insert(0, str(ROOT / "tools"))
from hq_data import GitTree
from hq_navigation import check_document
import hq_smoke


def git(root, *args, env=None):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True,
                                   stderr=subprocess.PIPE, env=env).strip()


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
            path.write_bytes(body if isinstance(body, bytes) else body.encode())
        git(root, "add", ".")
        git(root, "-c", "user.name=README HQ audit", "-c", "user.email=audit@example.invalid",
            "commit", "-qm", "Add fixture")
        yield root, git(root, "rev-parse", "HEAD")


def run(script, *args, cwd=ROOT):
    return subprocess.run([sys.executable, str(script), *map(str, args)], cwd=cwd,
                          capture_output=True, text=True)


def links(tree):
    errors, unchecked = [], []
    checked = check_document(tree, "README.md", errors, unchecked)
    return {"checked": checked, "errors": errors, "unchecked": unchecked}


def receipt_scope():
    body = "# Example\n\nThis reference project exposes an installation guide.\n\n[Install](guide.md)\n"
    with fixture({"README.md": body, "guide.md": "# Guide\n"},
                 "https://github.com/example/first-fixture.git") as (root, _):
        path = root / "receipt.json"
        def audit(profile):
            r = run(CHECKER, "--repo", root, "--profile", profile, "--receipt", path)
            assert r.returncode == 0, r.stderr
            return r.stdout, path.read_bytes()
        first_stdout, first = audit("reference")
        same_stdout, second = audit("application")
        git(root, "remote", "set-url", "origin", "https://github.com/example/second-fixture.git")
        other_stdout, third = audit("application")
        assert "example/first-fixture" in first_stdout and "example/second-fixture" in other_stdout
        assert first_stdout == same_stdout and first == second == third
        return {"profiles": ["reference", "application"], "origins": ["example/first-fixture", "example/second-fixture"],
                "three_receipts_are_byte_identical": True}


def workflow_attempt():
    with fixture({"README.md": "# Example\n"}) as (root, _):
        tree = GitTree(root)
        first, second = root / "first.json", root / "second.json"
        environment = {"GITHUB_RUN_ID": "123456", "GITHUB_REPOSITORY": "example/evidence-fixture"}
        with patch.dict(os.environ, {**environment, "GITHUB_RUN_ATTEMPT": "1", "GITHUB_JOB": "linux"}):
            hq_smoke.write_receipt(first, tree, {}, [], [])
        with patch.dict(os.environ, {**environment, "GITHUB_RUN_ATTEMPT": "2", "GITHUB_JOB": "verification"}):
            hq_smoke.write_receipt(second, tree, {}, [], [])
        assert first.read_bytes() == second.read_bytes()
        receipt = json.loads(first.read_bytes())
        assert receipt["run_url"].endswith("/123456")
        return {"attempts": [1, 2], "jobs": ["linux", "verification"],
                "receipts_are_byte_identical": True, "run_url": receipt["run_url"]}


def smoke_worktree_config():
    with fixture({"README.md": "# Example\n"}) as (root, sha):
        config_key = "readmehq.auditMarker"
        git(root, "config", "--local", config_key, "before")
        argv = [sys.executable, "-c", 'import subprocess; subprocess.run(["git", "config", "--local", '
                '"readmehq.auditMarker", "after"], check=True); print("READY")']
        spec = root / "smoke.json"
        spec.write_text(json.dumps({"commit": sha, "argv": argv, "expected": {"exit": 0, "contains": "READY"}}),
                        encoding="utf-8")
        result = hq_smoke.verify_first_action(GitTree(root), spec)
        changed = git(root, "config", "--local", "--get", config_key)
        assert result["result"] == "passed" and changed == "after" and git(root, "rev-parse", "HEAD") == sha
        return {"smoke_result": result["result"], "original_checkout_config_before": "before",
                "original_checkout_config_after": changed, "original_commit_unchanged": True}


def promisor_fetch():
    with fixture({"README.md": "# Partial clone fixture\n"}) as (source, _), TemporaryDirectory() as temp:
        clone = Path(temp) / "clone"
        git(source, "config", "uploadpack.allowFilter", "true")
        git(source, "config", "uploadpack.allowAnySHA1InWant", "true")
        git(source, "clone", "-q", "--filter=blob:none", "--no-checkout", source.as_uri(), str(clone))
        tree = GitTree(clone)
        blob = tree.entries()["README.md"][1]
        env = {**os.environ, "GIT_NO_LAZY_FETCH": "1"}
        def has_object():
            return subprocess.run(["git", "-C", str(clone), "cat-file", "-e", blob], env=env,
                                  capture_output=True).returncode == 0
        assert not has_object()
        assert tree.read("README.md") == b"# Partial clone fixture\n"
        assert has_object()
        return {"allow_network_option_used": False, "blob_present_before_reader": False,
                "blob_present_after_reader": True, "remote_fixture_protocol": "file"}


def empty_graph():
    with fixture({"README.md": "# Example\n"}) as (root, sha), TemporaryDirectory() as temp:
        work = Path(temp)
        manifest = work / "manifest.json"
        manifest.write_text(json.dumps({"repository": "example/evidence-fixture", "source_commit": sha,
                                        "title": "Empty audit fixture", "features": [], "source_files": []}),
                            encoding="utf-8")
        output = work / "outputs"
        build = run(COMPILER, manifest, output, cwd=root)
        assert build.returncode == 0, build.stderr
        receipt = json.loads((output / "receipt.json").read_bytes())
        assert receipt["mcp_verified"] and receipt["nodes"] == 1 and receipt["edges"] == 0
        return {"manifest_features": 0, "manifest_file_inventory": 0, "nodes": receipt["nodes"],
                "edges": receipt["edges"], "mcp_verified": receipt["mcp_verified"]}


def incorrect_svg_namespace():
    bad = '<svg xmlns="urn:example:non-svg"><rect width="10" height="10" /></svg>'
    good = '<svg xmlns="http://www.w3.org/2000/svg"><rect width="10" height="10" /></svg>'
    assert ElementTree.fromstring(bad).tag == "{urn:example:non-svg}svg"
    assert ElementTree.fromstring(good).tag == "{http://www.w3.org/2000/svg}svg"
    with fixture({"README.md": "![Invalid wrapper](bad.svg)\n\n![Control](good.svg)\n",
                  "bad.svg": bad, "good.svg": good}) as (root, _):
        result = links(GitTree(root))
        assert result == {"checked": 2, "errors": [], "unchecked": []}
        return {"non_svg_namespace": "urn:example:non-svg", **result}


def plain_query_option():
    base = "https://github.com/example/evidence-fixture/blob/main/guide.md"
    control = f"[Plain line]({base}?plain=1#L2)\n"
    combined = f"[Plain line with ref type]({base}?plain=1&ref_type=heads#L2)\n"
    with fixture({"README.md": control + "\n" + combined, "guide.md": "# Guide\n\nText\n"},
                 "https://github.com/example/evidence-fixture.git") as (root, _):
        result = links(GitTree(root))
        assert result["checked"] == 1 and len(result["errors"]) == 1 and not result["unchecked"]
        assert "missing local heading or named anchor" in result["errors"][0] and "ref_type=heads" in result["errors"][0]
        return {"single_plain_option_checked": True, "plain_with_second_option": result["errors"][0]}


def main():
    assert git(ROOT, "rev-parse", "HEAD") == CANDIDATE
    results = {}
    for case in (receipt_scope, workflow_attempt, smoke_worktree_config, promisor_fetch,
                 empty_graph, incorrect_svg_namespace, plain_query_option):
        results[case.__name__] = case()
        print("Observed", case.__name__, flush=True)
    Path(sys.argv[1]).write_text(json.dumps({"candidate": CANDIDATE, "observations": results}, indent=2) + "\n",
                                encoding="utf-8")


if __name__ == "__main__":
    main()
