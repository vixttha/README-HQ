"""Exercise README HQ adopter, rendering, and receipt boundaries on a disposable checkout."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from PIL import Image

ROOT = Path.cwd()
CANDIDATE = "8d50caec2bc6fcb998994a1fd302294a029325f9"
CHECKER = ROOT / "tools/check_readme_hq.py"
INTRO = "# Example project\n\nThis project turns example input into a downloadable report.\n\n"


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, timeout=30).strip()


def pin(repo):
    git(repo, "add", "--all")
    git(repo, "-c", "user.email=fixture@example.invalid", "-c", "user.name=Fixture", "commit", "-qm", "Fixture")
    return git(repo, "rev-parse", "HEAD")


def observe(repo, output, *args):
    result = subprocess.run([sys.executable, str(CHECKER), "--repo", str(repo), "--receipt", str(output), *args],
                            capture_output=True, encoding="utf-8", errors="replace", timeout=30)
    receipt = json.loads(output.read_bytes())
    return {"exit": result.returncode, "result": receipt["result"], "cases": receipt["cases"],
            "errors": receipt["errors"], "unchecked": receipt["unchecked"]}


def setup(base, name):
    repo = base / name
    repo.mkdir()
    git(repo, "init", "--quiet")
    git(repo, "config", "core.autocrlf", "false")
    return repo


def linked_quickstart(base):
    repo = setup(base, "linked-guide")
    docs = repo / "docs"
    docs.mkdir()
    (repo / "README.md").write_text(INTRO + "## Quickstart\n\n[Install the tool](docs/README.md)\n", encoding="utf-8")
    (docs / "README.md").write_text(INTRO + "[Required setup instructions](install.md)\n", encoding="utf-8")
    revision = pin(repo)
    output = base / "guide-receipt.json"
    first = observe(repo, output)
    guide = observe(repo, output, "--subproject", "docs", "--profile", "reference")
    assert first["exit"] == 0 and first["cases"]["local_links"] == 1, first
    assert guide["exit"] == 1 and "install.md" in " ".join(guide["errors"]), guide
    (docs / "install.md").write_text("# Installation\n", encoding="utf-8")
    pin(repo)
    control = observe(repo, output, "--subproject", "docs", "--profile", "reference")
    assert control["exit"] == 0, control
    return {"fixture_commit": revision, "homepage": first, "linked_quickstart_guide": guide, "repaired_guide_control": control}


def media_receipts(base):
    repo = setup(base, "draft-media")
    (repo / "README.md").write_text(INTRO + "![Report screenshot](report.png)\n", encoding="utf-8")
    path = repo / "report.png"
    Image.new("RGB", (3, 3), "red").save(path)
    revision = pin(repo)
    output = base / "media-receipt.json"
    checks = []
    for color in ("red", "blue"):
        Image.new("RGB", (3, 3), color).save(path)
        run = observe(repo, output, "--draft", "--profile", "reference")
        assert run["exit"] == 0 and run["cases"]["local_links"] == 1, run
        checks.append((hashlib.sha256(path.read_bytes()).hexdigest(), output.read_bytes()))
    assert checks[0][0] != checks[1][0] and checks[0][1] == checks[1][1]
    path.write_text("ordinary text, not an image", encoding="utf-8")
    broken = observe(repo, output, "--draft", "--profile", "reference")
    assert broken["exit"] == 1 and "invalid or unreadable image" in " ".join(broken["errors"]), broken
    return {"fixture_commit": revision, "asset_sha256": [digest for digest, _ in checks],
            "passing_receipts_byte_identical": True, "receipt_sha256": hashlib.sha256(checks[0][1]).hexdigest(),
            "corrupt_media_control": broken}


def image_link_rendering(base):
    sys.path.insert(0, str(ROOT / "tools"))
    from hq_navigation import PARSER

    repo = setup(base, "image-link")
    Image.new("RGB", (3, 3), "green").save(repo / "report.png")
    (repo / "report.md").write_text("# Report\n", encoding="utf-8")
    readme = repo / "README.md"
    output = base / "render-receipt.json"
    markup = {
        "markdown_control": "[![View report](report.png)](report.md)",
        "html_control": '<a href="report.md"><img src="report.png" alt="View report"></a>',
        "mixed_markup": '[<img src="report.png" alt="View report">](report.md)',
        "empty_alt_control": "[![](report.png)](report.md)",
    }
    results = {}
    for name, example in markup.items():
        readme.write_text(INTRO + example + "\n", encoding="utf-8")
        pin(repo)
        rendered = PARSER.render(example).strip()
        outcome = observe(repo, output, "--profile", "reference")
        results[name] = {"rendered": rendered, "audit": outcome}
    assert "<a href=\"report.md\"><img" in results["mixed_markup"]["rendered"]
    assert 'alt="View report"' in results["mixed_markup"]["rendered"]
    assert [results[name]["audit"]["exit"] for name in markup] == [0, 0, 1, 1], results
    assert "link has no accessible name" in " ".join(results["mixed_markup"]["audit"]["errors"])
    return results


def main():
    assert git(ROOT, "rev-parse", "HEAD") == CANDIDATE
    with TemporaryDirectory(prefix="readme-hq-stack-") as temp:
        base = Path(temp)
        cases = {"linked_quickstart": linked_quickstart(base),
                 "draft_asset_receipts": media_receipts(base),
                 "mixed_image_link": image_link_rendering(base)}
    row = {"candidate": CANDIDATE, "platform": sys.platform, "workflow_run_id": os.getenv("GITHUB_RUN_ID"),
           "workflow_attempt": os.getenv("GITHUB_RUN_ATTEMPT"), "cases": cases}
    Path(sys.argv[1]).write_text(json.dumps(row, indent=2) + "\n", encoding="utf-8")
    print("Confirmed:", ", ".join(cases))


if __name__ == "__main__":
    main()
