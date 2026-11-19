"""Repeatable audit for the pinned README HQ candidate in disposable Git trees."""
import asyncio
from contextlib import chdir, contextmanager
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

ROOT = Path.cwd()
EXPECTED = "8d50caec2bc6fcb998994a1fd302294a029325f9"
CHECKER = ROOT / "tools/check_readme_hq.py"
sys.path[:0] = [str(ROOT / path) for path in ("tools", "learning", "graphify-hq/template/v0.0.8")]
from hq_data import GitTree
from hq_navigation import check_document, readme_path
import evidence_map
import intake


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, stderr=subprocess.PIPE).strip()


def commit(root):
    git(root, "add", ".")
    git(root, "-c", "user.name=README HQ Audit", "-c", "user.email=audit@example.invalid",
        "commit", "-qm", "Record synthetic audit fixture")
    return git(root, "rev-parse", "HEAD")


@contextmanager
def fixture(files, origin=None):
    with TemporaryDirectory() as temp:
        root = Path(temp)
        git(root, "init", "-qb", "main")
        if origin:
            git(root, "remote", "add", "origin", origin)
        for name, contents in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding="utf-8")
        yield root, commit(root)


def checker(target, *args):
    return subprocess.run([sys.executable, str(target), *map(str, args)], capture_output=True, text=True)


def observe(root, source):
    errors, gaps = [], []
    checked = check_document(GitTree(root), source, errors, gaps)
    return {"errors": errors, "gaps": gaps, "checked": checked}


def receipt_validator_digest():
    marker = "This adopter fixture is a text marker and is never executed.\n"
    tool_path = "tools/check_readme_hq.py"
    with fixture({"README.md": "# Example\n\nA detailed description for this reference project.\n",
                  tool_path: marker}) as (root, _):
        output = root / "receipt.json"
        result = checker(CHECKER, "--repo", root, "--profile", "reference", "--receipt", output)
        assert result.returncode == 0, result.stderr
        receipt = json.loads(output.read_bytes())
        reported = receipt["sources"][tool_path]
        installed = sha256(CHECKER.read_bytes()).hexdigest()
        assert reported == sha256(marker.encode()).hexdigest() and reported != installed
        assert installed not in receipt["sources"].values()
        return {"recorded_adopter_file_as_validator_path": True, "installed_validator_hash_absent": True}


def wrong_top_level():
    with TemporaryDirectory() as temp:
        checkout = Path(temp) / "candidate"
        git(ROOT, "worktree", "add", "--detach", str(checkout), EXPECTED)
        try:
            registry = checkout / "techniques/registry.json"
            registry.write_text("[]\n", encoding="utf-8")
            commit(checkout)
            output = Path(temp) / "bad-registry.json"
            command = checker(checkout / "tools/check_readme_hq.py", "--receipt", output)
            assert command.returncode == 1 and not output.exists()
            assert "AttributeError: 'list' object has no attribute 'get'" in command.stderr
            return {"syntax_valid_json": True, "exit": command.returncode, "python_traceback": True,
                    "receipt_exists": output.exists(), "error": command.stderr.splitlines()[-1]}
        finally:
            git(ROOT, "worktree", "remove", "--force", str(checkout))


def root_readme_anchor():
    files = {".github/README.md": "# Preferred Homepage\n", "README.md": "# Root Fallback\n",
             "docs/guide.md": "[Preferred](/#preferred-homepage)\n\n[Fallback](/#root-fallback)\n"}
    with fixture(files) as (root, _):
        tree = GitTree(root)
        selected = readme_path(tree.entries(), homepage=True)
        result = observe(root, "docs/guide.md")
        assert selected == ".github/README.md" and result["checked"] == 1 and not result["gaps"]
        assert len(result["errors"]) == 1 and result["errors"][0].endswith("/#preferred-homepage")
        return {"homepage_selected_by_cli": selected, "root_fragment_result": result}


def multiline_link_location():
    files = {"README.md": "# Project\n\nA single paragraph starts here.\n"
                          "On its next line, [first](missing-a.md) appears.\n"
                          "On its final line, [second](missing-b.md) appears.\n"}
    with fixture(files) as (root, _):
        result = observe(root, "README.md")
        assert len(result["errors"]) == 2
        assert all(text.startswith("README.md:3:") for text in result["errors"])
        return {"actual_lines": [4, 5], "reported_lines": [3, 3], **result}


def duplicate_resolved_graph_edge():
    with fixture({"README.md": "# Evidence\n"}) as (root, sha), TemporaryDirectory() as temp:
        anchor = {"path": "README.md", "anchor": "# Evidence"}
        data = {"repository": "example/fixture", "source_commit": sha, "title": "Evidence",
                "features": [{"id": "case", "label": "Case", "documented_in": [anchor, {**anchor, "line": 1}],
                              "changed_in": [anchor], "tested_by": [anchor]}]}
        with chdir(root):
            evidence_map.validate_manifest(data)
            path, receipt = evidence_map.build(data, Path(temp))
            try:
                asyncio.run(evidence_map.verify_mcp(path, receipt))
            except ValueError as error:
                assert "Graph evidence destinations differ from the pinned manifest" in str(error)
                return {"manifest_validated": True, "duplicate_references_resolve_to_same_line": True,
                        "graph_verification_error": str(error)}
    raise AssertionError("expected duplicate destination drift")


def learning_registry_snapshot():
    origin = "https://github.com/example/readme-hq-audit-fixture.git"
    repository = "example/readme-hq-audit-fixture"
    record = {"id": "example-technique", "status": "active"}
    first = json.dumps({"techniques": [record]}).encode()
    second = json.dumps({"techniques": [{**record, "status": "retired"}]}).encode()
    with fixture({"README.md": "# Evidence\n"}, origin) as (root, sha), TemporaryDirectory() as temp:
        directory = Path(temp)
        registry = directory / "techniques/registry.json"
        registry.parent.mkdir()
        registry.write_bytes(first)
        source = {"checkout": str(root), "repository": repository, "ref": sha, "path": "README.md",
                  "line": 1, "anchor": "Evidence", "visibility": "public"}
        request = {"visibility": "public", "sources": [{"id": "a", **source}], "selected": ["a"],
                   "target": {**source, "audience": "Readers", "capability": "Evidence"},
                   "findings": [{"source": "a", "technique": record["id"], "decision": "adopt",
                                 "rationale": "Keep the project entry point explicit."}]}
        def fetch(path):
            return {"private": False, "visibility": "public"} if path == repository else {"sha": sha}
        read = intake.read_json
        def change_after_read(path):
            data = read(path)
            registry.write_bytes(second)
            return data
        with patch.object(intake, "ROOT", directory), patch.object(intake, "read_json", change_after_read):
            output = intake.record_intake(request, directory / "receipts", fetch=fetch)
        saved = json.loads(output.read_bytes())
        assert saved["recommendations"][0]["technique"] == record["id"]
        assert saved["registry_sha256"] == sha256(second).hexdigest()
        return {"recommendation_retained": True, "digest_identifies_retired_registry": True}


def main():
    assert git(ROOT, "rev-parse", "HEAD") == EXPECTED
    observations = {}
    cases = (receipt_validator_digest, wrong_top_level, root_readme_anchor, multiline_link_location,
             duplicate_resolved_graph_edge, learning_registry_snapshot)
    for case in cases:
        observations[case.__name__] = case()
        print("Observed", case.__name__, flush=True)
    Path(sys.argv[1]).write_text(json.dumps({"candidate": EXPECTED, "observations": observations}, indent=2) + "\n",
                                encoding="utf-8")


if __name__ == "__main__":
    main()
