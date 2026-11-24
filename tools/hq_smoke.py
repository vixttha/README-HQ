"""Record explicitly requested first-action outcomes for a pinned checkout."""

from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from hq_data import read_json


def verify_first_action(tree, path, *, allow_network=False):
    spec = read_json(path)
    expected = spec.get("expected")
    if not isinstance(expected, dict) or not expected:
        raise ValueError("first action requires an expected result")
    if tree.draft:
        return {"result": "unchecked", "detail": "an exact commit is required"}
    if spec.get("commit") != tree.commit:
        raise ValueError("smoke specification does not match the selected commit")
    if "url" in spec:
        target = spec["url"]
        url = urlsplit(target)
        if url.scheme != "https" or not url.hostname or url.username or url.password:
            raise ValueError("an HTTPS reader URL without credentials is required")
        if not allow_network:
            return {"result": "unchecked", "detail": "network probe not authorized"}
        if type(expected.get("http_status")) is not int:
            raise ValueError("remote smoke requires expected.http_status")
        try:
            with urlopen(Request(target, headers={"User-Agent": "README-HQ"}), timeout=20) as response:
                status = response.status
                if "contains" in expected:
                    body = response.read(1_000_000).decode("utf-8", "replace")
                    matched = expected["contains"] in body
                else:
                    matched = True
        except HTTPError as error:
            if error.code in (401, 403, 429):
                return {"result": "gated", "detail": f"HTTP {error.code}"}
            status, matched = error.code, "contains" not in expected
        except (OSError, URLError):
            return {"result": "unresolved", "detail": "network destination could not be reached"}
        return {"result": "passed" if matched and status == expected["http_status"] else "failed",
                "url": target, "expected": expected, "observed": {"http_status": status, "content_match": matched}}
    argv = spec.get("argv")
    if not isinstance(argv, list) or not argv or not all(isinstance(arg, str) and arg for arg in argv):
        raise ValueError("local smoke needs a nonempty argv array")
    if type(expected.get("exit")) is not int or not (expected.get("contains") or expected.get("file")):
        raise ValueError("local smoke requires an exit code and a recognizable output or file")
    with TemporaryDirectory(prefix="readme-hq-smoke-") as temp:
        checkout = Path(temp) / "checkout"
        tree.git("worktree", "add", "--detach", str(checkout), tree.commit)
        try:
            timeout = spec.get("timeout", 60)
            if type(timeout) is not int or not 1 <= timeout <= 300:
                raise ValueError("smoke timeout must be between 1 and 300 seconds")
            try:
                result = subprocess.run(argv, cwd=checkout, capture_output=True, timeout=timeout, check=False)
            except (OSError, subprocess.TimeoutExpired) as error:
                return {"result": "failed", "detail": str(error), "argv": argv, "expected": expected}
            output = result.stdout + result.stderr
            matched = expected.get("contains") is None or expected["contains"].encode() in output
            if "file" in expected:
                path = (checkout / expected["file"]).resolve()
                matched &= path.is_relative_to(checkout) and path.is_file()
            return {"result": "passed" if result.returncode == expected["exit"] and matched else "failed",
                    "argv": argv, "expected": expected,
                    "observed": {"exit": result.returncode, "outcome_match": bool(matched),
                                 "output_sha256": sha256(output).hexdigest()}}
        finally:
            tree.git("worktree", "remove", "--force", str(checkout))


def write_receipt(destination, tree, cases, errors, gaps):
    sources = {}
    if tree:
        name = cases.get("entrypoint") or "README.md"
        for path in (name, "tools/check_readme_hq.py"):
            if path in tree.entries():
                sources[path] = sha256(tree.read(path)).hexdigest()
    run = os.environ.get("GITHUB_RUN_ID")
    repo = os.environ.get("GITHUB_REPOSITORY")
    data = {
        "schema": 1,
        "commit": tree.commit if tree else None,
        "draft": tree.draft if tree else None,
        "tools": {"python": sys.version.split()[0], "platform": platform.platform()},
        "run_url": f"https://github.com/{repo}/actions/runs/{run}" if repo and run else None,
        "sources": sources, "cases": cases, "errors": errors, "unchecked": gaps,
        "result": "failed" if errors else "passed",
    }
    destination.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
