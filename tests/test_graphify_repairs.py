"""Regression cases for exact Graphify targets and version evidence."""

import asyncio
from hashlib import sha256
import os
import subprocess
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "graphify-hq/template/v0.0.8"
sys.path.insert(0, str(KIT))
from evidence_map import build, flex_text, locate, publish_pair, read_published_pair, read_manifest, valid_branch, verify_mcp
from github_provenance import Page, pages

spec = importlib.util.spec_from_file_location("version_maps", ROOT / "graphify-hq/version_maps.py")
maps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(maps)


class GraphifyRepairs(unittest.TestCase):
    def test_exact_anchors_and_explicit_line(self):
        self.assertTrue(flex_text("# 👩‍💻 Setup"))
        self.assertFalse(flex_text("a\u200db"))
        self.assertEqual(locate(["Heading", "Heading"], "Heading", "README.md", 2), 2)
        self.assertTrue(valid_branch("_docs/nested"))
        self.assertFalse(valid_branch("docs/../nested"))

    def test_duplicate_resolved_destinations_and_distinct_evidence(self):
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        first = {"path": "guide.md", "anchor": "Heading"}
        explicit = {**first, "line": 1}
        second = {"path": "guide.md", "anchor": "Another heading", "line": 2}
        feature = {"id": "sample", "label": "Sample", "documented_in": [first, explicit],
                   "changed_in": [first], "tested_by": [second]}
        manifest = {"source_commit": commit, "repository": "example/project", "title": "Sample",
                    "features": [feature]}
        with tempfile.TemporaryDirectory() as folder, patch(
            "evidence_map.source_lines", return_value=(["Heading", "Another heading"], "a" * 64)
        ):
            with self.assertRaisesRegex(ValueError, "duplicate resolved destination guide.md:L1"):
                build(manifest, Path(folder))
            feature["documented_in"] = [first, second]
            graph, receipt = build(manifest, Path(folder))
            self.assertEqual(receipt["feature_links"]["feature:sample"],
                             {"documented_in": 2, "changed_in": 1, "tested_by": 1})
            asyncio.run(verify_mcp(graph, receipt))

    def test_existing_graphify_map_keeps_disambiguated_display_labels(self):
        path = ROOT / "graphify-hq/maps/v0.0.1/graph.json"
        data = json.loads(path.read_bytes())
        self.assertTrue(any(node["id"].startswith("file:") and node["label"] != node["source_file"]
                            for node in data["nodes"]))
        receipt = json.loads(path.with_name("receipt.json").read_bytes())
        asyncio.run(verify_mcp(path, receipt))

    def test_graphify_evidence_line_links_use_source_mode_for_rendered_formats(self):
        revision = "a" * 40
        sources = [({"path": "doc/" + path}, line) for path, line in
                   (("README.md", 2), ("read me.rst", 3), ("guide.adoc", 4), ("brief.asciidoc", 5), ("card.asc", 6))]
        outline = [({"title": "Fixture", "summary": "Pinned lines"}, sources, ({"path": "CHANGELOG.txt"}, 7))]
        body = maps.render_outline("v0.0.6", "example/project",
                                   {"source_commit": revision, "nodes": 1, "edges": 0}, outline)
        for ref, line in sources:
            self.assertIn(f"{ref['path'].replace(' ', '%20')}?plain=1#L{line}", body)
        self.assertIn("CHANGELOG.txt#L7", body)

    def test_graphify_attempt_keeps_verified_evidence_after_a_failed_stage(self):
        import os
        from tools import verify_graphify_ci

        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "attempt"
            tests = unittest.mock.Mock(returncode=0)
            failed = unittest.mock.Mock(returncode=7)
            with patch.object(verify_graphify_ci.subprocess, "run", side_effect=[tests, tests, tests, failed]):
                self.assertEqual(verify_graphify_ci.verify(output), 7)
            receipt = json.loads((output / "attempt.json").read_bytes())
            self.assertEqual(receipt["result"], "failed")
            self.assertEqual(receipt["steps"][-1]["name"], "repair plan")
            self.assertFalse(receipt["prior_or_unchecked_receipts_included"])
            saved = sorted((output / "verified").rglob("receipt.json"))
            self.assertEqual(len(saved), 6)
            self.assertTrue(all("maps" in item.parts for item in saved))
            self.assertEqual(os.getcwd(), str(ROOT))

    def test_release_heading_beats_a_draft_placeholder(self):
        content = b"Release notes\n=============\n\nUnreleased\n----------\n\n- TODO\n\n2.34.2 (2026-05-14)\n-------------------\n"
        with patch.object(maps, "source_bytes", return_value=content):
            self.assertEqual(maps.reference("a"*40, "HISTORY.md", change=True, version="v2.34.2")[0]["anchor"],
                             "2.34.2 (2026-05-14)")
        with patch.object(maps, "source_bytes", return_value=b"Sphinx\n======\n"):
            self.assertEqual(maps.reference("a"*40, "README.rst")[0]["anchor"], "Sphinx")
        with patch.object(maps, "source_bytes", return_value=b"= Asciidoctor\n"):
            self.assertEqual(maps.reference("a"*40, "README.adoc")[0]["anchor"], "= Asciidoctor")
        self.assertIn("&#124;", maps.table_cell("Outcome | evidence"))

    def test_coverage_and_duplicate_manifest_keys(self):
        expected = {"v0.0.6": ["a", "b"]}
        with self.assertRaisesRegex(ValueError, "missing"):
            maps.coverage_for({"v0.0.6": [{"id": "a"}]}, ["v0.0.6"], expected)
        with self.assertRaisesRegex(ValueError, "disagree"):
            maps.coverage_for({"v0.0.6": [{"id": "a"}, {"id": "b"}]}, ["v0.0.6"] * 2, expected)
        with tempfile.TemporaryDirectory() as folder:
            manifest = Path(folder) / "manifest.json"
            manifest.write_text('{"repository":"a/b","repository":"c/d"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                read_manifest(manifest)

    def test_full_final_review_page_is_complete_with_metadata(self):
        calls = []
        def fetch(route):
            calls.append(route)
            return Page([{}] * 100, len(calls) < 10)
        self.assertEqual(len(list(pages(fetch, "pulls/1/reviews"))), 1000)
        self.assertEqual(len(calls), 10)

    def test_atomic_pair_preserves_prior_graph_on_conflict(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "output"
            output.mkdir()
            (output / "graph.json").write_bytes(b"old")
            (output / "receipt.json").mkdir()
            with self.assertRaisesRegex(ValueError, "non-regular"):
                publish_pair(output, {"graph.json": b"new", "receipt.json": b"receipt"})
            self.assertEqual((output / "graph.json").read_bytes(), b"old")

    def test_graphify_reader_and_writer_recover_an_interrupted_publication(self):
        def pair(data):
            return {"graph.json": data, "receipt.json": json.dumps({"graph_sha256": sha256(data).hexdigest()}).encode()}

        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "output"
            old = pair(b"old graph")
            new = pair(b"new graph")
            publish_pair(output, old)
            real_replace = os.replace

            def read_between_names(source, destination):
                real_replace(source, destination)
                if Path(destination).name == "previous":
                    self.assertEqual(read_published_pair(output), old)
                    with self.assertRaisesRegex(ValueError, "already active"):
                        publish_pair(output, old)

            with patch("evidence_map.os.replace", side_effect=read_between_names):
                publish_pair(output, new)
            self.assertEqual(read_published_pair(output), new)

            code = """
import os, sys
from pathlib import Path
import evidence_map
replace = os.replace
def stop(source, destination):
    replace(source, destination)
    if Path(destination).name == 'previous':
        os._exit(77)
evidence_map.os.replace = stop
evidence_map.publish_pair(Path(sys.argv[1]), {'graph.json': b'broken', 'receipt.json': b'broken'})
"""
            result = subprocess.run([sys.executable, "-c", code, str(output)], cwd=KIT, check=False)
            self.assertEqual(result.returncode, 77)
            self.assertEqual(read_published_pair(output), new)
            publish_pair(output, old)
            self.assertEqual(read_published_pair(output), old)

    def test_receipt_graph_digest_is_verified(self):
        with tempfile.TemporaryDirectory() as folder:
            graph = Path(folder) / "graph.json"
            graph.write_text(json.dumps({"links": []}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "digest"):
                asyncio.run(verify_mcp(graph, {"graph_sha256": "a"*64}))
