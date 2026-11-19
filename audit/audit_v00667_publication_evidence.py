"""Reproduce new README HQ findings at the exact v0.0.6.67 candidate."""
from contextlib import contextmanager
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.error import HTTPError

from PIL import Image

ROOT = Path.cwd()
CANDIDATE = "8d50caec2bc6fcb998994a1fd302294a029325f9"
CHECKER = ROOT / "tools/check_readme_hq.py"
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "learning")]
from check_readme_hq import check_evidence
from hq_data import GitTree
from hq_navigation import check_document, readme_path
import hq_smoke
import intake


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, stderr=subprocess.PIPE).strip()


def commit(root):
    git(root, "add", ".")
    git(root, "-c", "user.name=README HQ Audit", "-c", "user.email=audit@example.invalid",
        "commit", "-qm", "Add synthetic audit fixture")
    return git(root, "rev-parse", "HEAD")


@contextmanager
def fixture(files, origin=None):
    with TemporaryDirectory() as temp:
        root = Path(temp)
        git(root, "init", "-qb", "main")
        if origin:
            git(root, "remote", "add", "origin", origin)
        for name, content in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content if isinstance(content, bytes) else content.encode())
        yield root, commit(root)


@contextmanager
def candidate_checkout():
    with TemporaryDirectory() as temp:
        root = Path(temp) / "candidate"
        git(ROOT, "worktree", "add", "--detach", str(root), CANDIDATE)
        try:
            yield root
        finally:
            git(ROOT, "worktree", "remove", "--force", str(root))


def invoke(script, *args, cwd=ROOT):
    return subprocess.run([sys.executable, str(script), *map(str, args)], cwd=cwd, capture_output=True, text=True)


def navigation(root, name="README.md"):
    errors, gaps = [], []
    checked = check_document(GitTree(root), name, errors, gaps)
    return {"checked": checked, "errors": errors, "gaps": gaps}


def smoke_spec(root, sha, **spec):
    path = root / "fixture-smoke.json"
    path.write_text(json.dumps({"commit": sha, **spec}), encoding="utf-8")
    return path


def publication_readme():
    with candidate_checkout() as root:
        preferred = root / ".github/README.md"
        preferred.write_text("# Alternate homepage\n\nThis is the visible reference documentation entry point.\n\n[Missing](missing.md)\n",
                             encoding="utf-8")
        commit(root)
        repo_checker = root / "tools/check_readme_hq.py"
        default = invoke(repo_checker)
        targeted = invoke(repo_checker, "--repo", root, "--profile", "reference")
        assert readme_path(GitTree(root).entries(), homepage=True) == ".github/README.md"
        assert default.returncode == 0 and targeted.returncode == 1
        assert ".github/README.md" in targeted.stderr and "missing tracked local target" in targeted.stderr
        return {"effective_entrypoint": ".github/README.md", "repository_default_exit": default.returncode,
                "adopter_mode_exit": targeted.returncode, "adopter_diagnostic": targeted.stderr.strip()}


def subproject_smoke():
    readme = "# Package\n\nA reference package with a reproducible first action.\n"
    files = {"README.md": readme, "packages/example/README.md": readme,
             "packages/example/first.py": 'print("PACKAGE_READY")\n'}
    with fixture(files) as (root, sha):
        relative = "packages/example"
        command = [sys.executable, "first.py"]
        hand_run = subprocess.run(command, cwd=root / relative, capture_output=True, text=True)
        spec = smoke_spec(root, sha, argv=command, expected={"exit": 0, "contains": "PACKAGE_READY"})
        receipt = root / "out.json"
        audited = invoke(CHECKER, "--repo", root, "--subproject", relative, "--profile", "reference",
                         "--smoke", spec, "--receipt", receipt)
        cases = json.loads(receipt.read_bytes())["cases"]
        assert hand_run.returncode == 0 and hand_run.stdout.strip() == "PACKAGE_READY"
        assert audited.returncode == 1 and cases["entrypoint"] == relative + "/README.md"
        assert cases["first_action"]["result"] == "failed"
        return {"entrypoint": cases["entrypoint"], "command_from_package_exit": hand_run.returncode,
                "checked_command_exit": cases["first_action"]["observed"]["exit"],
                "smoke_result": cases["first_action"]["result"]}


def split_stream_output():
    with fixture({"README.md": "# Example\n"}) as (root, sha):
        argv = [sys.executable, "-c", 'import sys; sys.stdout.write("PACK"); sys.stderr.write("AGE_READY")']
        direct = subprocess.run(argv, capture_output=True, text=True)
        spec = smoke_spec(root, sha, argv=argv, expected={"exit": 0, "contains": "PACKAGE_READY"})
        audited = hq_smoke.verify_first_action(GitTree(root), spec)
        assert "PACKAGE_READY" not in direct.stdout and "PACKAGE_READY" not in direct.stderr
        assert audited["result"] == "passed"
        return {"stdout": direct.stdout, "stderr": direct.stderr, "expected_marker": "PACKAGE_READY",
                "smoke_result": audited["result"]}


def expected_http_error_body():
    with fixture({"README.md": "# Example\n"}) as (root, sha):
        url = "https://example.invalid/audit-fixture"
        spec = smoke_spec(root, sha, url=url, expected={"http_status": 404, "contains": "Expected missing page"})
        response = HTTPError(url, 404, "Not Found", {}, BytesIO(b"Expected missing page"))
        with patch.object(hq_smoke, "urlopen", side_effect=response):
            audited = hq_smoke.verify_first_action(GitTree(root), spec, allow_network=True)
        assert audited["result"] == "failed" and audited["observed"] == {"http_status": 404, "content_match": False}
        return {"expected_status": 404, "response_body_has_expected_text": True,
                "smoke_result": audited["result"], "body_comparison": audited["observed"]["content_match"]}


def bare_gfm_links():
    readme = ("# Project\n\nVisit https://example.invalid/one and www.example.invalid/two.\n\n"
              "For comparison visit [this explicit route](https://example.invalid/control).\n")
    with fixture({"README.md": readme}) as (root, _):
        observed = navigation(root)
        assert not observed["errors"] and observed["checked"] == 0
        assert len(observed["gaps"]) == 1 and "/control" in observed["gaps"][0]
        return {"renderable_bare_url_count": 2, "unchanged_explicit_link_control": True,
                "checked": observed["checked"], "unchecked_count": len(observed["gaps"])}


def lfs_media():
    image = BytesIO()
    Image.new("RGB", (1, 1), "blue").save(image, format="PNG")
    png = image.getvalue()
    oid = sha256(png).hexdigest()
    pointer = f"version https://git-lfs.github.com/spec/v1\noid sha256:{oid}\nsize {len(png)}\n"
    with fixture({"README.md": "# Example\n\n![Project logo](logo.png)\n\n![Control](control.png)\n",
                  ".gitattributes": "logo.png filter=lfs diff=lfs merge=lfs -text\n",
                  "logo.png": pointer, "control.png": png}) as (root, _):
        assert GitTree(root).read("logo.png") == pointer.encode()
        observed = navigation(root)
        assert observed["checked"] == 1 and not observed["gaps"]
        assert len(observed["errors"]) == 1 and "invalid or unreadable image: logo.png" in observed["errors"][0]
        return {"git_blob_kind": "valid Git LFS pointer", "equivalent_png_control_passed": True, **observed}


def contradictory_learning():
    repository = "example/readme-hq-audit-fixture"
    with fixture({"README.md": "# Evidence\n"}, "https://github.com/" + repository + ".git") as (root, sha):
        catalog = json.loads((ROOT / "techniques/registry.json").read_bytes())["techniques"]
        technique = next(row["id"] for row in catalog if row["status"] == "active")
        source = {"checkout": str(root), "repository": repository, "ref": sha, "path": "README.md",
                  "line": 1, "anchor": "Evidence", "visibility": "public"}
        base = {"source": "src", "technique": technique}
        findings = [{**base, "decision": "adopt", "rationale": "Fits the target."},
                    {**base, "decision": "declined", "rationale": "Does not fit the target."}]
        request = {"visibility": "public", "sources": [{"id": "src", **source}], "selected": ["src"],
                   "target": {**source, "audience": "Readers", "capability": "Evidence"}, "findings": findings}
        def fetch(path):
            return {"private": False, "visibility": "public"} if path == repository else {"sha": sha}
        saved = intake.record_intake(request, root / "receipts", fetch=fetch)
        records = json.loads(saved.read_bytes())["recommendations"]
        assert len(records) == 2 and records[0]["source"] == records[1]["source"]
        assert records[0]["target"] == records[1]["target"] and records[0]["technique"] == records[1]["technique"]
        decisions = sorted(row["decision"] for row in records)
        assert decisions == ["adopt", "declined"]
        return {"same_target": True, "same_source": True, "same_technique": True, "recorded_decisions": decisions}


def plan_inventory_loss():
    rel = Path("graphify-hq/plans/v0.0.6-repairs")
    with candidate_checkout() as root:
        folder = root / rel
        manifest_file = folder / "manifest.json"
        before = json.loads((folder / "receipt.json").read_bytes())
        manifest = json.loads(manifest_file.read_bytes())
        assert manifest["source_files"]
        manifest["source_files"] = []
        manifest_file.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        compiler = root / "graphify-hq/template/v0.0.8/evidence_map.py"
        rebuilt = invoke(compiler, manifest_file, folder, cwd=root)
        assert rebuilt.returncode == 0, rebuilt.stderr
        checked = invoke(root / "tools/verify_plan.py", "--mcp", cwd=root)
        receipt = json.loads((folder / "receipt.json").read_bytes())
        assert receipt["mcp_verified"] and before["source_files"] and receipt["source_files"] == []
        assert receipt["nodes"] < before["nodes"]
        assert checked.returncode == 0 and "Verified 67 repair checkpoints" in checked.stdout, checked.stderr
        return {"baseline_inventory_count": len(before["source_files"]), "rebuilt_inventory_count": 0,
                "baseline_nodes": before["nodes"], "rebuilt_nodes": receipt["nodes"], "plan_check_exit": checked.returncode}


def verified_receipt_bridge():
    with fixture({"README.md": "# Evidence\n\nThis reference README supplies a concrete project description.\n"}) as (root, _):
        tree = GitTree(root)
        file = root / "evidence/public/observed.json"
        file.parent.mkdir(parents=True)
        verification = invoke(CHECKER, "--repo", root, "--profile", "reference", "--receipt", file)
        assert verification.returncode == 0, verification.stderr
        emitted = json.loads(file.read_bytes())
        commit(root)
        item = {"status": "verified", "receipt": "evidence/public/observed.json",
                "url": "https://github.com/example/fixture/blob/" + tree.commit + "/README.md#L1"}
        try:
            check_evidence(item, GitTree(root))
        except ValueError as error:
            assert "run receipt does not establish the stated source and result" in str(error)
            assert emitted["result"] == "passed" and "source_commit" not in emitted
            return {"generated_receipt_result": emitted["result"], "registry_accepts_generated_receipt": False,
                    "generated_receipt_top_level_keys": sorted(emitted), "registry_diagnostic": str(error)}
    raise AssertionError("a raw CLI receipt unexpectedly satisfied the registry schema")


def nested_repo_path():
    root_home = "# Project\n\nThis project uses a complete public homepage readme.\n\n[Missing](missing.md)\n"
    nested_home = "# Package\n\nThis project package has a different readme.\n"
    with fixture({"README.md": root_home, "nested/README.md": nested_home}) as (root, sha):
        actual = invoke(CHECKER, "--repo", root, "--profile", "reference")
        nested = invoke(CHECKER, "--repo", root / "nested", "--profile", "reference")
        assert actual.returncode == 1 and nested.returncode == 0
        assert sha in nested.stdout and "README: README.md" in nested.stdout
        return {"repo_root_exit": actual.returncode, "repo_subdirectory_exit": nested.returncode,
                "intent_explicit_subproject": False, "same_commit_reported": True}


def main():
    assert git(ROOT, "rev-parse", "HEAD") == CANDIDATE
    cases = (publication_readme, subproject_smoke, split_stream_output, expected_http_error_body,
             bare_gfm_links, lfs_media, contradictory_learning, plan_inventory_loss,
             verified_receipt_bridge, nested_repo_path)
    results = {}
    for case in cases:
        results[case.__name__] = case()
        print("Observed", case.__name__, flush=True)
    Path(sys.argv[1]).write_text(json.dumps({"candidate": CANDIDATE, "observations": results}, indent=2) + "\n",
                                encoding="utf-8")


if __name__ == "__main__":
    main()
