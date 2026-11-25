"""Verify public-source findings and save project-specific recommendation receipts."""

import argparse
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from functools import lru_cache
from hashlib import sha256
import json
import re
from pathlib import Path
import sys
from tempfile import NamedTemporaryFile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from hq_data import GitTree, REPOSITORY, SHA, parse_json, physical_lines, read_json


CATALOG_REPOSITORY = "vixttha/README-HQ"
CATALOG_BRANCH = "README-Technique-Library"
CATALOG_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


class UnknownTechniqueError(ValueError):
    """A finding names an ID absent from the registry."""


def verify_anchor(tree, path, line, anchor):
    if type(line) is not int or line < 1 or not isinstance(anchor, str) or not anchor.strip():
        raise ValueError("source evidence requires a positive line and nonempty anchor")
    body = tree.read(path)
    lines = physical_lines(body.decode("utf-8"))
    if line > len(lines) or anchor not in lines[line - 1]:
        raise ValueError("source anchor does not match the selected Git tree")
    return {"commit": tree.commit, "path": path, "line": line, "anchor": anchor, "sha256": sha256(body).hexdigest()}


def fetch_github(route):
    request = Request(f"https://api.github.com/repos/{route}", headers={"User-Agent": "README-HQ"})
    try:
        with urlopen(request, timeout=15) as response:
            return json.load(response)
    except TimeoutError as error:
        raise URLError("GitHub response timed out") from error


def public_checkpoint(tree, repo, fetch=fetch_github):
    if not REPOSITORY.fullmatch(repo) or not tree.repository or tree.repository.casefold() != repo.casefold():
        raise ValueError("GitHub repository identity is not independently established")
    requested = repo.casefold()

    def identity(metadata):
        if metadata.get("private") is not False or metadata.get("visibility") != "public":
            raise ValueError("source or target is not confirmed public")
        name, stable_id = metadata.get("full_name"), metadata.get("id")
        if not isinstance(name, str) or not REPOSITORY.fullmatch(name) or type(stable_id) is not int or stable_id < 1:
            raise ValueError("GitHub repository metadata lacks a verified canonical name or stable ID")
        return name, stable_id

    name, stable_id = identity(fetch(requested))
    canonical = name.casefold()
    if canonical != requested:
        confirmed_name, confirmed_id = identity(fetch(canonical))
        if confirmed_name.casefold() != canonical or confirmed_id != stable_id:
            raise ValueError("GitHub repository identity does not match the canonical name and stable ID")
    if fetch(f"{canonical}/commits/{tree.commit}").get("sha") != tree.commit:
        raise ValueError("GitHub did not verify this source revision")
    return {"requested_repository": requested, "canonical_repository": name, "repository_id": stable_id}


def validate_request(specification):
    def fields(value, names, label):
        if not isinstance(value, dict) or any(
            not isinstance(value.get(name), str) or not value[name].strip() for name in names
        ):
            raise ValueError(f"invalid {label} fields")

    fields(specification, ("visibility",), "learning request")
    if specification["visibility"] != "public":
        raise ValueError("only public requests use this shared intake")
    catalog = specification.get("catalog")
    fields(catalog, ("checkout", "commit"), "external catalog")
    if not SHA.fullmatch(catalog["commit"]):
        raise ValueError("learning requires an external catalog checkout and full commit")
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


def catalog_checkout(specification, fetch):
    catalog = specification.get("catalog")
    if not isinstance(catalog, dict) or not isinstance(catalog.get("commit"), str) or not SHA.fullmatch(catalog["commit"]):
        raise ValueError("learning requires an external catalog checkout and full commit")
    tree = GitTree(catalog["checkout"], catalog["commit"])
    provenance = public_checkpoint(tree, CATALOG_REPOSITORY, fetch)
    comparison = fetch(f"{provenance['canonical_repository'].casefold()}/compare/{tree.commit}...{CATALOG_BRANCH}")
    if comparison.get("status") not in {"ahead", "identical"}:
        raise ValueError("catalog commit is not on README-Technique-Library")
    return tree, provenance


def catalog_record(tree, kind, identifier):
    if not isinstance(identifier, str) or len(identifier) > 80 or not CATALOG_ID.fullmatch(identifier):
        raise ValueError("catalog record IDs must use lowercase hyphenated slugs")
    folder = {"technique": "techniques", "combination": "combinations"}[kind]
    path = f"{folder}/{identifier}.md"
    if path not in tree.entries():
        error = UnknownTechniqueError if kind == "technique" else ValueError
        raise error(f"unknown {kind} ID {identifier!r}: absent from the pinned external catalog")
    raw = tree.read(path)
    body = raw.decode("utf-8").replace("\r\n", "\n")
    marker = "<!-- catalog\n"
    header, end, text = body.removeprefix(marker).partition("\n-->\n")
    if not body.startswith(marker) or not end or not text.strip():
        raise ValueError(f"{path}: missing catalog metadata or record body")
    metadata = parse_json(header, path)
    if not isinstance(metadata, dict) or metadata.get("status") not in {"active", "retired"}:
        raise ValueError(f"{path}: invalid catalog status")
    record = {"path": path, "sha256": sha256(raw).hexdigest(), "status": metadata["status"]}
    if kind == "technique" or metadata["status"] == "retired":
        return record
    steps = metadata.get("steps")
    if (not isinstance(steps, list) or not 2 <= len(steps) <= 12
            or any(not isinstance(step, str) for step in steps) or len(set(steps)) != len(steps)):
        raise ValueError(f"{path}: expected distinct ordered technique steps")
    for step in steps:
        if catalog_record(tree, "technique", step)["status"] != "active":
            raise ValueError(f"{path}: expected an active record for each combination step")
    return {**record, "steps": steps}


def record_intake(specification, directory, *, fetch=fetch_github):
    validate_request(specification)
    lookup = lru_cache(maxsize=None)(fetch)
    catalog, catalog_provenance = catalog_checkout(specification, lookup)
    sources = {}
    for source in specification["sources"]:
        if source.get("visibility") != "public":
            raise ValueError("only verified public sources enter shared intake")
        if source["id"] in sources:
            raise ValueError("learning source IDs must be unique")
        tree = GitTree(source["checkout"], source["ref"])
        provenance = public_checkpoint(tree, source["repository"], lookup)
        receipt = verify_anchor(tree, source["path"], source["line"], source["anchor"])
        identity = (provenance["canonical_repository"].casefold(), tree.commit,
                    receipt["path"], receipt["line"], receipt["anchor"])
        sources[source["id"]] = {"identity": list(identity), **provenance, **receipt}
    target = specification["target"]
    if target.get("visibility") != "public":
        raise ValueError("only verified public targets enter shared intake")
    target_tree = GitTree(target["checkout"], target["ref"])
    target_provenance = public_checkpoint(target_tree, target["repository"], lookup)
    target_receipt = {**target_provenance, **verify_anchor(target_tree, target["path"], target["line"], target["anchor"])}
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
        if "technique" in entry and "combination" in entry:
            raise ValueError("a recommendation selects one technique or one combination")
        kind = "combination" if "combination" in entry else "technique"
        if kind not in entry:
            if not draft:
                raise ValueError("learning finding requires a technique, combination or candidate")
            continue
        identifier = entry[kind]
        record = catalog_record(catalog, kind, identifier)
        status = record["status"]
        if status != "active" and source_id in selected:
            raise ValueError("expected an active record in the pinned catalog")
        if source_id not in selected:
            excluded.append({kind: identifier, "source": sources[source_id]["identity"],
                             "reason": status if status != "active" else "source not selected"})
            continue
        decision = entry.get("decision")
        if decision not in {"adopt", "adapt", "already present", "declined", "irrelevant", "insufficient evidence"}:
            raise ValueError("recommendation needs a supported target decision")
        rationale = entry.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            raise ValueError("recommendation needs a target-specific rationale")
        identity = (kind, identifier, *sources[source_id]["identity"])
        if decisions.setdefault(identity, decision) != decision:
            raise ValueError(f"conflicting recommendation decisions for {identifier} and the same source evidence")
        uses.append({kind: identifier, "catalog_record": record, "decision": decision, "rationale": rationale,
                     "source": sources[source_id], "target": target_receipt})
    def unique(items):
        return [json.loads(record) for record in sorted({json.dumps(item, sort_keys=True) for item in items})]

    audience, capability = target["audience"], target["capability"]
    data = {"schema": 2, "visibility": "public", "target": {"repository": target["repository"],
            "audience": audience, "capability": capability, **target_receipt},
            "catalog": {"repository": CATALOG_REPOSITORY, "branch": CATALOG_BRANCH,
                        "commit": catalog.commit, **catalog_provenance},
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


def intake_error(error):
    if isinstance(error, HTTPError):
        rate_limited = is_github_rate_limit(error)
        if not rate_limited and error.code not in {500, 502, 503, 504}:
            return {"code": "invalid-or-unverified-evidence", "retryable": False}, (
                "learning request or source proof is invalid or unverified")
        code = "github-rate-limited" if rate_limited else "github-temporarily-unavailable"
        result = {"code": code, "retryable": True, "http_status": error.code}
        retry = error.headers.get("Retry-After", "") if error.headers else ""
        if len(retry) <= 9 and retry.isascii() and retry.isdecimal():
            result["retry_after_seconds"] = int(retry)
        elif retry:
            try:
                when = parsedate_to_datetime(retry)
                if when.tzinfo is not None:
                    result["retry_at"] = when.astimezone(timezone.utc).isoformat()
            except (TypeError, ValueError, OverflowError):
                pass
        elif error.headers:
            reset = error.headers.get("X-RateLimit-Reset", "")
            if len(reset) <= 10 and reset.isascii() and reset.isdecimal():
                result["retry_at"] = datetime.fromtimestamp(int(reset), timezone.utc).isoformat()
        message = "GitHub API rate limit reached" if rate_limited else "GitHub API is temporarily unavailable"
        return result, f"{message} (HTTP {error.code}); retry later"
    if isinstance(error, URLError):
        return {"code": "github-transport-unavailable", "retryable": True}, "GitHub API connection failed; retry later"
    if isinstance(error, UnknownTechniqueError):
        return {"code": "unknown-technique", "retryable": False}, str(error)
    return {"code": "invalid-or-unverified-evidence", "retryable": False}, (
        "learning request or source proof is invalid or unverified")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="public sources, selected references, and target evidence")
    parser.add_argument("output", type=Path, help="directory for reviewed public receipt records")
    parser.add_argument("--json-errors", action="store_true", help="emit structured diagnostics on standard error")
    args = parser.parse_args()
    try:
        print(record_intake(read_json(args.spec), args.output))
    except (KeyError, OSError, TypeError, ValueError) as error:
        diagnostic, message = intake_error(error)
        if args.json_errors:
            print(json.dumps({**diagnostic, "message": message}), file=sys.stderr)
            raise SystemExit(2)
        parser.error(message)


if __name__ == "__main__":
    main()
