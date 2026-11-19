# README HQ reader and evidence audit

Fixtures pin the README HQ baseline [f50e374](https://github.com/vixttha/README-HQ/commit/f50e3749dab90ddfe35894284d1660097a1fb1a8) and [learning pilot a8d97d0](https://github.com/vixttha/README-HQ/commit/a8d97d0559853538d4d814edf5c998e42cfec3d2). The script uses disposable Git fixtures, the shipped checker and Graphify compiler, the pinned Graphify MCP server, and an injected GitHub API response for the documented pull-request commit cap.

| Fixture | What the check measures |
| --- | --- |
| P41 | Git locates evidence on line 2, while Graphify records line 3 and accepts it over MCP. [Python line splitting](https://docs.python.org/3.12/library/stdtypes.html#str.splitlines) |
| P42 | A file-only inventory cannot include an existing archived WebP because the compiler decodes it as text. |
| P43 | A failed standalone receipt write overwrites the existing graph with bytes that do not match the retained prior receipt. |
| P44 | With a simulated 252-commit pull request, an omitted historical member is rejected based on the capped listing. [GitHub endpoint limit](https://docs.github.com/en/rest/pulls/pulls#list-commits-on-a-pull-request) |
| P45 | A declared browser entry point on a reserved invalid domain passes the checker without an unchecked-route diagnostic. [RFC 6761](https://www.rfc-editor.org/rfc/rfc6761.html#section-6.4) |
| P46 | Normal Python execution accepts a zero line coordinate and an empty anchor in the learning source verifier. |
| P47 | The pilot still recommends a technique after retirement in the canonical registry. |
| P48 | The fixed MCP query budget truncates a valid 48-reference feature. The verifier rejects it, while a larger query returns every edge. |
| P49 | The optional pull request manifest rejects a branch Git accepts. [GitHub branch names](https://docs.github.com/en/get-started/using-git/dealing-with-special-characters-in-branch-and-tag-names) |

The public workflow uses the existing Graphify lockfile with Python 3.12. Successful execution means the fixtures reproduced the baseline failures. The tests cover those behaviors only. Cross-project reliability and reader-facing README quality need separate evaluation on held-out projects.
