"""Directed foundation controls: run only against the exact candidate checkout."""
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests"))
from hq_data import GitTree
from hq_navigation import check_document
from check_readme_hq import check_versions
from test_readme_repairs import repository

expected = "79619d43bc04ccc49097e62058fd3dc0653dd672"
if GitTree(ROOT).commit != expected:
    raise RuntimeError("wrong candidate")
results = []
def require(condition, message):
    if not condition:
        raise AssertionError(message)

def control(issue, case, fn):
    try:
        fn()
        results.append({"issue": issue, "case": case, "result": "passed"})
        print(f"#{issue} {case}: passed", flush=True)
    except Exception as error:
        results.append({"issue": issue, "case": case, "result": "failed", "detail": str(error)})
        print(f"#{issue} {case}: failed: {error}", flush=True)

def version_routes():
    tree = GitTree(ROOT)
    read = tree.read
    errors = []
    check_versions(errors, tree)
    require(not errors, errors)
    mutations = (
        ("versions/README.md", b"maps/v0.0.6/README.md)", b"maps/v0.0.5/README.md)"),
        ("README.md", b"versions/v0.0.6/README.md)", b"versions/v0.0.1/README.md)"),
    )
    for source, old, new in mutations:
        require(old in read(source), "mutation target missing: " + source)
        def edited(path, commit=None):
            body = read(path, commit)
            return body.replace(old, new, 1) if path == source and commit is None else body
        errors = []
        with patch.object(tree, "read", side_effect=edited):
            check_versions(errors, tree)
        require(bool(errors), "wrong valid route accepted: " + source)

def missing_link_forms():
    text = ("[Titled](absent-title.md \"title\")\n"
            "[Reference][ref]\n\n[ref]: absent-reference.md\n\n"
            "<a href=\"absent-html.md\">HTML</a>\n\n"
            "[Setext](guide.md#section)\n\n"
            "Inline example \u0060[Ignore](literal.md)\u0060.\n")
    with repository({"README.md": text, "guide.md": "Section\n=======\n"}) as tree:
        errors, gaps = [], []
        count = check_document(tree, "README.md", errors, gaps)
        require(count == 1 and len(errors) == 3 and not gaps, (count, errors, gaps))
        for missing in ("absent-title.md", "absent-reference.md", "absent-html.md"):
            require(any(missing in e for e in errors), missing)
        require(not any("literal.md" in e for e in errors), errors)

def nested_routes():
    with repository({"docs/README.md": "[Relative](guide.md#here)\n[Root](/root.md#top)\n[Escape](../../outside.md)\n",
                     "docs/guide.md": "# Here\n", "root.md": "# Top\n"}) as tree:
        errors, gaps = [], []
        count = check_document(tree, "docs/README.md", errors, gaps)
        require(count == 2 and len(errors) == 1 and not gaps, (count, errors, gaps))
        require("outside.md" in errors[0], errors)

def pinned_adopter():
    text = "# Original\n\nA meaningful description of a plain fixture.\n\n[Local](guide.md)\n"
    with repository({"README.md": text, "guide.md": "# Guide\n"}) as tree:
        old = tree.commit
        (tree.root / "README.md").write_text("# Changed\n\nA different description for the fixture.\n\n[Broken](missing.md)\n", encoding="utf-8")
        tree.git("add", "README.md")
        tree.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "advance fixture")
        require(tree.resolve("HEAD") != old, "fixture ref did not move")
        receipt = tree.root / "acceptance.json"
        args = [sys.executable, str(ROOT / "tools/check_readme_hq.py"), "--repo", str(tree.root),
                "--ref", old, "--profile", "reference", "--receipt", str(receipt)]
        run = subprocess.run(args, capture_output=True, text=True)
        require(run.returncode == 0, run.stdout + run.stderr)
        data = json.loads(receipt.read_bytes())
        require(data["commit"] == old and data["cases"]["entrypoint"] == "README.md" and data["cases"]["local_links"] == 1, data)
        args[args.index(old)] = "HEAD"
        run = subprocess.run(args, capture_output=True, text=True)
        require(run.returncode == 1, "broken newer ref should fail")

for issue, case, fn in ((5, "exact wrong map and homepage targets", version_routes),
                        (6, "negative rendered link forms", missing_link_forms),
                        (12, "plain adopter explicitly pinned to earlier commit", pinned_adopter),
                        (15, "nested relative, root-relative and escaping paths", nested_routes)):
    control(issue, case, fn)
out = Path(sys.argv[1])
out.write_text(json.dumps({"candidate":expected,"run_id":os.environ.get("GITHUB_RUN_ID"),"os":os.environ.get("RUNNER_OS"),
                           "controls":results},indent=2)+"\n",encoding="utf-8")
if any(row["result"] != "passed" for row in results):
    sys.exit(1)
