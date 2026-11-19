# README HQ assurance audit

The audit exercises the released baseline [f50e374](https://github.com/vixttha/README-HQ/commit/f50e3749dab90ddfe35894284d1660097a1fb1a8), the [learning pilot](https://github.com/vixttha/README-HQ/tree/a8d97d0559853538d4d814edf5c998e42cfec3d2/learning), and the previous [24-checkpoint plan](https://github.com/vixttha/README-HQ/tree/6d011b0e2e2dd521074819e688b802e786fb5d5a). Disposable fixtures test pass/fail behavior and leave the inspected source revisions pinned.

| Check | Evidence |
| --- | --- |
| Q25 · Source line navigation | All six committed map outlines use rendered Markdown URLs with line-number fragments. GitHub's documented line-link format uses plain-file mode. [GitHub permalink format](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-a-permanent-link-to-a-code-snippet#linking-to-markdown) |
| Q26 · Source anchor meaning | A code fence containing heading-like or bullet-like text wins over the actual rendered notes. |
| Q27 · First-use outcomes | The README checker passes both a nonzero command and a zero-exit command with the wrong output. The audit executes its own two harmless fixtures directly. |
| Q28 · Media and accessible navigation | A corrupt PNG and a linked image with no text alternative both pass. [W3C functional images](https://www.w3.org/WAI/tutorials/images/functional/) |
| Q29 · Complete diagnostics | One malformed URL blocks reporting a separate, independently failing target in the same file. |
| Q30 · Target provenance | A recommendation persists when the target evidence is absent and its target receipt points to a nonexistent record. |
| Q31 · Verification under runtime options | Optimized Python skips the pilot's blob and source-anchor assertions, then prints a successful source observation for the same input. [Python assert statement](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement) |
| Q32 · Durable acceptance evidence | The inspected workflows print their outcomes into GitHub logs or summaries. Graphify stores graph-generation receipts. The audited verification runs carry no downloadable package for independent first-use and learning acceptance. [GitHub retention settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#configuring-the-retention-period-for-checks-workflow-runs-commit-statuses-artifacts-and-logs-in-your-repository) |

## Candidate acceptance

1. Track distinct outcomes for a workflow run and its output README. Record failed, unsupported, deliberately skipped, and incomplete cases explicitly. A skipped or inapplicable check carries no passing behavioral evidence.
2. Maintain held-out, pinned repositories spanning the supported project types, documentation placements, execution paths, scopes, and modes. Keep learning references and closely related forks out of the held-out sample. Freeze the evaluation rubric and corpus before scoring a candidate.
3. For a supported project, measure whether the workflow reaches a usable output and whether the README's documented first action produces its expected result. Use declared, authorized smoke commands tied to source. For docs-only projects, verify the actual reader path.
4. For quality, review source accuracy, audience fit, navigation, clarity, accessible media, and usefulness. Use mechanical checks for stream, link, media, and result integrity. Record a separate reviewer verdict for editorial quality and inspect ambiguous claims.
5. Preserve a machine-readable receipt tied to the exact candidate SHA, workflow and job IDs, selected target evidence, comparison conditions, tool versions, expected and actual results, environment, status, and relevant hashes. Link to the live CI run and keep accepted receipts in the appropriate public or private evidence store.

The fixtures demonstrate individual failure modes. A 99% claim needs independent outcome measurements and uncertainty bounds for both workflow reliability and README quality on the held-out sample.
