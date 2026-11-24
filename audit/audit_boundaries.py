"""Verify consumer entry points and record independent boundary failures."""

from contextlib import contextmanager
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
BASE = "f50e3749dab90ddfe35894284d1660097a1fb1a8"
CHECKER = "tools/check_readme_hq.py"
REGISTRY = Path("techniques/registry.json")
PROVENANCE = Path("graphify-hq/template/v0.0.8/github_provenance.py")


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def execute(directory, *args, env=None):
    return subprocess.run(args, cwd=directory, capture_output=True, encoding="utf-8", env=env)


def run(directory, *args, env=None):
    result = execute(directory, *args, env=env)
    require(result.returncode == 0, result.stdout + result.stderr)
    return result.stdout


@contextmanager
def pinned_checkout(directory):
    run(ROOT, "git", "worktree", "add", "--quiet", "--detach", str(directory), BASE)
    try:
        yield directory
    finally:
        run(ROOT, "git", "worktree", "remove", "--force", str(directory))


def check_list_output_encoding(directory):
    base = {**os.environ, "LC_ALL": "C", "PYTHONCOERCECLOCALE": "0", "PYTHONUTF8": "0"}
    ascii_env = {**base, "PYTHONIOENCODING": "ascii"}
    utf8_env = {**base, "PYTHONIOENCODING": "utf-8"}
    control = run(directory, sys.executable, CHECKER, "--list", env=utf8_env)
    registry = json.loads((directory / REGISTRY).read_bytes())
    expected = len(registry["techniques"])
    require(sum(" — " in line for line in control.splitlines()) == expected, control)
    standard = run(directory, sys.executable, CHECKER, env=ascii_env)
    result = execute(directory, sys.executable, CHECKER, "--list", env=ascii_env)
    require(result.returncode != 0 and "UnicodeEncodeError" in result.stderr, result.stderr)
    require("Validated" in standard and result.stdout == standard, result.stdout)
    print(f"B60: The shipped technique-list command exits nonzero under ASCII after printing a passing validation summary; UTF-8 emits all {expected} techniques.", flush=True)


def check_cross_field_identifier_collision(directory):
    path = directory / REGISTRY
    original = path.read_bytes()
    registry = json.loads(original)
    first, second = registry["techniques"][:2]
    require(first["id"] != second["id"], "Fixture needs two distinct techniques")
    require(first["id"] not in {entry["outcome_key"] for entry in registry["techniques"]},
            "Fixture needs an unused outcome key")

    try:
        second["aliases"].append(first["id"])
        path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        alias_result = execute(directory, sys.executable, CHECKER, "--list")
        require(alias_result.returncode != 0 and "name collision" in alias_result.stderr, alias_result.stderr)

        second["aliases"].pop()
        second["outcome_key"] = first["id"]
        path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        result = run(directory, sys.executable, CHECKER, "--list")
        require("Validated" in result and first["id"] in result and second["id"] in result, result)
    finally:
        path.write_bytes(original)
    print("B61: The validator rejects a duplicate alias but accepts the same cross-record collision between a stable technique ID and an outcome key.", flush=True)


def check_review_pagination_boundary(directory):
    spec = importlib.util.spec_from_file_location("github_provenance", directory / PROVENANCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    repository = "vixttha/README-HQ"
    source = "a" * 40
    expected = {"number": 17, "source_branch": "docs/readme"}
    route = "pulls/17"

    def reviews(number):
        requested = []

        def fetch(endpoint):
            if endpoint == route:
                project = {"full_name": repository}
                return {"number": 17, "state": "open", "merged": False, "draft": False,
                        "base": {"repo": project, "ref": "main", "sha": "c" * 40},
                        "head": {"repo": project, "ref": "docs/readme", "sha": source}}
            prefix = route + "/reviews?per_page=100&page="
            require(endpoint.startswith(prefix), endpoint)
            page = int(endpoint.removeprefix(prefix))
            requested.append(page)
            start = (page - 1) * 100
            finish = min(start + 100, number)
            return [{"state": "APPROVED", "user": {"id": index + 1}, "commit_id": source}
                    for index in range(start, finish)]

        return fetch, requested

    control, pages = reviews(999)
    observation = module.verify_pull_request(repository, source, expected, control)
    require(observation["exact_commit_approvals"] == 999 and pages == list(range(1, 11)), str(observation))
    full, pages = reviews(1000)
    try:
        module.verify_pull_request(repository, source, expected, full)
    except ValueError as exc:
        require("pagination limit reached" in str(exc) and pages == list(range(1, 11)), str(exc))
    else:
        raise ValueError("An exactly full final review page unexpectedly returned a valid observation")
    require(full(route + "/reviews?per_page=100&page=11") == [], "Fixture should have no more reviews")
    print("B62: Injected GitHub review responses give an exact observation at 999 reviews and an error at 1,000, even though the tenth page completes the list.", flush=True)


def verify_clean_baseline(directory):
    checker = run(directory, sys.executable, CHECKER)
    require(checker.startswith("Validated "), checker)
    result = run(directory, sys.executable, "graphify-hq/version_maps.py", "--check")
    require(result.count("Graphify MCP verified") == 6 and "6 maps covering 17 version records" in result, result)
    print("Control: The clean pinned checkout passes the documented checker and all six Graphify map rebuilds and MCP checks.", flush=True)


def main():
    with TemporaryDirectory(prefix="readme-hq-boundary-fixtures-") as out:
        with pinned_checkout(Path(out) / "baseline") as directory:
            check_list_output_encoding(directory)
            check_cross_field_identifier_collision(directory)
            check_review_pagination_boundary(directory)
            verify_clean_baseline(directory)


if __name__ == "__main__":
    main()
