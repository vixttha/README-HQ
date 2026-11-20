"""Reproduce and verify the Batch 4 checkpoints on an exact public checkout."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory


BASE = "dc8ef21763240168227d67445f02fc4a05ea071c"
POINTS = [
    (113, "c66d5abc6cd2f05677b29f814c3c1d9ec91e8645", "14ec4f8469ddba514fefbf45709dcb99e99fa637", "html_image_alt_distinguishes"),
    (114, "5fd3a97996409836d406b6fdf26019576fb1d623", "d9946682967b76c2f5588a6f58a3b8b2925969b3", "adopter_selectors_require"),
    (115, "51698997a54659d0f21078adfe87e2bef3062f40", "5594747f886c7e65f71828ac3e947aeec9ec42d2", "learning_rejects_malformed"),
    (116, "2cd471c3d12dbff258d88431f29456ba395e87a6", "3b7fb99c4c6a959ffccb405071cabb0affaf8460", "mcp_inventory_rejects"),
    (117, "845599f6a5c3ff9e0ec6ccab05f0e36ca9a5be1c", "14d50a6f91f2cbf9e6f7f64a4d70c7baaf18e774", "public_reader_workflow_preserves"),
    (118, "3fca076c946f48a107ab8f79282b4a1c20cc242b", "744f33acd0acb1e628e585cf25477febeb5be78e", "first_action_follows"),
    (119, "329b66d05eb789e52b1a1da6d6fd54ae2a4acf01", "64f7c069ff924d726ba9efb75826015741834dc8", "rich_text_navigation_reports"),
    (120, "f038580d06db9fe296c52f3531c874289437e758", "6179cf940277af791c804c430851f3f05fa60373", "documented_first_action_example"),
    (121, "5d853265fda236b67fd61cd8fe54d2511ec4c955", "2325f9003745e93924333a91b06f968222352088", "pinned_fragment_cache"),
    (122, "233c8296b8b91f348ce9e999ce617b8ffe8226a3", "358c2448018ac481e6cc0762cb9a0c79046b03af", "retained_plan_installs"),
    (123, "210f3a62c21baadbe64af3c66cded808b4a9d6b2", "f34f949f49c080eef68aadffd81d6a1c04f5d683", "graphify_evidence_line_links"),
    (124, "0caafcb1830823758ec4c46a4b1be30be7c2fd15", "a6d8566149727d522aeae251fe4f0752f8fe5f81", "graphify_attempt_keeps"),
    (125, "156e79849bdeb356219de4b6e18b6cd9362a1dc1", "003447666df6a3fb7e015970c17cbb925c43ba6c", "partition_late_write_failure"),
    (126, "7768439b8822f59955284aa29d171ea6641a0cd5", "1eee8a085161f11774364490a4ed8586ead03613", "required_smoke_distinguishes"),
    (127, "b43c8c0299d5065e08b045a0ce627342e2c75e1f", "afdf729bd7d3975599a674618ce91b9cacc956ef", "smoke_failure_codes_and_private_output"),
]
FOLLOW_UPS = [
    ("Graphify and retained plan integration follow-up", "f696cec1c74897298deb6c75aba4206fe9728688", "885539e9ab0f72e83bdba434cf82aaa9d0280b97", [(123, "existing_graphify_map_keeps"), (122, "retained_plan_installs")]),
    ("Graphify self-map workflow anchor follow-up", "92ae3fc3db62ebe69404d8a253c7dfef6114b3d4", "8e88b42fc61477fc23c67ea203099a3efb3da91b", []),
]
GRAPHIFY_ONLY = {116, 122, 123, 124}
KIT = Path("graphify-hq/template/v0.0.8")
READER = Path("tests/test_readme_repairs.py")


def commands(checkout, *argv):
    result = subprocess.run(argv, cwd=checkout, check=False, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    print(result.stdout, end="", flush=True)
    return result


def run(checkout, *argv):
    result = commands(checkout, *argv)
    result.check_returncode()
    return result.stdout


def focused(checkout, test, selector, *, baseline=False):
    result = commands(checkout, sys.executable, "-m", "unittest", "discover", "-s", str(test.parent),
                      "-p", test.name, "-k", selector, "-v")
    if selector not in result.stdout or "Ran 1 test " not in result.stdout:
        raise ValueError(f"The intended single regression did not run for {selector}")
    if baseline:
        if result.returncode != 1 or "\nFAILED (" not in result.stdout:
            raise ValueError(f"The predecessor did not reproduce {selector}")
    else:
        result.check_returncode()


def test_file(issue):
    if issue == 116:
        return KIT / "test_evidence_map.py"
    if issue in {123, 124}:
        return Path("tests/test_graphify_repairs.py")
    return READER


def copied_test(checkout, revision, path, selector, *, baseline):
    data = subprocess.check_output(["git", "show", f"{revision}:{path.as_posix()}"], cwd=checkout)
    temporary = path.with_name("_batch4_fixture_test.py")
    target = checkout / temporary
    with target.open("xb") as handle:
        handle.write(data)
    try:
        focused(checkout, temporary, selector, baseline=baseline)
    finally:
        target.unlink()


def demo_proof(checkout, evidence):
    with TemporaryDirectory() as temporary:
        fixture = Path(temporary) / "first-action-evidence"
        run(checkout, sys.executable, "examples/first_action_demo.py", str(fixture))
        target = evidence / "first-action-example"
        target.mkdir()
        for file in fixture.glob("*.json"):
            shutil.copyfile(file, target / file.name)


def main():
    checkout, output = (Path(value).resolve() for value in sys.argv[1:])
    linux = os.environ["RUNNER_OS"] == "Linux"
    output.mkdir(exist_ok=True)
    report = {"run_id": os.environ["GITHUB_RUN_ID"], "attempt": os.environ["GITHUB_RUN_ATTEMPT"],
              "os": os.environ["RUNNER_OS"], "job": os.environ["GITHUB_JOB"],
              "observer_commit": os.environ["GITHUB_SHA"], "base": BASE, "checkpoints": [],
              "follow_ups": [], "combined": []}

    def save():
        (output / "results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    def select(sha, parent, tree):
        run(checkout, "git", "checkout", "--detach", sha)
        actual = run(checkout, "git", "rev-parse", "HEAD", "HEAD^", "HEAD^{tree}").split()
        if actual != [sha, parent, tree]:
            raise ValueError("Exact commit, parent, or source tree differs")

    parent = BASE
    run(checkout, "git", "checkout", "--detach", parent)
    for issue, sha, tree, selector in POINTS:
        row = {"checkpoint": f"v0.0.6.{issue}", "commit": sha, "parent": parent,
               "tree": tree, "test": selector, "result": "started"}
        report["checkpoints"].append(row)
        save()
        print(f"::group::Checkpoint {issue} at {sha}", flush=True)
        try:
            applicable = linux or issue not in GRAPHIFY_ONLY
            file = test_file(issue)
            if applicable:
                copied_test(checkout, sha, file, selector, baseline=True)
                row["baseline"] = "reproduced"
            select(sha, parent, tree)
            if not applicable:
                row.update(result="not_applicable", detail="Qualified in the Ubuntu Graphify environment")
                continue
            focused(checkout, file, selector)
            if issue == 120:
                demo_proof(checkout, output)
            row["result"] = "passed"
        except Exception as error:
            row.update(result="failed", detail=str(error))
            raise
        finally:
            parent = sha
            save()
            print("::endgroup::", flush=True)

    for label, sha, tree, tests in FOLLOW_UPS:
        row = {"label": label, "commit": sha, "parent": parent, "tree": tree, "result": "started"}
        report["follow_ups"].append(row)
        save()
        try:
            select(sha, parent, tree)
            for issue, selector in tests:
                if linux or issue not in GRAPHIFY_ONLY:
                    focused(checkout, test_file(issue), selector)
            row["result"] = "passed"
        except Exception as error:
            row.update(result="failed", detail=str(error))
            raise
        finally:
            parent = sha
            save()

    report["candidate"] = parent
    tasks = [
        ("reader CLI", ("tools/check_readme_hq.py", "--receipt", str(output / "reader.json"))),
        ("reader regressions", ("-m", "unittest", "discover", "-s", "tests", "-p", "test_readme*.py", "-v")),
    ]
    if linux:
        tasks.append(("Graphify template, maps, plan and self-map", ("tools/verify_graphify_ci.py", str(output / "graphify"))))
    for name, argv in tasks:
        row = {"name": name, "commit": parent, "result": "started"}
        report["combined"].append(row)
        try:
            run(checkout, sys.executable, *argv)
            row["result"] = "passed"
        except subprocess.CalledProcessError:
            row["result"] = "failed"
            raise
        finally:
            save()


if __name__ == "__main__":
    main()
