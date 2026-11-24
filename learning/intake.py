"""Verify public-source findings and save project-specific recommendation receipts."""

import argparse
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import sys
from tempfile import NamedTemporaryFile
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from hq_data import GitTree, REPOSITORY, parse_json, physical_lines, read_json


class UnknownTechniqueError(ValueError):
    """A finding names an ID absent from the registry."""


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
    repo = repo.casefold()
    metadata = fetch(repo)
    if metadata.get("private") is not False or metadata.get("visibility") != "public":
        raise ValueError("source or target is not confirmed public")
    if fetch(f"{repo}/commits/{tree.commit}").get("sha") != tree.commit:
        raise ValueError("GitHub did not verify this source revision")


def validate_request(specification):
    def fields(value, names, label):
        if not isinstance(value, dict) or any(
            not isinstance(value.get(name), str) or not value[name].strip() for name in names
        ):
            raise ValueError(f"invalid {label} fields")

    fields(specification, ("visibility",), "learning request")
    if specification["visibility"] != "public":
        raise ValueError("only public requests use this shared intake")
    for name in ("sources", "selected", "findings"):
        if not isinstance(specification.get(name), list):
            raise ValueError(f"learning request requires a {name} array")
    evidence_fields = ("checkout", "ref", "repository", "path", "anchor", "visibility")
    for source in specification["sources"]:
        fields(source, (*evidence_fields, "id"), "source")
        if type(source.get("line")) is not int or source["line"] < 1:
            raise ValueError("invalid source line")
    target = specification.get("target")
    fields(target, (*evidence_fields, "audience", "capability"), "target")
    if type(target.get("line")) is not int or target["line"] < 1:
        raise ValueError("invalid target line")
    if any(not isinstance(item, str) or not item.strip() for item in specification["selected"]):
        raise ValueError("selected sources must be nonempty string IDs")
    for entry in specification["findings"]:
        fields(entry, ("source",), "finding")
        if entry.get("candidate") is not None:
            fields(entry["candidate"], ("problem", "practice", "outcome"), "candidate")
        if "decision" in entry and not isinstance(entry["decision"], str):
            raise ValueError("invalid finding decision")


def record_intake(specification, directory, *, fetch=fetch_github):
    validate_request(specification)
    lookup = lru_cache(maxsize=None)(fetch)
    sources = {}
    for source in specification["sources"]:
        if source.get("visibility") != "public":
            raise ValueError("only verified public sources enter shared intake")
        if source["id"] in sources:
            raise ValueError("learning source IDs must be unique")
        tree = GitTree(source["checkout"], source["ref"])
        public_checkpoint(tree, source["repository"], lookup)
        receipt = verify_anchor(tree, source["path"], source["line"], source["anchor"])
        identity = (source["repository"].casefold(), tree.commit, source["path"], source["line"])
        sources[source["id"]] = {"identity": list(identity), **receipt}
    target = specification["target"]
    if target.get("visibility") != "public":
        raise ValueError("only verified public targets enter shared intake")
    target_tree = GitTree(target["checkout"], target["ref"])
    public_checkpoint(target_tree, target["repository"], lookup)
    target_receipt = verify_anchor(target_tree, target["path"], target["line"], target["anchor"])
    registry = ROOT / "techniques/registry.json"
    registry_bytes = registry.read_bytes()
    techniques = {row["id"]: row["status"] for row in parse_json(registry_bytes, registry)["techniques"]}
    selected = set(specification["selected"])
    if not selected <= set(sources):
        raise ValueError("chosen learning sources must have independently verified intake evidence")
    uses = []
    candidates = []
    excluded = []
    decisions = {}
    for entry in specification["findings"]:
        source_id = entry["source"]
        if source_id not in sources:
            raise ValueError("learning findings require a verified source")
        draft = entry.get("candidate")
        if draft:
            fields = ("problem", "practice", "outcome")
            if draft.get("copied_material"):
                raise ValueError("copied material requires an owner-approved rights review outside shared intake")
            candidates.append({"definition": {key: draft[key] for key in fields},
                               "evidence": sources[source_id], "state": "review-required"})
        if "technique" not in entry:
            continue
        technique = entry["technique"]
        if not isinstance(technique, str) or technique not in techniques:
            raise UnknownTechniqueError("learning finding names an unknown technique ID")
        status = techniques[technique]
        if status != "active" or source_id not in selected:
            excluded.append({"technique": technique, "source": sources[source_id]["identity"],
                             "reason": status if status != "active" else "source not selected"})
            continue
        decision = entry.get("decision")
        if decision not in {"adopt", "adapt", "already present", "declined", "irrelevant", "insufficient evidence"}:
            raise ValueError("recommendation needs a supported target decision")
        rationale = entry.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            raise ValueError("recommendation needs a target-specific rationale")
        identity = (technique, *sources[source_id]["identity"])
        if decisions.setdefault(identity, decision) != decision:
            raise ValueError(f"conflicting recommendation decisions for {technique} and the same source evidence")
        uses.append({"technique": technique, "decision": decision, "rationale": rationale,
                     "source": sources[source_id], "target": target_receipt})
    def unique(items):
        return [json.loads(record) for record in sorted({json.dumps(item, sort_keys=True) for item in items})]

    audience, capability = target["audience"], target["capability"]
    data = {"schema": 1, "visibility": "public", "target": {"repository": target["repository"],
            "audience": audience, "capability": capability, **target_receipt},
            "registry_sha256": sha256(registry_bytes).hexdigest(),
            "sources": unique(sources.values()), "selected": sorted({tuple(sources[key]["identity"]) for key in selected}),
            "candidates": unique(candidates), "recommendations": unique(uses)}
    if excluded:
        data["excluded"] = unique(excluded)
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


def is_github_rate_limit(error):
    if error.code == 429:
        return True
    if error.code != 403:
        return False
    if error.headers and (
        error.headers.get("X-RateLimit-Remaining") == "0" or error.headers.get("Retry-After")
    ):
        return True
    try:
        with error:
            payload = json.loads(error.read(8192))
    except (OSError, ValueError):
        return False
    message = payload.get("message") if isinstance(payload, dict) else None
    return isinstance(message, str) and "secondary rate limit" in message.casefold()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="public sources, selected references, and target evidence")
    parser.add_argument("output", type=Path, help="directory for reviewed public receipt records")
    args = parser.parse_args()
    try:
        print(record_intake(read_json(args.spec), args.output))
    except UnknownTechniqueError as error:
        parser.error(str(error))
    except HTTPError as error:
        if is_github_rate_limit(error):
            parser.error(f"GitHub API rate limit reached (HTTP {error.code}); retry later")
        parser.error("learning request or source proof is invalid or unverified")
    except (KeyError, OSError, TypeError, ValueError):
        parser.error("learning request or source proof is invalid or unverified")


if __name__ == "__main__":
    main()
