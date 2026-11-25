"""Verify the Graphify build and preserve proof from each completed CI stage."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


KIT = Path("graphify-hq/template/v0.0.8")


def verify(output):
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    report = {"commit": os.environ.get("GITHUB_SHA"), "run_id": os.environ.get("GITHUB_RUN_ID"),
              "attempt": os.environ.get("GITHUB_RUN_ATTEMPT"), "job": os.environ.get("GITHUB_JOB"),
              "result": "started", "steps": [], "prior_or_unchecked_receipts_included": False}
    diagnostic = output / "attempt.json"

    def save():
        diagnostic.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    def stage(name, *args, receipts=(), source_root=Path(".")):
        row = {"name": name, "result": "started", "verified_receipts": []}
        report["steps"].append(row)
        save()
        result = subprocess.run([sys.executable, *map(str, args)], check=False)
        row["exit"] = result.returncode
        if result.returncode:
            row["result"] = report["result"] = "failed"
            save()
            return result.returncode
        for receipt in sorted(receipts):
            relative = receipt.relative_to(source_root)
            stored = output / "verified" / relative
            stored.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(receipt, stored)
            row["verified_receipts"].append((Path("verified") / relative).as_posix())
        row["result"] = "passed"
        save()
        return 0

    try:
        for name, arguments, paths in (
            ("template tests", ("-m", "unittest", "discover", "-s", KIT, "-p", "test_*.py", "-v"), ()),
            ("integration tests", ("-m", "unittest", "discover", "-s", "tests", "-p", "test_graphify*.py", "-v"), ()),
            ("version maps", ("graphify-hq/version_maps.py", "--check"), Path("graphify-hq/maps").glob("*/receipt.json")),
            ("repair plan", ("tools/verify_plan.py", "--mcp"), (manifest.with_name("receipt.json") for manifest in
                 [Path("graphify-hq/plans/v0.0.6-repairs/manifest.json"),
                  *Path("graphify-hq/plans/v0.0.6-repairs").glob("*/manifest.json")])),
        ):
            if code := stage(name, *arguments, receipts=paths):
                return code
        work = output.parent / (output.name + "-work")
        work.mkdir()
        manifest = work / "self-map.json"
        self_map = work / "self-map"
        if code := stage("self-map manifest", KIT / "self_map.py", manifest):
            return code
        if code := stage("self-map verification", KIT / "evidence_map.py", manifest, self_map,
                         receipts=(self_map / "receipt.json",), source_root=work):
            return code
    except (OSError, ValueError):
        report["result"] = "failed"
        save()
        raise
    report["result"] = "passed"
    save()
    return 0


if __name__ == "__main__":
    sys.exit(verify(Path(sys.argv[1])))
