"""Verify a coherent GitHub pull-request observation for an exact source commit."""

from dataclasses import dataclass
import json
import os
import re
from urllib.request import Request, urlopen

REPOSITORY = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9_.-]{1,100}")
COMMIT = re.compile(r"[0-9a-f]{40}")


@dataclass(frozen=True)
class Page:
    items: list
    has_next: bool


def github_json(repository, route):
    if not REPOSITORY.fullmatch(repository):
        raise ValueError("Expected a GitHub owner/repository")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "Graphify-HQ"}
    if token := os.environ.get("GH_TOKEN"):
        headers["Authorization"] = "Bearer " + token
    request = Request(f"https://api.github.com/repos/{repository}/{route}", headers=headers)
    with urlopen(request, timeout=15) as response:
        data = json.load(response)
        if isinstance(data, list):
            link = response.headers.get("Link", "")
            return Page(data, bool(re.search(r';\s*rel="next"', link)))
        return data


def pages(fetch, route):
    for page in range(1, 101):
        result = fetch(f"{route}?per_page=100&page={page}")
        items = result.items if isinstance(result, Page) else result
        if not isinstance(items, list):
            raise ValueError("Expected a GitHub API list: " + route)
        yield from items
        more = result.has_next if isinstance(result, Page) else len(items) == 100
        if not more:
            return
    raise ValueError("GitHub pagination incomplete within the observation limit: " + route)


def fingerprint(pr):
    head = pr["head"]
    return (head["sha"], head["ref"], (head["repo"] or {}).get("full_name"),
            pr["state"], pr["draft"], pr["merged"], pr.get("merge_commit_sha"))


def verify_pull_request(repository, source, expected, fetch=None):
    """Return exact-SHA membership and reviews, or fail on an incomplete observation."""
    num = expected["number"]
    route = f"pulls/{num}"
    if fetch is None:
        def fetch(path):
            return github_json(repository, path)

    pr = fetch(route)
    observed = fingerprint(pr)
    head = pr["head"]
    if (
        pr["number"] != num
        or pr["base"]["repo"]["full_name"].lower() != repository.lower()
        or (head["repo"] or {}).get("full_name", "").lower() != repository.lower()
        or head["ref"] != expected["source_branch"]
        or not COMMIT.fullmatch(head["sha"])
    ):
        raise ValueError(f"GitHub PR #{num} does not match the expected source repository and branch")

    is_head = source == head["sha"]
    if not is_head:
        commits = list(pages(fetch, route + "/commits"))
        if not any(item["sha"] == source for item in commits):
            if len(commits) >= 250:
                raise ValueError(f"GitHub PR #{num} history may be truncated; source membership is unverified")
            raise ValueError(f"{source} is absent from the GitHub commit list for PR #{num}")

    decisions = {}
    for review in pages(fetch, route + "/reviews"):
        if review["state"] in {"APPROVED", "CHANGES_REQUESTED", "DISMISSED"} and review["user"]:
            decisions[review["user"]["id"]] = review
    if fingerprint(fetch(route)) != observed:
        raise ValueError(f"GitHub PR #{num} changed during provenance verification; retry")
    approvals = sum(
        review["state"] == "APPROVED" and review["commit_id"] == source
        for review in decisions.values()
    )
    state = "merged" if pr["merged"] else ("draft" if pr["state"] == "open" and pr["draft"] else pr["state"])
    return {
        "pull_request": f"https://github.com/{repository}/pull/{num}",
        "source_commit": source,
        "source_relation": "current head" if is_head else "historical PR commit",
        "head_commit": head["sha"],
        "pr_state": state,
        "merge_commit": pr["merge_commit_sha"] if pr["merged"] else None,
        "exact_commit_approvals": approvals,
    }
