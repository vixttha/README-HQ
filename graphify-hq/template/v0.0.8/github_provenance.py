"""Verify a coherent GitHub pull-request observation for an exact source commit."""

from dataclasses import dataclass
import json
import os
import re
from urllib.error import HTTPError
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
    base = pr["base"]
    return (base["sha"], base["ref"], base["repo"]["full_name"],
            head["sha"], head["ref"], (head["repo"] or {}).get("full_name"),
            pr["state"], pr["draft"], pr["merged"], pr.get("merge_commit_sha"))


def reviewer_qualification(user, author, fetch):
    if not isinstance(author, dict) or type(author.get("id")) is not int:
        return None
    if user["id"] == author["id"] or user.get("type") == "Bot":
        return False
    name = user.get("login")
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}", name):
        return None
    try:
        data = fetch(f"collaborators/{name}/permission")
    except HTTPError as error:
        with error:
            if error.code in {401, 403, 404, 429} or 500 <= error.code <= 599:
                return None
            raise
    except OSError:
        return None
    if not isinstance(data, dict) or (data.get("user") or {}).get("id") != user["id"]:
        return None
    role = data.get("permission")
    if role in {"admin", "maintain", "write"}:
        return True
    return False if role in {"triage", "read", "none"} else None


def verify_pull_request(repository, source, expected, fetch=None):
    """Return exact-SHA membership and reviews, or fail on an incomplete observation."""
    num = expected["number"]
    route = f"pulls/{num}"
    if fetch is None:
        def fetch(path):
            return github_json(repository, path)

    pr = fetch(route)
    observed = fingerprint(pr)
    head, base = pr["head"], pr["base"]
    if (
        pr["number"] != num
        or pr["base"]["repo"]["full_name"].lower() != repository.lower()
        or (head["repo"] or {}).get("full_name", "").lower() != repository.lower()
        or head["ref"] != expected["source_branch"]
        or not COMMIT.fullmatch(head["sha"])
        or not base["ref"] or not COMMIT.fullmatch(base["sha"])
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
    approvals = [review["user"] for review in decisions.values()
                 if review["state"] == "APPROVED" and review["commit_id"] == source]
    qualification = [reviewer_qualification(user, pr.get("user"), fetch) for user in approvals]
    if fingerprint(fetch(route)) != observed:
        raise ValueError(f"GitHub PR #{num} changed during provenance verification; retry")
    state = "merged" if pr["merged"] else ("draft" if pr["state"] == "open" and pr["draft"] else pr["state"])
    return {
        "pull_request": f"https://github.com/{repository}/pull/{num}",
        "source_commit": source,
        "source_relation": "current head" if is_head else "historical PR commit",
        "head_commit": head["sha"],
        "base_ref": base["ref"],
        "base_commit": base["sha"],
        "pr_state": state,
        "merge_commit": pr["merge_commit_sha"] if pr["merged"] else None,
        "exact_commit_approvals": len(approvals),
        "observed_exact_commit_approvals": len(approvals),
        "qualifying_exact_commit_approvals": qualification.count(True) if None not in qualification else None,
        "verified_eligible_exact_commit_approvals": qualification.count(True),
        "unresolved_reviewer_eligibility": qualification.count(None),
    }
