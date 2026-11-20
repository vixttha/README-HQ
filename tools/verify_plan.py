"""Check repair-plan coverage, exact references, index links, and Graphify readback."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory

from hq_data import GitTree, parse_json, read_json
from hq_navigation import rendered_table_rows

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "graphify-hq/plans/v0.0.6-repairs"
PLAN = "plans/v0.0.6-repairs/README.md"
BASELINE_PLAN = "7f4562b8f44544bc9dd4b479fcd1bc30ca07ca94"


def split_checkpoints(features, limit=32):
    if not 1 <= limit <= 32:
        raise ValueError("invalid Graphify feature limit")
    return [features[start:start + limit] for start in range(0, len(features), limit)]


def evidence_paths(feature):
    relations = ("documented_in", "changed_in", "tested_by")
    paths = {ref["path"] for relation in relations for ref in feature[relation]}
    paths.update(ref["path"] for ref in feature.get("implemented_in", []))
    return paths


def stage_partitions(features, destination, source_commit, repository):
    if not features:
        raise ValueError("at least one checkpoint is needed")
    names = [feature["id"] for feature in features]
    if len(names) != len(set(names)):
        raise ValueError("duplicate checkpoint IDs")

    partitions = []
    part, files = [], set()
    for feature in features:
        paths = evidence_paths(feature)
        if len(paths) > 64:
            raise ValueError(f"{feature['id']}: exceeds the Graphify source-file limit")
        if len(part) == 32 or len(files | paths) > 64:
            partitions.append((part, files))
            part, files = [], set()
        part.append(feature)
        files.update(paths)
    partitions.append((part, files))
    manifests = [
        {"repository": repository, "source_commit": source_commit,
         "title": f"README HQ repair checkpoints, part {number}",
         "source_files": sorted(paths), "features": items}
        for number, (items, paths) in enumerate(partitions, 1)
    ]
    if os.path.lexists(destination):
        raise FileExistsError(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".plan-", dir=destination.parent) as temporary:
        staging = Path(temporary) / "partitions"
        staging.mkdir()
        output = []
        for number, manifest in enumerate(manifests, 1):
            relative = Path(f"part-{number:03}") / "manifest.json"
            file = staging / relative
            file.parent.mkdir()
            file.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            output.append(destination / relative)
        if os.path.lexists(destination):
            raise FileExistsError(destination)
        staging.rename(destination)
    return output


def rows(content):
    return [line for line in rendered_table_rows(content) if line.startswith("| " + chr(96) + "v0.0.6.")]


def acceptance_sections(content):
    verified = []
    sections = []
    fence = None
    start = offset = 0
    for line in content.splitlines(keepends=True):
        delimiter = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if delimiter:
            marker, rest = delimiter.groups()
            if fence is None and (marker[0] == "~" or "`" not in rest):
                fence = marker
            elif fence and marker[0] == fence[0] and len(marker) >= len(fence) and not rest.strip():
                fence = None
        elif fence is None and re.match(r"^#{1,3} ", line):
            sections.append(content[start:offset])
            start = offset
        offset += len(line)
    sections.append(content[start:])
    for section in sections:
        heading = section.split("\n", 1)[0].rstrip()
        if re.fullmatch(r"### v0\.0\.6\.[0-9]+", heading) or heading in {
            "## Checkpoint workflow", "## Portability and quality acceptance",
        }:
            verified.append(section.rstrip())
    return verified


def verify_index(index, partitions):
    expected = []
    for folder, features in partitions:
        numbers = sorted(int(row["id"].rsplit("-", 1)[1]) for row in features)
        if numbers != list(range(numbers[0], numbers[-1] + 1)):
            raise ValueError("partition is not an uninterrupted checkpoint range")
        prefix = "" if folder == GRAPH else folder.relative_to(GRAPH).as_posix() + "/"
        artifacts = ("graph.json", "manifest.json", "receipt.json")
        if not all((folder / item).is_file() for item in artifacts):
            raise ValueError(f"{folder}: missing plan index artifact")
        expected.append((f"{numbers[0]}–{numbers[-1]}", [prefix + item for item in artifacts]))
    actual = []
    for line in rendered_table_rows(index):
        if match := re.match(r"^\| (\d+–\d+) \|", line):
            actual.append((match[1], re.findall(r"\]\(([^)]+)\)", line)))
    if actual != expected:
        raise ValueError("Graphify plan index does not link to each exact partition and its artifacts")


def verify(check_mcp):
    git = GitTree(ROOT)
    plan = (ROOT / PLAN).read_text(encoding="utf-8")
    baseline = git.read(PLAN, BASELINE_PLAN).decode()
    plan_rows = rows(plan)
    if plan_rows != rows(baseline):
        raise ValueError("repair rows differ from the approved checkpoint ledger")
    if acceptance_sections(plan) != acceptance_sections(baseline):
        raise ValueError("repair acceptance criteria differ from the approved checkpoint ledger")
    canonical, inventories = {}, {}
    prefix = GRAPH.relative_to(ROOT).as_posix() + "/"
    for path in sorted(git.entries(BASELINE_PLAN)):
        if path.startswith(prefix) and path.endswith("/manifest.json"):
            manifest = parse_json(git.read(path, BASELINE_PLAN), path)
            inventories[path] = sorted(manifest["source_files"])
            canonical.update((feature["id"], feature) for feature in manifest["features"])
    validated, partitions, commits = {}, [], set()
    manifests = [GRAPH / "manifest.json", *sorted(GRAPH.glob("*/manifest.json"))]
    for manifest in manifests:
        data = read_json(manifest)
        path = manifest.relative_to(ROOT).as_posix()
        if path not in inventories or sorted(data.get("source_files", [])) != inventories[path]:
            raise ValueError(f"{path}: source inventory differs from the approved partition")
        features = data["features"]
        if not features or len(features) > 32:
            raise ValueError(f"{manifest}: invalid feature partition size")
        commits.add(data["source_commit"])
        partitions.append((manifest.parent, features))
        for feature in features:
            name = feature["id"]
            if name in validated or feature != canonical.get(name):
                raise ValueError(f"{name}: duplicate checkpoint or unrelated label, change, documentation, or test evidence")
            validated[name] = feature
    if len(commits) != 1 or validated != canonical or len(validated) != len(plan_rows):
        raise ValueError("checkpoint evidence coverage is incomplete")
    if rows(git.read(PLAN, commits.pop()).decode()) != plan_rows:
        raise ValueError("repair map references a different checkpoint ledger")
    verify_index((GRAPH / "README.md").read_text(encoding="utf-8"), partitions)
    if check_mcp:
        compiler = ROOT / "graphify-hq/template/v0.0.8/evidence_map.py"
        for manifest in manifests:
            subprocess.run([sys.executable, str(compiler), str(manifest), str(manifest.parent), "--check"],
                           cwd=ROOT, check=True)
    print(f"Verified {len(validated)} repair checkpoints and {len(partitions)} Graphify map partitions.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mcp", action="store_true")
    parser.add_argument("--partition", type=Path, metavar="LEDGER",
                        help="stage new manifests from an ordered checkpoint ledger JSON")
    parser.add_argument("--output", type=Path, help="empty destination for staged partitions")
    args = parser.parse_args()
    try:
        if args.partition:
            if not args.output:
                parser.error("--partition requires --output")
            data = read_json(args.partition)
            tree = GitTree(ROOT, data["source_commit"])
            if tree.commit != data["source_commit"]:
                raise ValueError("partitioning requires an exact Git commit")
            paths = stage_partitions(data["features"], args.output, tree.commit, data["repository"])
            print(f"Staged {len(data['features'])} ordered checkpoints in {len(paths)} manifests.")
        else:
            verify(args.mcp)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        parser.error(str(error))
