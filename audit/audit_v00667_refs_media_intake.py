"""Reproduce README HQ link identity, smoke, learning and Graphify findings."""
from contextlib import contextmanager, chdir
from io import BytesIO
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PIL import Image

ROOT = Path.cwd()
CANDIDATE = "8d50caec2bc6fcb998994a1fd302294a029325f9"
KIT = ROOT / "graphify-hq/template/v0.0.8"
sys.path[:0] = [str(ROOT / path) for path in ("tools", "learning", "graphify-hq")]
sys.path.insert(0, str(KIT))
import evidence_map
from github_provenance import Page, verify_pull_request
from hq_data import GitTree
from hq_navigation import check_document
import hq_smoke
import intake
import version_maps


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, stderr=subprocess.PIPE).strip()


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
        git(root, "add", ".")
        git(root, "-c", "user.name=README HQ Audit", "-c", "user.email=audit@example.invalid", "commit", "-qm", "Fixture")
        yield root, git(root, "rev-parse", "HEAD")


@contextmanager
def candidate_checkout():
    with TemporaryDirectory() as temp:
        root = Path(temp) / "candidate"
        git(ROOT, "worktree", "add", "--detach", str(root), CANDIDATE)
        try:
            yield root
        finally:
            git(ROOT, "worktree", "remove", "--force", str(root))


def run(path, *args, cwd=ROOT):
    return subprocess.run([sys.executable, str(path), *map(str, args)], cwd=cwd, capture_output=True, text=True)


def navigation(root, name="README.md"):
    errors, unchecked = [], []
    checked = check_document(GitTree(root), name, errors, unchecked)
    return {"checked": checked, "errors": errors, "unchecked": unchecked}


def smoke_spec(root, sha, **kwargs):
    path = root / "smoke.json"
    path.write_text(json.dumps({"commit": sha, **kwargs}), encoding="utf-8")
    return path


def remote_tracking_url():
    repo = "vixttha/README-HQ"
    readme = (f"[Wrong published URL](https://github.com/{repo}/blob/origin/main/README.md)\n\n"
              f"[Correct published URL](https://github.com/{repo}/blob/main/README.md)\n")
    with fixture({"README.md": readme}, "https://github.com/" + repo + ".git") as (root, sha):
        git(root, "update-ref", "refs/remotes/origin/main", sha)
        assert not git(root, "for-each-ref", "--format=%(refname)", "refs/heads/origin/main")
        result = navigation(root)
        assert result == {"checked": 2, "errors": [], "unchecked": []}
        return {"github_path_with_no_published_branch": "blob/origin/main/README.md",
                "local_repo_matching_remote_tracking_only": True, **result}


def head_default_branch():
    repo = "vixttha/README-HQ"
    href = f"https://github.com/{repo}/blob/HEAD/only-in-topic.md"
    readme = f"[Topic file through the remote default]({href})\n"
    with fixture({"README.md": readme}, "https://github.com/" + repo + ".git") as (root, main):
        git(root, "update-ref", "refs/remotes/origin/main", main)
        git(root, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
        git(root, "checkout", "-qb", "topic")
        (root / "only-in-topic.md").write_text("# Topic only\n", encoding="utf-8")
        git(root, "add", "only-in-topic.md")
        git(root, "-c", "user.name=Audit", "-c", "user.email=audit@example.invalid", "commit", "-qm", "Topic file")
        assert not git(root, "ls-tree", "refs/remotes/origin/HEAD", "--", "only-in-topic.md")
        result = navigation(root)
        assert result == {"checked": 1, "errors": [], "unchecked": []}
        return {"published_default_has_target": False, "current_local_topic_has_target": True, **result}


def redirect_receipt():
    requested = "https://example.invalid/expected-start"
    destination = "https://example.invalid/a-different-page"
    with fixture({"README.md": "# Route\n"}) as (root, sha):
        spec = smoke_spec(root, sha, url=requested, expected={"http_status": 200, "contains": "Example"})
        class RedirectedResponse(BytesIO):
            status = 200
            def geturl(self):
                return destination
        with patch.object(hq_smoke, "urlopen", return_value=RedirectedResponse(b"Example page")):
            receipt = hq_smoke.verify_first_action(GitTree(root), spec, allow_network=True)
        assert receipt["result"] == "passed" and receipt["url"] == requested
        assert destination not in json.dumps(receipt)
        return {"requested_url": requested, "fixture_final_url": destination, "configured_probe_result": receipt["result"],
                "recorded_final_url": False}


def mixed_smoke_mode():
    with fixture({"README.md": "# Example\n"}) as (root, sha):
        argv = [sys.executable, "-c", 'print("READY")']
        local = smoke_spec(root, sha, argv=argv, expected={"exit": 0, "contains": "READY"})
        tree = GitTree(root)
        assert hq_smoke.verify_first_action(tree, local)["result"] == "passed"
        mixed = smoke_spec(root, sha, argv=argv, url="https://example.invalid/audit",
                           expected={"exit": 0, "contains": "READY"})
        result = hq_smoke.verify_first_action(tree, mixed)
        assert result == {"result": "unchecked", "detail": "network probe not authorized"}
        return {"local_control": "passed", "config_contains_two_modes": True, "mixed_configuration": result}


def unknown_technique():
    repo = "example/readme-hq-audit-fixture"
    with fixture({"README.md": "# Evidence\n"}, "https://github.com/" + repo + ".git") as (root, sha):
        records = json.loads((ROOT / "techniques/registry.json").read_bytes())["techniques"]
        active = next(row["id"] for row in records if row["status"] == "active")
        typo = active + "-typo"
        assert typo not in {row["id"] for row in records}
        proof = {"checkout": str(root), "repository": repo, "visibility": "public", "ref": sha,
                 "path": "README.md", "line": 1, "anchor": "Evidence"}
        request = {"visibility": "public", "sources": [{"id": "source", **proof}],
                   "target": {**proof, "audience": "Readers", "capability": "Evidence"}, "selected": ["source"]}
        def public_fetch(path):
            return {"visibility": "public", "private": False} if path == repo else {"sha": sha}
        def intake_for(technique):
            finding = {"technique": technique, "source": "source", "decision": "adopt", "rationale": "Fits the target."}
            file = intake.record_intake({**request, "findings": [finding]}, root / "receipts", fetch=public_fetch)
            return json.loads(file.read_bytes())
        control, dropped = intake_for(active), intake_for(typo)
        assert len(control["recommendations"]) == 1 and dropped["recommendations"] == []
        assert typo not in json.dumps(dropped) and "errors" not in dropped
        return {"control_recommendations": 1, "typo_recommendations": 0, "typo_or_diagnostic_retained": False}


def truncated_gif():
    image = BytesIO()
    frames = [Image.new("RGB", (6, 6), color) for color in ("red", "blue")]
    frames[0].save(image, format="GIF", save_all=True, append_images=frames[1:], loop=0)
    original = image.getvalue()
    truncated = original[:-3]
    with Image.open(BytesIO(original)) as full:
        full.seek(1)
        full.load()
    with Image.open(BytesIO(truncated)) as bad:
        bad.seek(0)
        bad.load()
        try:
            bad.seek(1)
            bad.load()
        except (OSError, EOFError) as error:
            failure = type(error).__name__
        else:
            raise AssertionError("expected second frame decode failure")
    with fixture({"README.md": "![Animation](broken.gif)\n", "broken.gif": truncated}) as (root, _):
        result = navigation(root)
        assert result == {"checked": 1, "errors": [], "unchecked": []}
        return {"first_frame_decodes": True, "second_frame_decode_error": failure, **result}


def retargeted_pr():
    repo = "example/readme-hq-audit-fixture"
    expected = {"number": 10, "source_branch": "topic"}
    old, new = "1" * 40, "2" * 40
    sha = "3" * 40
    common = {"number": 10, "head": {"sha": sha, "ref": "topic", "repo": {"full_name": repo}},
              "state": "open", "draft": False, "merged": False, "merge_commit_sha": None}
    before = {**common, "base": {"ref": "main", "sha": old, "repo": {"full_name": repo}}}
    after = {**common, "base": {"ref": "release", "sha": new, "repo": {"full_name": repo}}}
    bases = iter([before, after])
    def fetch(route):
        if route == "pulls/10":
            return next(bases)
        assert route == "pulls/10/reviews?per_page=100&page=1"
        return Page([{"state": "APPROVED", "user": {"id": 42}, "commit_id": sha}], False)
    result = verify_pull_request(repo, sha, expected, fetch=fetch)
    assert result["source_relation"] == "current head" and result["exact_commit_approvals"] == 1
    assert "base_commit" not in result and "base_branch" not in result
    return {"initial_base": "main", "final_base": "release", "observation_returned": True,
            "approval_count": result["exact_commit_approvals"]}


def checkpoint_text_loss():
    with candidate_checkout() as checkout:
        plan = checkout / "plans/v0.0.6-repairs/README.md"
        original = plan.read_text(encoding="utf-8")
        heading = "### v0.0.6.1\n"
        following = "### v0.0.6.2\n"
        assert heading in original and following in original
        prefix, rest = original.split(heading, 1)
        previous, suffix = rest.split(following, 1)
        total = sum(line.startswith("- ") for line in previous.splitlines())
        assert total > 0
        plan.write_text(prefix + heading + "\n" + following + suffix, encoding="utf-8")
        checked = run(checkout / "tools/verify_plan.py", "--mcp", cwd=checkout)
        assert checked.returncode == 0 and "Verified 67 repair checkpoints" in checked.stdout, checked.stderr
        return {"checkpoint": "v0.0.6.1", "acceptance_bullets_removed": total,
                "map_artifacts_changed": False, "plan_check_exit": checked.returncode}


def oversize_graph_inventory():
    buffer = BytesIO()
    Image.new("RGB", (700, 700), "green").save(buffer, format="PNG", compress_level=0)
    image = buffer.getvalue()
    with Image.open(BytesIO(image)) as decoded:
        decoded.load()
    with fixture({"README.md": "# Evidence\n", "hero.png": image}) as (root, sha), TemporaryDirectory() as temp:
        ref = {"path": "README.md", "anchor": "# Evidence"}
        manifest = {"repository": "example/readme-hq-audit-fixture", "source_commit": sha, "title": "Evidence",
                    "source_files": ["README.md", "hero.png"], "features": [{"id": "evidence", "label": "Evidence",
                    "documented_in": [ref], "changed_in": [ref], "tested_by": [ref]}]}
        assert evidence_map.validate_manifest(manifest)
        try:
            with chdir(root):
                evidence_map.build(manifest, Path(temp))
        except ValueError as error:
            assert "source blob size exceeds limit" in str(error) and len(image) > evidence_map.MAX_SOURCE_BYTES
            return {"valid_png_bytes": len(image), "verified_as_image": True, "compiler_error": str(error)}
    raise AssertionError("expected the media inventory size failure")


def prerelease_as_stable():
    markdown = "# Changes\n\n## v0.0.6-rc.1\n\nThis is a release candidate.\n"
    with patch.object(version_maps, "source_bytes", return_value=markdown.encode()):
        anchor, line = version_maps.reference(CANDIDATE, "CHANGELOG.md", change=True, version="v0.0.6")
    assert anchor["anchor"] == "## v0.0.6-rc.1" and line == 3
    return {"requested_release": "v0.0.6", "selected_heading": anchor["anchor"], "selected_line": line}


def main():
    assert git(ROOT, "rev-parse", "HEAD") == CANDIDATE
    cases = (remote_tracking_url, head_default_branch, redirect_receipt, mixed_smoke_mode, unknown_technique,
             truncated_gif, retargeted_pr, checkpoint_text_loss, oversize_graph_inventory, prerelease_as_stable)
    observed = {}
    for case in cases:
        observed[case.__name__] = case()
        print("Observed", case.__name__, flush=True)
    Path(sys.argv[1]).write_text(json.dumps({"candidate": CANDIDATE, "observations": observed}, indent=2) + "\n",
                                encoding="utf-8")


if __name__ == "__main__":
    main()
