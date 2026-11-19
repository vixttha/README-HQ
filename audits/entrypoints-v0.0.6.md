# README HQ entry-point and provenance audit

The public audit pins [v0.0.6 at f50e374](https://github.com/vixttha/README-HQ/commit/f50e3749dab90ddfe35894284d1660097a1fb1a8). The script exercises the shipped Graphify CLI, the full six-map rebuild and MCP checks, the shipped workflow declaration, and the optional PR verifier with injected GitHub API responses.

| Fixture | Observed behavior |
| --- | --- |
| E56 | Adding the documented repository and SHA to the packaged Graphify self-map still fails because it refers to paths from the upstream template tree. |
| E57 | Duplicating the valid v0.0.6 row passes the README checker and all six Graphify rebuild and MCP checks. |
| E58 | The workflow declares pull-request checks for main and omits merge_group. The static finding applies to adopters using a GitHub merge queue with required README HQ checks. [GitHub merge queue requirements](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue#triggering-merge-group-checks-with-github-actions) |
| E59 | A simulated head change between PR metadata and commit list reads yields a stale head and a false historical-member classification. The stable control reports current head. [GitHub pull request API](https://docs.github.com/en/rest/pulls/pulls) |

A successful audit run means the fixtures reproduced the listed gaps. The fixtures do not evaluate editorial quality or measure reliability across an independent set of adopter repositories.
