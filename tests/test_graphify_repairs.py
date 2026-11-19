"""Regression cases for exact Graphify targets and version evidence."""

import asyncio
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
from evidence_map import flex_text, locate, publish_pair, read_manifest, valid_branch, verify_mcp
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

    def test_receipt_graph_digest_is_verified(self):
        with tempfile.TemporaryDirectory() as folder:
            graph = Path(folder) / "graph.json"
            graph.write_text(json.dumps({"links": []}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "digest"):
                asyncio.run(verify_mcp(graph, {"graph_sha256": "a"*64}))
