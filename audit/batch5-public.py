"""Run the Batch 5 regressions against immutable predecessor and repair trees."""
import ast
import json
from importlib.metadata import version
import os
from pathlib import Path
import subprocess
import sys

POINTS = [
    (128, "d845a551e424f68e79b789dc835c154c3e132270", "921609e7a037d0ca37c66d8ef6438642cbeb17ea", "0495b487b40919d5c87eff648d247f8962be61a7", "learning_structured_rate_limit"),
    (129, "ce818c0e47ebdfb035e9c46a986090f6af8be54b", "d845a551e424f68e79b789dc835c154c3e132270", "3bc75936ba5454d25a1fe45d436eab8779273535", "required_smoke_needs_a_matching"),
    (130, "8b6d2baa778c4d6178fb19120cec669961fc3da5", "ce818c0e47ebdfb035e9c46a986090f6af8be54b", "94f1685c966db445f853d2971f7473dbb235f20b", "unchecked_http_probes_keep"),
    (131, "298f75d3211e1d0751ecaad54855212253c6f54e", "8b6d2baa778c4d6178fb19120cec669961fc3da5", "6677a209ef523e462a240cd293683f6b1aa41944", "adopter_detects_an_org"),
    (132, "8a9969b8c239434973e56a8b73214435d70fc81e", "298f75d3211e1d0751ecaad54855212253c6f54e", "62d739da70f132b1ee736ff36918c759c7c82700", "publication_gate_checks_pr"),
    (133, "ccc7d7376381267be7a161d3d2d23a686739555c", "8a9969b8c239434973e56a8b73214435d70fc81e", "ef77400c699e5252128b6a35500a3d6696ef8edf", "active_plan_rejects_invalid"),
    (134, "5e265eaca336bbfe6c50dd6104c562c67e2f1a4c", "ccc7d7376381267be7a161d3d2d23a686739555c", "5355df2e385e50a0bb6c6eaa81a6275fab106844", "pr_review_totals_distinguish"),
    (135, "966431df4a6fc3c94794756b38641008a281177e", "5e265eaca336bbfe6c50dd6104c562c67e2f1a4c", "ea0b354d653405695730fcd750d17e191ae88969", None),
    (136, "84a541b9ce2ebec5f86db23707aab1b5a93c5b8b", "966431df4a6fc3c94794756b38641008a281177e", "c74203164b5b09bb460b0aae66b889f8b75cbc02", "learning_records_verified_canonical"),
    (137, "76eee25d2ec93e8a29c180d633d9fe7373700a80", "84a541b9ce2ebec5f86db23707aab1b5a93c5b8b", "0221593002beb51ff415306aa0d6cd98255ea636", "learning_distinguishes_matched_anchors"),
    (138, "3031e45d1691d68745319ad6350d42fbd265fa45", "76eee25d2ec93e8a29c180d633d9fe7373700a80", "ccfcca213205db4a0c104d3a0fde6ce1d7b63dab", "quickstart_validates_the_local_guide"),
    (139, "cccef67e3f534928dde32b37f63c806136b40e79", "3031e45d1691d68745319ad6350d42fbd265fa45", "a795ae47b33e44020d56abdb2fc6fa1d0bc5278e", "draft_receipt_fingerprints"),
    (140, "3c349cfbe3cc5b259656783321361e91ee0d3dec", "cccef67e3f534928dde32b37f63c806136b40e79", "a5402be4a167b9ba210aab7fa396697ac70d4695", "mixed_markdown_html_image_link"),
]
FOLLOW_UPS = [
    ("7ac278c3b7e23775ea4001128e7ce6e999a3e4f7", "3c349cfbe3cc5b259656783321361e91ee0d3dec", "47fef24aacbb768215a92b5ae9c65b7e8c9ac342", ["learning_structured_rate_limit","required_smoke_needs_a_matching","shell_only_syntax_does_not_bind"]),
    ("bb2c3b89a5b470d9236ed9b76f7c5784a07a48b5", "7ac278c3b7e23775ea4001128e7ce6e999a3e4f7", "cbb5aec4967961d3703ea4da08cef5a9abd3f2f4", ["batch5_review_shell_matching","batch5_review_publication_rule_pages","batch5_review_quickstart_checks","active_plan_rejects_invalid","pr_review_totals_distinguish"]),
    ("aa07e7ab89e4bb2d3d28c9d0a5302394b9b1839b", "bb2c3b89a5b470d9236ed9b76f7c5784a07a48b5", "4ad9a1d50246f6dcc1d4066d693f0a50fbda4350", ["batch5_review_github_response_timeout"]),
    ("bd47fa18607bbffb34345ff72d9ac3aeec3ea99f", "aa07e7ab89e4bb2d3d28c9d0a5302394b9b1839b", "27cbbe0a4d4bcc6ac70e3442c67304310f6a2840", []),
    ("6c81133b912c08e998b227f03b5cff001b0118de", "bd47fa18607bbffb34345ff72d9ac3aeec3ea99f", "debb48c810c9429b7ff6885105dcc85c12a1c50a", ["batch5_review_logical_shell_commands","active_plan_rejects_invalid"]),
    ("844f97a8a140238411fb98cf584bf05a09aba1c4", "6c81133b912c08e998b227f03b5cff001b0118de", "691778d256a07e6553d9a90843dfbdf17a55ea0a", ["active_plan_rejects_invalid"]),
]
READER = "tests/test_readme_repairs.py"
GRAPHIFY = "graphify-hq/template/v0.0.8/test_evidence_map.py"
LINUX_ONLY = {132, 133, 136, 137}

def command(root, *args):
    result = subprocess.run(args, cwd=root, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", check=False)
    print(result.stdout + result.stderr, end="", flush=True)
    return result

def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root)

def select(root, sha, parent, tree):
    command(root, "git", "checkout", "--detach", sha).check_returncode()
    if git(root, "rev-parse", "HEAD", "HEAD^", "HEAD^{tree}").decode().split() != [sha, parent, tree]:
        raise ValueError("Git commit, parent or tree differs")

def test(root, path, selector, baseline=False):
    file = Path(path)
    result = command(root, sys.executable, "-m", "unittest", "discover", "-s", str(file.parent),
                     "-p", file.name, "-k", selector, "-v")
    outcome = result.stdout + result.stderr
    if "Ran 1 test " not in outcome or selector not in outcome:
        raise ValueError("The required regression did not run")
    if baseline and result.returncode == 1 and "\nFAILED (" in outcome:
        return
    if baseline or result.returncode:
        raise ValueError("The required predecessor failure or repair pass did not occur")

def baseline(root, sha, path, selector):
    relative = Path(path).with_name("_batch5_fixture_test.py")
    target = root / relative
    with target.open("xb") as handle:
        handle.write(git(root, "show", f"{sha}:{path}"))
    try:
        test(root, relative, selector, baseline=True)
    finally:
        target.unlink()

def provenance_test(root, sha, selector, *, before):
    # The GitHub evidence control is standard library only. Keep the unrelated
    # Graphify platform dependencies in the real MCP job.
    source = git(root, "show", f"{sha}:{GRAPHIFY}").decode("utf-8")
    tree = ast.parse(source)
    cases = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "ProvenanceTests")
    fixture = Path(GRAPHIFY).with_name("_batch5_provenance_test.py")
    target = root / fixture
    with target.open("x", encoding="utf-8") as handle:
        handle.write("import unittest\nfrom github_provenance import verify_pull_request\n\n")
        handle.write(ast.get_source_segment(source, cases))
        handle.write("\n")
    try:
        test(root, fixture, selector, baseline=before)
    finally:
        target.unlink()

def dependency(root, old=False):
    requirements = (root / "tools/requirements.txt").read_text(encoding="utf-8")
    docs = (root / "README.md").read_text(encoding="utf-8")
    expected = ("12.1.1", "3.10") if old else ("13.0.0", "3.11")
    assert f"Pillow=={expected[0]}" in requirements
    assert f"Python {expected[1]} or newer" in docs
    if not old:
        assert version("Pillow") == "13.0.0"
        assert sys.version_info[:2] >= (3, 11)

def main():
    root, out = (Path(v).resolve() for v in sys.argv[1:])
    out.mkdir(parents=True, exist_ok=True)
    is_linux = os.environ["RUNNER_OS"] == "Linux"
    result = {"observer_commit": os.environ["GITHUB_SHA"], "run": os.environ["GITHUB_RUN_ID"],
              "attempt": os.environ["GITHUB_RUN_ATTEMPT"], "runner": os.environ["RUNNER_OS"],
              "base": POINTS[0][2], "candidate": FOLLOW_UPS[-1][0], "checkpoints": [], "follow_ups": []}

    def save():
        (out / "results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    command(root, "git", "checkout", "--detach", POINTS[0][2]).check_returncode()
    for issue, sha, parent, tree, selector in POINTS:
        row = {"issue": issue, "commit": sha, "parent": parent, "tree": tree, "selector": selector, "result": "started"}
        result["checkpoints"].append(row)
        print(f"::group::Checkpoint {issue} at {sha}", flush=True)
        try:
            assert git(root, "rev-parse", "HEAD").decode().strip() == parent
            if not is_linux and issue in LINUX_ONLY:
                select(root, sha, parent, tree)
                row["result"] = "ubuntu_only"
                continue
            if issue == 135:
                dependency(root, old=True)
                row["predecessor"] = "old_dependency_and_runtime_confirmed"
                select(root, sha, parent, tree)
                dependency(root)
            elif issue == 134:
                provenance_test(root, sha, selector, before=True)
                row["predecessor"] = "failure_reproduced"
                select(root, sha, parent, tree)
                provenance_test(root, sha, selector, before=False)
            else:
                baseline(root, sha, READER, selector)
                row["predecessor"] = "failure_reproduced"
                select(root, sha, parent, tree)
                test(root, READER, selector)
            row["result"] = "passed"
        except Exception as failure:
            row.update(result="failed", detail=str(failure))
            raise
        finally:
            save()
            print("::endgroup::", flush=True)
    for sha, parent, tree, selectors in FOLLOW_UPS:
        row = {"commit": sha, "parent": parent, "tree": tree, "result": "started"}
        result["follow_ups"].append(row)
        save()
        for selector in selectors:
            if selector == "pr_review_totals_distinguish":
                provenance_test(root, sha, selector, before=True)
            else:
                baseline(root, sha, READER, selector)
        row["predecessor"] = "failure_reproduced" if selectors else "prior_documentation_checked"
        if not selectors:
            assert "effective URL’s origin and SHA-256 digest" not in (root / "README.md").read_text(encoding="utf-8")
        select(root, sha, parent, tree)
        if not selectors:
            assert "effective URL’s origin and SHA-256 digest" in (root / "README.md").read_text(encoding="utf-8")
        for selector in selectors:
            if selector == "pr_review_totals_distinguish":
                provenance_test(root, sha, selector, before=False)
            else:
                test(root, READER, selector)
        row["result"] = "passed"
        save()
    command(root, sys.executable, "tools/check_readme_hq.py", "--receipt", str(out / "reader.json")).check_returncode()
    result["combined"] = "passed"
    save()

if __name__ == "__main__":
    main()
