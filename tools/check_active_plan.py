"""Check the active README HQ repair ledger and its rendered checkpoint obligations."""

import argparse
from pathlib import Path
import re
import sys

from hq_data import read_json

VERSION = re.compile(r"v0\.0\.6\.(\d+)")
HEADING = re.compile(r"^### (v0\.0\.6\.\d+)\s*$")
ROW = re.compile(r"^\| `(v0\.0\.6\.\d+)` \| \[#(\d+)\]\(https://github\.com/vixttha/README-HQ/issues/\2\) \|")
REQUIRED_PROOF = {"original_failure_replay", "passing_control", "relevant_regressions", "public_job_and_attempt_evidence"}


def ledger_rows(ledger):
    return [(item["version"], item["issue"]) for item in ledger["checkpoints"]]


def check_plan(markdown, ledger, previous=None):
    rows = ledger_rows(ledger)
    scope = ledger["scope"]
    gate = ledger["post_fix_debug_gate"]
    if (ledger.get("schema") != 1 or ledger.get("debug_before_merge") is not True
            or ledger.get("public_github_hosted_runners_only") is not True
            or not {"advance", "merge_consideration"} <= set(gate["required_before"])
            or not REQUIRED_PROOF <= set(gate["evidence_on_exact_repair_sha"])):
        raise ValueError("active plan debug gate or public runner policy is incomplete")
    if not rows or (scope["first"], scope["last"], scope["checkpoint_count"]) != (rows[0][0], rows[-1][0], len(rows)):
        raise ValueError("active plan scope does not match the ledger")
    versions = [VERSION.fullmatch(version) for version, _ in rows]
    if not all(versions) or any(type(issue) is not int or issue <= 0 for _, issue in rows):
        raise ValueError("invalid checkpoint or issue number")
    first = int(versions[0][1])
    if [int(match[1]) for match in versions] != list(range(first, first + len(rows))) or len({issue for _, issue in rows}) != len(rows):
        raise ValueError("active plan checkpoints must be continuous with unique issue mappings")
    if previous is not None:
        retained = ledger_rows(previous)
        if rows[:len(retained)] != retained:
            raise ValueError("published checkpoint mappings must be preserved")

    for offset, item in enumerate(ledger["checkpoints"], first):
        debug = item["debug"]
        if (item["after"] != f"v0.0.6.{offset - 1}"
                or not all(isinstance(debug.get(key), str) and debug[key].strip() for key in ("reproduce", "acceptance"))
                or not isinstance(debug["public_runners"], list) or not debug["public_runners"]
                or not set(debug["public_runners"]) <= {"ubuntu-latest", "windows-latest"}
                or type(debug["graphify_mcp"]) is not bool):
            raise ValueError(f"checkpoint {item['version']} has incomplete debug obligations")

    sections, observed = [], []
    fence = None
    for line in markdown.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker and (fence is None or (
            marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip()
        )):
            fence = marker[1] if fence is None else None
            continue
        if fence:
            continue
        if heading := HEADING.fullmatch(line):
            sections.append((heading[1], []))
        elif re.match(r"^#{1,3}\s", line):
            sections.append((None, []))
        elif row := ROW.match(line):
            observed.append((row[1], int(row[2])))
        elif sections and sections[-1][0]:
            sections[-1][1].append(line)
    checkpoints = [(name, body) for name, body in sections if name]
    if observed != rows or [name for name, _ in checkpoints] != [version for version, _ in rows]:
        raise ValueError("Markdown table or checkpoint sections disagree with the ordered ledger")
    for (version, issue), (_, body) in zip(rows, checkpoints):
        for label in ("Replay", "After the repair", "Public runners"):
            if sum(line.startswith(f"- **{label}** ") and bool(line.removeprefix(f"- **{label}** ").strip())
                   for line in body) != 1:
                raise ValueError(f"{version} lacks one visible {label} obligation")
        if not any(f"https://github.com/vixttha/README-HQ/issues/{issue})" in line
                   for line in body if line.startswith("- **Public runners** ")):
            raise ValueError(f"{version} has no matching issue link in its runner obligation")
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--previous-ledger", type=Path)
    args = parser.parse_args()
    try:
        count = check_plan((args.directory / "README.md").read_text(encoding="utf-8"),
                           read_json(args.directory / "checkpoints.json"),
                           read_json(args.previous_ledger) if args.previous_ledger else None)
    except (OSError, KeyError, AttributeError, TypeError, ValueError) as error:
        print(f"Active repair ledger is invalid: {error}", file=sys.stderr)
        return 1
    print(f"Verified structural obligations for {count} active checkpoints.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
