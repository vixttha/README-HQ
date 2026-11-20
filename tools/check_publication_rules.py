"""Read the effective GitHub publication rules without changing the repository."""

import argparse
import json
import re
from urllib.parse import quote
from urllib.request import Request, urlopen

from hq_data import REPOSITORY


def evaluate_rules(branch, rules, required_checks):
    if not isinstance(branch.get("protected"), bool) or not isinstance(rules, list):
        raise ValueError("invalid GitHub branch rules response")
    if any(not isinstance(rule, dict) or not isinstance(rule.get("type"), str) for rule in rules):
        raise ValueError("invalid GitHub rule record")
    contexts = {
        check["context"]
        for rule in rules if rule["type"] == "required_status_checks"
        for check in rule.get("parameters", {}).get("required_status_checks", [])
    }
    requires_pr = any(rule["type"] == "pull_request" for rule in rules)
    missing = sorted(set(required_checks) - contexts)
    return {
        "protected": branch["protected"],
        "requires_pull_request": requires_pr,
        "observed_required_checks": sorted(contexts),
        "missing_required_checks": missing,
        "mechanical_gate": "observed" if branch["protected"] and requires_pr and not missing else "incomplete",
        "owner_exact_sha_publication_decision": "separate",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository")
    parser.add_argument("branch")
    parser.add_argument("--require-check", action="append", required=True)
    options = parser.parse_args()
    if not REPOSITORY.fullmatch(options.repository) or not re.fullmatch(r"[A-Za-z0-9_./-]+", options.branch):
        parser.error("expected a GitHub repository and valid branch name")
    base = f"https://api.github.com/repos/{options.repository}"
    branch = quote(options.branch, safe="")

    def get(path):
        request = Request(base + path, headers={"Accept": "application/vnd.github+json", "User-Agent": "README-HQ"})
        with urlopen(request, timeout=15) as response:
            return json.load(response)

    try:
        metadata = get(f"/branches/{branch}")
        result = evaluate_rules(metadata, get(f"/rules/branches/{branch}"), options.require_check)
        result.update(repository=options.repository, branch=options.branch, branch_commit=metadata["commit"]["sha"])
    except (KeyError, OSError, TypeError, ValueError):
        print(json.dumps({"mechanical_gate": "unavailable", "owner_exact_sha_publication_decision": "separate"}))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["mechanical_gate"] == "observed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
