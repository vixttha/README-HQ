"""Qualify each Batch 3 checkpoint and verify the complete candidate."""
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

BASE = "941f6b49aac6ab78076f088ad6b58a00e9f03477"
POINTS = [
    (98, "b3d4ab576be023e1e5ca53fc9f70698439035f68", "994150bd03cb01d654cd947856858f78ab0ac698", "base_provenance"),
    (99, "c0f7e3624ce790e6dfc2eb6ba034705b543607e5", "ca403d98fb4be9fa8ec96d40eb81289ceb62ed35", "smoke_spec_modes"),
    (100, "1b239f083609c012f974d1dc550115a1b7d7407b", "825bb363790f1d310643423e8c69c8e40f4cee82", "inventory_blob_cap"),
    (101, "ee88c916088e3d46ff2430799ddabc3c62d4743b", "5e49f311ebdab2d2427f3598eaad265cdb1d095c", "smoke_checkout_keeps"),
    (102, "aee1c15c6e71334ada06a744ee3393bf6c817677", "184f8a6a0552853e450bee3791d9bd0c49378178", "adopter_receipt_distinguishes_scope"),
    (103, "9ba84651b1adf28b31ff95720de822f04af64fbd", "6f66e44f0e7383d4a9d6cdb56cee50253a67daed", "receipt_distinguishes_actions"),
    (104, "db0053471026ee578334f6c1a689e396962170f4", "13bd26cfd23800cbdb0d6bd9f3a1fd0383d1b46e", "partial_clone_blob_fetch"),
    (105, "6c024300f2f3a3cb623371c53d641c8a1c19e87b", "e96d948a8e876ab5c1baed852c5fa9a671ef915b", "evidence_map_requires_features"),
    (106, "6a729011e509ea132a36e51f125c10aa5e06142b", "4b2fc28304cdfd8f504af6f450eacfa62b2987c1", "svg_root_requires"),
    (107, "e176faf069782772e62e708813dbc987487c4c11", "6067559f302523a48d659e644d190fdb6ba822ab", "plain_query_parameters"),
    (108, "39102b05ab1678c8922e02252c6b2ae4f0b389f5", "905c0a41e6884278f0392a3e9a5144da0a622fe0", "rendered_tables_ignore"),
    (109, "6b419e10061dc2c5c3d902c371dbc126117fca9d", "07b32c4d4245730775eebca377287310f2647c89", "learning_reuses_metadata"),
    (110, "93443ac4a34d41a50a4f3c5daf2df5f061a8d5d3", "37f8145dae0b28fc7cfe2a7973ef77d8bdb64d47", "raw_github_files"),
    (111, "5786639b128fa5db83663b7fee8b8c6c1d4926a7", "89c29a7274f1af1fabf191690ebf6826ef69fa5c", "draft_rejects_symlink"),
    (112, "44174db2d70c6af6a7fb58d5fa5683bf64c48458", "808446d8de38e5dfe7e87224b090b69d8389e59b", "receipt_persistence_failure"),
]
FOLLOW_UPS = []
GRAPHIFY_ONLY = {98, 100, 105}
KIT = Path("graphify-hq/template/v0.0.8")
READER_TEST = Path("tests/test_readme_repairs.py")
GRAPHIFY_TEST = KIT / "test_evidence_map.py"


def command(cwd, *argv):
    result = subprocess.run(argv, cwd=cwd, check=False, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    print(result.stdout, end="", flush=True)
    return result


def run(cwd, *argv):
    result = command(cwd, *argv)
    result.check_returncode()
    return result.stdout


def focused(checkout, path, selector, *, baseline=False):
    result = command(checkout, sys.executable, "-m", "unittest", "discover", "-s",
                     str(path.parent), "-p", path.name, "-k", selector, "-v")
    if selector not in result.stdout or "Ran 1 test " not in result.stdout:
        raise ValueError(f"The intended single regression did not run for {selector}")
    if baseline:
        if result.returncode != 1 or "\nFAILED (" not in result.stdout:
            raise ValueError(f"The predecessor did not reproduce {selector}")
    else:
        result.check_returncode()


def repro(checkout, repair, test, selector):
    content = subprocess.check_output(["git", "show", f"{repair}:{test.as_posix()}"], cwd=checkout)
    temporary = test.with_name("_batch3_predecessor_test.py")
    target = checkout / temporary
    with target.open("xb") as handle:
        handle.write(content)
    try:
        focused(checkout, temporary, selector, baseline=True)
    finally:
        target.unlink()


def reject_fenced_table(checkout, relative, selector, *argv):
    document = checkout / relative
    original = document.read_bytes()
    paragraphs = original.decode("utf-8").replace("\r\n", "\n").split("\n\n")
    altered = "\n\n".join(
        "```markdown\n" + paragraph + "\n```" if paragraph.startswith("| ") else paragraph
        for paragraph in paragraphs
    )
    if "```markdown" not in altered:
        raise ValueError(f"No live table fixture in {relative}")
    try:
        document.write_text(altered, encoding="utf-8")
        result = command(checkout, sys.executable, *argv)
        if result.returncode == 0 or selector not in result.stdout:
            raise ValueError(f"Fenced table did not fail the expected check for {relative}")
    finally:
        document.write_bytes(original)


def inventory_boundary(checkout, output):
    with TemporaryDirectory() as folder:
        root = Path(folder)
        run(root, "git", "init", "--quiet")
        (root / "small.bin").write_bytes(b"\xff" * 999_999)
        (root / "large.bin").write_bytes(b"\xff" * 1_000_001)
        run(root, "git", "add", "small.bin", "large.bin")
        run(root, "git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
            "commit", "--quiet", "-m", "Graphify byte boundaries")
        commit = run(root, "git", "rev-parse", "HEAD").strip()
        for name in ("small.bin", "large.bin"):
            manifest = {"repository": "example/project", "source_commit": commit, "title": "Inventory boundary",
                        "source_files": [name], "features": []}
            spec = root / "manifest.json"
            spec.write_text(json.dumps(manifest), encoding="utf-8")
            result = command(root, sys.executable, str(checkout / KIT / "evidence_map.py"),
                             str(spec), str(root / name.removesuffix(".bin")))
            if name == "large.bin":
                if result.returncode == 0 or "1000001 exceeds limit of 1000000 bytes" not in result.stdout:
                    raise ValueError("Oversized inventory blob did not return its documented diagnostic")
            else:
                result.check_returncode()
                receipt = json.loads((root / "small" / "receipt.json").read_bytes())
                if not receipt["mcp_verified"] or receipt["source_files"] != [name]:
                    raise ValueError("MCP did not verify the under-limit inventory fixture")
                (output / "inventory-boundary.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")


def main():
    checkout, output = (Path(value).resolve() for value in sys.argv[1:])
    linux = os.environ["RUNNER_OS"] == "Linux"
    output.mkdir(exist_ok=True)
    report = {"run_id": os.environ["GITHUB_RUN_ID"], "attempt": os.environ["GITHUB_RUN_ATTEMPT"],
              "os": os.environ["RUNNER_OS"], "job": os.environ["GITHUB_JOB"],
              "observer_commit": os.environ["GITHUB_SHA"], "base": BASE,
              "checkpoints": [], "combined": []}

    def save():
        (output / "results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    parent = BASE
    run(checkout, "git", "checkout", "--detach", parent)
    for issue, sha, tree, selector in [*POINTS, *FOLLOW_UPS]:
        row = {"checkpoint": f"v0.0.6.{issue}", "commit": sha, "parent": parent,
               "tree": tree, "test": selector, "result": "started"}
        report["checkpoints"].append(row)
        save()
        print(f"::group::Checkpoint {issue} at {sha}", flush=True)
        try:
            applicable = linux or issue not in GRAPHIFY_ONLY
            test = GRAPHIFY_TEST if issue in GRAPHIFY_ONLY else READER_TEST
            if applicable:
                repro(checkout, sha, test, selector)
                row["baseline"] = "reproduced"
            run(checkout, "git", "checkout", "--detach", sha)
            actual = run(checkout, "git", "rev-parse", "HEAD", "HEAD^", "HEAD^{tree}").split()
            if actual != [sha, parent, tree]:
                raise ValueError("Exact revision, parent, or source tree differs")
            if not applicable:
                row.update(result="not_applicable", detail="Graphify compiler and MCP run on Ubuntu")
                continue
            focused(checkout, test, selector)
            if issue == 100:
                inventory_boundary(checkout, output)
            if issue == 108:
                reject_fenced_table(checkout, "plans/v0.0.6-repairs/README.md", "repair rows differ",
                                    "tools/verify_plan.py", "--mcp")
                if linux:
                    reject_fenced_table(checkout, "versions/README.md", "version index",
                                        "graphify-hq/version_maps.py", "--check")
                    run(checkout, sys.executable, "tools/verify_plan.py", "--mcp")
            row["result"] = "passed"
        except Exception as error:
            row.update(result="failed", detail=str(error))
            raise
        finally:
            parent = sha
            save()
            print("::endgroup::", flush=True)
    report["candidate"] = parent
    tasks = [
        ("reader CLI", ("tools/check_readme_hq.py", "--receipt", str(output / "reader.json"))),
        ("reader regressions", ("-m", "unittest", "discover", "-s", "tests", "-p", "test_readme*.py", "-v")),
    ]
    if linux:
        tasks.extend([
            ("Graphify template regressions", ("-m", "unittest", "discover", "-s", str(KIT), "-p", "test_*.py", "-v")),
            ("Graphify integration regressions", ("-m", "unittest", "discover", "-s", "tests", "-p", "test_graphify*.py", "-v")),
            ("version maps and MCP", ("graphify-hq/version_maps.py", "--check")),
            ("repair plan and MCP", ("tools/verify_plan.py", "--mcp")),
        ])
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
