"""Reproduce README HQ setup, evidence-link, and validation findings at the pinned candidate."""
from collections import Counter
from contextlib import contextmanager
import json
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

ROOT = Path.cwd()
CANDIDATE = "8d50caec2bc6fcb998994a1fd302294a029325f9"
CHECKER = ROOT / "tools/check_readme_hq.py"
sys.path[:0] = [str(ROOT / part) for part in ("tools", "graphify-hq")]
from hq_data import GitTree
import hq_navigation
import hq_smoke
import version_maps


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE, text=True).strip()


def commit(root):
    git(root, "add", ".")
    git(root, "-c", "user.name=README HQ audit", "-c", "user.email=audit@example.invalid", "commit", "-qm", "Fixture")
    return git(root, "rev-parse", "HEAD")


@contextmanager
def fixture(files):
    with TemporaryDirectory() as temp:
        root = Path(temp)
        git(root, "init", "-qb", "main")
        for name, body in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
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


def run(script, *args, cwd=ROOT):
    return subprocess.run([sys.executable, str(script), *map(str, args)], cwd=cwd, capture_output=True, text=True)


def repeated_anchor_reads():
    count = 64
    heading = "# Guide heading\n"
    readme = "# Project\n\n" + "\n\n".join(f"[Guide reference {i}](guide.md#guide-heading)" for i in range(count))
    with fixture({"README.md": readme, "guide.md": heading}) as (root, _):
        tree = GitTree(root)
        actual_git = tree.git
        nav_parse = hq_navigation.parse_markdown
        calls = Counter()
        parsed = Counter()
        def traced_git(*args):
            if args[:2] == ("cat-file", "blob"):
                calls[args[2]] += 1
            return actual_git(*args)
        def traced_parse(text):
            parsed["guide" if text == heading else "root"] += 1
            return nav_parse(text)
        errors, gaps = [], []
        with patch.object(tree, "git", traced_git), patch.object(hq_navigation, "parse_markdown", traced_parse):
            validated = hq_navigation.check_document(tree, "README.md", errors, gaps)
        guide_blob = tree.entries()["guide.md"][1]
        assert validated == count and not errors and not gaps
        assert calls[guide_blob] == count and parsed == {"root": 1, "guide": count}
        return {"checked_heading_links": validated, "distinct_target_blobs": 1, "target_git_blob_reads": calls[guide_blob],
                "target_markdown_parses": parsed["guide"]}


def legacy_plan_dependency_order():
    workflow = (ROOT / ".github/workflows/verify-repair-plan.yml").read_text(encoding="utf-8")
    assert workflow.index("run: python tools/check_readme_hq.py") < workflow.index("python -m pip install")
    with TemporaryDirectory() as temp:
        env = Path(temp) / "clean"
        subprocess.run([sys.executable, "-m", "venv", "--without-pip", str(env)], check=True)
        clean = subprocess.run([str(env / "bin/python"), str(CHECKER)], capture_output=True, text=True, cwd=ROOT)
        control = run(CHECKER)
        assert clean.returncode == 1 and "No module named 'markdown_it'" in clean.stderr and control.returncode == 0
        return {"workflow_checks_before_dependency_install": True, "clean_python_exit": clean.returncode,
                "missing_module": "markdown_it", "installed_python_exit": control.returncode}


def late_smoke_type_validation():
    readme = "# Project\n\nThis reference fixture has an explicit first action.\n"
    with fixture({"README.md": readme}) as (root, sha):
        marker = root / "fixture-only-marker"
        spec = root / "smoke.json"
        args = [sys.executable, "-c", "import pathlib,sys; pathlib.Path(sys.argv[1]).write_text('fixture effect'); print('READY')",
                str(marker)]
        spec.write_text(json.dumps({"commit": sha, "argv": args, "expected": {"exit": 0, "contains": 99}}),
                        encoding="utf-8")
        result = run(CHECKER, "--repo", root, "--profile", "reference", "--smoke", spec)
        assert marker.read_text() == "fixture effect" and result.returncode == 1
        assert "AttributeError: 'int' object has no attribute 'encode'" in result.stderr
        return {"invalid_expected_contains_type": "integer", "fixture_command_ran": True, "cli_exit": result.returncode,
                "unhandled_error": "AttributeError"}


def rich_text_line_links():
    repository = "sphinx-doc/sphinx"
    sha = "035a07c32c3241fd3356f4d827800c1f88525272"
    def render(path):
        ref = {"path": path, "anchor": "Source"}
        feature = {"title": "Example", "summary": "Example"}
        return version_maps.render_outline("v0.0.6", repository, {"source_commit": sha, "nodes": 1, "edges": 0},
                                           [(feature, [(ref, 3)], (ref, 3))])
    markdown, rst, asciidoc = (render(path) for path in ("README.md", "README.rst", "README.adoc"))
    assert "README.md?plain=1#L3" in markdown
    assert "README.rst#L3" in rst and "README.rst?plain=1#L3" not in rst
    assert "README.adoc#L3" in asciidoc and "README.adoc?plain=1#L3" not in asciidoc
    return {"markdown_uses_plain": True, "restructuredtext_uses_plain": False, "asciidoc_uses_plain": False}


def synchronized_version_rollback():
    with candidate_checkout() as root:
        for name in ("README.md", "versions/README.md"):
            p = root / name
            old = p.read_text(encoding="utf-8")
            new, changed = re.subn(r"(\*\*Current version\*\*[^\n]*)v0\.0\.6(\]|/)",
                                   r"\g<1>v0.0.1\2", old, count=1)
            assert changed == 1 and new != old
            new = re.sub(r"^(\*\*Current version\*\*[^\n]*)v0\.0\.6(\]|/)", r"\g<1>v0.0.1\2", new, flags=re.M)
            p.write_text(new, encoding="utf-8")
            current = next(line for line in new.splitlines() if "**Current version**" in line)
            assert "v0.0.1/README.md" in current
        commit(root)
        check = run(root / "tools/check_readme_hq.py", cwd=root)
        assert check.returncode == 0 and (root / "versions/v0.0.6/README.md").is_file(), check.stderr
        return {"both_current_links_downgraded_to": "v0.0.1", "v0.0.6_still_in_index_and_archive": True,
                "validator_exit": check.returncode}


def main():
    assert git(ROOT, "rev-parse", "HEAD") == CANDIDATE
    cases = (repeated_anchor_reads, legacy_plan_dependency_order, late_smoke_type_validation,
             rich_text_line_links, synchronized_version_rollback)
    observed = {}
    for case in cases:
        observed[case.__name__] = case()
        print("Observed", case.__name__, flush=True)
    Path(sys.argv[1]).write_text(json.dumps({"candidate": CANDIDATE, "observations": observed}, indent=2) + "\n",
                                encoding="utf-8")


if __name__ == "__main__":
    main()
