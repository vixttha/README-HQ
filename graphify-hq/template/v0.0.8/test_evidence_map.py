import asyncio
from hashlib import sha256
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evidence_map import MAX_SOURCE_BYTES, build, locate, source_blob, source_lines, validate_manifest, verify_mcp
from github_provenance import verify_pull_request

class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {
            "repository": "sample/example",
            "source_commit": "a" * 40,
            "title": "Example evidence",
            "features": [{
                "id": "export",
                "label": "Evidence export",
                "documented_in": [{"path": "README.md", "anchor": "## Export"}],
                "changed_in": [{"path": "CHANGELOG.md", "anchor": "## v1.0.0"}],
                "tested_by": [{"path": "test_export.py", "anchor": "def test_export():"}],
            }],
        }

    def test_existing_manifest_needs_no_inventory_or_implementation_links(self):
        accepted = validate_manifest(self.manifest)
        self.assertEqual(len(accepted["features"][0]["tested_by"]), 1)

    def test_inventory_and_implementation_links_are_accepted(self):
        self.manifest["source_files"] = ["export.py", "README.md"]
        self.manifest["features"][0]["implemented_in"] = [
            {"path": "export.py", "anchor": "def export():"},
        ]
        self.assertEqual(validate_manifest(self.manifest), self.manifest)

    def test_inventory_blob_cap_and_text_anchor_boundary(self):
        binary = b"\xff" * MAX_SOURCE_BYTES
        name = b"inventory.bin"
        entry = b"100644 blob " + b"a" * 40 + b"\t" + name + b"\0"
        for size in (MAX_SOURCE_BYTES - 1, MAX_SOURCE_BYTES, MAX_SOURCE_BYTES + 1):
            responses = [entry, str(size).encode(), binary[:size]]
            with self.subTest(size=size), patch("evidence_map.git", side_effect=responses) as git:
                if size > MAX_SOURCE_BYTES:
                    with self.assertRaisesRegex(ValueError, f"{size} exceeds limit of {MAX_SOURCE_BYTES} bytes"):
                        source_blob(self.manifest["source_commit"], name.decode())
                    self.assertEqual(git.call_count, 2)
                else:
                    self.assertEqual(source_blob(self.manifest["source_commit"], name.decode()), binary[:size])
        with patch("evidence_map.source_blob", return_value=binary):
            with self.assertRaisesRegex(ValueError, "require UTF-8"):
                source_lines(self.manifest["source_commit"], name.decode())
        anchor = "a" * 500
        feature = self.manifest["features"][0]
        feature["documented_in"] = [{"path": "README.md", "anchor": anchor, "line": 1}]
        self.assertEqual(validate_manifest(self.manifest), self.manifest)
        with patch("evidence_map.source_blob", return_value=(anchor + "\n").encode()):
            lines, _ = source_lines(self.manifest["source_commit"], "README.md")
            self.assertEqual(locate(lines, anchor, "README.md", 1), 1)
        feature["documented_in"][0]["anchor"] += "a"
        with self.assertRaisesRegex(ValueError, "Invalid or duplicate source link"):
            validate_manifest(self.manifest)

    def test_inventory_rejects_invalid_paths_and_duplicates(self):
        for paths in (["README.md", "README.md"], ["tools/../README.md"], [None], "README.md"):
            with self.subTest(paths=paths):
                self.manifest["source_files"] = paths
                with self.assertRaisesRegex(ValueError, "unique source file paths"):
                    validate_manifest(self.manifest)

    def test_implementation_anchor_connects_feature_to_inventory_file(self):
        self.manifest["source_files"] = ["export.py"]
        self.manifest["features"][0]["implemented_in"] = [
            {"path": "export.py", "anchor": "def export():"},
        ]
        lines = {
            "export.py": ["def export():"],
            "README.md": ["## Export"],
            "CHANGELOG.md": ["## v1.0.0"],
            "test_export.py": ["def test_export():"],
        }
        with (
            tempfile.TemporaryDirectory() as folder,
            patch("evidence_map.git", return_value=b"commit"),
            patch("evidence_map.source_blob", return_value=b"fixture"),
            patch("evidence_map.source_lines", side_effect=lambda commit, path: (lines[path], path)),
        ):
            graph, receipt = build(validate_manifest(self.manifest), Path(folder))
            links = json.loads(graph.read_text(encoding="utf-8"))["links"]
        anchor = "implemented_in:export.py:L1"
        edges = {(edge["source"], edge["target"], edge["relation"]) for edge in links}
        self.assertIn(("feature:export", anchor, "implemented_in"), edges)
        self.assertIn((anchor, "file:export.py", "located_in"), edges)
        self.assertEqual(receipt["source_files"], ["export.py"])

    def test_evidence_map_requires_features_or_inventory(self):
        feature = self.manifest["features"][0]
        self.manifest["features"] = []
        with self.assertRaisesRegex(ValueError, "at least one feature or inventory"):
            validate_manifest(self.manifest)
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        self.manifest.update(source_commit=commit, source_files=["README.md"])
        checkout_bytes = subprocess.check_output(["git", "show", f"{commit}:README.md"])
        anchor = checkout_bytes.decode("utf-8").splitlines()[0]
        reference = {"path": "README.md", "anchor": anchor, "line": 1}
        mapped = {**feature, **dict.fromkeys(("documented_in", "changed_in", "tested_by"), [reference])}
        for features, nodes, edges in (([], 2, 1), ([mapped], 6, 8)):
            self.manifest["features"] = features
            with self.subTest(features=features), tempfile.TemporaryDirectory() as folder:
                graph, receipt = build(validate_manifest(self.manifest), Path(folder))
                self.assertEqual((receipt["nodes"], receipt["edges"]), (nodes, edges))
                self.assertEqual(receipt["source_sha256"]["README.md"], sha256(checkout_bytes).hexdigest())
                asyncio.run(verify_mcp(graph, receipt))

    def test_source_path_must_stay_inside_commit(self):
        test = self.manifest["features"][0]["tested_by"][0]
        for path in ("../secrets.md", "/etc/passwd", "tools/../README.md", ".git/config", "HEAD:README.md"):
            with self.subTest(path=path):
                test["path"] = path
                with self.assertRaisesRegex(ValueError, "source link"):
                    validate_manifest(self.manifest)

    def test_anchor_resolves_to_one_exact_line(self):
        self.assertEqual(locate(["paragraph", "    evidence", "last"], "evidence", "case"), 2)
        for lines in (["no match"], ["evidence", "evidence"]):
            with self.subTest(lines=lines):
                with self.assertRaisesRegex(ValueError, "exactly one match"):
                    locate(lines, "evidence", "case")


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.repo = "sample/example"
        self.source = "a" * 40
        self.head = "b" * 40
        self.expected = {"number": 3, "source_branch": "topic"}
        self.pr = {
            "number": 3, "state": "open", "draft": False, "merged": False,
            "base": {"repo": {"full_name": self.repo}, "ref": "main", "sha": "c" * 40},
            "head": {"repo": {"full_name": self.repo}, "ref": "topic", "sha": self.head},
            "merge_commit_sha": None,
        }
        self.commits = [{"sha": self.source}, {"sha": self.head}]
        self.reviews = []

    def fetch(self, route):
        return {
            "pulls/3": self.pr,
            "pulls/3/commits?per_page=100&page=1": self.commits,
            "pulls/3/reviews?per_page=100&page=1": self.reviews,
        }[route]

    def verify(self):
        return verify_pull_request(self.repo, self.source, self.expected, self.fetch)

    def test_base_provenance_rejects_retargeting_with_the_same_head(self):
        outcome = verify_pull_request(self.repo, self.head, self.expected, self.fetch)
        self.assertEqual((outcome["base_ref"], outcome["base_commit"], outcome["head_commit"]),
                         ("main", "c" * 40, self.head))
        for change in ({"ref": "develop"}, {"sha": "d" * 40}):
            with self.subTest(change=change):
                retargeted = {**self.pr, "base": {**self.pr["base"], **change}}
                metadata = iter((self.pr, retargeted))
                def fetch(route):
                    return next(metadata) if route == "pulls/3" else self.fetch(route)
                with self.assertRaisesRegex(ValueError, "changed during provenance verification"):
                    verify_pull_request(self.repo, self.head, self.expected, fetch)

    def test_historical_commit_requires_github_membership(self):
        self.assertEqual(self.verify()["source_relation"], "historical PR commit")
        self.commits = [{"sha": self.head}]
        with self.assertRaisesRegex(ValueError, "absent"):
            self.verify()

    def test_unrelated_repository_or_branch_is_rejected(self):
        self.pr["head"]["ref"] = "unrelated"
        with self.assertRaisesRegex(ValueError, "source repository and branch"):
            self.verify()
        self.pr["head"]["ref"] = "topic"
        self.pr["head"]["repo"]["full_name"] = "another/example"
        with self.assertRaisesRegex(ValueError, "source repository and branch"):
            self.verify()

    def test_superseded_and_later_commit_approvals_are_excluded(self):
        self.reviews = [
            {"user": {"id": 1}, "state": "APPROVED", "commit_id": self.source},
            {"user": {"id": 1}, "state": "CHANGES_REQUESTED", "commit_id": self.head},
            {"user": {"id": 2}, "state": "APPROVED", "commit_id": self.head},
            {"user": {"id": 3}, "state": "APPROVED", "commit_id": self.source},
        ]
        self.assertEqual(self.verify()["exact_commit_approvals"], 1)

    def test_merge_sha_is_distinct_from_source_sha(self):
        self.pr.update(state="closed", merged=True, merge_commit_sha="c" * 40)
        outcome = self.verify()
        self.assertEqual(outcome["source_commit"], self.source)
        self.assertEqual(outcome["merge_commit"], "c" * 40)
        self.assertEqual(outcome["pr_state"], "merged")


if __name__ == "__main__":
    unittest.main()
