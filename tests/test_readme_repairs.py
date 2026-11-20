"""Regression tests for selected-tree navigation and verified reader outcomes."""

import contextlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from hq_data import GitTree, parse_json
from hq_navigation import check_document, readme_path
from hq_smoke import verify_first_action
from check_readme_hq import check_evidence, evidence_identity, target_readme
from verify_plan import split_checkpoints, stage_partitions


@contextlib.contextmanager
def repository(files):
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        for name, content in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content.encode() if isinstance(content, str) else content)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=test@example.invalid",
                        "commit", "-qm", "Fixture"], cwd=root, check=True)
        yield GitTree(root)


class ReaderTests(unittest.TestCase):
    def test_pinned_readme_and_monorepo_routes(self):
        with repository({"README.md": "# Root", ".github/README.md": "# Published",
                         "docs/README.md": "# Docs", "packages/example/README.md": "# Subproject"}) as tree:
            self.assertEqual(readme_path(tree.entries(), homepage=True), ".github/README.md")
            self.assertEqual(readme_path(tree.entries(), "packages/example"), "packages/example/README.md")
        with repository({"docs/README.markdown": "# Docs"}) as tree:
            self.assertEqual(readme_path(tree.entries(), homepage=True), "docs/README.markdown")

    def test_fragments_and_rendered_link_forms(self):
        body = """# Fixture
[Section](guides/#present)
[Alternate](guides/guide.markdown#available)
[Named](guides/README.md#reviewed)
[Root](/guides/README.md#present)
[Relative link][route]

[route]: guides/README.md#present "A title"
<a href="guides/README.md#present">HTML</a>

[Out of bounds](code.py#L9)
[Last line](code.py#L2)
[Missing directory anchor](guides/#absent)
[Missing alternate anchor](guides/guide.markdown#absent)
[Untracked](untracked.md)
[Titled](missing.md "A title")

Literal example `[Ignore](literal.md)`.
"""
        with repository({"README.md": body, "guides/README.md": "Present\n=======\n\n<a name=\"reviewed\"></a>\n",
                         "guides/guide.markdown": "## Available\n", "code.py": "first\nsecond\n"}) as tree:
            (tree.root / "untracked.md").write_text("draft", encoding="utf-8")
            errors, gaps = [], []
            self.assertEqual(check_document(tree, "README.md", errors, gaps), 7)
            self.assertEqual(len(errors), 5)
            self.assertIn("outside the file", errors[0])
            self.assertTrue(any("untracked.md" in issue for issue in errors))
            self.assertFalse(any("literal.md" in issue for issue in errors))
            self.assertEqual(gaps, [])

    def test_bad_image_and_unnamed_image_link_are_separate(self):
        readme = "# Images\n[![](broken.png)](README.md)\n[Another dead link](absent.md)\n"
        with repository({"README.md": readme, "broken.png": b"not a PNG"}) as tree:
            errors = []
            check_document(tree, "README.md", errors, [])
            self.assertEqual(len(errors), 3)
            self.assertTrue(any("accessible name" in issue for issue in errors))
            self.assertTrue(any("unreadable image" in issue for issue in errors))
            self.assertTrue(any("absent.md" in issue for issue in errors))

    def test_quality_and_smoke_have_separate_outcomes(self):
        with repository({"README.md": "# Package\n\nTODO: document the behavior.\n"}) as tree:
            errors, gaps = [], []
            self.assertEqual(target_readme(tree, ".", errors, gaps, "application")[0], "README.md")
            self.assertTrue(any("placeholder" in error for error in errors))
            spec = tree.root / "smoke.json"
            def smoke(data, network=False):
                spec.write_text(json.dumps({"commit": tree.commit, **data}), encoding="utf-8")
                return verify_first_action(tree, spec, allow_network=network)["result"]
            action = {"argv": [sys.executable, "-c", "print('ready')"], "expected": {"exit": 0, "contains": "ready"}}
            self.assertEqual(smoke(action), "passed")
            action["expected"]["contains"] = "wrong"
            self.assertEqual(smoke(action), "failed")
            self.assertEqual(smoke({"url": "https://example.invalid", "expected": {"http_status": 200}}), "unchecked")

    def test_ascii_technique_listing(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/check_readme_hq.py"), "--list"],
                                cwd=ROOT, env={**os.environ, "PYTHONIOENCODING": "ascii"},
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("exact-revision-walkthrough [active]", result.stdout)


class EvidenceTests(unittest.TestCase):
    def test_json_duplicates_and_canonical_evidence(self):
        with self.assertRaisesRegex(ValueError, "repeated JSON key"):
            parse_json(b'{"x":{"schema":1,"schema":2}}', "registry")
        url = f"https://github.com/acme/example/blob/{'a'*40}/docs/Guide.md"
        first = {"url": url + "?plain=1#L7", "status": "observed"}
        second = {"url": url + "?x=1#L9", "status": "observed"}
        self.assertEqual(evidence_identity(first), evidence_identity(second))
        with self.assertRaisesRegex(ValueError, "public"):
            evidence_identity({**first, "visibility": "private"})
        with self.assertRaisesRegex(ValueError, "receipt"):
            check_evidence({**first, "status": "verified"}, None)

    def test_partition_capacity_preserves_order(self):
        features = list(range(100))
        parts = split_checkpoints(features)
        self.assertEqual([len(part) for part in parts], [32, 32, 32, 4])
        self.assertEqual([item for part in parts for item in part], features)

    def test_partition_writer_handles_more_than_three_partitions(self):
        ref = [{"path": "README.md", "anchor": "# Evidence"}]
        features = [{"id": f"checkpoint-{i}", "documented_in": ref, "changed_in": ref, "tested_by": ref}
                    for i in range(100)]
        with tempfile.TemporaryDirectory() as folder:
            files = stage_partitions(features, Path(folder) / "parts", "a" * 40, "example/project")
            published = [item for path in files for item in json.loads(path.read_bytes())["features"]]
        self.assertEqual(published, features)

    def test_learning_receipt_is_pinned_and_idempotent(self):
        spec = importlib.util.spec_from_file_location("intake", ROOT / "learning/intake.py")
        intake = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(intake)
        def catalog_body(status="active", **fields):
            return "<!-- catalog\n" + json.dumps({"status": status, **fields}) + "\n-->\n# Catalog record\n"

        files = {
            "techniques/relative-navigation.md": catalog_body(),
            "techniques/another-technique.md": catalog_body(),
            "techniques/retired-technique.md": catalog_body("retired"),
            "combinations/first-reader-path.md": catalog_body(
                steps=["relative-navigation", "another-technique"]),
            "combinations/missing-step.md": catalog_body(
                steps=["relative-navigation", "not-in-catalog"]),
        }
        with repository({"README.md": "# Evidence\\n"}) as tree, repository(files) as catalog:
            tree.git("remote", "add", "origin", "https://github.com/example/project.git")
            catalog.git("remote", "add", "origin", "https://github.com/vixttha/README-HQ.git")
            record = {"id": "example", "checkout": str(tree.root), "ref": "HEAD",
                      "repository": "example/project", "path": "README.md",
                      "line": 1, "anchor": "# Evidence", "visibility": "public"}
            rationale = {"source": "example", "decision": "adapt", "rationale": "Explain the first result."}
            spec = {"visibility": "public", "sources": [record], "selected": ["example"],
                    "catalog": {"checkout": str(catalog.root), "commit": catalog.commit},
                    "target": {**record, "audience": "developer", "capability": "command line"},
                    "findings": [{**rationale, "technique": "relative-navigation"},
                                 {**rationale, "combination": "first-reader-path"}]}

            def fetch(route):
                if route in {"example/project", "vixttha/README-HQ"}:
                    return {"private": False, "visibility": "public"}
                if route == f"vixttha/README-HQ/compare/{catalog.commit}...README-Technique-Library":
                    return {"status": "ahead"}
                if route == f"vixttha/README-HQ/commits/{catalog.commit}":
                    return {"sha": catalog.commit}
                if route == f"example/project/commits/{tree.commit}":
                    return {"sha": tree.commit}
                self.fail(f"Unexpected GitHub request {route}")

            destination = tree.root / "receipts"
            first = intake.record_intake(spec, destination, fetch=fetch)
            (catalog.root / "techniques/relative-navigation.md").write_text(catalog_body("retired"))
            self.assertEqual(first, intake.record_intake(spec, destination, fetch=fetch))
            result = json.loads(first.read_bytes())
            self.assertEqual(result["schema"], 2)
            self.assertEqual(result["catalog"]["commit"], catalog.commit)
            self.assertEqual(result["catalog"]["branch"], "README-Technique-Library")
            technique = next(row for row in result["recommendations"] if "technique" in row)
            self.assertEqual(technique["technique"], "relative-navigation")
            self.assertEqual(technique["target"]["commit"], tree.commit)
            combination = next(row for row in result["recommendations"] if "combination" in row)
            self.assertEqual(combination["catalog_record"]["steps"], ["relative-navigation", "another-technique"])
            for choice, error in (
                ({"technique": "first-success-milestone"}, "absent from the pinned external catalog"),
                ({"technique": "retired-technique"}, "expected an active record"),
                ({"combination": "missing-step"}, "absent from the pinned external catalog"),
            ):
                with self.subTest(choice=choice), self.assertRaisesRegex(ValueError, error):
                    intake.record_intake({**spec, "findings": [{**rationale, **choice}]}, destination, fetch=fetch)
            without_catalog = {key: value for key, value in spec.items() if key != "catalog"}
            with self.assertRaisesRegex(ValueError, "requires an external catalog"):
                intake.record_intake(without_catalog, destination, fetch=fetch)
            def unrelated_branch(route):
                if "/compare/" in route:
                    return {"status": "diverged"}
                return fetch(route)

            with self.assertRaisesRegex(ValueError, "not on README-Technique-Library"):
                intake.record_intake(spec, destination, fetch=unrelated_branch)
            self.assertEqual(list(destination.iterdir()), [first])
            spec["selected"] = []
            second = intake.record_intake(spec, destination, fetch=fetch)
            self.assertNotEqual(first, second)
            self.assertEqual(json.loads(second.read_bytes())["recommendations"], [])

    def test_public_learning_refusal_writes_nothing(self):
        spec = importlib.util.spec_from_file_location("intake", ROOT / "learning/intake.py")
        intake = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(intake)
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "receipts"
            with self.assertRaisesRegex(ValueError, "public"):
                intake.record_intake({"visibility": "private", "target": {"id": "private-probe"}}, destination)
            self.assertFalse(destination.exists())
