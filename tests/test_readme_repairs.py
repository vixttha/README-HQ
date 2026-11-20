"""Regression tests for selected-tree navigation and verified reader outcomes."""

import contextlib
from hashlib import sha256
import importlib.util
from io import BytesIO, StringIO
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
from urllib.error import HTTPError
from urllib.parse import urlsplit
from hq_smoke import verify_first_action
from check_readme_hq import check_evidence, check_registry, check_versions, evidence_identity, target_readme
from verify_plan import acceptance_sections, split_checkpoints, stage_partitions, verify


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
    def test_repo_cli_requires_root_and_supports_explicit_subproject(self):
        body = "# Guide\n\nThis guide explains the reference fixture.\n"
        with repository({"README.md": body, "packages/demo/README.md": body}) as tree:
            receipt = tree.root / "audit.json"
            argv = [sys.executable, str(ROOT / "tools/check_readme_hq.py"), "--profile", "reference",
                    "--receipt", str(receipt), "--repo"]
            for path, options, expected in (
                (tree.root, [], "README.md"),
                (tree.root / "packages/demo", [], None),
                (tree.root, ["--subproject", "packages/demo"], "packages/demo/README.md"),
            ):
                with self.subTest(path=path, options=options):
                    result = subprocess.run([*argv, str(path), *options], capture_output=True)
                    record = json.loads(receipt.read_bytes())
                    self.assertEqual(result.returncode, int(expected is None), result.stderr)
                    if expected is None:
                        self.assertIn(b"--repo must name the Git root", result.stderr)
                        self.assertIn(b"--subproject", result.stderr)
                        self.assertIsNone(record["commit"])
                    else:
                        self.assertEqual(record["cases"]["entrypoint"], expected)

    def test_adopter_selectors_require_an_explicit_repository(self):
        argv = [sys.executable, str(ROOT / "tools/check_readme_hq.py")]
        result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("standalone version(s)", result.stdout)
        for options in (["--subproject", "missing"], ["--subproject", "."], ["--profile", "application"],
                        ["--profile", "reference"], ["--allow-network"]):
            with self.subTest(options=options):
                result = subprocess.run([*argv, *options], cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn(f"{options[0]} requires an explicit --repo", result.stderr)

    def test_quickstart_recognizes_usage_rendering_and_nested_sections(self):
        from check_readme_hq import has_first_action
        from hq_navigation import parse_markdown

        command = "\n\n```sh\npython run.py\n```\n"
        fixtures = (
            ("## Usage", True),
            ("## **Quickstart**", True),
            ("## Quickstart\n\n### Install\n\n### Configure", True),
            ("## Quickstart\n\n### Install\n\n## Development", False),
            ("## Development", False),
        )
        for heading, expected in fixtures:
            with self.subTest(heading=heading):
                self.assertEqual(has_first_action(parse_markdown(heading + command)[2]), expected)

    def test_first_action_follows_a_real_quickstart_section(self):
        from check_readme_hq import target_readme

        own = GitTree(ROOT)
        self.assertEqual(target_readme(own, ".", [], [], "application")[0], "README.md")
        errors = []
        target_readme(own, ".", errors, [], "application")
        self.assertEqual(errors, [])
        preamble = "# Demo\n\nThe demo verifies the first useful action.\n\n"
        table = "| A | B |\n| --- | --- |\n" + "| Example | Note |\n" * 45
        for ending, expected in (
            ("## Quickstart\n\n```sh\npython run.py\n```", False),
            ("## Quickstart\n\n[Launch the demo](launch.md)", False),
            ("## Quickstart\n\n[License](LICENSE)\n\n## Development\n\n```sh\npython build.py\n```", True),
        ):
            content = preamble + table + "\n" + ending
            with repository({"README.md": content, "launch.md": "# Launch", "LICENSE": "fixture"}) as tree:
                errors = []
                self.assertEqual(target_readme(tree, ".", errors, [], "application")[0], "README.md")
                self.assertEqual(any("no discoverable first action" in error for error in errors), expected)

    def test_rich_text_navigation_reports_explicit_incomplete_status(self):
        cases = {"rst": "Guide\n=====\n\nSee `start <guide.rst#start>`_ and `lost <gone.rst#missing>`_.\n\n"
                         "Quickstart\n----------\n\n::\n\n    python run.py\n",
                 "adoc": "= Guide\n\nlink:guide.adoc#start[Start] and link:gone.adoc#missing[Lost].\n\n"
                          "== Quickstart\n\n[source,shell]\n----\npython run.py\n----\n"}
        for extension, body in cases.items():
            source = "README." + extension
            with self.subTest(extension=extension), repository({source: body, "guide." + extension: body}) as tree:
                file = tree.root / "receipt.json"
                result = subprocess.run([sys.executable, str(ROOT / "tools/check_readme_hq.py"), "--repo",
                                         str(tree.root), "--receipt", str(file)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, result.stderr)
                receipt = json.loads(file.read_bytes())
                self.assertEqual(receipt["result"], "incomplete")
                self.assertEqual(receipt["cases"]["entrypoint"], source)
                self.assertEqual(receipt["cases"]["navigation"]["result"], "unchecked")
                self.assertEqual(receipt["cases"]["local_links"], 0)
                self.assertTrue(any("navigation, anchors, and first-use" in gap for gap in receipt["unchecked"]))

    def test_adopter_receipt_distinguishes_scope_at_one_commit(self):
        readme = "# Guide\n\nThis is a portable demonstration.\n\n## Quickstart\n\n```sh\npython run.py\n```\n"
        with repository({"README.md": readme, "packages/demo/README.md": readme}) as tree:
            receipt = tree.root / "audit.json"
            argv = [sys.executable, str(ROOT / "tools/check_readme_hq.py"), "--repo", str(tree.root),
                    "--receipt", str(receipt)]
            for origin, profile, subproject in (
                ("example/first", "reference", "."),
                ("example/first", "application", "."),
                ("example/second", "application", "packages/demo"),
            ):
                with self.subTest(origin=origin, profile=profile, subproject=subproject):
                    tree.git("config", "remote.origin.url", f"https://github.com/{origin}.git")
                    result = subprocess.run([*argv, "--profile", profile, "--subproject", subproject],
                                            capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    record = json.loads(receipt.read_bytes())
                    self.assertEqual(record["scope"], {"repository": origin,
                        "repository_identity": "inferred-from-origin", "profile": profile,
                        "subproject": subproject, "commit": tree.commit})

    def test_receipt_distinguishes_actions_attempts_jobs_and_standalone(self):
        from hq_smoke import write_receipt

        with repository({"README.md": "# Guide"}) as tree:
            receipt = tree.root / "audit.json"
            env = {"GITHUB_ACTIONS": "true", "GITHUB_REPOSITORY": "example/project",
                   "GITHUB_RUN_ID": "23", "RUNNER_OS": "Linux"}
            for attempt, job in (("1", "linux"), ("2", "linux"), ("2", "verification")):
                with patch.dict(os.environ, {**env, "GITHUB_RUN_ATTEMPT": attempt, "GITHUB_JOB": job}):
                    write_receipt(receipt, tree, {}, [], [])
                result = json.loads(receipt.read_bytes())
                self.assertEqual(result["github_actions"], {
                    "status": "provided-by-runner", "run_id": "23", "attempt": attempt,
                    "attempt_url": f"https://github.com/example/project/actions/runs/23/attempts/{attempt}",
                    "job": job, "runner_os": "Linux"})
            with patch.dict(os.environ, {"GITHUB_ACTIONS": "false"}):
                write_receipt(receipt, tree, {}, [], [])
            result = json.loads(receipt.read_bytes())
            self.assertIsNone(result["run_url"])
            self.assertEqual(result["github_actions"]["status"], "unavailable")
            self.assertIsNone(result["github_actions"]["job"])

    def test_partial_clone_blob_fetch_requires_explicit_permission(self):
        with repository({"README.md": "# Partial clone fixture\n\nThis guide explains the partial clone fixture."}) as source, tempfile.TemporaryDirectory() as folder:
            source.git("config", "uploadpack.allowFilter", "true")
            source.git("config", "uploadpack.allowAnySHA1InWant", "true")
            clone = Path(folder) / "clone"
            subprocess.run(["git", "clone", "--quiet", "--no-checkout", "--filter=blob:none",
                            source.root.as_uri(), str(clone)], check=True)
            tree = GitTree(clone)
            blob = tree.entries()["README.md"][1]
            receipt = Path(folder) / "audit.json"
            argv = [sys.executable, str(ROOT / "tools/check_readme_hq.py"), "--repo", str(clone),
                    "--profile", "reference", "--receipt", str(receipt)]
            offline = subprocess.run(argv, capture_output=True, text=True)
            self.assertEqual(offline.returncode, 1)
            self.assertIn("unavailable with Git fetching disabled", offline.stderr)
            with self.assertRaises(ValueError):
                tree.git("cat-file", "-e", blob)
            record = json.loads(receipt.read_bytes())
            self.assertEqual(record["git_objects"], {"fetch_policy": "offline", "fetched_blobs": []})
            for extra, mode, fetched in ((["--allow-git-fetch"], "allow", [blob]), ([], "offline", [])):
                result = subprocess.run([*argv, *extra], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                record = json.loads(receipt.read_bytes())
                self.assertEqual(record["git_objects"], {"fetch_policy": mode, "fetched_blobs": fetched})
            self.assertEqual(source.read("README.md"), tree.read("README.md"))

    def test_draft_rejects_symlink_ancestors_inside_and_outside_checkout(self):
        documents = {"README.md": "[Guide](docs/guide.md#draft)",
                     "docs/guide.md": "# Original", "other/guide.md": "# Draft"}
        with repository(documents) as tree, tempfile.TemporaryDirectory() as outside:
            docs = tree.root / "docs"
            (docs / "guide.md").write_text("# Draft", encoding="utf-8")
            draft = GitTree(tree.root, draft=True)
            self.assertEqual(check_document(draft, "README.md", [], []), 1)
            docs.rename(tree.root / "original-docs")
            external = Path(outside)
            (external / "guide.md").write_text("# Draft", encoding="utf-8")
            for target in (tree.root / "other", external):
                with self.subTest(target=target):
                    try:
                        docs.symlink_to(target, target_is_directory=True)
                    except OSError:
                        if os.name != "nt":
                            raise
                        subprocess.run(["cmd", "/c", "mklink", "/J", str(docs), str(target)],
                                       check=True, capture_output=True)
                    try:
                        errors = []
                        self.assertEqual(check_document(draft, "README.md", errors, []), 0)
                        self.assertEqual(len(errors), 1)
                        self.assertIn("symlink or reparse point", errors[0])
                    finally:
                        if docs.is_symlink():
                            docs.unlink()
                        else:
                            docs.rmdir()

    def test_public_reader_workflow_preserves_the_validator_exit(self):
        config = (ROOT / ".github/workflows/readme-hq.yml").read_text(encoding="utf-8")
        self.assertIn("\n        run: python tools/check_readme_hq.py --receipt readme-hq-result.json\n"
                      "      - name: Run reader regressions\n"
                      "        run: python -m unittest discover", config)
        self.assertIn("      - name: Preserve the exact-SHA receipt\n        if: always()", config)

    def test_receipt_persistence_failure_preserves_audit_diagnostics(self):
        for good in (True, False):
            target = "README.md" if good else "missing.md"
            with self.subTest(good=good), repository({"README.md": f"# Guide\n\nThis guide explains the receipt persistence fixture.\n\n[Link]({target})\n"}) as tree:
                argv = [sys.executable, str(ROOT / "tools/check_readme_hq.py"), "--repo", str(tree.root),
                        "--profile", "reference", "--receipt"]
                result = subprocess.run([*argv, str(tree.root)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertIn("could not write receipt", result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual("missing tracked local target" in result.stderr, not good)
                receipt = tree.root / "audit.json"
                control = subprocess.run([*argv, str(receipt)], capture_output=True, text=True)
                self.assertEqual(control.returncode, int(not good), control.stderr)
                record = json.loads(receipt.read_bytes())
                self.assertEqual(record["result"], "passed" if good else "failed")

    def test_review_followup_partial_clone_smoke_and_missing_link_diagnostics(self):
        description = "# Guide\n\nThis guide explains the source fixture.\n\n[Guide](extra.md#details)"
        files = {"README.md": description, "extra.md": "# Details", "run.py": "print('ready')"}
        with repository(files) as source, tempfile.TemporaryDirectory() as folder:
            source.git("config", "uploadpack.allowFilter", "true")
            source.git("config", "uploadpack.allowAnySHA1InWant", "true")
            clone = Path(folder) / "clone"
            subprocess.run(["git", "clone", "--quiet", "--no-checkout", "--filter=blob:none",
                            source.root.as_uri(), str(clone)], check=True)
            tree = GitTree(clone, allow_git_fetch=True)
            tree.read("README.md")
            runner_blob = tree.entries()["run.py"][1]
            with self.assertRaises(ValueError):
                tree.git("cat-file", "-e", runner_blob)
            tree.git("remote", "set-url", "origin", str(Path(folder) / "missing"))
            errors, gaps = [], []
            self.assertEqual(check_document(tree, "README.md", errors, gaps), 0)
            self.assertEqual(gaps, [])
            self.assertIn("unavailable after permitted Git read", errors[0])
            tree.git("remote", "set-url", "origin", source.root.as_uri())
            spec = Path(folder) / "smoke.json"
            spec.write_text(json.dumps({"commit": tree.commit, "argv": [sys.executable, "run.py"],
                                        "expected": {"exit": 0, "contains": "ready"}}), encoding="utf-8")
            with patch.dict(os.environ, {"GIT_NO_LAZY_FETCH": "1"}):
                self.assertEqual(verify_first_action(tree, spec)["result"], "passed")
            self.assertIn(runner_blob, tree.fetched_blobs)

    def test_review_followup_raw_ref_namespace_is_explicit(self):
        with repository({"guide.md": "# First"}) as tree:
            repository_url = "https://github.com/example/project.git"
            tree.git("remote", "add", "origin", repository_url)
            tree.git("tag", "release", tree.commit)
            tree.git("-c", "user.name=Fixture", "-c", "user.email=test@example.invalid",
                     "commit", "--allow-empty", "-qm", "Branch release")
            other = GitTree(tree.root)
            tree.git("update-ref", "refs/remotes/origin/release", other.commit)
            root = "https://raw.githubusercontent.com/example/project"
            for ref, expected in (("refs/tags/release", tree.commit), ("refs/heads/release", other.commit)):
                self.assertEqual(same_repo_target(other, urlsplit(f"{root}/{ref}/guide.md")),
                                 ("guide.md", expected))
            with self.assertRaisesRegex(ValueError, "conflicting commits"):
                same_repo_target(other, urlsplit(f"{root}/release/guide.md"))

    def test_review_followup_rendered_rows_normalize_line_endings(self):
        from hq_navigation import rendered_table_rows

        for newline in ("\n", "\r\n", "\r"):
            content = newline.join(["| Name |", "| --- |", "| Value |", ""])
            self.assertEqual(rendered_table_rows(content), ["| Name |", "| Value |"])

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

    def test_bare_gfm_urls_report_gaps_without_including_code_or_punctuation(self):
        body = ("# Links\n\n"
                "See https://example.test/a_(part).\n"
                "Also (www.example.test/start), plus [https://example.test](README.md).\n\n"
                "`https://example.test/inline`\n\n"
                "```text\nwww.example.test/fenced\n```\n")
        with repository({"README.md": body}) as tree:
            errors, gaps = [], []
            self.assertEqual(check_document(tree, "README.md", errors, gaps), 1)
            self.assertEqual(errors, [])
            self.assertEqual(gaps, [
                "README.md:3: bare GFM URL was not checked: https://example.test/a_(part)",
                "README.md:4: bare GFM URL was not checked: www.example.test/start",
            ])

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

    def test_plain_query_parameters_allow_order_independent_line_links(self):
        with repository({"guide.md": "# Heading\nsecond line\n", "README.md": "# Links"}) as tree:
            tree.git("remote", "add", "origin", "https://github.com/example/project.git")
            route = f"https://github.com/example/project/blob/{tree.commit}/guide.md"
            queries = ("plain=1", "plain=1&ref_type=heads", "ref_type=heads&plain=1", "plain=true")
            readme = "\n".join(f"[Line]({route}?{query}#L2)" for query in queries)
            readme += f"\n[Out of bounds]({route}?ignored=1&plain=1#L99)\n"
            (tree.root / "README.md").write_text(readme, encoding="utf-8")
            errors, gaps = [], []
            self.assertEqual(check_document(GitTree(tree.root, draft=True), "README.md", errors, gaps), 4)
            self.assertEqual(gaps, [])
            self.assertEqual(len(errors), 1)
            self.assertIn("outside the file", errors[0])

    def test_pinned_fragment_cache_reuses_objects_without_stale_drafts(self):
        import hq_navigation

        readme = "[Start](guide.md#start)\n" * 64 + "[Missing](guide.md#missing)\n"
        with repository({"README.md": readme, "guide.md": "# Start"}) as tree:
            errors = []
            with (patch.object(tree, "read", wraps=tree.read) as read,
                  patch.object(hq_navigation, "parse_markdown", wraps=hq_navigation.parse_markdown) as parse):
                self.assertEqual(check_document(tree, "README.md", errors, []), 64)
                self.assertEqual(sum(call.args[0] == "guide.md" for call in read.call_args_list), 1)
                self.assertEqual(parse.call_count, 2)
            self.assertEqual(len(errors), 1)
            self.assertIn("missing local heading", errors[0])
            path = tree.root / "guide.md"
            old = tree.commit
            path.write_text("# Other", encoding="utf-8")
            draft = GitTree(tree.root, draft=True)
            self.assertEqual(check_document(draft, "README.md", [], []), 0)
            path.write_text("# Start", encoding="utf-8")
            self.assertEqual(check_document(draft, "README.md", [], []), 64)
            path.write_text("# Other", encoding="utf-8")
            tree.git("add", "guide.md")
            tree.git("-c", "user.name=Fixture", "-c", "user.email=test@example.invalid",
                     "commit", "--quiet", "-m", "Change anchor")
            current = GitTree(tree.root)
            cache = {}
            hq_navigation.check_fragment(current, "guide.md", old, "start", cache=cache)
            with self.assertRaisesRegex(ValueError, "missing local heading"):
                hq_navigation.check_fragment(current, "guide.md", current.commit, "start", cache=cache)

    def test_raw_github_files_do_not_verify_rendered_heading_fragments(self):
        with repository({"guide.md": "# Heading\n", "README.md": "# Links"}) as tree:
            tree.git("remote", "add", "origin", "https://github.com/example/project.git")
            github = "https://github.com/example/project"
            raw = "https://raw.githubusercontent.com/example/project"
            routes = (f"{github}/raw/{tree.commit}/guide.md#heading",
                      f"{raw}/{tree.commit}/guide.md#heading",
                      f"{github}/blob/{tree.commit}/guide.md#heading",
                      f"{raw}/{tree.commit}/guide.md",
                      f"{raw}/{tree.commit}/missing.md#heading")
            readme = "\n".join(f"[File]({route})" for route in routes)
            (tree.root / "README.md").write_text(readme, encoding="utf-8")
            errors, gaps = [], []
            self.assertEqual(check_document(GitTree(tree.root, draft=True), "README.md", errors, gaps), 4)
            self.assertEqual(len(gaps), 2)
            self.assertTrue(all("raw GitHub file fragment was not checked" in gap for gap in gaps))
            self.assertEqual(len(errors), 1)
            self.assertIn("missing tracked local target", errors[0])

    def test_public_refs_ignore_local_aliases_and_use_the_remote_default(self):
        with repository({"README.md": "# Default"}) as original:
            original.git("remote", "add", "origin", "https://github.com/example/project.git")
            original.git("update-ref", "refs/remotes/origin/main", original.commit)
            original.git("update-ref", "refs/remotes/origin/release/next", original.commit)
            original.git("switch", "-c", "topic")
            original.git("-c", "user.name=Fixture", "-c", "user.email=test@example.invalid",
                         "commit", "--allow-empty", "-qm", "Topic revision")
            topic = GitTree(original.root)
            self.assertNotEqual(topic.commit, original.commit)

            def resolve(ref):
                return same_repo_target(topic, urlsplit(f"https://github.com/example/project/blob/{ref}/README.md"))

            for ref in ("origin/main", "topic", "HEAD"):
                with self.assertRaisesRegex(LookupError, "unresolved"):
                    resolve(ref)
            original.git("symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
            self.assertEqual(resolve("HEAD"), ("README.md", original.commit))
            self.assertEqual(resolve("release/next"), ("README.md", original.commit))
            original.git("update-ref", "refs/remotes/origin/origin/main", topic.commit)
            self.assertEqual(resolve("origin/main"), ("README.md", topic.commit))

    def test_html_image_alt_distinguishes_missing_and_explicit_empty(self):
        image = '<svg xmlns="http://www.w3.org/2000/svg"/>'
        fields = ("", ' alt=""', ' alt="A schematic"')
        for attributes in fields:
            doc = f'<img src="diagram.svg"{attributes}>'
            with self.subTest(attributes=attributes), repository({"README.md": doc, "diagram.svg": image}) as tree:
                errors, gaps = [], []
                self.assertEqual(check_document(tree, "README.md", errors, gaps), 1)
                self.assertTrue(any("requires an alt attribute" in error for error in errors) if not attributes else not errors)
                self.assertEqual(gaps, [])

    def test_html_image_accepts_nonblank_aria_label(self):
        image = '<svg xmlns="http://www.w3.org/2000/svg"/>'
        cases = (
            ('<img src="diagram.svg" aria-label="A schematic">', 1, False),
            ('<img src="diagram.svg" aria-label=" ">', 1, True),
            ('<a href="./guide.md"><img src="diagram.svg" aria-label="Open the guide"></a>', 2, False),
        )
        for readme, checked, missing in cases:
            with self.subTest(readme=readme), repository({"README.md": readme, "diagram.svg": image,
                                                        "guide.md": "# Guide"}) as tree:
                errors, gaps = [], []
                self.assertEqual(check_document(tree, "README.md", errors, gaps), checked)
                self.assertEqual(len(errors), int(missing), errors)
                if missing:
                    self.assertIn("requires an alt attribute", errors[0])
                self.assertEqual(gaps, [])

    def test_html_srcset_link_uses_image_name(self):
        image = '<svg xmlns="http://www.w3.org/2000/svg"/>'
        for attrs, named in (('aria-label="Open the guide"', True), ('alt="Open the guide"', True),
                             ('alt="" aria-label=" "', False)):
            readme = f'<a href="./guide.md"><img srcset="diagram.svg 1x" {attrs}></a>'
            with self.subTest(attrs=attrs), repository({"README.md": readme, "diagram.svg": image,
                                                       "guide.md": "# Guide"}) as tree:
                errors, gaps = [], []
                self.assertEqual(check_document(tree, "README.md", errors, gaps), 2 if named else 1)
                self.assertEqual(gaps, [])
                if named:
                    self.assertEqual(errors, [])
                else:
                    self.assertEqual(len(errors), 1)
                    self.assertIn("link has no accessible name", errors[0])

    def test_readme_html_hidden_image_does_not_name_link(self):
        from hq_navigation import parse_markdown

        for attrs, unnamed in (('aria-hidden="true"', True), ('hidden', True),
                               ('aria-hidden="false"', False), ('', False)):
            text = f'<a href="guide.md"><img srcset="diagram.svg 1x" alt="Guide" {attrs}></a>'
            with self.subTest(attrs=attrs):
                _, links, _ = parse_markdown(text)
                self.assertEqual([(link.path, link.unnamed) for link in links],
                                 [("diagram.svg", False), ("guide.md", unnamed)])

    def test_readme_html_hidden_ancestors_do_not_name_links(self):
        from hq_navigation import parse_markdown

        image = '<img srcset="diagram.svg 1x" alt="Guide">'
        invisible = f'<span aria-hidden="true"><span aria-hidden="false">{image}</span>Hidden</span>'
        cases = (
            (f'<a href="guide.md">{invisible}</a>', [True]),
            (f'<a href="guide.md">{invisible}<br hidden>Visit the guide</a>', [False]),
            (f'<div hidden><a href="guide.md">{image}</a></div><a href="guide.md">{image}</a>', [False, False]),
        )
        for markup, expected in cases:
            for document in (markup, f"See {markup} for details."):
                with self.subTest(document=document):
                    _, links, _ = parse_markdown(document)
                    self.assertEqual([link.unnamed for link in links if not link.image], expected)
                    self.assertEqual(sum(link.image for link in links), len(expected))

    def test_svg_root_requires_the_svg_namespace(self):
        default = '<svg xmlns="http://www.w3.org/2000/svg"/>'
        prefixed = '<s:svg xmlns:s="http://www.w3.org/2000/svg"/>'
        invalid = {"foreign.svg": '<svg xmlns="urn:other"/>', "bare.svg": "<svg/>",
                   "broken.svg": '<svg xmlns="http://www.w3.org/2000/svg">'}
        images = {"default.svg": default, "prefixed.svg": prefixed, **invalid}
        readme = "\n".join(f"![Diagram]({name})" for name in images)
        with repository({"README.md": readme, **images}) as tree:
            errors, gaps = [], []
            self.assertEqual(check_document(tree, "README.md", errors, gaps), 2)
            self.assertEqual(gaps, [])
            self.assertEqual(len(errors), 3)
            self.assertTrue(all("SVG namespace" in error for error in errors[:2]))
            self.assertIn("invalid SVG image", errors[2])

    def test_animated_media_decodes_later_frames_and_bounds_coverage(self):
        from PIL import Image
        from hq_navigation import verify_media

        red = Image.new("RGB", (32, 32), "red")
        blue = Image.new("RGB", (32, 32), "blue")
        animated, static = BytesIO(), BytesIO()
        red.save(animated, format="GIF", save_all=True, append_images=[blue], duration=50)
        red.save(static, format="PNG")
        data = animated.getvalue()
        verify_media("good.gif", data)
        verify_media("still.png", static.getvalue())
        damaged = data[:-20] + b";"
        with Image.open(BytesIO(damaged)) as first:
            first.load()
        with self.assertRaisesRegex(ValueError, "invalid or unreadable image"):
            verify_media("bad.gif", damaged)
        with self.assertRaisesRegex(ValueError, "GIF trailer missing"):
            verify_media("truncated.gif", data[:-1])
        with patch("hq_navigation.MAX_MEDIA_FRAMES", 1):
            with self.assertRaisesRegex(LookupError, "frame or decoded pixel limit"):
                verify_media("limited.gif", data)

    def test_animated_media_reports_truncated_frame_descriptor_in_receipt(self):
        from PIL import Image

        still = BytesIO()
        Image.new("RGB", (8, 8), "red").save(still, format="GIF")
        broken = still.getvalue()[:-1] + b",\x00\x00;"
        readme = "# Images\n\n![Example](broken.gif)\n\n[Guide](guide.md)\n"
        with repository({"README.md": readme, "broken.gif": broken, "guide.md": "# Guide\n"}) as tree:
            receipt = tree.root / "audit.json"
            result = subprocess.run([sys.executable, str(ROOT / "tools/check_readme_hq.py"),
                                     "--repo", str(tree.root), "--profile", "reference",
                                     "--receipt", str(receipt)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            diagnostic = "README.md:3: invalid or unreadable image: broken.gif"
            self.assertIn(diagnostic, result.stderr)
            record = json.loads(receipt.read_bytes())
            self.assertEqual(record["result"], "failed")
            self.assertIn(diagnostic, record["errors"])
            self.assertEqual(record["cases"]["local_links"], 1)

    def test_bad_image_and_unnamed_image_link_are_separate(self):
        readme = "# Images\n[![](broken.png)](README.md)\n[Another dead link](absent.md)\n"
        with repository({"README.md": readme, "broken.png": b"not a PNG"}) as tree:
            errors = []
            check_document(tree, "README.md", errors, [])
            self.assertEqual(len(errors), 3)
            self.assertTrue(any("accessible name" in issue for issue in errors))
            self.assertTrue(any("unreadable image" in issue for issue in errors))
            self.assertTrue(any("absent.md" in issue for issue in errors))

    def test_lfs_media_distinguishes_unavailable_invalid_and_verified(self):
        svg = b'<svg xmlns="http://www.w3.org/2000/svg"/>'
        oid = sha256(svg).hexdigest()
        pointer = f"version https://git-lfs.github.com/spec/v1\noid sha256:{oid}\nsize {len(svg)}\n"
        with repository({"README.md": "![Diagram](diagram.svg)\n![Broken](broken.svg)",
                         "diagram.svg": pointer, "broken.svg": pointer.replace(oid, "bad")}) as tree:
            def audit():
                errors, gaps = [], []
                return check_document(tree, "README.md", errors, gaps), errors, gaps

            count, errors, gaps = audit()
            self.assertEqual(count, 0)
            self.assertIn("malformed Git LFS media pointer", errors[0])
            self.assertIn("unavailable in the local cache", gaps[0])
            cache = tree.root / ".git/lfs/objects" / oid[:2] / oid[2:4] / oid
            cache.parent.mkdir(parents=True)
            cache.write_bytes(b"x" * len(svg))
            count, errors, gaps = audit()
            self.assertEqual((count, gaps), (0, []))
            self.assertTrue(any("does not match the pointer" in error for error in errors))
            cache.write_bytes(svg)
            count, errors, gaps = audit()
            self.assertEqual((count, len(errors), gaps), (1, 1, []))

    def test_lfs_rejects_malformed_extensions_and_reports_valid_ones(self):
        lines = "version https://git-lfs.github.com/spec/v1\n"
        fields = "oid sha256:" + "a" * 64 + "\nsize 128\n"
        extension = "ext-0-foo sha256:" + "b" * 64 + "\n"
        with repository({"README.md": "![Valid](valid.svg)\n![Invalid](invalid.svg)",
                         "valid.svg": lines + extension + fields,
                         "invalid.svg": lines + extension + extension + fields}) as tree:
            errors, gaps = [], []
            self.assertEqual(check_document(tree, "README.md", errors, gaps), 0)
            self.assertEqual(len(errors), 1)
            self.assertIn("malformed Git LFS media pointer", errors[0])
            self.assertEqual(len(gaps), 1)
            self.assertIn("Git LFS pointer extensions were not inspected", gaps[0])

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

    def test_documented_first_action_example_produces_pinned_receipts(self):
        guide = (ROOT / "README-GUIDE.md").read_text(encoding="utf-8")
        self.assertIn("python examples/first_action_demo.py first-action-evidence", guide)
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / "first-action-evidence"
            result = subprocess.run([sys.executable, str(ROOT / "examples/first_action_demo.py"), str(destination)],
                                    cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            receipts = [json.loads((destination / (name + ".json")).read_bytes())
                        for name in ("passing", "failing", "url-unchecked")]
            self.assertEqual(len({item["commit"] for item in receipts}), 1)
            self.assertEqual([item["cases"]["first_action"]["result"] for item in receipts],
                             ["passed", "failed", "unchecked"])
            self.assertEqual(receipts[0]["cases"]["first_action"]["cwd"], "packages/demo")

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

    def test_smoke_checkout_keeps_git_metadata_and_files_isolated(self):
        readme = "# Original"
        with repository({"README.md": readme}) as tree:
            tree.git("config", "readme-hq.fixture", "original")
            before = tree.git("show-ref")
            command = (
                "import pathlib, subprocess; "
                "subprocess.run(['git', 'config', 'readme-hq.fixture', 'changed'], check=True); "
                "subprocess.run(['git', 'branch', 'smoke-fixture'], check=True); "
                "pathlib.Path('README.md').write_text('changed'); print('ready')"
            )
            spec = tree.root / "smoke.json"
            spec.write_text(json.dumps({"commit": tree.commit, "argv": [sys.executable, "-c", command],
                                        "expected": {"exit": 0, "contains": "ready"}}), encoding="utf-8")
            self.assertEqual(verify_first_action(tree, spec)["result"], "passed")
            self.assertEqual(tree.git("config", "readme-hq.fixture").strip(), b"original")
            self.assertEqual(tree.git("show-ref"), before)
            self.assertEqual((tree.root / "README.md").read_text(encoding="utf-8"), readme)

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

    def test_required_smoke_distinguishes_pass_failure_and_incomplete_coverage(self):
        from check_readme_hq import main

        readme = ("# Guide\n\nThis is the first action fixture.\n\n## Quickstart\n\n"
                  "[Open demo](https://example.invalid/first-action)\n\n"
                  "```sh\npython -c \"print('ready')\"\n```")
        with repository({"README.md": readme}) as tree:
            receipt, spec = tree.root / "receipt.json", tree.root / "spec.json"
            url = "https://example.invalid/first-action"
            remote = {"commit": tree.commit, "url": url, "expected": {"http_status": 200}}
            local = {"commit": tree.commit, "argv": [sys.executable, "-c", "print('ready')"],
                     "expected": {"exit": 0, "contains": "ready"}}
            for values, observed, allow, exit_code, result in (
                (remote, None, False, 2, "unchecked"),
                (remote, HTTPError(url, 403, "gated", {}, BytesIO()), True, 2, "gated"),
                (remote, OSError("not reachable"), True, 2, "unresolved"),
                (remote, HTTPError(url, 404, "missing", {}, BytesIO()), True, 1, "failed"),
                (local, None, False, 0, "passed"),
            ):
                with self.subTest(result=result):
                    spec.write_text(json.dumps(values), encoding="utf-8")
                    argv = ["check", "--repo", str(tree.root), "--profile", "reference", "--smoke", str(spec),
                            "--require-smoke", "--receipt", str(receipt)]
                    if allow:
                        argv.append("--allow-network")
                    with (patch.object(sys, "argv", argv), patch("hq_smoke.urlopen", side_effect=observed) as request,
                          contextlib.redirect_stdout(StringIO()), contextlib.redirect_stderr(StringIO())):
                        self.assertEqual(main(), exit_code)
                        self.assertEqual(request.call_count, int(allow))
                    data = json.loads(receipt.read_bytes())
                    self.assertTrue(data["cases"]["first_action"]["required"])
                    self.assertEqual(data["cases"]["first_action"]["result"], result)
                    self.assertEqual(data["result"], {0: "passed", 1: "failed", 2: "incomplete"}[exit_code])

    def test_required_smoke_needs_a_matching_documented_action(self):
        from check_readme_hq import main

        readme = "# Demo\n\nA meaningful description of the demo.\n\n## Quickstart\n\n```sh\npython demo.py\n```"
        for actual_script, requested, expected in (
            ("raise SystemExit(1)", "other.py", 2),
            ("raise SystemExit(1)", "demo.py", 1),
            ("print('ready')", "demo.py", 0),
        ):
            files = {"README.md": readme, "demo.py": actual_script, "other.py": "print('ready')"}
            with self.subTest(requested=requested, expected=expected), repository(files) as tree:
                spec, receipt = tree.root / "smoke.json", tree.root / "receipt.json"
                spec.write_text(json.dumps({"commit": tree.commit, "argv": [sys.executable, requested],
                                            "expected": {"exit": 0, "contains": "ready"}}), encoding="utf-8")
                argv = ["check", "--repo", str(tree.root), "--smoke", str(spec),
                        "--require-smoke", "--receipt", str(receipt)]
                with (patch.object(sys, "argv", argv), contextlib.redirect_stdout(StringIO()),
                      contextlib.redirect_stderr(StringIO())):
                    self.assertEqual(main(), expected)
                binding = json.loads(receipt.read_bytes())["cases"]["first_action"]["documentation"]
                if expected == 2:
                    self.assertEqual(binding, {"status": "supplemental"})
                else:
                    self.assertEqual(binding, {"status": "matched", "path": "README.md", "line": 8})

    def test_smoke_failure_codes_and_private_output_distinguish_same_exit(self):
        with repository({"README.md": "# Guide"}) as tree:
            spec = tree.root / "smoke.json"
            messages = ("network unavailable", "unsupported format")
            digests = []
            for message in messages:
                action = {"commit": tree.commit,
                          "argv": [sys.executable, "-c",
                                   f"import sys; sys.stderr.write({message!r} + 'z' * 600); sys.exit(7)"],
                          "expected": {"exit": 0, "contains": "ready", "file": "result.txt"}}
                spec.write_text(json.dumps(action), encoding="utf-8")
                result = verify_first_action(tree, spec)
                self.assertEqual(result["failure_codes"], ["exit-mismatch", "output-marker-mismatch",
                                                           "expected-file-missing"])
                self.assertNotIn("private_output", result)
                digests.append(result["observed"]["stream_sha256"]["stderr"])
                private = verify_first_action(tree, spec, include_output=True)["private_output"]["stderr"]
                self.assertTrue(private["text"].startswith(message))
                self.assertEqual(len(private["text"]), 512)
                self.assertTrue(private["truncated"])
            self.assertNotEqual(*digests)

    def test_smoke_spec_modes_are_validated_before_execution(self):
        with repository({"README.md": "# Example"}) as tree:
            spec = tree.root / "smoke.json"
            base = {"commit": tree.commit}
            argv = [sys.executable, "-c", "print('ready')"]
            url = "https://example.invalid/start"

            def run(values, *, online=False):
                spec.write_text(json.dumps({**base, **values}), encoding="utf-8")
                return verify_first_action(tree, spec, allow_network=online)

            local = {"argv": argv, "expected": {"exit": 0, "contains": "ready"}}
            remote = {"url": url, "expected": {"http_status": 200, "contains": "ready"}}
            self.assertEqual(run(local)["result"], "passed")
            self.assertEqual(run(remote)["result"], "unchecked")
            with patch("hq_smoke.urlopen", return_value=HTTPError(url, 200, "fixture", {}, BytesIO(b"ready"))):
                self.assertEqual(run(remote, online=True)["result"], "passed")
            invalid = (
                ({**local, "url": url}, "exactly one"),
                ({"expected": local["expected"]}, "exactly one"),
                ({**remote, "expected": {"http_status": 200, "contains": 1}}, "expected.contains"),
                ({**local, "expected": {"exit": 0, "file": "ready", "contains": 1}}, "expected.contains"),
                ({**remote, "expected": {"http_status": 200, "file": "ready"}}, "local action"),
                ({**local, "expected": {"exit": 0, "contains": "ready", "final_url": url}}, "URL action"),
            )
            with patch("hq_smoke.urlopen") as network, patch("hq_smoke.TemporaryDirectory") as execution:
                for values, message in invalid:
                    with self.subTest(values=values), self.assertRaisesRegex(ValueError, message):
                        run(values)
                network.assert_not_called()
                execution.assert_not_called()

    def test_http_smoke_checks_expected_error_bodies_and_preserves_auth_gates(self):
        with repository({"README.md": "# Guide"}) as tree:
            spec = tree.root / "smoke.json"
            url = "https://example.invalid/guide"
            for status, body, result in (
                (404, b"expected marker", "passed"),
                (404, b"different text", "failed"),
                (200, b"expected marker", "passed"),
                (401, b"expected marker", "gated"),
                (403, b"expected marker", "gated"),
                (429, b"expected marker", "gated"),
            ):
                with self.subTest(status=status, body=body):
                    spec.write_text(json.dumps({"commit": tree.commit, "url": url, "expected": {
                        "http_status": status, "contains": "expected marker"}}), encoding="utf-8")
                    content = BytesIO(body)
                    response = HTTPError(url, status, "fixture", {}, content)
                    with patch("hq_smoke.urlopen", **(
                        {"side_effect": response} if status != 200 else {"return_value": response}
                    )), patch.object(content, "read", wraps=content.read) as read:
                        outcome = verify_first_action(tree, spec, allow_network=True)
                        self.assertEqual(outcome["result"], result)
                        if result == "gated":
                            read.assert_not_called()
                        else:
                            read.assert_called_once_with(1_000_000)
                    self.assertTrue(content.closed)

    def test_http_smoke_records_and_can_require_the_effective_url(self):
        with repository({"README.md": "# Guide"}) as tree:
            spec = tree.root / "smoke.json"
            url = "https://example.invalid/guide"
            final = "https://example.invalid/start"
            for landing, expected, result in (
                (final, final, "passed"),
                ("https://example.invalid/unrelated", final, "failed"),
                (url, url, "passed"),
                (final, None, "passed"),
            ):
                with self.subTest(landing=landing, expected=expected):
                    requirements = {"http_status": 200, "contains": "ready"}
                    if expected is not None:
                        requirements["final_url"] = expected
                    spec.write_text(json.dumps({"commit": tree.commit, "url": url, "expected": requirements}),
                                    encoding="utf-8")
                    response = HTTPError(landing, 200, "fixture", {}, BytesIO(b"ready"))
                    with patch("hq_smoke.urlopen", return_value=response) as request:
                        self.assertEqual(verify_first_action(tree, spec)["result"], "unchecked")
                        request.assert_not_called()
                        outcome = verify_first_action(tree, spec, allow_network=True)
                    self.assertEqual(outcome["result"], result)
                    self.assertEqual(outcome["url"], url)
                    self.assertEqual(outcome["observed"]["final_url"], landing)
                    self.assertIs(outcome["observed"]["final_url_match"], None if expected is None else landing == expected)

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
    def test_documented_review_receipt_passes_and_raw_or_incomplete_receipts_fail(self):
        guide = (ROOT / "techniques/README.md").read_text(encoding="utf-8")
        example = json.loads(guide.split("```json\n", 1)[1].split("```", 1)[0])
        key = (example["source_repository"], example["source_commit"], example["source_path"])
        inventory = {key: ("unused-in-this-test", sha256(b"# Guide\n").hexdigest(), 1)}
        path = "evidence/public/sample.json"
        item = {"url": f"https://github.com/{key[0]}/blob/{key[1]}/{key[2]}#L1",
                "status": "verified", "receipt": path}
        incomplete = {key: value for key, value in example.items() if key != "run_url"}
        raw = {"schema": 1, "commit": key[1], "result": "passed", "cases": {}, "sources": {}}
        for record in (example, incomplete, raw):
            with self.subTest(fields=sorted(record)), repository({path: json.dumps(record)}) as tree:
                if record is example:
                    self.assertEqual(check_evidence(item, tree, inventory), key)
                else:
                    with self.assertRaisesRegex(ValueError, "does not establish"):
                        check_evidence(item, tree, inventory)

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

    def test_rendered_tables_ignore_fenced_rows_and_reject_missing_navigation(self):
        from verify_plan import PLAN, rows

        def fence_table(text):
            blocks = text.split("\n\n")
            for i, paragraph in enumerate(blocks):
                if paragraph.startswith("| "):
                    blocks[i] = "```markdown\n" + paragraph + "\n```"
            return "\n\n".join(blocks)

        tree = GitTree(ROOT)
        plan = tree.read(PLAN).decode()
        self.assertEqual(len(rows(plan)), 67)
        self.assertEqual(rows(fence_table(plan)), [])
        self.assertEqual(rows(plan + "\n" + fence_table(plan)), rows(plan))
        index = tree.read("versions/README.md").decode()
        sample = "\n\n".join(block for block in fence_table(index).split("\n\n") if block.startswith("```markdown"))
        self.assertTrue(sample)
        for content, accepted in ((fence_table(index), False), (index + "\n" + sample, True)):
            errors = []
            read = tree.read

            def read_index(path, commit=None):
                return content.encode() if path == "versions/README.md" and commit is None else read(path, commit)

            with patch.object(tree, "read", side_effect=read_index):
                check_versions(errors, tree)
            if accepted:
                self.assertEqual(errors, [])
            else:
                self.assertTrue(any("missing an approved rendered release row" in error for error in errors))

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

    def test_plan_acceptance_checks_reject_missing_or_changed_obligations(self):
        from verify_plan import PLAN
        path = ROOT / PLAN
        original = path.read_text(encoding="utf-8")
        start = original.index("### v0.0.6.1\n") + len("### v0.0.6.1\n")
        end = original.index("### v0.0.6.2\n")
        real_read = Path.read_text

        def verify_with(content):
            with patch.object(Path, "read_text", lambda path, *a, **kw: (
                content if path == ROOT / PLAN else real_read(path, *a, **kw)
            )):
                verify(False)

        for body in ("\n", "\n- Repair is now optional.\n\n"):
            with self.assertRaisesRegex(ValueError, "acceptance criteria differ"):
                verify_with(original[:start] + body + original[end:])
        with contextlib.redirect_stdout(StringIO()):
            verify_with(original)

    def test_plan_acceptance_preserves_heading_text_inside_fenced_examples(self):
        documented = "### v0.0.6.1\n\n- Run the example.\n"
        example = ("   ````markdown\n## This is literal\n```\n"
                   "### v0.0.6.99\n~~~\n````\n"
                   "~~~markdown\n## Also literal\n~~~\n")
        next_checkpoint = "### v0.0.6.2\n\n- Check the result.\n"
        plan = "# Plan\n" + documented + example + next_checkpoint
        self.assertEqual(acceptance_sections(plan), [(documented + example).rstrip(), next_checkpoint.rstrip()])
        altered = plan.replace("This is literal", "Changed example")
        self.assertNotEqual(acceptance_sections(altered), acceptance_sections(plan))

    def test_retained_plan_installs_reader_dependencies_before_validation(self):
        config = (ROOT / ".github/workflows/verify-repair-plan.yml").read_text(encoding="utf-8")
        reader = config.index("run: python -m pip install --require-hashes -r tools/requirements.txt")
        validator = config.index("run: python tools/check_readme_hq.py")
        graphify = config.index(" - name: Install pinned Graphify dependencies")
        plan = config.index("Check checkpoint order and verify all three Graphify maps over MCP")
        self.assertTrue(reader < validator < graphify < plan)

    def test_retained_plan_pins_complete_published_bytes(self):
        import re

        plan = "plans/v0.0.6-repairs/README.md"
        config = (ROOT / ".github/workflows/verify-repair-plan.yml").read_text(encoding="utf-8")
        statement = rf"^ +git show ([0-9a-f]{{40}}):{re.escape(plan)} \| cmp - {re.escape(plan)}$"
        pinned = re.search(statement, config, re.M)
        self.assertIsNotNone(pinned)
        tree = GitTree(ROOT)
        self.assertEqual(tree.read(plan, pinned.group(1)), tree.read(plan))

    def test_plan_file_inventory_is_bound_to_approved_partition(self):
        from verify_plan import GRAPH, read_json
        original = read_json(GRAPH / "manifest.json")
        unchanged = {**original, "source_files": list(reversed(original["source_files"]))}
        with contextlib.redirect_stdout(StringIO()):
            for files in (original["source_files"][1:], [*original["source_files"], "README.md"]):
                with patch("verify_plan.read_json", side_effect=lambda path: (
                    {**original, "source_files": files} if path == GRAPH / "manifest.json" else read_json(path)
                )):
                    with self.assertRaisesRegex(ValueError, "source inventory differs"):
                        verify(False)
            with patch("verify_plan.read_json", side_effect=lambda path: (
                unchanged if path == GRAPH / "manifest.json" else read_json(path)
            )):
                verify(False)

    def test_partition_capacity_preserves_order(self):
        features = list(range(100))
        parts = split_checkpoints(features)
        self.assertEqual([len(part) for part in parts], [32, 32, 32, 4])
        self.assertEqual([item for part in parts for item in part], features)

    def test_partition_late_write_failure_leaves_destination_available_for_retry(self):
        features = [{"id": f"item-{i}", "documented_in": [], "changed_in": [], "tested_by": []}
                    for i in range(33)]
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / "output"
            write_text = Path.write_text
            def fail_second(path, *args, **kwargs):
                if path.parent.name == "part-002":
                    raise OSError("fixture later write failed")
                return write_text(path, *args, **kwargs)
            with patch.object(Path, "write_text", fail_second):
                with self.assertRaisesRegex(OSError, "later write failed"):
                    stage_partitions(features, destination, "a" * 40, "example/project")
            self.assertFalse(destination.exists())
            result = stage_partitions(features, destination, "a" * 40, "example/project")
            self.assertEqual([len(json.loads(path.read_bytes())["features"]) for path in result], [32, 1])

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

    def test_learning_reuses_metadata_and_verifies_each_source_anchor(self):
        loader = importlib.util.spec_from_file_location("intake", ROOT / "learning/intake.py")
        intake = importlib.util.module_from_spec(loader)
        loader.loader.exec_module(intake)
        headings = ["# Evidence"] + [f"Unique source {i}" for i in range(32)]
        with repository({"README.md": "\n".join(headings)}) as tree:
            tree.git("remote", "add", "origin", "https://github.com/example/project.git")
            first = [{"id": f"source-{i}", "checkout": str(tree.root), "ref": tree.commit,
                      "repository": "Example/Project", "path": "README.md", "line": i+2,
                      "anchor": headings[i+1], "visibility": "public"} for i in range(32)]
            tree.git("-c", "user.name=Fixture", "-c", "user.email=test@example.invalid",
                     "commit", "--allow-empty", "-qm", "Distinct source revision")
            later = GitTree(tree.root).commit
            target = {**first[0], "ref": later, "repository": "example/project",
                      "audience": "reader", "capability": "audit"}
            spec = {"visibility": "public", "sources": first, "target": target,
                    "selected": [], "findings": []}
            routes = []

            def fetch(route):
                routes.append(route)
                if len(routes) > 3:
                    raise HTTPError("https://api.github.com", 429, "fixture budget", {}, None)
                return {"private": False, "visibility": "public"} if "/commits/" not in route else {
                    "sha": route.rsplit("/", 1)[1]}

            destination = tree.root / "receipts"
            record = json.loads(intake.record_intake(spec, destination, fetch=fetch).read_bytes())
            self.assertEqual({row["line"] for row in record["sources"]}, set(range(2, 34)))
            self.assertEqual(routes, ["example/project", f"example/project/commits/{tree.commit}",
                                      f"example/project/commits/{later}"])
            limited = HTTPError("https://api.github.com", 429, "fixture budget", {}, None)
            def reject(route):
                raise limited

            with self.assertRaises(HTTPError) as raised:
                intake.record_intake(spec, destination, fetch=reject)
            self.assertEqual(raised.exception.code, 429)
            spec["sources"][-1] = {**spec["sources"][-1], "anchor": "absent"}
            routes.clear()
            with self.assertRaisesRegex(ValueError, "anchor does not match"):
                intake.record_intake(spec, destination, fetch=fetch)

    def test_learning_structured_rate_limit_and_invalid_anchor_diagnostics(self):
        loader = importlib.util.spec_from_file_location("intake", ROOT / "learning/intake.py")
        intake = importlib.util.module_from_spec(loader)
        loader.loader.exec_module(intake)
        limited = HTTPError("https://secret.invalid/path?token=hidden", 429,
                            "private body", {"Retry-After": "15"}, BytesIO())
        argv = ["intake", "request.json", "receipts", "--json-errors"]
        for returned, expected in (
            (limited, {"code": "github-rate-limited", "retryable": True,
                       "http_status": 429, "retry_after_seconds": 15}),
            (ValueError("source anchor does not match"), {"code": "invalid-or-unverified-evidence",
                                                        "retryable": False}),
        ):
            err = StringIO()
            with (patch.object(sys, "argv", argv), patch.object(intake, "read_json"),
                  patch.object(intake, "record_intake", side_effect=returned), contextlib.redirect_stderr(err),
                  self.assertRaises(SystemExit) as exited):
                intake.main()
            self.assertEqual(exited.exception.code, 2)
            data = json.loads(err.getvalue())
            data.pop("message")
            self.assertEqual(data, expected)
            self.assertNotIn("secret", err.getvalue())

    def test_learning_rejects_malformed_request_before_io(self):
        loader = importlib.util.spec_from_file_location("intake", ROOT / "learning/intake.py")
        intake = importlib.util.module_from_spec(loader)
        loader.loader.exec_module(intake)
        source = {"checkout": ".", "ref": "HEAD", "repository": "example/project",
                  "path": "README.md", "anchor": "Guide", "visibility": "public", "line": 1, "id": "one"}
        good = {"visibility": "public", "sources": [source], "selected": [], "findings": [],
                "target": {**source, "audience": "reader", "capability": "check"}}
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            spec, output = folder / "request.json", folder / "receipts"
            for request in ([], None, {**good, "sources": [None]}, {**good, "target": []},
                            {**good, "target": {**good["target"], "line": True}},
                            {**good, "selected": [["one"]]}, {**good, "findings": [{"source": "one", "candidate": []}]}):
                with self.subTest(request=request), patch.object(intake, "GitTree") as git:
                    spec.write_text(json.dumps(request), encoding="utf-8")
                    stderr = StringIO()
                    with (patch.object(sys, "argv", ["intake.py", str(spec), str(output)]),
                          contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as error):
                        intake.main()
                    self.assertEqual(error.exception.code, 2)
                    self.assertIn("learning request or source proof is invalid or unverified", stderr.getvalue())
                    git.assert_not_called()
                    self.assertFalse(output.exists())
            intake.validate_request(good)

    def test_learning_cli_distinguishes_secondary_rate_limits_from_forbidden(self):
        loader = importlib.util.spec_from_file_location("intake", ROOT / "learning/intake.py")
        intake = importlib.util.module_from_spec(loader)
        loader.loader.exec_module(intake)
        for status, headers, message, limited in (
            (403, {"X-RateLimit-Remaining": "17"}, "You have exceeded a secondary rate limit.", True),
            (403, {"X-RateLimit-Remaining": "0"}, "API rate limit exceeded.", True),
            (403, {"Retry-After": "60"}, "Request throttled.", True),
            (429, {}, "Too many requests.", True),
            (403, {"X-RateLimit-Remaining": "17"}, "Resource not accessible.", False),
        ):
            with self.subTest(status=status, headers=headers, message=message):
                body = BytesIO(json.dumps({"message": message}).encode("utf-8"))
                response = HTTPError("https://api.github.com", status, "fixture", headers, body)
                stderr = StringIO()
                with (patch.object(sys, "argv", ["intake.py", "request.json", "receipts"]),
                      patch.object(intake, "read_json", return_value={}),
                      patch.object(intake, "record_intake", side_effect=response),
                      contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as exit_error):
                    intake.main()
                self.assertEqual(exit_error.exception.code, 2)
                self.assertEqual("retry later" in stderr.getvalue(), limited)
                self.assertEqual("invalid or unverified" in stderr.getvalue(), not limited)

    def test_learning_conflicting_decisions_at_same_source_are_rejected(self):
        loader = importlib.util.spec_from_file_location("intake", ROOT / "learning/intake.py")
        intake = importlib.util.module_from_spec(loader)
        loader.loader.exec_module(intake)
        with repository({"README.md": "# Evidence\nOther evidence\n"}) as tree:
            tree.git("remote", "add", "origin", "https://github.com/example/project.git")
            source = {"id": "first", "checkout": str(tree.root), "ref": "HEAD",
                      "repository": "example/project", "path": "README.md",
                      "line": 1, "anchor": "# Evidence", "visibility": "public"}
            alias = {**source, "id": "alias"}
            other = {**source, "id": "other", "line": 2, "anchor": "Other evidence"}
            first = {"source": "first", "technique": "first-success-milestone",
                     "decision": "adopt", "rationale": "Explain the first result."}
            second = {**first, "source": "alias", "decision": "declined"}
            request = {"visibility": "public", "sources": [source, alias, other],
                       "selected": ["first", "alias", "other"],
                       "target": {**source, "audience": "reader", "capability": "audit"},
                       "findings": [first, second]}
            def fetch(route):
                return ({"private": False, "visibility": "public"} if route == "example/project"
                        else {"sha": tree.commit})
            destination = tree.root / "receipts"
            with self.assertRaisesRegex(ValueError, "conflicting recommendation decisions"):
                intake.record_intake(request, destination, fetch=fetch)
            self.assertFalse(destination.exists())
            for sid, decision, count in (("alias", "adopt", 1), ("other", "declined", 2)):
                request["findings"][1] = {**second, "source": sid, "decision": decision}
                result = intake.record_intake(request, destination, fetch=fetch)
                self.assertEqual(len(json.loads(result.read_bytes())["recommendations"]), count)

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

    def test_learning_distinguishes_unknown_retired_and_unselected_ids(self):
        loader = importlib.util.spec_from_file_location("intake", ROOT / "learning/intake.py")
        intake = importlib.util.module_from_spec(loader)
        loader.loader.exec_module(intake)
        with repository({"README.md": "# Evidence"}) as tree:
            tree.git("remote", "add", "origin", "https://github.com/example/project.git")
            source = {"id": "example", "checkout": str(tree.root), "ref": "HEAD",
                      "repository": "example/project", "path": "README.md",
                      "line": 1, "anchor": "# Evidence", "visibility": "public"}
            finding = {"source": "example", "decision": "adapt", "rationale": "Explain the result."}
            request = {"visibility": "public", "sources": [source], "selected": [],
                       "target": {**source, "audience": "reader", "capability": "audit"},
                       "findings": [{**finding, "technique": "typo"}]}
            registry = tree.root / "techniques/registry.json"
            registry.parent.mkdir()
            registry.write_text(json.dumps({"techniques": [
                {"id": "sample", "status": "active"}, {"id": "old", "status": "retired"},
            ]}), encoding="utf-8")

            def fetch(route):
                return ({"private": False, "visibility": "public"} if route == "example/project"
                        else {"sha": tree.commit})

            destination = tree.root / "evidence"
            with patch.object(intake, "ROOT", tree.root):
                with self.assertRaisesRegex(ValueError, "unknown technique ID"):
                    intake.record_intake(request, destination, fetch=fetch)
                self.assertFalse(destination.exists())
                for identifier, selected, reason in (
                    ("old", [], "retired"),
                    ("sample", [], "source not selected"),
                    ("sample", ["example"], None),
                ):
                    request["selected"] = selected
                    request["findings"][0]["technique"] = identifier
                    receipt = intake.record_intake(request, destination, fetch=fetch)
                    record = json.loads(receipt.read_bytes())
                    if reason:
                        self.assertEqual(record["recommendations"], [])
                        self.assertEqual(record["excluded"][0]["reason"], reason)
                    else:
                        self.assertEqual(record["recommendations"][0]["technique"], identifier)
                        self.assertNotIn("excluded", record)

    def test_public_learning_refusal_writes_nothing(self):
        spec = importlib.util.spec_from_file_location("intake", ROOT / "learning/intake.py")
        intake = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(intake)
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "receipts"
            with self.assertRaisesRegex(ValueError, "public"):
                intake.record_intake({"visibility": "private", "target": {"id": "private-probe"}}, destination)
            self.assertFalse(destination.exists())
