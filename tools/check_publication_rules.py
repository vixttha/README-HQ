"""Read the effective GitHub publication rules without changing the repository."""

import argparse
from http.client import HTTPException
import json
import os
import re
import subprocess
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

from hq_data import REPOSITORY


def evaluate_rules(branch, rules, required_checks, classic=None):
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
    if classic is not None:
        if not isinstance(classic, dict):
            raise ValueError("invalid classic branch protection response")
        status_rules = classic.get("required_status_checks") or {}
        contexts.update(status_rules.get("contexts", []))
        contexts.update(entry["context"] for entry in status_rules.get("checks", []))
        requires_pr |= isinstance(classic.get("required_pull_request_reviews"), dict)
    missing = sorted(set(required_checks) - contexts)
    if branch["protected"] and requires_pr and not missing:
        gate = "observed"
    else:
        gate = "unavailable" if branch["protected"] and classic is None else "incomplete"
    return {
        "protected": branch["protected"],
        "requires_pull_request": requires_pr,
        "observed_required_checks": sorted(contexts),
        "missing_required_checks": missing,
        "mechanical_gate": gate,
        "classic_protection_observation": ("observed" if classic is not None else
                                           "unavailable" if branch["protected"] else "not active"),
        "owner_exact_sha_publication_decision": "separate",
    }


def valid_branch(name):
    result = subprocess.run(["git", "check-ref-format", "--branch", name],
                            capture_output=True, check=False)
    return result.returncode == 0 and result.stdout.rstrip(b"\r\n") == name.encode()


def read_branch_rules(get, branch):
    rules = []
    for page in range(1, 101):
        items, links = get(f"/rules/branches/{branch}?per_page=100&page={page}")
        if not isinstance(items, list):
            raise ValueError("invalid GitHub rule page")
        rules.extend(items)
        if not re.search(r';\s*rel="next"', links):
            return rules
    raise ValueError("GitHub rule pagination exceeded the observation limit")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository")
    parser.add_argument("branch")
    parser.add_argument("--require-check", action="append", required=True)
    options = parser.parse_args()
    if not REPOSITORY.fullmatch(options.repository) or not valid_branch(options.branch):
        parser.error("expected a GitHub repository and valid branch name")
    base = f"https://api.github.com/repos/{options.repository}"
    branch = quote(options.branch, safe="")

    def get(path):
        request = Request(base + path, headers={"Accept": "application/vnd.github+json", "User-Agent": "README-HQ"})
        if token := os.environ.get("GH_TOKEN"):
            request.add_unredirected_header("Authorization", "Bearer " + token)
        with urlopen(request, timeout=15) as response:
            return json.load(response), response.headers.get("Link", "")

    try:
        metadata, _ = get(f"/branches/{branch}")
        rules = read_branch_rules(get, branch)
        def read_classic(protected):
            if not protected:
                return None
            try:
                return get(f"/branches/{branch}/protection")[0]
            except HTTPError as error:
                with error:
                    if error.code not in {401, 403, 404, 429} and not 500 <= error.code <= 599:
                        raise
            except (HTTPException, OSError):
                pass
            return None

        classic = read_classic(metadata["protected"])
        repeated_rules = read_branch_rules(get, branch)
        repeated_metadata, _ = get(f"/branches/{branch}")
        repeated_classic = read_classic(repeated_metadata["protected"])
        result = evaluate_rules(metadata, rules, options.require_check, classic)
        # Separate REST endpoints cannot provide an atomic snapshot.
        if (rules != repeated_rules or classic != repeated_classic
                or metadata["protected"] != repeated_metadata["protected"]
                or metadata["commit"]["sha"] != repeated_metadata["commit"]["sha"]):
            result.update(mechanical_gate="incomplete", configuration_observation="changed-during-read")
        else:
            result["configuration_observation"] = "repeated-reads-agree-not-atomic"
        result.update(repository=options.repository, branch=options.branch, branch_commit=metadata["commit"]["sha"])
    except (KeyError, OSError, TypeError, ValueError, HTTPException):
        print(json.dumps({"mechanical_gate": "unavailable", "owner_exact_sha_publication_decision": "separate"}))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["mechanical_gate"] == "observed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
