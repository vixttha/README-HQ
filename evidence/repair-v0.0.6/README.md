# README HQ repair review

The repair candidate covers the changes tracked in the [v0.0.6.1 through v0.0.6.67 plan](https://github.com/vixttha/README-HQ/blob/7f4562b8f44544bc9dd4b479fcd1bc30ca07ca94/plans/v0.0.6-repairs/README.md). The owner can review it in [draft PR #68](https://github.com/vixttha/README-HQ/pull/68).

| Public GitHub Actions run | Git commit checked out | Outcome |
| --- | --- | --- |
| [Repair branch](https://github.com/vixttha/README-HQ/actions/runs/44538439592) | `8d50caec2bc6fcb998994a1fd302294a029325f9` | Ubuntu reader, Windows reader, and Graphify passed |
| [Proposed merge tree](https://github.com/vixttha/README-HQ/actions/runs/44538450099) | `1475e0cea2b516b1577cf9a190708547d90548f7` | Ubuntu reader, Windows reader, and Graphify passed |

GitHub generated the second commit from the candidate and base `a7a989ffb6b664df86aae0ea01053ea2fc0a4405` for the pull request run. The default branch remained at that base at review time. The [receipt manifest](manifest.json) records all six job IDs, the original GitHub ZIP hashes, and the hashes of the 24 extracted JSON receipts published here.

## Checks performed

- Each reader job passed 10 tests and checked 193 local links, 159 imported files, 17 technique records, and two standalone snapshots. The receipts list 87 unchecked observations, comprising external routes and destinations outside the selected historical imports. A separate single-branch clone passed with 192 local links and 88 unchecked observations because one cross-ref was unavailable locally.
- Each Graphify job passed 11 template tests and six repair tests. It checked six release maps covering 17 version records and traversed all 67 checkpoint nodes across three plan maps. Each run also built the vendored self-map and read its 33 nodes and 51 edges over MCP.
- The archive source inventory was reconciled with pinned Git objects from the ten original source snapshots. The implementation also records SHA-256 digests and line bounds for 21 distinct public technique source documents.
- Local checks exercised a real autocrlf checkout, graph evidence readback with active Git replacement refs, and preservation of an existing graph when a tracked symlink was rejected.

## Acceptance still open

- The plan calls for a distinct commit and an issue-specific regression receipt at every checkpoint. Shared repairs are grouped in the implementation history, and the evidence here applies to the combined candidate. The Graphify count confirms plan coverage. The original acceptance checks and all 67 issue records remain open for review.
- [#1](https://github.com/vixttha/README-HQ/issues/1) stages the revised default homepage in the draft. Live publication awaits owner approval.
- [#24](https://github.com/vixttha/README-HQ/issues/24) needs the owner's decision on standalone reuse terms. The draft documents the current reuse and attribution boundary.
- [#58](https://github.com/vixttha/README-HQ/issues/58) adds the merge queue trigger. The hosted evidence covers the branch and GitHub's pull request test merge. A live queue event remains unverified.
