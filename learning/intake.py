"""Verify public-source findings and save project-specific recommendation receipts."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from tempfile import NamedTemporaryFile
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from hq_data import GitTree, REPOSITORY, SHA, parse_json, physical_lines, read_json

CATALOG_REPOSITORY = "vixttha/README-HQ"
CATALOG_BRANCH = "README-Technique-Library"
CATALOG_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def verify_anchor(tree, path, line, anchor):
    if type(line) is not int or line < 1 or not isinstance(anchor, str) or not anchor.strip():
        raise ValueError("source evidence requires a positive line and nonempty anchor")
    body = tree.read(path)
    lines = physical_lines(body.decode("utf-8"))
    if line > len(lines) or anchor not in lines[line - 1]:
        raise ValueError("source anchor does not match the selected Git tree")
    return {"commit": tree.commit, "path": path, "line": line, "sha256": sha256(body).hexdigest()}


def fetch_github(route):
    with urlopen(Request(f"https://api.github.com/repos/{route}", headers={"User-Agent": "README-HQ"}), timeout=15) as response:
        return json.load(response)


def public_checkpoint(tree, repo, fetch=fetch_github):
    if not REPOSITORY.fullmatch(repo) or not tree.repository or tree.repository.casefold() != repo.casefold():
        raise ValueError("GitHub repository identity is not independently established")
    metadata = fetch(repo)
    if metadata.get("private") is not False or metadata.get("visibility") != "public":
        raise ValueError("source or target is not confirmed public")
    if fetch(f"{repo}/commits/{tree.commit}").get("sha") != tree.commit:
        raise ValueError("GitHub did not verify this source revision")


def catalog_checkout(specification, fetch):
    catalog = specification.get("catalog")
    if not isinstance(catalog, dict) or not isinstance(catalog.get("commit"), str) or not SHA.fullmatch(catalog["commit"]):
        raise ValueError("learning requires an external catalog checkout and full commit")
    tree = GitTree(catalog["checkout"], catalog["commit"])
    public_checkpoint(tree, CATALOG_REPOSITORY, fetch)
    comparison = fetch(f"{CATALOG_REPOSITORY}/compare/{tree.commit}...{CATALOG_BRANCH}")
    if comparison.get("status") not in {"ahead", "identical"}:
        raise ValueError("catalog commit is not on README-Technique-Library")
    return tree


def catalog_record(tree, kind, identifier):
    if not isinstance(identifier, str) or len(identifier) > 80 or not CATALOG_ID.fullmatch(identifier):
        raise ValueError("catalog record IDs must use lowercase hyphenated slugs")
    folder = {"technique": "techniques", "combination": "combinations"}[kind]
    path = f"{folder}/{identifier}.md"
    if path not in tree.entries():
        raise ValueError(f"{kind} {identifier!r} is absent from the pinned external catalog")
    body = tree.read(path).decode("utf-8").replace("\r\n", "\n")
    marker = "<!-- catalog\n"
    header, end, text = body.removeprefix(marker).partition("\n-->\n")
    if not body.startswith(marker) or not end or not text.strip():
        raise ValueError(f"{path}: missing catalog metadata or record body")
    metadata = parse_json(header, path)
    if not isinstance(metadata, dict) or metadata.get("status") != "active":
        raise ValueError(f"{path}: expected an active record in the pinned catalog")
    if kind == "technique":
        return {"path": path}
    steps = metadata.get("steps")
    if (not isinstance(steps, list) or not 2 <= len(steps) <= 12
            or any(not isinstance(step, str) for step in steps) or len(set(steps)) != len(steps)):
        raise ValueError(f"{path}: expected distinct ordered technique steps")
    for step in steps:
        catalog_record(tree, "technique", step)
    return {"path": path, "steps": steps}


def record_intake(specification, directory, *, fetch=fetch_github):
    if specification.get("visibility") != "public":
        raise ValueError("only public requests use this shared intake")
    catalog = catalog_checkout(specification, fetch)
    sources = {}
    for source in specification["sources"]:
        if source.get("visibility") != "public":
            raise ValueError("only verified public sources enter shared intake")
        if source["id"] in sources:
            raise ValueError("learning source IDs must be unique")
        tree = GitTree(source["checkout"], source["ref"])
        public_checkpoint(tree, source["repository"], fetch)
        receipt = verify_anchor(tree, source["path"], source["line"], source["anchor"])
        identity = (source["repository"].casefold(), tree.commit, source["path"], source["line"])
        sources[source["id"]] = {"identity": list(identity), **receipt}
    target = specification["target"]
    if target.get("visibility") != "public":
        raise ValueError("only verified public targets enter shared intake")
    target_tree = GitTree(target["checkout"], target["ref"])
    public_checkpoint(target_tree, target["repository"], fetch)
    target_receipt = verify_anchor(target_tree, target["path"], target["line"], target["anchor"])
    selected = set(specification["selected"])
    if not selected <= set(sources):
        raise ValueError("chosen learning sources must have independently verified intake evidence")
    uses = []
    candidates = []
    for entry in specification["findings"]:
        source_id = entry["source"]
        if source_id not in sources:
            raise ValueError("learning findings require a verified source")
        draft = entry.get("candidate")
        if draft:
            fields = ("problem", "practice", "outcome")
            if any(not isinstance(draft.get(key), str) or not draft[key].strip() for key in fields):
                raise ValueError("new candidates require an original problem, practice, and outcome")
            if draft.get("copied_material"):
                raise ValueError("copied material requires an owner-approved rights review outside shared intake")
            candidates.append({"definition": {key: draft[key] for key in fields},
                               "evidence": sources[source_id], "state": "review-required"})
        if source_id not in selected:
            continue
        if "technique" in entry and "combination" in entry:
            raise ValueError("a recommendation selects one technique or one combination")
        kind = "combination" if "combination" in entry else "technique"
        if kind not in entry:
            continue
        identifier = entry[kind]
        record = catalog_record(catalog, kind, identifier)
        decision = entry.get("decision")
        if decision not in {"adopt", "adapt", "already present", "declined", "irrelevant", "insufficient evidence"}:
            raise ValueError("recommendation needs a supported target decision")
        rationale = entry.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            raise ValueError("recommendation needs a target-specific rationale")
        uses.append({kind: identifier, "catalog_record": record, "decision": decision, "rationale": rationale,
                     "source": sources[source_id], "target": target_receipt})
    def unique(items):
        return [json.loads(record) for record in sorted({json.dumps(item, sort_keys=True) for item in items})]

    audience, capability = target["audience"], target["capability"]
    if not isinstance(audience, str) or not audience.strip() or not isinstance(capability, str) or not capability.strip():
        raise ValueError("target receipts require an audience and capability")
    data = {"schema": 2, "visibility": "public", "target": {"repository": target["repository"],
            "audience": audience, "capability": capability, **target_receipt},
            "catalog": {"repository": CATALOG_REPOSITORY, "branch": CATALOG_BRANCH, "commit": catalog.commit},
            "sources": unique(sources.values()), "selected": sorted(selected),
            "candidates": unique(candidates), "recommendations": unique(uses)}
    body = (json.dumps(data, indent=2, sort_keys=True) + "\n").encode()
    directory.mkdir(parents=True, exist_ok=True)
    receipt = directory / f"{sha256(body).hexdigest()}.json"
    if not receipt.exists():
        with NamedTemporaryFile(dir=directory, delete=False) as file:
            file.write(body)
        Path(file.name).replace(receipt)
    elif receipt.read_bytes() != body:
        raise ValueError("existing learning receipt differs from its content identity")
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="public sources, selected references, and target evidence")
    parser.add_argument("output", type=Path, help="directory for reviewed public receipt records")
    args = parser.parse_args()
    try:
        print(record_intake(read_json(args.spec), args.output))
    except (KeyError, OSError, TypeError, ValueError):
        parser.error("learning request or source proof is invalid or unverified")


if __name__ == "__main__":
    main()
