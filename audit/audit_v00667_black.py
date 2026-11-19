"""Read public advisory and provenance metadata for the exact README HQ candidate."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path.cwd()
CANDIDATE = "8d50caec2bc6fcb998994a1fd302294a029325f9"


def fetch(url, binary=False):
    request = Request(url, headers={"User-Agent": "README-HQ-public-source-audit"})
    with urlopen(request, timeout=25) as result:
        return result.read() if binary else json.load(result)


def git(directory, *args):
    return subprocess.check_output(["git", "-C", str(directory), *args], text=True, timeout=45).strip()


def learning_controls():
    sys.path.insert(0, str(ROOT / "learning"))
    from intake import record_intake

    with TemporaryDirectory(prefix="readme-hq-black-") as directory:
        base = Path(directory)
        repo = base / "fixture"
        repo.mkdir()
        git(repo, "init", "--quiet")
        git(repo, "config", "core.autocrlf", "false")
        git(repo, "remote", "add", "origin", "https://github.com/example/source-docs.git")
        (repo / "README.md").write_text("# Fixture\nBring the quickstart and architecture guide together.\n", encoding="utf-8")
        git(repo, "add", "--", "README.md")
        git(repo, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "Fixture")
        commit = git(repo, "rev-parse", "HEAD")
        source = {"checkout": str(repo), "repository": "example/source-docs", "ref": commit,
                  "path": "README.md", "line": 2, "anchor": "quickstart", "visibility": "public"}
        target = {**source, "audience": "maintainer", "capability": "documentation"}
        data = {"visibility": "public", "target": target,
                "sources": [{"id": "example", **source}], "selected": ["example"], "findings": []}

        def api(canonical, public=True):
            def mock(route):
                if "/commits/" in route:
                    return {"sha": commit}
                return {"id": 71, "full_name": canonical, "visibility": "public" if public else "private",
                        "private": not public}
            return mock

        trusted = record_intake(data, base / "control", fetch=api("example/source-docs"))
        moved = record_intake(data, base / "renamed", fetch=api("example/renamed-docs"))
        assert trusted.read_bytes() == moved.read_bytes()
        readback = json.loads(moved.read_bytes())
        assert readback["sources"][0]["identity"][0] == "example/source-docs"
        assert readback["target"]["repository"] == "example/source-docs"
        other_source = {"id": "example", **source, "anchor": "architecture guide"}
        other = record_intake({**data, "sources": [other_source]}, base / "different-anchor",
                              fetch=api("example/source-docs"))
        assert trusted.read_bytes() == other.read_bytes()
        try:
            record_intake(data, base / "private", fetch=api("example/source-docs", public=False))
        except ValueError as error:
            assert "not confirmed public" in str(error)
        else:
            raise AssertionError("Expected private metadata to be rejected")
        return {"requested_repository": "example/source-docs", "synthetic_canonical_repository": "example/renamed-docs",
                "recorded_repository": readback["target"]["repository"], "renamed_and_control_receipts_identical": True,
                "same_line_different_anchor_receipts_identical": True, "private_control_rejected": True,
                "live_github_metadata_used": False}


def advisories():
    paths = ("tools/requirements.txt", "graphify-hq/template/v0.0.8/requirements.txt")
    pins = {(n, v) for path in paths for n, v in
            re.findall(r"^([A-Za-z0-9_-]+)==([^\s]+)", (ROOT / path).read_text(encoding="utf-8"), re.M)}

    def observe(pin):
        package, pinned = pin
        url = f"https://pypi.org/pypi/{package}/{pinned}/json"
        data = fetch(url)
        rows = [row for row in data.get("vulnerabilities", []) if not row.get("withdrawn")]
        records = [{"id": row["id"], "fixed_in": row.get("fixed_in", []),
                    "link": row.get("link")} for row in rows]
        return {"package": package, "version": pinned, "advisories": records}

    with ThreadPoolExecutor(max_workers=6) as pool:
        result = list(pool.map(observe, sorted(pins, key=lambda item: item[0].lower())))
    pillow = next(item for item in result if item["package"].lower() == "pillow")
    assert version("Pillow") == pillow["version"] and pillow["advisories"]
    latest = fetch("https://pypi.org/pypi/Pillow/json")["info"]
    return {"installed_pillow": version("Pillow"), "latest_pillow_at_observation": latest["version"],
            "latest_requires_python": latest["requires_python"], "pins_checked": len(result),
            "advisory_bearing_packages": [row for row in result if row["advisories"]]}


def upstream_sources():
    records = json.loads((ROOT / "techniques/public-source-inventory.json").read_bytes())
    repositories = sorted({record[0] for record in records})

    def observe(record):
        repo, commit, path, blob, sha256, lines = record
        url = f"https://raw.githubusercontent.com/{repo}/{commit}/{quote(path)}"
        data = fetch(url, binary=True)
        observed_git = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        observed = hashlib.sha256(data).hexdigest()
        assert observed == sha256 and observed_git == blob, (repo, commit, path, observed, observed_git)
        return {"repository": repo, "commit": commit, "path": path, "git_blob": observed_git,
                "sha256": observed, "recorded_lines": lines}

    with ThreadPoolExecutor(max_workers=5) as pool:
        verified = list(pool.map(observe, records))
    return {"repositories_with_anonymous_source_downloads": repositories, "documents": verified}


def main():
    assert git(ROOT, "rev-parse", "HEAD") == CANDIDATE
    result = {"candidate": CANDIDATE, "platform": sys.platform, "run_id": os.getenv("GITHUB_RUN_ID"),
              "attempt": os.getenv("GITHUB_RUN_ATTEMPT"), "observed_utc": datetime.now(timezone.utc).isoformat(),
              "installed_pillow": version("Pillow"), "learning_controls": learning_controls()}
    if sys.platform == "linux":
        result["dependency_advisories"] = advisories()
        result["public_technique_sources"] = upstream_sources()
    Path(sys.argv[1]).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Pinned candidate", CANDIDATE, "Pillow", result["installed_pillow"])
    if sys.platform == "linux":
        print("Public source files verified:", len(result["public_technique_sources"]["documents"]))
        print("Package versions checked:", result["dependency_advisories"]["pins_checked"])


if __name__ == "__main__":
    main()
