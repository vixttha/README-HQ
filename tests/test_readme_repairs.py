"""Regression tests for selected-tree navigation and verified reader outcomes."""

import contextlib
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from hq_data import GitTree, parse_json
from hq_navigation import check_document, readme_path, same_repo_target
from urllib.parse import urlsplit
from hq_smoke import verify_first_action
from check_readme_hq import check_evidence, check_registry, check_versions, evidence_identity, target_readme
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

    def test_broken_inline_links_reference_the_exact_occurrence_line(self):
        readme = """# Example

An introductory sentence
[same label](first.md) and [valid](README.md)
[same label](second.md) plus a literal `[same label](ignored.md)`.

> A quoted paragraph
> [same label][missing]

[missing]: third.md

A separate [same label](fourth.md).
"""
        with repository({"README.md": readme}) as tree:
            errors, gaps = [], []
            self.assertEqual(check_document(tree, "README.md", errors, gaps), 1)
            self.assertEqual([error.split(":")[1] for error in errors], ["4", "5", "8", "12"])
            self.assertEqual(gaps, [])

    def test_root_fragments_follow_the_effective_homepage(self):
        layouts = [
            (".github/README.md", {"README.md": "# Wrong", "docs/README.md": "# Different"}),
            ("README.md", {"docs/README.md": "# Wrong"}),
            ("docs/README.md", {}),
        ]
        reader = "[Preferred](/#preferred) [Wrong](/#wrong) [Package](/packages/widget/#separate)"
        for path, fallback in layouts:
            with repository({**fallback, path: "# Preferred", "guide.md": reader,
                             "packages/widget/README.md": "# Separate"}) as tree:
                errors, gaps = [], []
                self.assertEqual(check_document(tree, "guide.md", errors, gaps), 2)
                self.assertEqual(len(errors), 1)
                self.assertIn("/#wrong", errors[0])
                self.assertEqual(gaps, [])

    def test_fetched_repository_refs_are_resolved_without_a_local_branch(self):
        with repository({"README.md": "# Guide"}) as original:
            original.git("remote", "add", "origin", "https://github.com/example/project.git")
            original.git("update-ref", "refs/remotes/origin/release/next", original.commit)
            original.git("tag", "release/next", original.commit)
            tree = GitTree(original.root)
            url = urlsplit("https://github.com/example/project/blob/release/next/README.md")
            self.assertEqual(same_repo_target(tree, url), ("README.md", tree.commit))
            abbreviated = urlsplit(f"https://github.com/example/project/blob/{tree.commit[:12]}/README.md")
            self.assertEqual(same_repo_target(tree, abbreviated), ("README.md", tree.commit))
            exact = urlsplit(f"https://github.com/example/project/blob/{tree.commit}/README.md")
            self.assertEqual(same_repo_target(tree, exact), ("README.md", tree.commit))
            tree.git("-c", "user.name=Fixture", "-c", "user.email=test@example.invalid",
                     "commit", "--allow-empty", "-qm", "Different local commit")
            tree.git("branch", "release/next")
            with self.assertRaisesRegex(ValueError, "conflicting"):
                same_repo_target(tree, url)
            with self.assertRaisesRegex(LookupError, "unresolved"):
                same_repo_target(tree, urlsplit("https://github.com/example/project/blob/absent/README.md"))

    def test_bad_image_and_unnamed_image_link_are_separate(self):
        readme = "# Images\n[![](broken.png)](README.md)\n[Another dead link](absent.md)\n"
        with repository({"README.md": readme, "broken.png": b"not a PNG"}) as tree:
            errors = []
            check_document(tree, "README.md", errors, [])
            self.assertEqual(len(errors), 3)
            self.assertTrue(any("accessible name" in issue for issue in errors))
            self.assertTrue(any("unreadable image" in issue for issue in errors))
            self.assertTrue(any("absent.md" in issue for issue in errors))

    def test_responsive_image_sources_are_checked_alongside_fallback(self):
        body = ('<picture><source media="(prefers-color-scheme: dark)" '
                'srcset="dark.svg 1x, dark-large.svg 2x"><source srcset="invalid.svg bad">'
                '<img src="light.svg" alt="Diagram"></picture>')
        svg = '<svg xmlns="http://www.w3.org/2000/svg"></svg>'
        for include_large in (False, True):
            files = {"README.md": body, "dark.svg": svg, "light.svg": svg}
            if include_large:
                files["dark-large.svg"] = svg
            with repository(files) as tree:
                errors, gaps = [], []
                self.assertEqual(check_document(tree, "README.md", errors, gaps), 3 if include_large else 2)
                self.assertEqual(bool(errors), not include_large)
                if errors:
                    self.assertIn("dark-large.svg", errors[0])
                self.assertTrue(any("unsupported image source list" in gap for gap in gaps))

    def test_responsive_image_url_can_contain_a_comma(self):
        svg = '<svg xmlns="http://www.w3.org/2000/svg"></svg>'
        readme = ('<picture><source srcset="basic.svg 1x, diagram,large.svg 2x">'
                  '<img src="basic.svg" alt="Diagram"></picture>')
        with repository({"README.md": readme, "basic.svg": svg, "diagram,large.svg": svg}) as tree:
            errors, gaps = [], []
            self.assertEqual(check_document(tree, "README.md", errors, gaps), 3)
            self.assertEqual((errors, gaps), ([], []))

    def test_smoke_runs_in_the_selected_monorepo_package(self):
        description = "# Guide\n\nThis guide documents the test fixture.\n"
        with repository({"README.md": description, "packages/demo/README.md": description,
                         "run.py": "print('root marker')",
                         "packages/demo/run.py": "print('package marker')"}) as tree:
            spec = tree.root / "smoke.json"
            receipt = tree.root / "receipt.json"
            argv = [sys.executable, str(ROOT / "tools/check_readme_hq.py"), "--repo", str(tree.root),
                    "--profile", "reference", "--smoke", str(spec), "--receipt", str(receipt)]
            for subproject, marker, expected in (
                ("packages/demo", "root marker", "failed"),
                ("packages/demo", "package marker", "passed"),
                (".", "root marker", "passed"),
            ):
                with self.subTest(subproject=subproject, marker=marker):
                    spec.write_text(json.dumps({"commit": tree.commit, "argv": [sys.executable, "run.py"],
                                                "expected": {"exit": 0, "contains": marker}}), encoding="utf-8")
                    result = subprocess.run([*argv, "--subproject", subproject], capture_output=True)
                    self.assertEqual(result.returncode, int(expected == "failed"), result.stderr)
                    action = json.loads(receipt.read_bytes())["cases"]["first_action"]
                    self.assertEqual((action["result"], action["cwd"]), (expected, subproject))

    def test_smoke_marker_checks_each_stream_independently(self):
        with repository({"README.md": "# Guide"}) as tree:
            spec = tree.root / "smoke.json"
            for marker, stream, observed, result in (
                ("left", "stdout", ["stdout"], "passed"),
                ("right", "stderr", ["stderr"], "passed"),
                ("right", "either", ["stderr"], "passed"),
                ("right", "stdout", ["stderr"], "failed"),
                ("leftright", "either", [], "failed"),
            ):
                with self.subTest(marker=marker, stream=stream):
                    spec.write_text(json.dumps({"commit": tree.commit, "argv": [sys.executable, "-c",
                        "import sys; sys.stdout.write('left'); sys.stderr.write('right')"],
                        "expected": {"exit": 0, "contains": marker, "stream": stream}}), encoding="utf-8")
                    outcome = verify_first_action(tree, spec)
                    self.assertEqual(outcome["result"], result)
                    self.assertEqual(outcome["observed"]["matched_streams"], observed)
                    self.assertEqual(outcome["observed"]["stream_sha256"], {
                        "stdout": sha256(b"left").hexdigest(), "stderr": sha256(b"right").hexdigest()})

    def test_existence_only_smoke_never_opens_the_result(self):
        with repository({"README.md": "# Example"}) as tree:
            spec = tree.root / "smoke.json"
            spec.write_text(json.dumps({
                "commit": tree.commit, "argv": [sys.executable, "-c",
                    "from pathlib import Path; Path('output.txt').touch()"],
                "expected": {"exit": 0, "file": "output.txt", "file_mode": "exists"},
            }), encoding="utf-8")
            real_open = Path.open
            def reject_result_read(path, *args, **kwargs):
                if path.name == "output.txt":
                    raise PermissionError("unreadable result")
                return real_open(path, *args, **kwargs)
            with patch.object(Path, "open", reject_result_read):
                self.assertEqual(verify_first_action(tree, spec)["result"], "passed")

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

    def test_smoke_file_checks_prove_a_change(self):
        with repository({"README.md": "# Example", "existing.txt": "old"}) as tree:
            spec = tree.root / "smoke.json"
            def smoke(code, name, **expected):
                spec.write_text(json.dumps({
                    "commit": tree.commit, "argv": [sys.executable, "-c", code],
                    "expected": {"exit": 0, "file": name, **expected},
                }), encoding="utf-8")
                return verify_first_action(tree, spec)

            self.assertEqual(smoke("pass", "existing.txt")["result"], "failed")
            self.assertEqual(smoke("pass", "existing.txt", file_mode="exists")["result"], "passed")
            for name, mode in (("new.txt", "created"), ("existing.txt", "updated")):
                code = f"from pathlib import Path; Path({name!r}).write_bytes(b'new')"
                outcome = smoke(code, name, file_mode=mode, file_sha256=sha256(b"new").hexdigest())
                self.assertEqual(outcome["result"], "passed")
                self.assertNotEqual(outcome["observed"]["file_before_sha256"], outcome["observed"]["file_after_sha256"])
                self.assertEqual(smoke(code, name, file_sha256="0" * 64)["result"], "failed")

    def test_deleted_draft_still_writes_failure_receipt(self):
        with repository({"README.md": "# Guide\n\nThis repository has a reference guide."}) as tree:
            path = tree.root / "audit.json"
            argv = [sys.executable, str(ROOT / "tools/check_readme_hq.py"), "--repo", str(tree.root),
                    "--profile", "reference", "--draft", "--receipt", str(path)]
            good = subprocess.run(argv, capture_output=True, text=True)
            self.assertEqual(good.returncode, 0, good.stderr)
            self.assertIn("README.md", json.loads(path.read_bytes())["sources"])
            (tree.root / "README.md").unlink()
            failed = subprocess.run(argv, capture_output=True, text=True)
            receipt = json.loads(path.read_bytes())
            self.assertEqual(failed.returncode, 1, failed.stderr)
            self.assertNotIn("Traceback", failed.stderr)
            self.assertEqual(receipt["result"], "failed")
            self.assertEqual(receipt["unavailable_sources"], ["README.md"])
            self.assertTrue(any("README.md" in error for error in receipt["errors"]))

    def test_receipt_identifies_executing_validator_separately_from_target_bytes(self):
        validator = ROOT / "tools/check_readme_hq.py"
        target_path = "tools/check_readme_hq.py"
        for marker in (None, b"unrelated tracked bytes"):
            files = {"README.md": "# Guide\n\nThis repository has a reference guide."}
            if marker is not None:
                files[target_path] = marker
            with repository(files) as tree:
                receipt = tree.root / "audit.json"
                result = subprocess.run([sys.executable, str(validator), "--repo", str(tree.root),
                                         "--profile", "reference", "--receipt", str(receipt)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                audit = json.loads(receipt.read_bytes())
                self.assertEqual(audit["validator"]["sha256"], sha256(validator.read_bytes()).hexdigest())
                self.assertEqual(audit["sources"].get(target_path), sha256(marker).hexdigest() if marker else None)

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

    def test_version_rows_and_current_label_are_bound_to_archives(self):
        tree = GitTree(ROOT)
        changes = [
            ("versions/README.md", "versions/v0.0.5/README.md)", "versions/v0.0.4/README.md)", "approved archive"),
            ("graphify-hq/README.md", "maps/v0.0.5/README.md)", "maps/v0.0.6/README.md)", "landing row"),
        ]
        read = tree.read
        errors = []
        check_versions(errors, tree)
        self.assertEqual(errors, [])
        for changed, old, new, expected in changes:
            def edited(path, commit=None):
                body = read(path, commit)
                return body.replace(old.encode(), new.encode()) if path == changed and commit is None else body
            with patch.object(tree, "read", side_effect=edited):
                errors = []
                check_versions(errors, tree)
                self.assertTrue(any(expected in error for error in errors), errors)

        def rolled_back(path, commit=None):
            body = read(path, commit)
            if path in {"README.md", "versions/README.md"} and commit is None:
                return body.replace(b"v0.0.6/README.md)", b"v0.0.1/README.md)", 1)
            return body
        with patch.object(tree, "read", side_effect=rolled_back):
            errors = []
            check_versions(errors, tree)
            self.assertTrue(any("latest standalone archive" in error for error in errors), errors)

    def test_wrong_registry_shapes_fail_without_a_traceback_and_write_a_receipt(self):
        validator = ROOT / "tools/check_readme_hq.py"
        with tempfile.TemporaryDirectory() as folder:
            worktree = Path(folder) / "checkout"
            subprocess.run(["git", "-C", str(ROOT), "clone", "-q", str(ROOT), str(worktree)], check=True)
            registry = worktree / "techniques/registry.json"
            receipt = Path(folder) / "result.json"
            argv = [sys.executable, str(worktree / validator.relative_to(ROOT)), "--draft", "--receipt", str(receipt)]
            for invalid in ([], None, {"schema": 1, "techniques": [None]}):
                registry.write_text(json.dumps(invalid), encoding="utf-8")
                result = subprocess.run(argv, cwd=worktree, capture_output=True, text=True)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(json.loads(receipt.read_bytes())["result"], "failed")

    def test_registry_and_inventory_cannot_vouch_for_each_other(self):
        paths = ("techniques/registry.json", "techniques/public-source-inventory.json")
        files = {name: (ROOT / name).read_bytes() for name in paths}
        with repository(files) as tree:
            problems = []
            self.assertTrue(check_registry(problems, tree))
            self.assertEqual(problems, [])
            inventory = json.loads(files[paths[1]])
            registry = json.loads(files[paths[0]])
            inventory.append(["example/project", "a" * 40, "README.md", "b" * 40, "c" * 64, 2])
            registry["techniques"][0]["evidence"] = [{
                "status": "observed", "url": "https://github.com/example/project/blob/" + "a" * 40 + "/README.md",
            }]
            modified = {paths[0]: json.dumps(registry), paths[1]: json.dumps(inventory)}
            with repository(modified) as edited:
                with self.assertRaisesRegex(ValueError, "independently reviewed snapshot"):
                    check_registry([], edited)
            for invalid in (inventory + [inventory[-1]], [[42]]):
                with repository({**modified, paths[1]: json.dumps(invalid)}) as edited:
                    with self.assertRaisesRegex(ValueError, "duplicate|requires checked"):
                        check_registry([], edited)

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

    def test_partition_includes_implementation_paths_and_splits_at_inventory_limit(self):
        def feature(number, count):
            paths = [{"path": f"file-{number}-{i}.md", "anchor": "Evidence"} for i in range(count)]
            return {"id": f"checkpoint-{number}", "documented_in": paths[:1],
                    "changed_in": paths[:1], "tested_by": paths[:1], **({"implemented_in": paths[1:]} if count > 1 else {})}

        features = [feature(i, 3) for i in range(21)] + [feature(21, 1)] + [feature(i, 3) for i in range(22, 25)]
        with tempfile.TemporaryDirectory() as folder:
            parts = stage_partitions(features, Path(folder) / "parts", "a" * 40, "example/project")
            manifests = [json.loads(path.read_bytes()) for path in parts]
            self.assertEqual([len(m["source_files"]) for m in manifests], [64, 9])
            self.assertEqual([f for m in manifests for f in m["features"]], features)
            self.assertIn("file-0-2.md", manifests[0]["source_files"])

    def test_learning_receipt_is_pinned_and_idempotent(self):
        spec = importlib.util.spec_from_file_location("intake", ROOT / "learning/intake.py")
        intake = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(intake)
        with repository({"README.md": "# Evidence\\n"}) as tree:
            tree.git("remote", "add", "origin", "https://github.com/example/project.git")
            record = {"id": "example", "checkout": str(tree.root), "ref": "HEAD",
                      "repository": "example/project", "path": "README.md",
                      "line": 1, "anchor": "# Evidence", "visibility": "public"}
            spec = {"visibility": "public", "sources": [record], "selected": ["example"],
                    "target": {**record, "audience": "developer", "capability": "command line"},
                    "findings": [{"source": "example", "technique": "first-success-milestone",
                                  "decision": "adapt", "rationale": "Explain the first result."}]}
            def fetch(route):
                if route == "example/project":
                    return {"private": False, "visibility": "public"}
                return {"sha": tree.commit}
            destination = tree.root / "receipts"
            first = intake.record_intake(spec, destination, fetch=fetch)
            self.assertEqual(first, intake.record_intake(spec, destination, fetch=fetch))
            record["id"] = "alias"
            spec["selected"] = ["alias"]
            spec["findings"][0]["source"] = "alias"
            self.assertEqual(first, intake.record_intake(spec, destination, fetch=fetch))
            result = json.loads(first.read_bytes())
            self.assertEqual(result["recommendations"][0]["target"]["commit"], tree.commit)
            spec["selected"] = []
            second = intake.record_intake(spec, destination, fetch=fetch)
            self.assertNotEqual(first, second)
            self.assertEqual(json.loads(second.read_bytes())["recommendations"], [])

    def test_learning_hashes_the_registry_snapshot_used_by_the_decision(self):
        loader = importlib.util.spec_from_file_location("intake", ROOT / "learning/intake.py")
        intake = importlib.util.module_from_spec(loader)
        loader.loader.exec_module(intake)
        with repository({"README.md": "# Evidence"}) as tree:
            tree.git("remote", "add", "origin", "https://github.com/example/project.git")
            record = {"id": "example", "checkout": str(tree.root), "ref": "HEAD",
                      "repository": "example/project", "path": "README.md",
                      "line": 1, "anchor": "# Evidence", "visibility": "public"}
            request = {"visibility": "public", "sources": [record], "selected": ["example"],
                       "target": {**record, "audience": "reader", "capability": "audit"},
                       "findings": [{"source": "example", "technique": "sample", "decision": "adapt",
                                     "rationale": "Record a source."}]}
            registry = tree.root / "techniques/registry.json"
            registry.parent.mkdir()
            active = b'{"techniques":[{"id":"sample","status":"active"}]}'
            retired = active.replace(b"active", b"retired")
            registry.write_bytes(active)
            read_bytes = Path.read_bytes
            def read_then_retire(path):
                content = read_bytes(path)
                if path == registry:
                    path.write_bytes(retired)
                return content
            def fetch(route):
                if route == "example/project":
                    return {"private": False, "visibility": "public"}
                return {"sha": tree.commit}

            with patch.object(intake, "ROOT", tree.root):
                with patch.object(Path, "read_bytes", read_then_retire):
                    path = intake.record_intake(request, tree.root / "evidence", fetch=fetch)
                result = json.loads(path.read_bytes())
                self.assertEqual(result["registry_sha256"], sha256(active).hexdigest())
                self.assertEqual(len(result["recommendations"]), 1)
                path = intake.record_intake(request, tree.root / "evidence", fetch=fetch)
                result = json.loads(path.read_bytes())
                self.assertEqual(result["registry_sha256"], sha256(retired).hexdigest())
                self.assertEqual(result["recommendations"], [])

    def test_public_learning_refusal_writes_nothing(self):
        spec = importlib.util.spec_from_file_location("intake", ROOT / "learning/intake.py")
        intake = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(intake)
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "receipts"
            with self.assertRaisesRegex(ValueError, "public"):
                intake.record_intake({"visibility": "private", "target": {"id": "private-probe"}}, destination)
            self.assertFalse(destination.exists())
