<!-- catalog
{
  "title": "Show how to retrieve every page of results",
  "summary": "Give an example that spans multiple pages, follows the continuation link or cursor, and states when to stop.",
  "tasks": [
    "first-result",
    "quickstart"
  ],
  "tags": [
    "automation"
  ],
  "aliases": [
    "api pagination"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "A service limits result count or returns continuation tokens."
}
-->

# Show how to retrieve every page of results

**Use when.** A service limits result count or returns continuation tokens.

**Reader task.** First result and recovery.

**Practice.** Give an example that spans multiple pages, follows the continuation link or cursor, and states when to stop. GitHub’s REST guide demonstrates following the next-page link until it is absent.

**Example (illustrative).** Show the first request and how to follow the returned cursor until it is absent.

**Result to check.** A fixture spanning several pages returns each expected item exactly once.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [GitHub REST pagination](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api)
