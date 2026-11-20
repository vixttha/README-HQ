import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "catalog.py"


class CatalogTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.script = self.root / "tools" / SCRIPT.name
        self.script.parent.mkdir()
        shutil.copyfile(SCRIPT, self.script)

    def invoke(self, *args, expected=0):
        result = subprocess.run([sys.executable, "-X", "utf8", str(self.script), *args],
                                capture_output=True, encoding="utf-8")
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def record(self, identity, title, directory="techniques", **metadata):
        data = {"title": title, "summary": "Help readers find their first result.", "tasks": ["quickstart"],
                "aliases": [], "tags": [], "status": "active", "evidence": "observed", **metadata}
        path = self.root / directory / (identity + ".md")
        path.parent.mkdir(exist_ok=True)
        path.write_text("<!-- catalog\n" + json.dumps(data) + "\n-->\n\n# " + title + "\n",
                        encoding="utf-8")
        return path

    def search(self, *args):
        return json.loads(self.invoke("search", *args, "--json").stdout)

    def test_empty_catalog_and_stale_index(self):
        self.invoke("check", expected=1)
        self.invoke("build")
        self.invoke("check")
        self.assertEqual(self.search()["total"], 0)
        self.record("example", "Example technique")
        self.assertIn("need regeneration", self.invoke("check", expected=1).stderr)
        self.invoke("build")
        self.invoke("check")

    def test_combination_and_retired_steps(self):
        self.record("navigation", "Relative links")
        self.record("first-result", "Expected first result")
        self.record("paired", "Navigation with result", "combinations", steps=["navigation", "first-result"])
        self.invoke("build")
        page = (self.root / "catalog/quickstart.md").read_text(encoding="utf-8")
        self.assertIn("](../techniques/navigation.md) → [", page)
        self.assertEqual(self.search("--kind", "combination")["results"][0]["steps"],
                         ["navigation", "first-result"])
        self.record("navigation", "Relative links", status="retired")
        self.assertIn("retired technique", self.invoke("check", expected=1).stderr)
        self.record("paired", "Navigation with result", "combinations", steps=["first-result", "unknown"])
        self.assertIn("missing technique step", self.invoke("check", expected=1).stderr)

    def test_duplicate_names_ids_and_invalid_metadata(self):
        self.record("one", "Relative links", aliases=["Café route"])
        path = self.record("two", "Cafe route")
        self.assertIn("also belongs", self.invoke("build", expected=1).stderr)
        path.unlink()
        duplicate = self.record("one", "Duplicate ID", "combinations", steps=["one", "two"])
        self.assertIn("duplicate record ID", self.invoke("build", expected=1).stderr)
        duplicate.unlink()
        invalid = self.record("invalid", "Invalid task", tasks=["missing"])
        self.assertIn("documented task IDs", self.invoke("build", expected=1).stderr)
        invalid.write_text('<!-- catalog\n{"title":"one","title":"two"}\n-->\n# Record\n', encoding="utf-8")
        self.assertIn("duplicate metadata key", self.invoke("build", expected=1).stderr)

    def test_accent_aliases_ranking_and_filters(self):
        self.record("cafe", "Café navigation", aliases=["Entry proof"], tasks=["quickstart", "verification"],
                    tags=["cross-project"], evidence="verified")
        self.record("competitor", "AAA entry place", summary="Help show proof.")
        self.record("old", "Old technique", status="retired", aliases=["Legacy guide"])
        self.assertEqual(self.search("CAFE")["results"][0]["id"], "cafe")
        self.assertEqual(self.search("entry proof")["results"][0]["id"], "cafe")
        self.assertEqual(self.search("cross pro", "--task", "verification", "--tag", "cross-project",
                                     "--evidence", "verified")["total"], 1)
        self.assertEqual(self.search("legacy")["total"], 0)
        self.assertEqual(self.search("legacy", "--status", "all")["total"], 1)
        self.assertEqual(self.search("missing phrase")["total"], 0)
        self.assertEqual(self.search("--limit", "1", "--offset", "2")["results"], [])
        self.invoke("search", "--offset", "-1", expected=2)

    def test_600_records_browse_and_paginate(self):
        for i in range(600):
            self.record(f"fixture-{i:03}", f"Fixture {i:03}", tags=["synthetic"])
        self.invoke("build")
        self.invoke("check")
        result = self.search("fixture", "--limit", "25", "--offset", "575")
        self.assertEqual(result["total"], 600)
        self.assertEqual(len(result["results"]), 25)
        self.assertEqual(result["results"][0]["id"], "fixture-575")
        self.assertEqual(result["results"][-1]["id"], "fixture-599")
        finder = (self.root / "catalog/search.md").read_text(encoding="utf-8")
        self.assertEqual(finder.count("](../techniques/fixture-"), 600)
        self.assertIn("synthetic", finder)
        catalog = self.root / "catalog"
        task_pages = sorted(catalog.glob("quickstart*.md"))
        self.assertEqual(len(task_pages), 6)
        self.assertEqual(sum(page.read_text(encoding="utf-8").count("](../techniques/fixture-")
                             for page in task_pages), 600)
        self.assertIn("[6](quickstart-6.md)", (catalog / "quickstart.md").read_text(encoding="utf-8"))
        for item in (self.root / "techniques").glob("*.md"):
            if item.name != "fixture-000.md":
                item.unlink()
        self.invoke("build")
        self.invoke("check")
        self.assertFalse((catalog / "quickstart-6.md").exists())

    def test_long_browser_finder_splits_and_preserves_records(self):
        for i in range(250):
            aliases = [f"{'漢' * 70} {i:03} {j:02}" for j in range(12)]
            self.record(f"wide-{i:03}", f"Wide {i:03}", aliases=aliases)
        self.invoke("build")
        finder_pages = list((self.root / "catalog").glob("search*.md"))
        self.assertGreater(len(finder_pages), 1)
        self.assertTrue(all(page.stat().st_size < 230_000 for page in finder_pages))
        self.assertEqual(sum(page.read_text(encoding="utf-8").count("](../techniques/wide-")
                             for page in finder_pages), 250)
        self.assertEqual(self.search("wide")["total"], 250)


if __name__ == "__main__":
    unittest.main()
