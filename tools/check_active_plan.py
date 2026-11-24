"""Check the active README HQ repair ledger and its rendered checkpoint obligations."""

import argparse
from pathlib import Path
import re
import sys

from markdown_it import MarkdownIt

from hq_data import read_json

VERSION = re.compile(r"v0\.0\.6\.(\d+)")
HEADING = re.compile(r"^### (v0\.0\.6\.\d+)\s*$")
ROW = re.compile(r"^\| `(v0\.0\.6\.\d+)` \| \[#(\d+)\]\(https://github\.com/vixttha/README-HQ/issues/\2\) \|")
OBLIGATION = re.compile(r"^- \*\*(Replay|After the repair|Public runners)\*\* ")
REQUIRED_PROOF = {"original_failure_replay", "passing_control", "relevant_regressions", "public_job_and_attempt_evidence"}


def ledger_rows(ledger):
    return [(item["version"], item["issue"]) for item in ledger["checkpoints"]]


def named_link_targets(children):
    links = set()
    destination = None
    named = False
    for part in children:
        if part.type == "link_open":
            destination = part.attrGet("href")
            named = False
        elif part.type == "link_close":
            if destination and named:
                links.add(destination)
            destination = None
        elif destination and part.type in {"text", "code_inline", "image"} and part.content.strip():
            named = True
    return links


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
    lines = markdown.splitlines()
    parser = MarkdownIt("commonmark").enable("table")
    tokens = parser.parse(markdown)
    for index, token in enumerate(tokens):
        if token.map is None:
            continue
        line = lines[token.map[0]]
        if token.type == "heading_open" and token.level == 0:
            if heading := HEADING.fullmatch(line):
                sections.append((heading[1], []))
            elif int(token.tag[1:]) <= 3:
                sections.append((None, []))
        elif token.type == "tr_open" and (row := ROW.match(line)):
            observed.append((row[1], int(row[2])))
        elif token.type == "list_item_open" and token.level == 1 and sections and sections[-1][0]:
            obligation = OBLIGATION.match(line)
            inline = tokens[index + 2]
            if obligation is None or inline.type != "inline":
                continue
            label = obligation[1]
            children = inline.children or []
            visible = "".join(part.content for part in children if part.type in {"text", "code_inline", "image"})
            if visible.removeprefix(label).strip():
                sections[-1][1].append((label, named_link_targets(children)))
    checkpoints = [(name, body) for name, body in sections if name]
    if observed != rows or [name for name, _ in checkpoints] != [version for version, _ in rows]:
        raise ValueError("Markdown table or checkpoint sections disagree with the ordered ledger")
    for (version, issue), (_, body) in zip(rows, checkpoints):
        for label in ("Replay", "After the repair", "Public runners"):
            if sum(actual == label for actual, _ in body) != 1:
                raise ValueError(f"{version} lacks one visible {label} obligation")
        if not any(f"https://github.com/vixttha/README-HQ/issues/{issue}" in links
                   for label, links in body if label == "Public runners"):
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
