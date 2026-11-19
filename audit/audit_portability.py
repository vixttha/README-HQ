"""Measure README HQ v0.0.6 portability in disposable public-CI fixtures."""

from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory


BASELINE = "f50e3749dab90ddfe35894284d1660097a1fb1a8"
REPO = Path(__file__).resolve().parents[1]
WORKFLOW = ".github/workflows/readme-hq.yml"


def command(directory, *args):
    return subprocess.run(args, cwd=directory, text=True, capture_output=True)


def git(directory, *args):
    result = command(directory, "git", *args)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


def checker(directory, cwd=None):
    return command(cwd or directory, sys.executable, str(directory / "tools/check_readme_hq.py"))


def outcome(result, status, message=None):
    assert result.returncode == status, result.stdout + result.stderr
    if message:
        assert message in result.stderr, result.stderr


def check_readme(directory, text, status=0, message=None):
    path = directory / "README.md"
    original = path.read_bytes()
    path.write_bytes(text)
    try:
        outcome(checker(directory), status, message)
    finally:
        path.write_bytes(original)


def inspect_workflow(worktree):
    source = git(worktree, "show", f"{BASELINE}:{WORKFLOW}")
    trigger, jobs = source.split("\njobs:\n", 1)
    general, graphify = jobs.split("\n  graphify:", 1)
    assert "runs-on: ubuntu-latest" in general and re.search(r"^\s+if:", general, re.M) is None
    assert "github.event.repository.private == false" in graphify
    assert "visibility" not in source and "self-hosted" not in source
    print("A11 workflow inspection: standard hosted validation has no public-only job condition. No private job was dispatched.")
    push, pull = trigger.split("\n  pull_request:", 1)
    assert "branches: [readme-hq, graphify-hq]" in push
    assert "branches: [main, readme-hq, graphify-hq]" in pull
    print("A17 workflow inspection: main is covered by pull_request and excluded from push.")


def check_adopter(worktree, directory):
    adopter = directory / "adopter"
    (adopter / "tools").mkdir(parents=True)
    (adopter / "README.md").write_text("# Example\n\nInstall with the documented build.\n", encoding="utf-8")
    shutil.copyfile(worktree / "tools/check_readme_hq.py", adopter / "tools/check_readme_hq.py")
    outcome(checker(adopter), 1, "registry.json")
    outcome(checker(worktree, cwd=adopter), 0)
    print("A12 adopter fixture: copied checker demands HQ-only files and invoking the HQ checker audits HQ from an unrelated working directory.")


def check_surface(worktree):
    path = worktree / ".github/README.md"
    assert not path.exists()
    path.write_text("# Visible homepage\n\n[Broken target](missing-workflow-guide.md)\n", encoding="utf-8")
    try:
        outcome(checker(worktree), 0)
    finally:
        path.unlink()
    print("A13 README precedence: broken .github homepage passes while root README remains valid.")


def check_quality(worktree):
    check_readme(worktree, b"")
    check_readme(worktree, b"# Project name\n")
    check_readme(worktree, b"# Project name\n\nTODO: write setup.\n")
    check_readme(worktree, b"# Example\n" + b"x" * (501 * 1024) + b"\n\n## Get started\n")
    print("A14 content gate: empty, title-only, placeholder, and over-display-size fixture READMEs all pass.")


def check_root_relative(worktree):
    assert (worktree / "versions/README.md").is_file()
    check_readme(worktree, b"# Example\n\n[Versions](/versions/README.md)\n", 1, "path escapes")
    print("A15 root-relative link: the checker rejects an existing repository-root /versions/README.md destination.")


def check_same_repository_links(worktree):
    link = b"https://github.com/vixttha/README-HQ/blob/readme-hq/versions/nonexistent-audit/README.md"
    check_readme(worktree, b"# Example\n\n[Missing version](" + link + b")\n")
    target = worktree / "audit-untracked-example.md"
    target.write_text("# Untracked test file\n", encoding="utf-8")
    try:
        assert not git(worktree, "ls-files", "--", target.name)
        check_readme(worktree, b"# Example\n\n[Untracked](audit-untracked-example.md)\n")
        target.unlink()
        check_readme(worktree, b"# Example\n\n[Untracked](audit-untracked-example.md)\n", 1, "missing local target")
    finally:
        if target.exists():
            target.unlink()
    wrong_case = worktree / "versions/readme.md"
    status = 0 if wrong_case.exists() else 1
    check_readme(worktree, b"# Example\n\n[Wrong-case path](versions/readme.md)\n", status)
    assert not git(worktree, "ls-files", "--", "versions/readme.md")
    print(f"A16 publication-path parity: same-repo blob URL skipped, untracked target accepted, wrong-case path exit={status} on this filesystem.")


def main():
    with TemporaryDirectory(prefix="readme-hq-portability-") as directory:
        temporary = Path(directory)
        worktree = temporary / "baseline"
        git(REPO, "worktree", "add", "--quiet", "--detach", str(worktree), BASELINE)
        try:
            outcome(checker(worktree), 0)
            inspect_workflow(worktree)
            check_adopter(worktree, temporary)
            check_surface(worktree)
            check_quality(worktree)
            check_root_relative(worktree)
            check_same_repository_links(worktree)
        finally:
            git(REPO, "worktree", "remove", "--force", str(worktree))


if __name__ == "__main__":
    main()
