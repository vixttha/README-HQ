"""Produce example README HQ first-action receipts from a disposable Git repository."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SUBPROJECT = "packages/demo"
sys.path.insert(0, str(ROOT / "tools"))
from hq_data import clean_git_environment


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="new directory for the example and its receipts")
    output = parser.parse_args().output.resolve()
    output.mkdir()
    fixture = output / "fixture"
    package = fixture / SUBPROJECT
    package.mkdir(parents=True)
    (package / "README.md").write_text(
        "# Demo\n\nThis demo verifies the first command.\n\n## Quickstart\n\n```sh\npython run.py\n```\n",
        encoding="utf-8")
    (package / "run.py").write_text("print('first action ready')\n", encoding="utf-8")

    environment = clean_git_environment()

    def git(*args):
        return subprocess.check_output(["git", *args], cwd=fixture, text=True, env=environment).strip()

    git("init", "--quiet")
    git("add", ".")
    git("-c", "user.name=README HQ Example", "-c", "user.email=example@users.noreply.github.com",
        "commit", "--quiet", "-m", "First-action example")
    commit = git("rev-parse", "HEAD")
    command = [sys.executable, "run.py"]
    cases = (
        ("passing", {"argv": command, "expected": {"exit": 0, "contains": "first action ready", "stream": "stdout"}}, 0, "passed"),
        ("failing", {"argv": command, "expected": {"exit": 0, "contains": "different marker"}}, 1, "failed"),
        ("url-unchecked", {"url": "https://example.invalid/", "expected": {"http_status": 200}}, 0, "unchecked"),
    )
    for name, spec, exit_code, outcome in cases:
        spec_path, receipt_path = output / (name + "-spec.json"), output / (name + ".json")
        spec_path.write_text(json.dumps({"commit": commit, **spec}, indent=2) + "\n", encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, str(ROOT / "tools/check_readme_hq.py"), "--repo", str(fixture), "--ref", commit,
             "--subproject", SUBPROJECT, "--smoke", str(spec_path), "--receipt", str(receipt_path)], check=False, env=environment)
        if completed.returncode != exit_code:
            raise SystemExit(f"Unexpected exit {completed.returncode} for {name}")
        receipt = json.loads(receipt_path.read_bytes())
        if receipt["commit"] != commit or receipt["cases"]["first_action"]["result"] != outcome:
            raise SystemExit(f"Unexpected receipt for {name}")
    print(f"Receipts written to {output}")


if __name__ == "__main__":
    main()
