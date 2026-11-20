"""Bind the Batch 2 public-runner evidence to exact Git revisions."""

import json
import os
from pathlib import Path
import subprocess
import sys


BASE = "774bf783850162f731f3e38aff0f52b99a5202fc"
POINTS = [
    (83, "7551297c9cc2476ed2b112b45b72770b21eb23bc", "a6636f6b64acda10f4097b823cad3a92da5e601f", "duplicate_resolved"),
    (84, "686fc60e641670434453ff8020301b6e5c1d532e", "92057a28d94092bd9bc962d856ff99669dfb31f4", "selected_monorepo_package"),
    (85, "b1a3dd931b187e9a645dafa9610431d0983d46d3", "835ae759ae6cce75f618799928fbe26db6fb676f", "marker_checks"),
    (86, "6065e64e9d4f1c086aa13f895c72c54cfa8c79ce", "0b1d5752dd1467c3d4f42d8d2a366bb634eb1354", "plan_file_inventory"),
    (87, "decedeffa7ee4496caea601faef2c6305cd7b4e1", "3f1197667120b23cf874c70d707a97e9c7556c85", "conflicting_decisions"),
    (88, "014fb28ea0441c73dba591818341290437ad6ad2", "c79de9b02bda30acd6cee0e14700f2eb546fb6d7", "lfs_media"),
    (89, "293a37405db503cacb83ea3a0ccc24f3af359546", "98eba4fde503cf2d06a1d629a6cbaa03ee12d550", "bare_gfm"),
    (90, "44d16685256a436b3e78d01908bb5c2fb3c3a2e6", "d75df0d29e948103f361329da85b28ed7689452a", "requires_root"),
    (91, "a677e3e5416adfb0b4baed66c6db2b25bfecd58f", "5b1b7830ba7ff89f8261bd0dfc323ba4cfe057b3", "documented_review"),
    (92, "d33a03ec031c449a0af5f6abd348de7e2af17ce2", "e90ec14076d54201f49c2d1ecc698bd38f94df5e", "http_smoke_checks"),
    (93, "f870af8fb37aea54f52ce893ca8e046d810b51c4", "5fdbfacbcc563c629b09afd6384e8f4f5de0b4b0", "public_refs"),
    (94, "13d97fd1266811932abdbdf17f5e33c6e38e7ac5", "428ba3422fb53cc6c983b15f49bb2324d97d4def", "plan_acceptance"),
    (95, "3de96debed222a49f01b9839d112dd67f3d58ea5", "9b3c93deaf98b94b7955276af7f8b4178c4f33e6", "animated_media"),
    (96, "92681eb8c11acc404f82be47490875dcb7f80485", "de5bc104bca705225d4b8d7c0e9732ce2200390a", "effective_url"),
    (97, "82daa1a79a7b5f455496fee8974e4a37334bdd99", "e1967a1ab6f9559d2e45e13fd5641b29b86313b8", "unknown_retired"),
]
FOLLOW_UPS = []


def run(directory, *argv):
    completed = subprocess.run(argv, cwd=directory, check=False, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    print(completed.stdout, end="", flush=True)
    completed.check_returncode()
    return completed.stdout


def focused(directory, pattern, selector):
    output = run(directory, sys.executable, "-m", "unittest", "discover",
                 "-s", "tests", "-p", pattern, "-k", selector, "-v")
    if "Ran 0 tests" in output:
        raise ValueError(f"No focused regression ran for {selector}")


def main():
    checkout, output = (Path(value).resolve() for value in sys.argv[1:])
    linux = os.environ["RUNNER_OS"] == "Linux"
    output.mkdir(exist_ok=True)
    report = {"run_id": os.environ["GITHUB_RUN_ID"], "attempt": os.environ["GITHUB_RUN_ATTEMPT"],
              "os": os.environ["RUNNER_OS"], "job": os.environ["GITHUB_JOB"],
              "observer_commit": os.environ["GITHUB_SHA"], "base": BASE, "checkpoints": [], "combined": []}

    def save():
        (output / "results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    def check_revision(sha, parent, tree):
        run(checkout, "git", "checkout", "--detach", sha)
        observed = run(checkout, "git", "rev-parse", "HEAD", "HEAD^", "HEAD^{tree}").split()
        if observed != [sha, parent, tree]:
            raise ValueError("Exact revision, expected parent, or tested tree differs")

    parent = BASE
    for number, sha, tree, selector in [*POINTS, *FOLLOW_UPS]:
        name = f"v0.0.6.{number}" if isinstance(number, int) else number
        row = {"checkpoint": name, "commit": sha, "parent": parent, "tree": tree,
               "selector": selector, "result": "started"}
        report["checkpoints"].append(row)
        save()
        print(f"::group::{name} {sha}", flush=True)
        try:
            check_revision(sha, parent, tree)
            if number == 83 and not linux:
                row.update(result="not_applicable", detail="Graphify dependency lock is Linux-only")
                continue
            pattern = "test_graphify_repairs.py" if number == 83 else "test_readme_repairs.py"
            focused(checkout, pattern, selector)
            if number in {86, 94} and linux:
                result = run(checkout, sys.executable, "tools/verify_plan.py", "--mcp")
                row["graphify_mcp_partitions"] = result.count("Graphify MCP verified ")
                if row["graphify_mcp_partitions"] != 3:
                    raise ValueError("Graphify did not verify all three partitions")
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
            ("Graphify regressions", ("-m", "unittest", "discover", "-s", "tests", "-p", "test_graphify*.py", "-v")),
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
