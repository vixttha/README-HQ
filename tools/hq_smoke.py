"""Record explicitly requested first-action outcomes for a pinned checkout."""

from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import re
import shlex
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from hq_data import clean_git_environment, read_json


def require_https_url(value, field):
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an HTTPS URL without credentials")
    url = urlsplit(value)
    if url.scheme != "https" or not url.hostname or url.username is not None or url.password is not None:
        raise ValueError(f"{field} must be an HTTPS URL without credentials")


class HTTPSRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        require_https_url(newurl, "redirect destination")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def urlopen(request, *, timeout):
    return build_opener(HTTPSRedirectHandler()).open(request, timeout=timeout)


def url_subject(value):
    parsed = urlsplit(value)
    return {"origin": f"{parsed.scheme}://{parsed.hostname}",
            "sha256": sha256(value.encode()).hexdigest()}


def verify_first_action(tree, path, *, allow_network=False, subproject=".", include_output=False,
                        entrypoint=None, actions=None, source_sha256=None):
    spec = read_json(path)
    result = run_first_action(tree, spec, allow_network=allow_network, subproject=subproject,
                              include_output=include_output)
    if actions is not None:
        binding = next((action for action in actions if matches_documented_action(action, spec)), None)
        result["documentation"] = ({"status": "matched", "path": entrypoint, "line": binding["line"],
                                    "source_sha256": source_sha256}
                                   if binding else {"status": "supplemental"})
    return result


def matches_documented_action(action, spec):
    if action["kind"] == "url":
        return action["value"] == spec.get("url")
    actual = spec.get("argv")
    if not isinstance(actual, list) or not actual or not all(isinstance(arg, str) for arg in actual):
        return False
    documented = literal_shell_argv(action["value"], action.get("language", "sh"))
    if not documented:
        return False
    if documented[0] in {"python", "python3", "python.exe", "python3.exe"} and actual[0] == sys.executable:
        documented[0] = sys.executable
    return documented == actual


def shell_words_continued(lines, language):
    """Return the first logical command and its physical offset in the fence."""
    escape = "^" if language == "cmd" else "`" if language in {"powershell", "pwsh"} else "\\"
    quotes = '"' if language == "cmd" else "'\""
    literal_quote = '"' if language == "cmd" else "'"
    quote = start = None
    fragments = []
    for offset, line in enumerate(lines):
        if start is None:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            start = offset
        escaped = False
        for char in line:
            if escaped:
                escaped = False
            elif char == escape and quote != literal_quote:
                escaped = True
            elif quote is None and char in quotes:
                quote = char
            elif char == quote:
                quote = None
        if escaped:
            fragments.append(line[:-1])
        else:
            fragments.append(line)
            return "".join(fragments).strip(), start
    return None


def literal_shell_argv(value, language):
    windows = language in {"cmd", "powershell", "pwsh"}
    quotes = '"' if language == "cmd" else "'\""
    quote = None
    escaped = False
    for index, char in enumerate(value):
        following = value[index + 1:index + 2]
        if escaped:
            escaped = False
            continue
        if char == "\\" and not windows and quote != "'":
            # shlex does not decode all Bash double-quoted escapes identically.
            if quote == '"' and following in {"$", "`"}:
                return None
            escaped = True
            continue
        if windows and ((char == "\\" and following == '"') or (quote and char == quote == following)):
            return None  # Complex Windows escaping is outside this literal-argv grammar.
        if language == "cmd" and char in "%!^":
            return None
        if language != "cmd" and char in "$`" and quote != "'":
            return None
        if quote:
            if char == quote:
                quote = None
        elif char in quotes:
            quote = char
        elif char in "();|&<>*?[]~#" or (language == "bash" and char in "{}"):
            return None
    if quote or escaped:
        return None
    lexer = shlex.shlex(value, posix=True)
    lexer.whitespace_split = True
    lexer.commenters = ""
    lexer.quotes = quotes
    if windows:
        lexer.escape = ""
    try:
        return list(lexer)
    except ValueError:
        return None


def run_first_action(tree, spec, *, allow_network=False, subproject=".", include_output=False):
    if not isinstance(spec, dict) or ("url" in spec) == ("argv" in spec):
        raise ValueError("smoke specification requires exactly one of argv and url")
    expected = spec.get("expected")
    if not isinstance(expected, dict) or not expected:
        raise ValueError("first action requires an expected result")
    if spec.get("commit") != tree.commit:
        raise ValueError("smoke specification does not match the selected commit")
    if "contains" in expected and (
        not isinstance(expected["contains"], str) or not expected["contains"]
    ):
        raise ValueError("expected.contains must be a nonempty string")
    if "url" in spec:
        if expected.keys() & {"exit", "stream", "file", "file_mode", "file_sha256"}:
            raise ValueError("URL smoke does not support local action expectations")
        if type(expected.get("http_status")) is not int or not 100 <= expected["http_status"] <= 599:
            raise ValueError("remote smoke requires expected.http_status between 100 and 599")
        target = spec["url"]
        require_https_url(target, "url")
        final_url = expected.get("final_url")
        if "final_url" in expected:
            require_https_url(final_url, "expected.final_url")
        identity = {"subject": url_subject(target), "spec_sha256": sha256(
            json.dumps(spec, sort_keys=True, separators=(",", ":")).encode()).hexdigest()}
        if tree.draft or not allow_network:
            detail = "an exact commit is required" if tree.draft else "network probe not authorized"
            return {"result": "unchecked", "detail": detail, **identity}
        requirements = {"http_status": expected["http_status"]}
        if "contains" in expected:
            requirements["has_content_marker"] = True
        if final_url is not None:
            requirements["final_url"] = url_subject(final_url)
        try:
            try:
                response = urlopen(Request(target, headers={"User-Agent": "README-HQ"}), timeout=20)
            except HTTPError as error:
                response = error
            with response:
                status = response.status
                effective_url = response.geturl()
                require_https_url(effective_url, "effective URL")
                observation = {"http_status": status, "final_url": url_subject(effective_url),
                               "final_url_match": None if final_url is None else final_url == effective_url}
                if status in (401, 403, 429):
                    return {"result": "gated", "detail": f"HTTP {status}",
                            "expected": requirements, "observed": observation, **identity}
                matched = True
                if "contains" in expected:
                    body = response.read(1_000_000).decode("utf-8", "replace")
                    matched = expected["contains"] in body
        except ValueError:
            return {"result": "failed", "failure_codes": ["invalid-https-redirect"], **identity}
        except (OSError, URLError):
            return {"result": "unresolved", "detail": "network destination could not be reached", **identity}
        failures = []
        if status != expected["http_status"]:
            failures.append("http-status-mismatch")
        if not matched:
            failures.append("output-marker-mismatch")
        if observation["final_url_match"] is False:
            failures.append("final-url-mismatch")
        return {"result": "failed" if failures else "passed", "expected": requirements, **identity,
                "observed": {**observation, "content_match": matched}, "failure_codes": failures}
    if tree.draft:
        return {"result": "unchecked", "detail": "an exact commit is required"}
    if expected.keys() & {"http_status", "final_url"}:
        raise ValueError("argv smoke does not support URL action expectations")
    argv = spec["argv"]
    if not isinstance(argv, list) or not argv or not all(isinstance(arg, str) and arg for arg in argv):
        raise ValueError("local smoke needs a nonempty argv array")
    if type(expected.get("exit")) is not int or not (expected.get("contains") or expected.get("file")):
        raise ValueError("local smoke requires an exit code and a recognizable output or file")
    marker = expected.get("contains")
    stream = expected.get("stream", "either")
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
    timeout = spec.get("timeout", 60)
    if type(timeout) is not int or not 1 <= timeout <= 300:
        raise ValueError("smoke timeout must be between 1 and 300 seconds")
    selected = Path(subproject)
    if selected.is_absolute() or selected.drive or ".." in selected.parts or "\\" in subproject:
        raise ValueError("smoke working directory must be relative to the selected repository")
    with TemporaryDirectory(prefix="readme-hq-smoke-") as temp:
        checkout = Path(temp) / "checkout"
        environment = clean_git_environment()

        if tree.allow_git_fetch:
            tree.materialize_checkout_blobs()
        setup_env = {**environment, "GIT_NO_LAZY_FETCH": "1", "GIT_ALLOW_PROTOCOL": "file"}

        def prepare(*args):
            result = subprocess.run(["git", *args], cwd=temp, env=setup_env, capture_output=True)
            if result.returncode:
                raise ValueError("could not prepare the isolated smoke checkout")

        prepare("init", "--quiet", str(checkout))
        prepare("-C", str(checkout), "fetch", "--quiet", "--no-tags", "--depth=1", "--",
                str(tree.root), tree.commit)
        prepare("-C", str(checkout), "checkout", "--quiet", "--detach", tree.commit)
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
        try:
            result = subprocess.run(argv, cwd=cwd, env=environment, capture_output=True, timeout=timeout, check=False)
        except (OSError, subprocess.TimeoutExpired) as error:
            code = "command-timeout" if isinstance(error, subprocess.TimeoutExpired) else "command-start-failed"
            outcome = {"result": "failed", "failure_codes": [code], "argv": argv,
                       "cwd": directory, "expected": expected}
            if include_output:
                outcome["private_output"] = {
                    key: bounded_output(getattr(error, key, None) or b"") for key in ("stdout", "stderr")}
            return outcome
        streams = {"stdout": result.stdout, "stderr": result.stderr}
        marker_bytes = marker.encode() if marker is not None else None
        matched_streams = [key for key, data in streams.items() if marker_bytes is not None and marker_bytes in data]
        matched = marker is None or (bool(matched_streams) if stream == "either" else stream in matched_streams)
        failures = []
        if result.returncode != expected["exit"]:
            failures.append("exit-mismatch")
        if not matched:
            failures.append("output-marker-mismatch")
        observation = {}
        if name:
            path = result_file()
            after = file_digest(path) if mode != "exists" or digest is not None else None
            changed = before != after
            file_failure = None
            if path is None:
                file_failure = "expected-file-missing"
            elif mode != "exists" and (
                not changed or (mode == "created" and before is not None)
                or (mode == "updated" and before is None)
            ):
                file_failure = "expected-file-state-mismatch"
            elif digest is not None and after != digest:
                file_failure = "expected-file-digest-mismatch"
            if file_failure:
                failures.append(file_failure)
                matched = False
            observation = {"file_before_sha256": before, "file_after_sha256": after,
                           "file_match": file_failure is None}
        outcome = {"result": "failed" if failures else "passed", "failure_codes": failures,
                   "argv": argv, "cwd": directory, "expected": expected,
                   "observed": {"exit": result.returncode, "outcome_match": bool(matched),
                                "output_sha256": sha256(result.stdout + result.stderr).hexdigest(),
                                "stream_sha256": {key: sha256(data).hexdigest() for key, data in streams.items()},
                                "matched_streams": matched_streams, **observation}}
        if failures and include_output:
            outcome["private_output"] = {key: bounded_output(data) for key, data in streams.items()}
        return outcome


def bounded_output(data):
    return {"text": data[:512].decode("utf-8", "replace"), "truncated": len(data) > 512}


def coverage_incomplete(cases):
    smoke = cases.get("first_action", {})
    return (cases.get("navigation", {}).get("result") == "unchecked"
            or cases.get("first_action_route", {}).get("result") == "unchecked"
            or (smoke.get("required") is True
                and (smoke.get("result") != "passed" or smoke.get("documentation", {}).get("status") != "matched")))


def write_receipt(destination, tree, cases, errors, gaps, *, validator_path=None, scope=None):
    sources, unavailable_sources = {}, []
    if tree:
        name = cases.get("entrypoint") or "README.md"
        # Retain the first observed digest for every audited draft input.
        if tree.draft:
            sources.update(tree.draft_source_digests)
        for path in (name, "tools/check_readme_hq.py"):
            try:
                if path in tree.entries():
                    # Rechecking a known input may detect drift, but must not
                    # replace its original evidence.
                    sources.setdefault(path, sha256(tree.read(path)).hexdigest())
            except (KeyError, OSError, ValueError):
                unavailable_sources.append(path)
                if tree.draft and path in tree.draft_source_digests:
                    errors.append(f"{path}: draft evidence no longer matches the audited bytes")
    hosted = os.environ.get("GITHUB_ACTIONS") == "true"
    run = os.environ.get("GITHUB_RUN_ID") if hosted else None
    repo = os.environ.get("GITHUB_REPOSITORY") if hosted else None
    run_url = f"https://github.com/{repo}/actions/runs/{run}" if repo and run else None
    attempt = os.environ.get("GITHUB_RUN_ATTEMPT") if hosted else None
    data = {
        "schema": 1,
        "commit": tree.commit if tree else None,
        "draft": tree.draft if tree else None,
        "tools": {"python": sys.version.split()[0], "platform": platform.platform()},
        "run_url": run_url,
        "github_actions": {
            "status": "provided-by-runner" if hosted else "unavailable",
            "run_id": run, "attempt": attempt,
            "attempt_url": f"{run_url}/attempts/{attempt}" if run_url and attempt else None,
            "job": os.environ.get("GITHUB_JOB") if hosted else None,
            "runner_os": os.environ.get("RUNNER_OS") if hosted else None,
        },
        "sources": sources, "cases": cases, "errors": errors, "unchecked": gaps,
        "result": "failed" if errors else "incomplete" if coverage_incomplete(cases) else "passed",
    }
    if tree is not None:
        data["git_objects"] = {"fetch_policy": "allow" if tree.allow_git_fetch else "offline",
                               "fetched_blobs": sorted(tree.fetched_blobs)}
    if scope is not None:
        data["scope"] = scope
    if unavailable_sources:
        data["unavailable_sources"] = unavailable_sources
    if validator_path is not None:
        data["validator"] = {"filename": validator_path.name, "sha256": sha256(validator_path.read_bytes()).hexdigest()}
    destination.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
