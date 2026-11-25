"""Check README HQ or audit the selected README in another Git repository."""

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

from hq_data import GitTree, REPOSITORY, SHA, parse_json
from hq_navigation import MARKDOWN, check_document, parse_markdown, readme_path, suffix, rendered_table_rows, target_for


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "f50e3749dab90ddfe35894284d1660097a1fb1a8"
INVENTORY_SHA256 = "d628a1c29fea09fff6063bdb85368a6b2d6969025161b1928d82838a2980cfbb"
# Digest of the public inventory independently checked against the original Git blobs.
PUBLIC_INVENTORY_SHA256 = "c0567553cd707ce8b67fb29a242d85d3ad4fa72264544c3365b220e7a746ebd7"
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
VERSION = re.compile(r"v[0-9]+(?:\.[0-9]+){2,}")
SOURCE_SPAN = re.compile(r"L[1-9]\d*(?:-L[1-9]\d*)?")
MAX_README_BYTES = 500 * 1024


def normalize(value):
    return "".join(char for char in unicodedata.normalize("NFKC", value).casefold() if char.isalnum())


def evidence_identity(item):
    if not isinstance(item, dict) or not isinstance(item.get("url"), str):
        raise ValueError("evidence requires a source URL")
    if item.get("visibility", "public") != "public":
        raise ValueError("only public evidence belongs in the shared registry")
    url = urlsplit(item["url"])
    parts = unquote(url.path).strip("/").split("/", 4)
    repo = "/".join(parts[:2])
    if (url.scheme != "https" or url.netloc.lower() != "github.com" or len(parts) != 5
            or not REPOSITORY.fullmatch(repo) or parts[2] != "blob" or not SHA.fullmatch(parts[3])
            or any(x in {"", ".", ".."} for x in parts[4].split("/"))):
        raise ValueError("evidence requires an immutable public GitHub blob URL")
    if url.fragment and not SOURCE_SPAN.fullmatch(url.fragment):
        raise ValueError("invalid evidence source span")
    return repo.lower(), parts[3], parts[4]


def check_evidence(item, tree, known_sources=None):
    identity = evidence_identity(item)
    source = known_sources.get(identity) if known_sources is not None else None
    if known_sources is not None and source is None:
        raise ValueError("evidence is absent from the independently reviewed public source inventory")
    span = urlsplit(item["url"]).fragment
    if span and source:
        endpoints = [int(value.removeprefix("L")) for value in span.split("-")]
        if endpoints != sorted(endpoints) or endpoints[-1] > source[2]:
            raise ValueError("evidence span is reversed or outside the source blob")
    if item.get("status") == "observed":
        return identity
    if item.get("status") != "verified":
        raise ValueError("invalid evidence status")
    receipt_path = item.get("receipt")
    if not isinstance(receipt_path, str) or not receipt_path.startswith("evidence/public/"):
        raise ValueError("verified evidence requires a durable reviewed run receipt")
    receipt = parse_json(tree.read(receipt_path), receipt_path)
    fields = ("source_repository", "source_commit", "source_path", "source_span",
              "environment", "run_url", "source_sha256", "expected", "observed")
    if (
        not isinstance(receipt, dict)
        or any(not isinstance(receipt.get(key), str) or not receipt[key].strip() for key in fields)
        or receipt.get("result") != "pass" or receipt.get("visibility") != "public"
        or (receipt["source_repository"].lower(), receipt["source_commit"], receipt["source_path"]) != identity
        or not span or receipt["source_span"] != span
        or (source and receipt["source_sha256"] != source[1])
        or not re.fullmatch(r"[0-9a-f]{64}", receipt["source_sha256"])
        or not re.fullmatch(r"https://github\.com/[^/]+/[^/]+/actions/runs/\d+(?:/job/\d+)?", receipt["run_url"])
        or receipt["expected"] != receipt["observed"]
    ):
        raise ValueError("run receipt does not establish the stated source and result")
    return identity


def check_registry(errors, tree=None):
    tree = tree or GitTree(ROOT)
    path = "techniques/registry.json"
    data = parse_json(tree.read(path), path)
    if not isinstance(data, dict):
        raise ValueError("technique registry must be a JSON object")
    records = data.get("techniques")
    if type(data.get("schema")) is not int or data["schema"] != 1 or not isinstance(records, list) or not records:
        errors.append("technique registry must use integer schema 1 and a non-empty record array")
        return []
    inventory_path = "techniques/public-source-inventory.json"
    inventory_bytes = tree.read(inventory_path)
    inventory = parse_json(inventory_bytes, inventory_path)
    if not isinstance(inventory, list):
        raise ValueError("public source inventory must be a list")
    checked_sources = {}
    for item in inventory:
        if (not isinstance(item, list) or len(item) != 6
                or not all(isinstance(value, str) and value for value in item[:5])
                or not REPOSITORY.fullmatch(item[0]) or not SHA.fullmatch(item[1])
                or not SHA.fullmatch(item[3]) or not re.fullmatch(r"[0-9a-f]{64}", item[4])
                or type(item[5]) is not int or item[5] < 1):
            raise ValueError("public source inventory requires checked blob digests and line counts")
        identity = tuple(item[:3])
        if identity in checked_sources:
            raise ValueError("duplicate public source inventory identity")
        checked_sources[identity] = item[3:]
    if hashlib.sha256(inventory_bytes).hexdigest() != PUBLIC_INVENTORY_SHA256:
        raise ValueError("public source inventory differs from the independently reviewed snapshot")
    keys = ("title", "problem", "practice", "outcome")
    names, mechanisms, ids = {}, {}, set()
    for record in records:
        slug = record.get("id") if isinstance(record, dict) else None
        if not isinstance(slug, str) or not SLUG.fullmatch(slug) or slug in ids:
            errors.append(f"invalid or duplicate technique ID: {slug!r}")
            continue
        ids.add(slug)
        outcome_key, status = record.get("outcome_key"), record.get("status")
        aliases, items = record.get("aliases"), record.get("evidence")
        if (
            not isinstance(outcome_key, str) or not SLUG.fullmatch(outcome_key)
            or status not in ("active", "retired")
            or any(not isinstance(record.get(key), str) or not record[key].strip() for key in keys)
            or not isinstance(aliases, list) or not all(isinstance(a, str) and a.strip() for a in aliases)
            or not isinstance(items, list) or not items
        ):
            errors.append(f"{slug}: invalid technique fields, aliases, or evidence array")
            continue
        for value in [slug, record["title"], outcome_key, record["outcome"], *aliases]:
            key = normalize(value)
            previous = names.setdefault(key, slug)
            if not key or previous != slug:
                errors.append(f"{slug}: lookup key collision for {value!r} with {previous}")
        signature = tuple(normalize(record[key]) for key in ("problem", "practice"))
        previous = mechanisms.setdefault(signature, slug)
        if previous != slug:
            errors.append(f"{slug}: mechanism duplicates {previous}")
        seen = set()
        for item in items:
            try:
                identity = check_evidence(item, tree, checked_sources)
                content_key = checked_sources[identity][1]
                if content_key in seen:
                    raise ValueError("duplicate evidence content, regardless of URL, span, or mirror")
                seen.add(content_key)
            except (KeyError, TypeError, ValueError) as error:
                errors.append(f"{slug}: {error}")
    return [record for record in records if isinstance(record, dict)]


def check_history(errors, tree=None):
    tree = tree or GitTree(ROOT)
    path = "history/source-inventory.json"
    content = tree.read(path)
    if hashlib.sha256(content).hexdigest() != INVENTORY_SHA256:
        errors.append("historical inventory differs from the independently checked original trees")
        return 0
    expected = parse_json(content, path)["snapshots"]
    sources = parse_json(tree.read("history/sources.json"), "history/sources.json")["snapshots"]
    expected_sources = [
        {**item, "files": [{"path": row["path"], "blob": row["blob"]} for row in item["files"]]}
        for item in expected
    ]
    if expected_sources != sources:
        errors.append("history source manifest differs from independently pinned repositories, commits, and paths")
    entries = tree.entries()
    archived = set()
    for snapshot in expected:
        for file in snapshot["files"]:
            path = f'{snapshot["directory"]}/{file["path"]}'
            archived.add(path)
            if entries.get(path) != (file["mode"], file["blob"]):
                errors.append(f"{path}: tracked archive blob or mode differs from the original")
                continue
            if tree.draft:
                content = tree.read(path)
                digest = hashlib.sha1(f"blob {len(content)}\0".encode() + content).hexdigest()
                if digest != file["blob"]:
                    errors.append(f"{path}: working-tree archive bytes differ from the original")
    permitted = {"history/README.md", "history/sources.json", "history/source-inventory.json"}
    for path in sorted(set(name for name in entries if name.startswith("history/")) - archived - permitted):
        errors.append(f"{path}: untracked archive provenance")
    return len(archived)


def check_versions(errors, tree=None):
    tree = tree or GitTree(ROOT)
    entries = tree.entries()
    index = tree.read("versions/README.md").decode("utf-8")
    readme = tree.read("README.md").decode("utf-8")
    original = tree.entries(BASELINE)
    for path in sorted(name for name in original if re.fullmatch(r"versions/v[^/]+/(README|CHANGELOG)\.md", name)):
        if entries.get(path) != original[path] or (tree.draft and tree.read(path) != tree.read(path, BASELINE)):
            errors.append(f"{path}: frozen standalone snapshot differs from v0.0.6 baseline")
    index_rows = rendered_table_rows(index)
    rows = re.findall(r"^\| (v[0-9.]+) \| [^\n]+$", "\n".join(index_rows), re.M)
    approved_index = tree.read("versions/README.md", BASELINE).decode("utf-8")
    approved_rows = dict(re.findall(r"^\| (v[0-9.]+) \| ([^\n]+)$",
                                    "\n".join(rendered_table_rows(approved_index)), re.M))
    if not set(approved_rows) <= set(rows):
        errors.append("version index is missing an approved rendered release row")
    for version, count in Counter(rows).items():
        matching = [line for line in index_rows if line.startswith(f"| {version} |")]
        if count != 1 or not matching[0].endswith(f"| [Map](../graphify-hq/maps/{version}/README.md) |"):
            errors.append(f"{version}: expected one release row linking to its own map")
        guide_targets = re.findall(r"\]\(([^)]+)\)", matching[0])[:-1]
        if version in approved_rows:
            approved_guides = re.findall(r"\]\(([^)]+)\)", approved_rows[version])[:-1]
            if guide_targets != approved_guides:
                errors.append(f"{version}: release row guide destinations differ from the approved archive")

    graph_index = tree.read("graphify-hq/README.md").decode("utf-8")
    graph_index_rows = rendered_table_rows(graph_index)
    graph_rows = re.findall(r"^\| (v[0-9.]+) \| [^\n]+$", "\n".join(graph_index_rows), re.M)
    for version in set(rows) | set(graph_rows):
        matching = [line for line in graph_index_rows if line.startswith(f"| {version} |")]
        if (version not in rows or len(matching) != 1
                or re.findall(r"\]\(([^)]+)\)", matching[0]) != [f"maps/{version}/README.md"]):
            errors.append(f"{version}: Graphify landing row must link to its own map")
    def current_links(text, prefix):
        _, _, tokens = parse_markdown(text)
        result = []
        for i, token in enumerate(tokens[:-1]):
            if token.type != "paragraph_open" or token.level != 0:
                continue
            inline = tokens[i + 1]
            if inline.type != "inline" or not inline.content.startswith("**Current version**"):
                continue
            for child in inline.children or []:
                if child.type == "link_open":
                    match = re.fullmatch(prefix + r"(v[0-9.]+)/README\.md", child.attrGet("href") or "")
                    if match:
                        result.append(match[1])
        return result

    current = current_links(index, r"(?:versions/)?")
    home = current_links(readme, r"versions/")
    if len(current) != 1 or current != home or not set(current) <= set(rows):
        errors.append("homepage and index must agree on exactly one listed current version")
    dirs = sorted({path.split("/")[1] for path in entries if path.startswith("versions/") and path.count("/") >= 2})
    if not dirs:
        errors.append("missing standalone versions")
    elif all(re.fullmatch(r"v[0-9]+(?:\.[0-9]+)+", version) for version in dirs) and current != [
        max(dirs, key=lambda value: tuple(int(part) for part in value[1:].split(".")))
    ]:
        errors.append("current version must match the latest standalone archive")
    for version in dirs:
        if not VERSION.fullmatch(version) or not all(f"versions/{version}/{x}.md" in entries for x in ("README", "CHANGELOG")):
            errors.append(f"{version}: incomplete standalone version directory")
        if not any(f"]({version}/README.md)" in row for row in index_rows):
            errors.append(f"{version}: standalone README is missing from the index")
    return len(dirs)


def check_navigation(errors, tree=None, gaps=None, *, checked_media=None):
    tree = tree or GitTree(ROOT)
    gaps = gaps if gaps is not None else []
    entries = tree.entries()
    documents = {"README.md", "README-GUIDE.md", "AGENTS.md", "history/README.md",
                 "techniques/README.md", "graphify-hq/README.md"}
    documents.update(name for name in ("REUSE.md", "learning/README.md") if name in entries)
    documents.update(name for name in entries if suffix(name) in MARKDOWN and
                     name.startswith(("audits/", "versions/", "graphify-hq/maps/")))
    count = sum(check_document(tree, path, errors, gaps, checked_media=checked_media)
                for path in sorted(documents))
    for name in sorted(entries):
        if re.fullmatch(r"history/[^/]+/(?:published-v[^/]+|main-rebrand-v[^/]+)/README\.md", name):
            count += check_document(tree, name, errors, gaps, archive_scope=name.rsplit("/", 1)[0],
                                    checked_media=checked_media)
    return count


def documented_actions(blocks):
    from hq_smoke import shell_words_continued

    action = re.compile(r"^(?:quick[ -]?start|getting started|install(?:ation)?|setup|usage|use|run|try|play|build)\b", re.I)
    label = re.compile(r"^(?:install(?:ation)?|setup|quick[ -]?start|getting started|run|try|play|build|launch|open)\b", re.I)
    shell = {"", "sh", "shell", "bash", "zsh", "powershell", "pwsh", "cmd", "console", "terminal", "shell-session"}
    action_level = None
    start_line = 0
    for i, token in enumerate(blocks):
        if token.map is not None:
            start_line = token.map[0]
        if token.type == "heading_open":
            level = int(token.tag[1:])
            if action_level is not None and level <= action_level:
                action_level = None
            heading = "".join(part.content for part in blocks[i + 1].children or []
                              if part.type in {"text", "code_inline", "image"})
            if action_level is None and action.search(heading):
                action_level = level
        elif action_level is not None and token.type == "fence":
            info = token.info.strip().split()
            language = info[0].lower() if info else "sh"
            if language in shell and (logical := shell_words_continued(token.content.splitlines(), language)):
                command, offset = logical
                yield {"kind": "argv", "value": command, "line": token.map[0] + offset + 2,
                       "language": language}
        elif action_level is not None and token.type == "inline":
            children = token.children or []
            for index, item in enumerate(children):
                if item.type != "link_open":
                    continue
                end = next((j for j in range(index + 1, len(children)) if children[j].type == "link_close"), len(children))
                name = "".join(child.content for child in children[index + 1:end])
                href = item.attrGet("href") or ""
                if href and not href.startswith("#") and label.match(name.strip()):
                    offset = item.meta.get("source_line_offset", 0)
                    yield {"kind": "url", "value": href, "line": start_line + offset + 1}


def has_first_action(blocks):
    return next(documented_actions(blocks), None) is not None


def check_first_action_route(tree, source, actions, errors, gaps, route, *, checked_media=None):
    """Check local guide links selected by Quickstart, one guide hop deep."""
    guides = set()
    route["guides"] = []
    route["result"] = "passed"

    def mark_unchecked(message):
        gaps.append(message)
        if route["result"] != "failed":
            route["result"] = "unchecked"

    for action in actions:
        if action["kind"] != "url":
            continue
        url = urlsplit(action["value"])
        try:
            target = target_for(tree, source, url)
        except ValueError:
            continue  # The homepage link check reports the invalid path.
        except LookupError:
            mark_unchecked(f"{source}:{action['line']}: Quickstart guide revision could not be resolved")
            continue
        if target is None:
            continue
        path, commit = target
        entries = tree.entries(commit)
        guide = path if path in entries else readme_path(entries, path, homepage=not path)
        key = (guide, commit)
        if not guide or key == (source, None) or key in guides:
            continue
        if len(guides) >= 8:
            mark_unchecked(f"{source}: Quickstart links exceed the eight-guide route check limit")
            break
        guides.add(key)
        route["guides"].append(guide)
        if suffix(guide) not in MARKDOWN:
            mark_unchecked(f"{guide}: Quickstart route content is outside Markdown coverage")
            continue
        before = len(errors)
        guide_gaps = []
        check_document(tree, guide, errors, guide_gaps, checked_media=checked_media, source_commit=commit)
        for gap in guide_gaps:
            if ": external link not checked: " in gap:
                gaps.append(gap)
            else:
                mark_unchecked(gap)
        if len(errors) != before:
            route["result"] = "failed"


def target_readme(tree, subproject, errors, gaps, profile, *, route=None, checked_media=None):
    prefix = Path(subproject).as_posix().removeprefix("./")
    if Path(subproject).is_absolute() or ".." in Path(subproject).parts or "\\" in subproject:
        raise ValueError("subproject must be relative to the selected repository")
    source = readme_path(tree.entries(), "" if prefix == "." else prefix, homepage=prefix == ".")
    if not source:
        errors.append("no supported README found at the selected entry point")
        return None, 0
    body = tree.read(source)
    if len(body) > MAX_README_BYTES:
        errors.append(f"{source}: exceeds GitHub's 500 KiB rendered README limit")
    if suffix(source) not in MARKDOWN:
        gaps.append(f"{source}: editorial and first-use checks for this format require review")
        return source, 0
    text = body.decode("utf-8")
    _, _, blocks = parse_markdown(text)
    paragraphs = [blocks[i+1].content for i, token in enumerate(blocks)
                  if token.type == "paragraph_open" and blocks[i+1].type == "inline"]
    if not any(len(value.strip()) >= 20 for value in paragraphs):
        errors.append(f"{source}: README needs a meaningful project description")
    if any(re.search(r"^\s*(?:TODO|TBD|FIXME)(?:\b|:)", value, re.I) for value in paragraphs):
        errors.append(f"{source}: unresolved reader-facing placeholder")
    if profile != "reference" and not has_first_action(blocks):
        errors.append(f"{source}: no discoverable first action for {profile}")
    gaps.append(f"{source}: editorial quality and material claims require human or agent review")
    count = check_document(tree, source, errors, gaps, checked_media=checked_media)
    if route is not None and profile != "reference":
        check_first_action_route(tree, source, documented_actions(blocks), errors, gaps, route,
                                 checked_media=checked_media)
    return source, count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="print the technique index after HQ validation")
    parser.add_argument("--repo", type=Path, help="audit a consumer Git repository instead of HQ")
    parser.add_argument("--ref", default="HEAD", help="local ref or commit to validate")
    parser.add_argument("--subproject", help="repository-relative monorepo directory")
    parser.add_argument("--profile", choices=("application", "library", "reference"))
    parser.add_argument("--draft", action="store_true", help="inspect tracked working-tree bytes instead of the published tree")
    parser.add_argument("--receipt", type=Path, help="write a machine-readable check receipt")
    parser.add_argument("--smoke", type=Path, help="an explicit local first-action specification to execute")
    parser.add_argument("--allow-git-fetch", action="store_true", help="permit demand fetching missing Git blobs")
    parser.add_argument("--allow-network", action="store_true", help="allow the explicit remote first-action probe")
    parser.add_argument("--require-smoke", action="store_true", help="return incomplete unless the requested smoke check passes")
    parser.add_argument("--include-smoke-output", action="store_true",
                        help="retain bounded command output in a private failure receipt")
    args = parser.parse_args()
    if args.include_smoke_output and (not args.smoke or not args.receipt):
        parser.error("--include-smoke-output requires --smoke and --receipt")
    if args.require_smoke and not args.smoke:
        parser.error("--require-smoke requires an explicit --smoke")
    for option, value in (("--subproject", args.subproject), ("--profile", args.profile),
                          ("--smoke", args.smoke), ("--allow-network", args.allow_network or None)):
        if args.repo is None and value is not None:
            parser.error(f"{option} requires an explicit --repo")
    if args.subproject is None:
        args.subproject = "."
    if args.profile is None:
        args.profile = "application"
    errors, gaps, records = [], [], []
    cases = {}
    checked_media = set() if args.receipt else None
    scope = None
    try:
        if args.draft and args.ref != "HEAD":
            raise ValueError("--draft applies to the current checkout only")
        tree = GitTree(args.repo or ROOT, args.ref, draft=args.draft, allow_git_fetch=args.allow_git_fetch,
                       track_draft_reads=args.draft)
        if args.repo:
            top_level = Path(tree.git("rev-parse", "--show-toplevel").decode("utf-8").rstrip("\r\n")).resolve()
            if tree.root != top_level:
                tree = None
                raise ValueError("--repo must name the Git root; select a nested README with --subproject")
            scope = {"repository": tree.repository,
                     "repository_identity": "inferred-from-origin" if tree.repository else "unavailable",
                     "profile": args.profile, "subproject": PurePosixPath(args.subproject).as_posix(),
                     "commit": tree.commit}
            route = {}
            entry, count = target_readme(tree, args.subproject, errors, gaps, args.profile, route=route,
                                         checked_media=checked_media)
            cases.update(entrypoint=entry, local_links=count)
            if route:
                cases["first_action_route"] = route
            if entry and suffix(entry) not in MARKDOWN:
                cases["navigation"] = {"result": "unchecked", "format": suffix(entry) or "extensionless"}
                gaps.append(f"{entry}: rendered navigation, anchors, and first-use instructions remain unchecked")
            if args.smoke:
                from hq_smoke import verify_first_action
                actions, source_sha256 = [], None
                if entry and suffix(entry) in MARKDOWN:
                    source_bytes = tree.read(entry)
                    source_sha256 = hashlib.sha256(source_bytes).hexdigest()
                    actions = list(documented_actions(parse_markdown(source_bytes.decode("utf-8"))[2]))
                outcome = verify_first_action(tree, args.smoke, allow_network=args.allow_network,
                                              subproject=args.subproject, include_output=args.include_smoke_output,
                                              entrypoint=entry, actions=actions, source_sha256=source_sha256)
                if args.require_smoke:
                    outcome["required"] = True
                cases["first_action"] = outcome
                if outcome["result"] == "failed":
                    codes = outcome.get("failure_codes", [])
                    detail = ": " + ", ".join(codes) if codes else ""
                    errors.append(f"first action failed its expected result{detail}")
                elif outcome["result"] != "passed":
                    gaps.append(f"first action {outcome['result']}: {outcome['detail']}")
                elif outcome["documentation"]["status"] != "matched":
                    gaps.append("first action passed as supplemental evidence without a matching documented action")
            else:
                gaps.append("first action execution not checked: no explicit smoke spec")
        else:
            records = check_registry(errors, tree)
            cases.update(standalone_versions=check_versions(errors, tree), techniques=len(records),
                         local_links=check_navigation(errors, tree, gaps, checked_media=checked_media),
                         imported_files=check_history(errors, tree))
    except (KeyError, OSError, TypeError, ValueError) as error:
        errors.append(str(error))
    if args.receipt:
        if checked_media:
            cases["checked_media"] = [
                {"path": path, "base_commit": revision, "draft": draft, "sha256": digest}
                for path, revision, draft, digest in sorted(checked_media)
            ]
        from hq_smoke import write_receipt
        try:
            write_receipt(args.receipt, locals().get("tree"), cases, errors, gaps,
                          validator_path=Path(__file__).resolve(), scope=scope)
        except OSError as error:
            errors.append(f"could not write receipt {args.receipt}: {error.strerror or error}")
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.repo:
        print(f"Selected {tree.repository or 'local repository'} at {tree.commit} ({'draft' if args.draft else 'Git tree'})")
        print(f"README: {cases['entrypoint']}; checked {cases['local_links']} local links")
        for gap in gaps:
            print(f"Unchecked: {gap}")
        from hq_smoke import coverage_incomplete
        if coverage_incomplete(cases):
            return 2
    else:
        print(f"Validated {cases['standalone_versions']} standalone version(s), {cases['techniques']} techniques, "
              f"{cases['local_links']} local links, and {cases['imported_files']} imported files.")
        if gaps:
            print(f"{len(gaps)} observations remain unchecked. Use --receipt for details.")
    if args.list:
        for record in sorted(records, key=lambda item: item["id"]):
            print(f"{record['id']} [{record['status']}] - {record['title']}")
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    sys.exit(main())
