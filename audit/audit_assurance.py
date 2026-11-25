"""Reproduce README quality and evidence reliability gaps in disposable checkouts."""

import contextlib
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "f50e3749dab90ddfe35894284d1660097a1fb1a8"
LEARNING_BASELINE = "a8d97d0559853538d4d814edf5c998e42cfec3d2"


def command(directory, *args, expect=0):
    result = subprocess.run(args, cwd=directory, text=True, capture_output=True)
    assert result.returncode == expect, result.stdout + result.stderr
    return result


def git(directory, *args):
    return command(directory, "git", *args).stdout


def load(path):
    spec = spec_from_file_location(path.stem, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@contextlib.contextmanager
def readme_fixture(worktree, example):
    readme = worktree / "README.md"
    original = readme.read_bytes()
    readme.write_bytes(original + b"\n" + example)
    try:
        yield
    finally:
        readme.write_bytes(original)


def checker(worktree, expect=0):
    return command(worktree, sys.executable, "tools/check_readme_hq.py", expect=expect)


def check_evidence_permalinks(worktree):
    for page in sorted((worktree / "graphify-hq/maps").glob("*/README.md")):
        urls = re.findall(r"https://github\.com/[^)\s]+\.md(?:\?[^)#\s]*)?#L\d+", page.read_text(encoding="utf-8"))
        assert urls, page
        for url in urls:
            assert parse_qs(urlsplit(url).query).get("plain") != ["1"], url
    print("Q25: All six committed map outlines use Markdown line fragments without the GitHub plain-file parameter.")


def check_anchor_semantics(worktree):
    mapper = load(worktree / "graphify-hq/version_maps.py")
    sample = b"\x60\x60\x60sh\n# This is a shell comment\n- This is sample output\n\x60\x60\x60\n\n## Real release notes\n\n- Real change to README navigation\n"
    with patch.object(mapper, "source_bytes", return_value=sample):
        heading, heading_line = mapper.reference(BASELINE, "README.md")
        change, change_line = mapper.reference(BASELINE, "README.md", change=True)
    assert heading["anchor"] == "# This is a shell comment" and heading_line == 2
    assert change["anchor"] == "- This is sample output" and change_line == 3
    print("Q26: The graph anchor selector chose a fenced shell comment and sample output instead of the rendered notes.")


def check_first_use(worktree):
    marker = "FIRST_USE_OK"
    smoke = "print('ready to start')"
    snippet = f'\n## Quick start\n\n\x60\x60\x60sh\npython -c "{smoke}"\n\x60\x60\x60\n\nExpected output is {marker}.\n'
    with readme_fixture(worktree, snippet.encode()):
        checker(worktree)
        actual = command(worktree, sys.executable, "-c", smoke)
        assert marker not in actual.stdout and actual.stdout.strip() == "ready to start"
    smoke = "raise SystemExit(7)"
    snippet = f'\n## Quick start failure case\n\n\x60\x60\x60sh\npython -c "{smoke}"\n\x60\x60\x60\n'
    with readme_fixture(worktree, snippet.encode()):
        checker(worktree)
        command(worktree, sys.executable, "-c", smoke, expect=7)
    print("Q27: Both nonzero and zero-exit/wrong-result first-use commands passed README HQ validation.")


def check_media(worktree):
    image = worktree / "assurance-fixture.png"
    image.write_bytes(b"This is not PNG data.\n")
    try:
        with readme_fixture(worktree, b'\n![Quick-start screenshot](assurance-fixture.png)\n'):
            checker(worktree)
        valid = (worktree / "history/aldervale/published-v0.0.4/assets/breeze-campus.webp").relative_to(worktree)
        assert (worktree / valid).read_bytes().startswith(b"RIFF")
        with readme_fixture(worktree, f"\n[![]({valid.as_posix()})](README-GUIDE.md)\n".encode()):
            checker(worktree)
    finally:
        image.unlink()
    print("Q28: A corrupt image and an image-only navigation link with empty alt text both passed.")


def check_diagnostic_completeness(worktree):
    later = "missing-assurance-target.md"
    with readme_fixture(worktree, f"\n[Later fixture]({later})\n".encode()):
        assert later in checker(worktree, expect=1).stderr
    with readme_fixture(worktree, f"\n[Malformed fixture](https://[invalid)\n[Later fixture]({later})\n".encode()):
        result = checker(worktree, expect=1)
        assert "Invalid IPv6 URL" in result.stderr and later not in result.stderr, result.stderr
    print("Q29: A malformed URL stopped navigation checking before a second independently failing link.")


def check_target_provenance(learning):
    pilot = load(learning / "learning/audit_learning.py")
    corpus = json.loads((learning / "learning/pilot.json").read_bytes())
    target = corpus["targets"]["Lydite"]
    selected = set(corpus["sources"]) - {target["evidence"]}
    original = pilot.recommendations(corpus, target, selected)
    missing = pilot.recommendations(corpus, {"profile": target["profile"], "evidence": "missing-target-evidence"}, selected)
    assert original and original == missing
    print("Q30: Removing target evidence and substituting a nonexistent target receipt preserve the same pilot recommendation.")


def check_optimized_verifier(temporary, learning):
    project = temporary / "synthetic-repo"
    project.mkdir()
    git(project, "init", "--quiet")
    (project / "README.md").write_text("A real local fixture.\n", encoding="utf-8")
    git(project, "add", "README.md")
    git(project, "-c", "user.name=Audit fixture", "-c", "user.email=audit@example.invalid",
        "commit", "--quiet", "-m", "Create a synthetic source")
    revision = git(project, "rev-parse", "HEAD").strip()
    loader = f"""
import importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('audit_learning', {str(learning / "learning/audit_learning.py")!r})
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)
sources = {{'test': {{'repository': 'synthetic-repo', 'commit': {revision!r}, 'blob': '0' * 40,
                    'anchor': 'an absent anchor', 'line': 1, 'status': 'observed'}}}}
app.verify_sources(sources, Path({str(temporary)!r}))
"""
    normal = command(ROOT, sys.executable, "-c", loader, expect=1)
    assert "AssertionError" in normal.stderr
    optimized = command(ROOT, sys.executable, "-O", "-c", loader)
    assert "Observed exact README source" in optimized.stdout
    print("Q31: Optimized Python reported a known-wrong blob hash and source anchor as observed exact evidence.")


def check_receipt_retention(worktree):
    baseline = (worktree / ".github/workflows/readme-hq.yml").read_text(encoding="utf-8")
    previous = git(ROOT, "show", "6d011b0e2e2dd521074819e688b802e786fb5d5a:.github/workflows/verify-repair-plan.yml")
    audit = git(ROOT, "show", "6d011b0e2e2dd521074819e688b802e786fb5d5a:.github/workflows/audit-v006.yml")
    assert all("upload-artifact" not in y for y in (baseline, previous, audit))
    assert (worktree / "graphify-hq/maps/v0.0.6/receipt.json").is_file()
    print("Q32: The audited workflows retain no downloadable acceptance bundle. Graphify map receipts cover graph generation.")


def main():
    with TemporaryDirectory(prefix="readme-hq-assurance-") as tmp:
        temporary = Path(tmp)
        worktree = temporary / "baseline"
        git(ROOT, "worktree", "add", "--quiet", "--detach", str(worktree), BASELINE)
        try:
            checker(worktree)
            check_evidence_permalinks(worktree)
            check_anchor_semantics(worktree)
            check_first_use(worktree)
            check_media(worktree)
            check_diagnostic_completeness(worktree)
            learning = temporary / "historical-learning"
            git(ROOT, "--no-replace-objects", "worktree", "add", "--quiet", "--detach", str(learning), LEARNING_BASELINE)
            try:
                check_target_provenance(learning)
                check_optimized_verifier(temporary, learning)
            finally:
                git(ROOT, "worktree", "remove", "--force", str(learning))
            check_receipt_retention(worktree)
        finally:
            git(ROOT, "worktree", "remove", "--force", str(worktree))


if __name__ == "__main__":
    main()
