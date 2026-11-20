"""Record explicitly requested first-action outcomes for a pinned checkout."""

from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from hq_data import read_json


def require_https_url(value, field):
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an HTTPS URL without credentials")
    url = urlsplit(value)
    if url.scheme != "https" or not url.hostname or url.username is not None or url.password is not None:
        raise ValueError(f"{field} must be an HTTPS URL without credentials")


def verify_first_action(tree, path, *, allow_network=False, subproject="."):
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
        require_https_url(target, "url")
        final_url = expected.get("final_url")
        if "final_url" in expected:
            require_https_url(final_url, "expected.final_url")
        if not allow_network:
            return {"result": "unchecked", "detail": "network probe not authorized"}
        if type(expected.get("http_status")) is not int:
            raise ValueError("remote smoke requires expected.http_status")
        if "contains" in expected and (not isinstance(expected["contains"], str) or not expected["contains"]):
            raise ValueError("expected.contains must be a nonempty string")
        try:
            try:
                response = urlopen(Request(target, headers={"User-Agent": "README-HQ"}), timeout=20)
            except HTTPError as error:
                response = error
            with response:
                status = response.status
                effective_url = response.geturl()
                observation = {"http_status": status, "final_url": effective_url,
                               "final_url_match": None if final_url is None else final_url == effective_url}
                if status in (401, 403, 429):
                    return {"result": "gated", "detail": f"HTTP {status}",
                            "url": target, "expected": expected, "observed": observation}
                matched = True
                if "contains" in expected:
                    body = response.read(1_000_000).decode("utf-8", "replace")
                    matched = expected["contains"] in body
        except (OSError, URLError):
            return {"result": "unresolved", "detail": "network destination could not be reached"}
        passed = matched and status == expected["http_status"] and observation["final_url_match"] is not False
        return {"result": "passed" if passed else "failed", "url": target, "expected": expected,
                "observed": {**observation, "content_match": matched}}
    argv = spec.get("argv")
    if not isinstance(argv, list) or not argv or not all(isinstance(arg, str) and arg for arg in argv):
        raise ValueError("local smoke needs a nonempty argv array")
    if type(expected.get("exit")) is not int or not (expected.get("contains") or expected.get("file")):
        raise ValueError("local smoke requires an exit code and a recognizable output or file")
    marker = expected.get("contains")
    stream = expected.get("stream", "either")
    if "contains" in expected and (not isinstance(marker, str) or not marker):
        raise ValueError("expected.contains must be a nonempty string")
    if stream not in ("either", "stdout", "stderr") or ("stream" in expected and marker is None):
        raise ValueError("expected.stream requires a marker and must be either, stdout, or stderr")
    name = expected.get("file")
    mode = expected.get("file_mode", "changed")
    digest = expected.get("file_sha256")
    if "file" in expected:
        if not isinstance(name, str) or not name or Path(name).is_absolute() or Path(name).drive or ".." in Path(name).parts:
            raise ValueError("expected.file must be a repository-relative file")
        if mode not in ("changed", "created", "updated", "exists"):
            raise ValueError("expected.file_mode must be changed, created, updated, or exists")
        if "file_sha256" in expected and (not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest)):
            raise ValueError("expected.file_sha256 must be a lowercase SHA-256")
    elif "file_mode" in expected or "file_sha256" in expected:
        raise ValueError("file expectations require expected.file")
    selected = Path(subproject)
    if selected.is_absolute() or selected.drive or ".." in selected.parts or "\\" in subproject:
        raise ValueError("smoke working directory must be relative to the selected repository")
    with TemporaryDirectory(prefix="readme-hq-smoke-") as temp:
        checkout = Path(temp) / "checkout"
        tree.git("worktree", "add", "--detach", str(checkout), tree.commit)
        try:
            cwd = (checkout / selected).resolve()
            if not cwd.is_relative_to(checkout.resolve()) or not cwd.is_dir():
                raise ValueError("smoke working directory is outside the checkout or unavailable")
            directory = selected.as_posix()

            def result_file():
                if not name:
                    return None
                path = (cwd / name).resolve()
                return path if path.is_relative_to(cwd) and path.is_file() else None

            def file_digest(path):
                if path is None:
                    return None
                with path.open("rb") as handle:
                    checksum = sha256()
                    for chunk in iter(lambda: handle.read(65536), b""):
                        checksum.update(chunk)
                return checksum.hexdigest()

            before = file_digest(result_file()) if mode != "exists" else None
            timeout = spec.get("timeout", 60)
            if type(timeout) is not int or not 1 <= timeout <= 300:
                raise ValueError("smoke timeout must be between 1 and 300 seconds")
            try:
                result = subprocess.run(argv, cwd=cwd, capture_output=True, timeout=timeout, check=False)
            except (OSError, subprocess.TimeoutExpired) as error:
                return {"result": "failed", "detail": str(error), "argv": argv, "cwd": directory, "expected": expected}
            streams = {"stdout": result.stdout, "stderr": result.stderr}
            marker_bytes = marker.encode() if marker is not None else None
            matched_streams = [key for key, data in streams.items() if marker_bytes is not None and marker_bytes in data]
            matched = marker is None or (bool(matched_streams) if stream == "either" else stream in matched_streams)
            observation = {}
            if name:
                path = result_file()
                after = file_digest(path) if mode != "exists" or digest is not None else None
                changed = before != after
                file_match = path is not None and (
                    mode == "exists" or (changed and (
                        mode == "changed" or (mode == "created" and before is None)
                        or (mode == "updated" and before is not None)
                    ))
                ) and (digest is None or after == digest)
                matched &= file_match
                observation = {"file_before_sha256": before, "file_after_sha256": after, "file_match": file_match}
            return {"result": "passed" if result.returncode == expected["exit"] and matched else "failed",
                    "argv": argv, "cwd": directory, "expected": expected,
                    "observed": {"exit": result.returncode, "outcome_match": bool(matched),
                                 "output_sha256": sha256(result.stdout + result.stderr).hexdigest(),
                                 "stream_sha256": {key: sha256(data).hexdigest() for key, data in streams.items()},
                                 "matched_streams": matched_streams, **observation}}
        finally:
            tree.git("worktree", "remove", "--force", str(checkout))


def write_receipt(destination, tree, cases, errors, gaps, *, validator_path=None):
    sources, unavailable_sources = {}, []
    if tree:
        name = cases.get("entrypoint") or "README.md"
        for path in (name, "tools/check_readme_hq.py"):
            if path in tree.entries():
                try:
                    sources[path] = sha256(tree.read(path)).hexdigest()
                except (KeyError, OSError, ValueError):
                    unavailable_sources.append(path)
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
    if unavailable_sources:
        data["unavailable_sources"] = unavailable_sources
    if validator_path is not None:
        data["validator"] = {"filename": validator_path.name, "sha256": sha256(validator_path.read_bytes()).hexdigest()}
    destination.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
