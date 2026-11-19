"""Measure README audit coverage on exact public adopter commits."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

CANDIDATE = "8d50caec2bc6fcb998994a1fd302294a029325f9"
ROOT = Path.cwd()
SAMPLES = [
    ("vixttha/README-HQ", "a7a989ffb6b664df86aae0ea01053ea2fc0a4405", "application"),
    ("vixttha/README-HQ", CANDIDATE, "application"),
    ("vixttha/AlderVale-Pact-of-Ten", "a6c2060b8175f505cc6327ccb5658cc00a458b24", "application"),
    ("vixttha/Lydite-Test-Vault-Template", "87d25d80d3154d295052412b64b29a0f0f152c27", "application"),
    ("vixttha/Blender-Agent-Refinement-Toolkit", "3e7f9e02e61739825b56bcafecebbd0221cc9657", "application"),
    ("sphinx-doc/sphinx", "035a07c32c3241fd3356f4d827800c1f88525272", "library"),
    ("asciidoctor/asciidoctor", "743f47d5e4d12049744e6d5236ad16cdfb6dca3d", "application"),
]


def git(directory, *args):
    return subprocess.check_output(["git", "-C", str(directory), *args], text=True).strip()


def observe(base, sample):
    repository, revision, profile = sample
    directory = base / revision
    directory.mkdir()
    git(directory, "init", "--quiet")
    git(directory, "remote", "add", "origin", f"https://github.com/{repository}.git")
    git(directory, "fetch", "--quiet", "--depth=1", "origin", revision)
    if git(directory, "rev-parse", "FETCH_HEAD") != revision:
        raise AssertionError(f"Unexpected Git SHA for {repository}")
    path = base / f"{revision}.json"
    result = subprocess.run([
        sys.executable, str(ROOT / "tools/check_readme_hq.py"),
        "--repo", str(directory), "--ref", revision, "--profile", profile, "--receipt", str(path),
    ], encoding="utf-8", errors="replace", capture_output=True)
    data = json.loads(path.read_bytes())
    if data["commit"] != revision:
        raise AssertionError(data)
    return {"repository": repository, "commit": revision, "profile": profile, "exit": result.returncode,
            "readme": data["cases"].get("entrypoint"), "local_links": data["cases"].get("local_links"),
            "errors": data["errors"], "unchecked": data["unchecked"]}


def main():
    if git(ROOT, "rev-parse", "HEAD") != CANDIDATE:
        raise AssertionError("Expected the pinned README HQ validator")
    with TemporaryDirectory(prefix="readme-hq-adopters-") as temporary, ThreadPoolExecutor(max_workers=4) as pool:
        observations = list(pool.map(lambda sample: observe(Path(temporary), sample), SAMPLES))
    Path(sys.argv[1]).write_text(json.dumps({"candidate": CANDIDATE, "observations": observations}, indent=2)
                                + "\n", encoding="utf-8")
    for row in observations:
        print(json.dumps({**row, "unchecked": len(row["unchecked"])}))


if __name__ == "__main__":
    main()
