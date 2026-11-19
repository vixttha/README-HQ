# README HQ repair pipeline v0.0.6.68–v0.0.6.77

**Status** Awaiting owner approval. Implementation starts at `v0.0.6.68` after approval. The plan is based on [the exact v0.0.6.67 candidate](https://github.com/vixttha/README-HQ/commit/8d50caec2bc6fcb998994a1fd302294a029325f9) in [draft PR #68](https://github.com/vixttha/README-HQ/pull/68). The [prior repair ledger](https://github.com/vixttha/README-HQ/blob/7f4562b8f44544bc9dd4b479fcd1bc30ca07ca94/plans/v0.0.6-repairs/README.md) retains checkpoints .1–.67. The [public Ubuntu audit](https://github.com/vixttha/README-HQ/actions/runs/44541511368/job/135620777064) reproduced all ten findings. [Machine-readable ledger](checkpoints.json).

| Checkpoint | Issue | Repair | Start after |
| --- | --- | --- | --- |
| `v0.0.6.68` | [#69](https://github.com/vixttha/README-HQ/issues/69) | Route agent onboarding to the intended revision | Owner approval |
| `v0.0.6.69` | [#70](https://github.com/vixttha/README-HQ/issues/70) | Require independent proof for technique sources | `v0.0.6.68` |
| `v0.0.6.70` | [#71](https://github.com/vixttha/README-HQ/issues/71) | Verify first-use file outcomes | `v0.0.6.69` |
| `v0.0.6.71` | [#72](https://github.com/vixttha/README-HQ/issues/72) | Partition within both Graphify limits | `v0.0.6.70` |
| `v0.0.6.72` | [#73](https://github.com/vixttha/README-HQ/issues/73) | Resolve fetched refs in same-repository links | `v0.0.6.71` |
| `v0.0.6.73` | [#74](https://github.com/vixttha/README-HQ/issues/74) | Validate responsive README images | `v0.0.6.72` |
| `v0.0.6.74` | [#75](https://github.com/vixttha/README-HQ/issues/75) | Preserve receipts when a draft file is missing | `v0.0.6.73` |
| `v0.0.6.75` | [#76](https://github.com/vixttha/README-HQ/issues/76) | Deduplicate learning selections by evidence identity | `v0.0.6.74` |
| `v0.0.6.76` | [#77](https://github.com/vixttha/README-HQ/issues/77) | Keep a complete Graphify generation available | `v0.0.6.75` |
| `v0.0.6.77` | [#5](https://github.com/vixttha/README-HQ/issues/5) | Bind historical guide links to their version rows | `v0.0.6.76` |

The nine new issues take the first nine slots in issue order. The version-index follow-up [stays on #5](https://github.com/vixttha/README-HQ/issues/5#issuecomment-7011679375) and occupies the final slot. Later audit findings stay in GitHub Issues without changing this sequence.

## Acceptance by checkpoint

### v0.0.6.68

Follow the draft README and AGENTS instructions from a clean clone. The resolved revision exposes the adopter CLI and the learning intake. Verify the published route at promotion time under its separate owner approval. [#69](https://github.com/vixttha/README-HQ/issues/69)

### v0.0.6.69

Reject a synthetic registry entry even when its inventory row is added alongside it. Accept a source verified against independent public Git evidence, and report duplicate or malformed inventory rows. [#70](https://github.com/vixttha/README-HQ/issues/70)

### v0.0.6.70

Reject an unchanged tracked file as evidence of generation. Accept a newly generated file or an explicitly verified update, checking the expected digest when specified. [#71](https://github.com/vixttha/README-HQ/issues/71)

### v0.0.6.71

Keep ordering and coverage across 32-feature and 64-source-file boundaries. Build the 25-checkpoint, 75-file case successfully, verify every manifest over MCP, and exercise shared paths plus the optional implementation relation. [#72](https://github.com/vixttha/README-HQ/issues/72)

### v0.0.6.72

Check a nested branch held only in the origin-tracking namespace. Cover local/fetched disagreement, same-named tags, a pinned SHA, and a genuinely unfetched ref. [#73](https://github.com/vixttha/README-HQ/issues/73)

### v0.0.6.73

Report the missing dark-mode source when the fallback succeeds. Validate a correct light/dark pair and preserve the current fallback and accessible-name checks. [#74](https://github.com/vixttha/README-HQ/issues/74)

### v0.0.6.74

Return a failing exit and write parseable JSON with the original diagnostic when the tracked README is deleted. Confirm a successful check still records source digests. [#75](https://github.com/vixttha/README-HQ/issues/75)

### v0.0.6.75

Verify an alias-only edit reuses the receipt. Changing the selected evidence or commit should yield a distinct receipt. [#76](https://github.com/vixttha/README-HQ/issues/76)

### v0.0.6.76

Read while a replacement is staged and promoted. The reader can resolve an intact prior or new graph and matching receipt. Verify recovery from interrupted promotion. [#77](https://github.com/vixttha/README-HQ/issues/77)

### v0.0.6.77

Reject a v0.0.5 row routed to the v0.0.4 guide even when the map remains correct. Accept the canonical row and preserve the existing wrong-map and current-version controls. [#5](https://github.com/vixttha/README-HQ/issues/5)

## Execution and evidence

1. After owner approval, start with the pinned candidate. For each checkpoint, reproduce the linked finding on the preceding verified revision and retain a distinct repair commit.
2. Run the focused regression and the applicable existing checks on standard public GitHub-hosted runners. Use Ubuntu and Windows for reader and CLI behavior and Ubuntu with Graphify MCP for graph changes.
3. Record the exact commit, run and job links, expected and observed outcomes, and receipt or artifact on the linked issue before starting the next checkpoint. Keep the original .1–.67 acceptance work and the open merge-queue and standalone reuse decisions visible.
4. After .77, verify the combined candidate on public runners and present the result for owner review. The draft, main-branch merge, release, and promotion of published refs remain subject to the owner's approval.
