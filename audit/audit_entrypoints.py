"""Check the packaged Graphify entry point, version index, and GitHub provenance."""

from contextlib import contextmanager
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

import yaml


ROOT = Path(__file__).resolve().parents[1]
BASE = "f50e3749dab90ddfe35894284d1660097a1fb1a8"
KIT = Path("graphify-hq/template/v0.0.8")
VERSION_INDEX = Path("versions/README.md")
WORKFLOW = Path(".github/workflows/readme-hq.yml")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def command(directory, *args):
    return subprocess.run(args, cwd=directory, text=True, capture_output=True)


def run(directory, *args):
    result = command(directory, *args)
    require(result.returncode == 0, result.stdout + result.stderr)
    return result.stdout


@contextmanager
def worktree(directory):
    run(ROOT, "git", "worktree", "add", "--quiet", "--detach", str(directory), BASE)
    try:
        yield directory
    finally:
        run(ROOT, "git", "worktree", "remove", "--force", str(directory))


def compile_graph(directory, manifest_file, output):
    return command(directory, sys.executable, str(KIT / "evidence_map.py"), str(manifest_file), str(output))


def check_packaged_self_map(directory, temporary):
    kit_readme = (directory / KIT / "README.md").read_text(encoding="utf-8")
    require("[self-map manifest](self-map.json)" in kit_readme, "Packaged self-map link is missing")
    fixture = json.loads((directory / KIT / "self-map.json").read_bytes())
    fixture.update(repository="vixttha/README-HQ", source_commit=BASE)
    manifest = temporary / "self-map.json"
    manifest.write_text(json.dumps(fixture), encoding="utf-8")
    missing_path = ".github/workflows/graphify-hq-template.yml"
    require(missing_path in fixture["source_files"] and not (directory / missing_path).exists(), missing_path)
    result = compile_graph(directory, manifest, temporary / "self-map-output")
    require(result.returncode != 0 and missing_path in result.stderr, result.stdout + result.stderr)
    print("E56: The packaged self-map cannot build after providing both documented inputs. It still points to missing upstream paths.", flush=True)


def check_duplicate_version_row(directory):
    path = directory / VERSION_INDEX
    original = path.read_bytes()
    line = next(row for row in original.splitlines(keepends=True) if row.startswith(b"| v0.0.6 |"))
    mutant = original.replace(line, line + line, 1)
    require(original.count(line) == 1 and mutant.count(line) == 2, "Fixture does not duplicate precisely one valid row")
    path.write_bytes(mutant)
    try:
        check = run(directory, sys.executable, "tools/check_readme_hq.py")
        graph = run(directory, sys.executable, "graphify-hq/version_maps.py", "--check")
    finally:
        path.write_bytes(original)
    require("Validated" in check and "6 maps covering 17 version records" in graph, check + graph)
    require(graph.count("Graphify MCP verified") == 6, graph)
    print("E57: A byte-identical duplicate v0.0.6 row passes README checking and the exact six-map rebuild and MCP verification.", flush=True)


def check_merge_queue_trigger(directory):
    data = yaml.load((directory / WORKFLOW).read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    events = data["on"]
    require("main" in events["pull_request"]["branches"], str(events))
    require("validate" in data["jobs"] and "graphify" in data["jobs"], str(data["jobs"]))
    require("merge_group" not in events, str(events))
    print("E58: The public validation workflow serves pull requests to main and has no merge_group trigger for a required merge-queue check.", flush=True)


def check_moving_pr_observation(directory):
    path = directory / KIT / "github_provenance.py"
    spec = importlib.util.spec_from_file_location("github_provenance", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    repository = "vixttha/README-HQ"
    number = 4
    route = f"pulls/{number}"
    former_head = "a" * 40
    new_head = "b" * 40
    expected = {"number": number, "source_branch": "docs/readme"}
    branch_advanced = False

    def fetch(endpoint):
        nonlocal branch_advanced
        if endpoint == route:
            return {
                "number": number, "state": "open", "draft": False, "merged": False,
                "base": {"repo": {"full_name": repository}, "ref": "main", "sha": "c" * 40},
                "head": {"repo": {"full_name": repository}, "ref": expected["source_branch"],
                         "sha": new_head if branch_advanced else former_head},
            }
        if endpoint == route + "/commits?per_page=100&page=1":
            branch_advanced = True
            return [{"sha": former_head}, {"sha": new_head}]
        if endpoint == route + "/reviews?per_page=100&page=1":
            return []
        raise ValueError(f"Unexpected API route {endpoint}")

    receipt = module.verify_pull_request(repository, new_head, expected, fetch)
    require(branch_advanced and receipt["head_commit"] == former_head and
            receipt["source_relation"] == "historical PR commit", str(receipt))
    stable = module.verify_pull_request(repository, new_head, expected, fetch)
    require(stable["head_commit"] == new_head and stable["source_relation"] == "current head", str(stable))
    print("E59: A head change between GitHub API reads produces a false historical-member classification. The stable control reports current head.", flush=True)


def main():
    with TemporaryDirectory(prefix="readme-hq-entrypoint-fixtures-") as folder:
        temporary = Path(folder)
        with worktree(temporary / "baseline") as directory:
            run(directory, sys.executable, "tools/check_readme_hq.py")
            check_packaged_self_map(directory, temporary)
            check_merge_queue_trigger(directory)
            check_moving_pr_observation(directory)
            check_duplicate_version_row(directory)


if __name__ == "__main__":
    main()
