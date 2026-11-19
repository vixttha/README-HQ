# README HQ output and evidence boundaries

This audit uses [README HQ v0.0.6 at f50e374](https://github.com/vixttha/README-HQ/commit/f50e3749dab90ddfe35894284d1660097a1fb1a8). It exercises the shipped checker in a disposable checkout, the PR verifier with injected API responses, and a clean rebuild of the six release maps with the pinned Graphify engine and MCP service.

| Fixture | Observed behavior |
| --- | --- |
| B60 | The documented technique list exits with UnicodeEncodeError under an ASCII standard stream after printing a passing summary. UTF-8 emits all 17 techniques. [Python standard stream configuration](https://docs.python.org/3.12/using/cmdline.html#envvar-PYTHONIOENCODING) |
| B61 | A technique ID colliding with another technique's outcome key passes the checker. The control using the same value as an alias fails with a collision diagnostic. |
| B62 | Injected review pages give an exact observation at 999 reviews and fail at exactly 1,000, with no reviews beyond the tenth page. [GitHub review endpoint](https://docs.github.com/en/rest/pulls/reviews#list-reviews-for-a-pull-request) · [GitHub pagination](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api) |
| Clean control | The documented validation command succeeds and all six version maps, covering 17 records, rebuild and pass MCP verification at the original commit. |

The review-boundary check uses synthetic responses and makes no network requests. The passing control proves the documented default validation path for this checkout. It provides no score for a generated README or performance across adopter repositories.
