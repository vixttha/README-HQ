"""Build or verify README HQ version maps through the pinned Graphify compiler."""

import argparse
from collections import Counter
from html import escape
import json
import re
import subprocess
import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
HQ = ROOT / "graphify-hq"
KIT = HQ / "template/v0.0.8"
TEMPLATE = KIT / "evidence_map.py"
CHECKER = "tools/check_readme_hq.py"
CATALOG = "graphify-hq/catalog.json"
COVERAGE = "graphify-hq/version-inventory.json"

sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(KIT))
from evidence_map import publication_path, publish_directory
from hq_data import SHA, parse_json, physical_lines
from hq_navigation import MARKDOWN, PARSER, rendered_table_rows, suffix


def source_bytes(commit, path):
    return subprocess.check_output(["git", "--no-replace-objects", "show", f"{commit}:{path}"], cwd=ROOT)


def heading_rows(path, lines):
    extension = suffix(path)
    if extension in MARKDOWN:
        rows = []
        for token in PARSER.parse("\n".join(lines)):
            if token.type == "heading_open":
                rows.append(token.map[0])
            elif token.type == "html_block" and re.match(r"\s*<h[1-6](?:\s|>)", token.content, re.I):
                rows.append(token.map[0])
        return rows
    if extension == ".rst":
        return [
            index for index, line in enumerate(lines[:-1])
            if line.strip() and re.search(r"\w", line)
            and re.fullmatch(r"(?:=+|-+|~+|\^+|\x60+|\*+|#+)", lines[index + 1].strip())
            and len(lines[index + 1].strip()) >= len(line.strip())
        ]
    if extension in {".adoc", ".asciidoc", ".asc"}:
        blocks = set()
        rows = []
        for index, line in enumerate(lines):
            marker = line.strip()
            if re.fullmatch(r"(-{4,}|\.{4,}|\+{4,}|/{4,}|={4,})", marker):
                if not blocks:
                    blocks.add(marker)
                elif marker in blocks:
                    blocks.clear()
            elif not blocks and re.match(r"^={1,6}\s+\S", line):
                rows.append(index)
        return rows
    raise ValueError(f"{path}: unsupported heading format; supply a reviewed explicit anchor")


def reference(commit, path, change=False, version=None):
    if isinstance(path, dict):
        row = path
        if set(row) != {"path", "anchor", "line"} or type(row["line"]) is not int or row["line"] < 1:
            raise ValueError("reviewed source references need path, anchor, and positive line")
        lines = physical_lines(source_bytes(commit, row["path"]).decode("utf-8"))
        if row["line"] > len(lines) or lines[row["line"] - 1].strip() != row["anchor"]:
            raise ValueError(f"{row['path']}: reviewed anchor drift at line {row['line']}")
        return row, row["line"]
    lines = physical_lines(source_bytes(commit, path).decode("utf-8"))
    headings = heading_rows(path, lines)
    if change and version:
        number = re.escape(version.removeprefix("v"))
        matching = [
            i for i in headings if re.search(rf"(?<![\d.])v?{number}(?![\d.])", lines[i], re.I)
            and not re.search(r"\b(unreleased|placeholder|todo|draft)\b", lines[i], re.I)
        ]
        if len(matching) != 1:
            raise ValueError(f"{path}: select one {version} release heading or provide a reviewed anchor")
        headings = matching
    elif change:
        raise ValueError(f"{path}: a change anchor requires a release version or a reviewed line")
    valid = [i for i in headings if 0 < len(lines[i].strip()) <= 500]
    if not valid:
        raise ValueError(f"No unique source anchor at {commit}:{path}")
    index = valid[0]
    line = lines[index].strip()
    if sum(other.strip() == line for other in lines) != 1:
        raise ValueError(f"{path}: ambiguous heading; provide a reviewed anchor")
    return {"path": path, "anchor": line}, index + 1


def version_manifest(repository, commit, version, records):
    if not records:
        raise ValueError(f"{version}: empty version map")
    files = {CHECKER}
    features = []
    outline = []
    for record in records:
        references = [reference(commit, path) for path in record["documented_in"]]
        changes, change_line = reference(commit, record["changed_in"], change=True, version=version)
        files.update(ref["path"] for ref, _ in references)
        files.add(changes["path"])
        standalone = record["id"] == "standalone-hq"
        verification = "def check_versions(errors, tree=None):" if standalone else "def check_history(errors, tree=None):"
        features.append({
            "id": f"{record['id']}-{version.replace('.', '-')}",
            "label": record["title"],
            "documented_in": [ref for ref, _ in references],
            "changed_in": [changes],
            "tested_by": [{"path": CHECKER, "anchor": verification}],
        })
        outline.append((record, references, (changes, change_line)))
    return {
        "repository": repository, "source_commit": commit,
        "title": f"README HQ {version} version history", "source_files": sorted(files),
        "features": features,
    }, outline


def table_cell(text):
    value = escape(" ".join(text.split()), quote=False)
    return (value.replace("\\", "&#92;").replace("|", "&#124;").replace("[", "&#91;")
            .replace("]", "&#93;").replace("\x60", "&#96;").replace("*", "&#42;").replace("_", "&#95;"))


def render_outline(version, repository, receipt, outline):
    commit = receipt["source_commit"]

    def link(path, line, label):
        rendered = MARKDOWN | {".rst", ".adoc", ".asciidoc", ".asc"}
        plain = "?plain=1" if suffix(path) in rendered else ""
        return f"[{label}](https://github.com/{repository}/blob/{commit}/{quote(path)}{plain}#L{line})"

    heading = [
        f"# README HQ {version} map", "",
        f"{len(outline)} records · {receipt['nodes']} nodes · {receipt['edges']} edges", "",
        f"[Source commit](https://github.com/{repository}/commit/{commit}) · [Graph](graph.json) · [Receipt](receipt.json) · [Map index](../../README.md)",
        "", "| Record | What changed | Source evidence |", "| --- | --- | --- |",
    ]
    for record, docs, (change, line) in outline:
        references = [link(ref["path"], number, f"Source {i}") for i, (ref, number) in enumerate(docs, 1)]
        references.append(link(change["path"], line, "Change record"))
        heading.append(f"| {table_cell(record['title'])} | {table_cell(record['summary'])} | {' · '.join(references)} |")
    return "\n".join(heading) + "\n"


def coverage_for(versions, rows, expected):
    counts = Counter(rows)
    if dict(counts) != dict.fromkeys(expected, 1) or set(versions) != set(expected):
        raise ValueError("Graphify catalog, version index, and approved version inventory disagree")
    for version, records in versions.items():
        ids = [row["id"] for row in records]
        if not ids or Counter(ids) != Counter(expected[version]):
            missing = sorted(set(expected[version]) - set(ids))
            raise ValueError(f"{version}: missing, duplicated, or unexpected records: missing {missing}")


def build_maps(commit, catalog, target, *, check):
    versions = catalog["versions"]
    if check and {p.name for p in target.iterdir()} != set(versions):
        raise ValueError("map directories and catalog disagree")
    for version, records in versions.items():
        folder = target / version
        manifest, outline = version_manifest(catalog["repository"], commit, version, records)
        content = (json.dumps(manifest, indent=2) + "\n").encode()
        manifest_path = folder / "manifest.json"
        if check:
            if manifest_path.read_bytes() != content:
                raise ValueError(f"{version}: source manifest drift")
        else:
            folder.mkdir(parents=True)
            manifest_path.write_bytes(content)
        command = [sys.executable, str(TEMPLATE), str(manifest_path), str(folder)]
        if check:
            command.append("--check")
        subprocess.run(command, cwd=ROOT, check=True)
        if not check:
            # The version builder owns this private staging tree exclusively.
            shutil.rmtree(publication_path(folder))
        receipt = parse_json((folder / "receipt.json").read_bytes(), folder / "receipt.json")
        outline_bytes = render_outline(version, catalog["repository"], receipt, outline).encode()
        outline_path = folder / "README.md"
        if check:
            if outline_path.read_bytes() != outline_bytes:
                raise ValueError(f"{version}: map outline drift")
        else:
            outline_path.write_bytes(outline_bytes)
    print(f"Graphify verified {len(versions)} maps covering {sum(map(len, versions.values()))} version records.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--output", type=Path, help="build into an empty output directory")
    args = parser.parse_args()
    commit = (HQ / "source-commit.txt").read_text(encoding="ascii").strip()
    if not SHA.fullmatch(commit):
        parser.error("source-commit.txt must contain a full Git commit SHA")
    try:
        catalog_bytes = (ROOT / CATALOG).read_bytes()
        if catalog_bytes != source_bytes(commit, CATALOG):
            raise ValueError("catalog differs from the pinned source commit")
        catalog = parse_json(catalog_bytes, CATALOG)
        expected = parse_json((ROOT / COVERAGE).read_bytes(), COVERAGE)
        index = (ROOT / "versions/README.md").read_text(encoding="utf-8")
        if type(catalog.get("schema")) is not int or catalog["schema"] != 1:
            raise ValueError("Version catalog requires integer schema 1")
        coverage_for(catalog["versions"], re.findall(r"^\| (v\d+(?:\.\d+)+) \|", "\n".join(rendered_table_rows(index)), re.M), expected)
        target = (args.output or HQ / "maps").absolute()
        if args.check:
            build_maps(commit, catalog, target, check=True)
        else:
            if target.exists() and (not target.is_dir() or any(target.iterdir())):
                raise ValueError("output directory must be empty")
            target.parent.mkdir(parents=True, exist_ok=True)
            with TemporaryDirectory(dir=target.parent) as temporary:
                staged = Path(temporary) / "maps"
                staged.mkdir()
                build_maps(commit, catalog, staged, check=False)
                publish_directory(staged, target)
    except (KeyError, OSError, TypeError, ValueError, subprocess.CalledProcessError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
