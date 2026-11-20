# README HQ repair batches

**Status** Batch 1 is verified on public runners in [draft PR #141](https://github.com/vixttha/README-HQ/pull/141). Later batches remain planned. The pending sequence follows the combined [v0.0.6.67 candidate](https://github.com/vixttha/README-HQ/commit/8d50caec2bc6fcb998994a1fd302294a029325f9) in [draft PR #68](https://github.com/vixttha/README-HQ/pull/68).

Work on one batch at a time, with up to 15 sequential checkpoints per batch. This schedule covers the 73 pending checkpoints from `v0.0.6.68` through `v0.0.6.140`. The original [v0.0.6.1–v0.0.6.67 plan](https://github.com/vixttha/README-HQ/blob/7f4562b8f44544bc9dd4b479fcd1bc30ca07ca94/plans/v0.0.6-repairs/README.md) remains the record for qualifying its open criteria. The already-planned .77 follow-up stays with [issue #5](https://github.com/vixttha/README-HQ/issues/5).

| Batch | Checkpoints | Count | Start after |
| --- | --- | ---: | --- |
| [Batch 1](#batch-1) | `v0.0.6.68`–`v0.0.6.82` | 15 | Public runner evidence recorded in draft PR #141 |
| [Batch 2](#batch-2) | `v0.0.6.83`–`v0.0.6.97` | 15 | `v0.0.6.82` passes and batch evidence is reviewed |
| [Batch 3](#batch-3) | `v0.0.6.98`–`v0.0.6.112` | 15 | `v0.0.6.97` passes and batch evidence is reviewed |
| [Batch 4](#batch-4) | `v0.0.6.113`–`v0.0.6.127` | 15 | `v0.0.6.112` passes and batch evidence is reviewed |
| [Batch 5](#batch-5) | `v0.0.6.128`–`v0.0.6.140` | 13 | `v0.0.6.127` passes and batch evidence is reviewed |

## Verification at each batch boundary

1. Follow the existing checkpoint order. Reproduce each issue at the verified starting revision and keep the fix linked to its checkpoint and issue.
2. **Every repair gets a post-fix debug pass before it can advance or be considered for merge.** Replay the original failure and a passing control, and check relevant regressions on the exact repair commit. Record the run, attempt, job, and available evidence on the checkpoint. Use standard public GitHub-hosted runners, with platform coverage and Graphify MCP where required by the underlying plan.
3. At the end of the batch, review all checkpoint outcomes and run the relevant combined regressions on the exact batch head. Carry an unresolved checkpoint forward as an explicit blocker. Record the batch head and evidence used to start the next batch. The [plan’s verification gate](README.md#debug-and-verification-gate-for-every-repair) lists the interim safeguards for Windows outcomes, Graphify failure evidence, and pinned dependency setup.
4. A verified batch is eligible for review. The owner controls merge and publication separately.

The final batch currently has 13 checkpoints. Append later confirmed issues in sequence. Fill the remaining 2 slots before opening another batch when new checkpoints are planned and this batch has yet to start; preserve recorded batch membership once execution starts.

[Full-stack triage](TRIAGE.md) · [Checkpoint ledger](checkpoints.json)

## Batch 1

Agent entry, public technique evidence, first-use output, Graphify recovery, and receipt and navigation basics.

[Draft PR #141](https://github.com/vixttha/README-HQ/pull/141) records all 15 repair SHAs at batch head [`cf7871e`](https://github.com/vixttha/README-HQ/commit/cf7871eb2af31c6f3da9af3acf92715b388f2868). [Exact checkpoint verification](https://github.com/vixttha/README-HQ/actions/runs/44646802615/attempts/1) passed 15 checks on Ubuntu and 14 applicable checks on Windows. The Graphify recovery check (.76) used Ubuntu. The [batch push](https://github.com/vixttha/README-HQ/actions/runs/44646364029/attempts/1) and [proposed merge](https://github.com/vixttha/README-HQ/actions/runs/44646414531/attempts/1) passed the combined Ubuntu, Windows, and Graphify jobs.

| Checkpoint | Issue | Planned repair |
| --- | --- | --- |
| [`v0.0.6.68`](https://github.com/vixttha/README-HQ/blob/ac07987cfe11d6592b8def2ff16b72a6b2c0a203/plans/v0.0.6.68-to-v0.0.6.77/README.md#v00668) | [#69](https://github.com/vixttha/README-HQ/issues/69) | Route agent onboarding to the intended revision |
| [`v0.0.6.69`](https://github.com/vixttha/README-HQ/blob/ac07987cfe11d6592b8def2ff16b72a6b2c0a203/plans/v0.0.6.68-to-v0.0.6.77/README.md#v00669) | [#70](https://github.com/vixttha/README-HQ/issues/70) | Require independent proof for technique sources |
| [`v0.0.6.70`](https://github.com/vixttha/README-HQ/blob/ac07987cfe11d6592b8def2ff16b72a6b2c0a203/plans/v0.0.6.68-to-v0.0.6.77/README.md#v00670) | [#71](https://github.com/vixttha/README-HQ/issues/71) | Verify first-use file outcomes |
| [`v0.0.6.71`](https://github.com/vixttha/README-HQ/blob/ac07987cfe11d6592b8def2ff16b72a6b2c0a203/plans/v0.0.6.68-to-v0.0.6.77/README.md#v00671) | [#72](https://github.com/vixttha/README-HQ/issues/72) | Partition within both Graphify limits |
| [`v0.0.6.72`](https://github.com/vixttha/README-HQ/blob/ac07987cfe11d6592b8def2ff16b72a6b2c0a203/plans/v0.0.6.68-to-v0.0.6.77/README.md#v00672) | [#73](https://github.com/vixttha/README-HQ/issues/73) | Resolve fetched refs in same-repository links |
| [`v0.0.6.73`](https://github.com/vixttha/README-HQ/blob/ac07987cfe11d6592b8def2ff16b72a6b2c0a203/plans/v0.0.6.68-to-v0.0.6.77/README.md#v00673) | [#74](https://github.com/vixttha/README-HQ/issues/74) | Validate responsive README images |
| [`v0.0.6.74`](https://github.com/vixttha/README-HQ/blob/ac07987cfe11d6592b8def2ff16b72a6b2c0a203/plans/v0.0.6.68-to-v0.0.6.77/README.md#v00674) | [#75](https://github.com/vixttha/README-HQ/issues/75) | Preserve receipts when a draft file is missing |
| [`v0.0.6.75`](https://github.com/vixttha/README-HQ/blob/ac07987cfe11d6592b8def2ff16b72a6b2c0a203/plans/v0.0.6.68-to-v0.0.6.77/README.md#v00675) | [#76](https://github.com/vixttha/README-HQ/issues/76) | Deduplicate learning selections by evidence identity |
| [`v0.0.6.76`](https://github.com/vixttha/README-HQ/blob/ac07987cfe11d6592b8def2ff16b72a6b2c0a203/plans/v0.0.6.68-to-v0.0.6.77/README.md#v00676) | [#77](https://github.com/vixttha/README-HQ/issues/77) | Keep a complete Graphify generation available |
| [`v0.0.6.77`](https://github.com/vixttha/README-HQ/blob/ac07987cfe11d6592b8def2ff16b72a6b2c0a203/plans/v0.0.6.68-to-v0.0.6.77/README.md#v00677) | [#5](https://github.com/vixttha/README-HQ/issues/5) | Bind historical guide links to their version rows |
| [`v0.0.6.78`](README.md#v00678) | [#78](https://github.com/vixttha/README-HQ/issues/78) | Bind audit receipts to the executing validator |
| [`v0.0.6.79`](README.md#v00679) | [#79](https://github.com/vixttha/README-HQ/issues/79) | Hash the learning registry snapshot used for recommendations |
| [`v0.0.6.80`](README.md#v00680) | [#80](https://github.com/vixttha/README-HQ/issues/80) | Use homepage precedence for repository-root fragments |
| [`v0.0.6.81`](README.md#v00681) | [#81](https://github.com/vixttha/README-HQ/issues/81) | Handle malformed registry structure as a normal CLI failure |
| [`v0.0.6.82`](README.md#v00682) | [#82](https://github.com/vixttha/README-HQ/issues/82) | Report the actual line of each broken link |

## Batch 2

Graphify evidence, package-context smoke checks, plan integrity, published links, and learning input handling.

| Checkpoint | Issue | Planned repair |
| --- | --- | --- |
| [`v0.0.6.83`](README.md#v00683) | [#83](https://github.com/vixttha/README-HQ/issues/83) | Handle Graphify references that resolve to one edge |
| [`v0.0.6.84`](README.md#v00684) | [#84](https://github.com/vixttha/README-HQ/issues/84) | Run smoke checks in the selected package context |
| [`v0.0.6.85`](README.md#v00685) | [#85](https://github.com/vixttha/README-HQ/issues/85) | Keep smoke output streams distinct |
| [`v0.0.6.86`](README.md#v00686) | [#86](https://github.com/vixttha/README-HQ/issues/86) | Bind each repair-plan partition to its approved source inventory |
| [`v0.0.6.87`](README.md#v00687) | [#87](https://github.com/vixttha/README-HQ/issues/87) | Resolve contradictory learning decisions for one observation |
| [`v0.0.6.88`](README.md#v00688) | [#88](https://github.com/vixttha/README-HQ/issues/88) | Distinguish Git LFS pointers from corrupt media |
| [`v0.0.6.89`](README.md#v00689) | [#89](https://github.com/vixttha/README-HQ/issues/89) | Account for rendered bare GFM URLs |
| [`v0.0.6.90`](README.md#v00690) | [#90](https://github.com/vixttha/README-HQ/issues/90) | Resolve the publication root deterministically |
| [`v0.0.6.91`](README.md#v00691) | [#91](https://github.com/vixttha/README-HQ/issues/91) | Document how CLI evidence becomes a reviewed technique receipt |
| [`v0.0.6.92`](README.md#v00692) | [#92](https://github.com/vixttha/README-HQ/issues/92) | Check explicitly expected HTTP error bodies |
| [`v0.0.6.93`](README.md#v00693) | [#93](https://github.com/vixttha/README-HQ/issues/93) | Resolve published GitHub refs with published semantics |
| [`v0.0.6.94`](README.md#v00694) | [#94](https://github.com/vixttha/README-HQ/issues/94) | Verify the repair plan’s acceptance text |
| [`v0.0.6.95`](README.md#v00695) | [#95](https://github.com/vixttha/README-HQ/issues/95) | Check animation frames or report partial media coverage |
| [`v0.0.6.96`](README.md#v00696) | [#96](https://github.com/vixttha/README-HQ/issues/96) | Record and verify the final destination of remote smoke requests |
| [`v0.0.6.97`](README.md#v00697) | [#97](https://github.com/vixttha/README-HQ/issues/97) | Report unknown technique IDs explicitly |

## Batch 3

PR and run provenance, execution isolation, inventory limits, rendered navigation, and failure receipts.

| Checkpoint | Issue | Planned repair |
| --- | --- | --- |
| [`v0.0.6.98`](README.md#v00698) | [#98](https://github.com/vixttha/README-HQ/issues/98) | Bind Graphify PR verification to the base ref and SHA |
| [`v0.0.6.99`](README.md#v00699) | [#99](https://github.com/vixttha/README-HQ/issues/99) | Validate smoke mode and matcher types before execution |
| [`v0.0.6.100`](README.md#v006100) | [#100](https://github.com/vixttha/README-HQ/issues/100) | Make Graphify binary inventory size behavior explicit |
| [`v0.0.6.101`](README.md#v006101) | [#101](https://github.com/vixttha/README-HQ/issues/101) | Isolate smoke commands from the audited Git repository |
| [`v0.0.6.102`](README.md#v006102) | [#102](https://github.com/vixttha/README-HQ/issues/102) | Include audit scope in adopter receipts |
| [`v0.0.6.103`](README.md#v006103) | [#103](https://github.com/vixttha/README-HQ/issues/103) | Distinguish GitHub run attempts and jobs in receipts |
| [`v0.0.6.104`](README.md#v006104) | [#104](https://github.com/vixttha/README-HQ/issues/104) | Make partial-clone object fetching explicit |
| [`v0.0.6.105`](README.md#v006105) | [#105](https://github.com/vixttha/README-HQ/issues/105) | Reject empty or separately label empty Graphify output |
| [`v0.0.6.106`](README.md#v006106) | [#106](https://github.com/vixttha/README-HQ/issues/106) | Validate the SVG element namespace |
| [`v0.0.6.107`](README.md#v006107) | [#107](https://github.com/vixttha/README-HQ/issues/107) | Parse GitHub plain-mode query parameters |
| [`v0.0.6.108`](README.md#v006108) | [#108](https://github.com/vixttha/README-HQ/issues/108) | Require rendered checkpoint and version tables |
| [`v0.0.6.109`](README.md#v006109) | [#109](https://github.com/vixttha/README-HQ/issues/109) | Reuse public GitHub metadata within one learning intake |
| [`v0.0.6.110`](README.md#v006110) | [#110](https://github.com/vixttha/README-HQ/issues/110) | Distinguish raw GitHub files from rendered heading destinations |
| [`v0.0.6.111`](README.md#v006111) | [#111](https://github.com/vixttha/README-HQ/issues/111) | Prevent draft reads through symlinked ancestors |
| [`v0.0.6.112`](README.md#v006112) | [#112](https://github.com/vixttha/README-HQ/issues/112) | Keep validation errors visible when receipt writes fail |

## Batch 4

Adopter scope, Windows CI, Quickstart discoverability, Graphify evidence retention, and smoke check diagnostics.

| Checkpoint | Issue | Planned repair |
| --- | --- | --- |
| [`v0.0.6.113`](README.md#v006113) | [#113](https://github.com/vixttha/README-HQ/issues/113) | Detect missing HTML image alternatives |
| [`v0.0.6.114`](README.md#v006114) | [#114](https://github.com/vixttha/README-HQ/issues/114) | Apply or reject adopter-only flags explicitly |
| [`v0.0.6.115`](README.md#v006115) | [#115](https://github.com/vixttha/README-HQ/issues/115) | Validate the learning request structure before processing |
| [`v0.0.6.116`](README.md#v006116) | [#116](https://github.com/vixttha/README-HQ/issues/116) | Verify Graphify inventory relations over MCP |
| [`v0.0.6.117`](README.md#v006117) | [#117](https://github.com/vixttha/README-HQ/issues/117) | Make Windows CI fail on the validator’s actual exit |
| [`v0.0.6.118`](README.md#v006118) | [#118](https://github.com/vixttha/README-HQ/issues/118) | Recognize the repository’s actual Quickstart |
| [`v0.0.6.119`](README.md#v006119) | [#119](https://github.com/vixttha/README-HQ/issues/119) | Make rich-text navigation coverage explicit |
| [`v0.0.6.120`](README.md#v006120) | [#120](https://github.com/vixttha/README-HQ/issues/120) | Publish a copyable first-action proof guide |
| [`v0.0.6.121`](README.md#v006121) | [#121](https://github.com/vixttha/README-HQ/issues/121) | Reuse parsed anchors for a pinned Markdown blob |
| [`v0.0.6.122`](README.md#v006122) | [#122](https://github.com/vixttha/README-HQ/issues/122) | Prepare reader dependencies before the retained plan check |
| [`v0.0.6.123`](README.md#v006123) | [#123](https://github.com/vixttha/README-HQ/issues/123) | Link Graphify rich-text evidence to physical source lines |
| [`v0.0.6.124`](README.md#v006124) | [#124](https://github.com/vixttha/README-HQ/issues/124) | Retain real Graphify evidence after a failed CI attempt |
| [`v0.0.6.125`](README.md#v006125) | [#125](https://github.com/vixttha/README-HQ/issues/125) | Publish plan partitions only after all staged manifests succeed |
| [`v0.0.6.126`](README.md#v006126) | [#126](https://github.com/vixttha/README-HQ/issues/126) | Make required first-action verification distinguish skipped coverage |
| [`v0.0.6.127`](README.md#v006127) | [#127](https://github.com/vixttha/README-HQ/issues/127) | Preserve actionable first-action failure diagnostics |

## Batch 5

Learning errors, first-action proof, homepage discovery, publication gates, dependency qualification, and reader-facing media and accessibility.

| Checkpoint | Issue | Planned repair |
| --- | --- | --- |
| [`v0.0.6.128`](README.md#v006128) | [#128](https://github.com/vixttha/README-HQ/issues/128) | Distinguish retryable GitHub errors from invalid learning evidence |
| [`v0.0.6.129`](README.md#v006129) | [#129](https://github.com/vixttha/README-HQ/issues/129) | Bind smoke results to the documented first action |
| [`v0.0.6.130`](README.md#v006130) | [#130](https://github.com/vixttha/README-HQ/issues/130) | Record the identity of a required probe before it is skipped |
| [`v0.0.6.131`](README.md#v006131) | [#131](https://github.com/vixttha/README-HQ/issues/131) | Identify GitHub-selected Org homepages |
| [`v0.0.6.132`](README.md#v006132) | [#132](https://github.com/vixttha/README-HQ/issues/132) | Qualify the owner-controlled publication gate |
| [`v0.0.6.133`](README.md#v006133) | [#133](https://github.com/vixttha/README-HQ/issues/133) | Verify every published revision of the active repair ledger |
| [`v0.0.6.134`](README.md#v006134) | [#134](https://github.com/vixttha/README-HQ/issues/134) | Separate observed reviews from qualifying approvals |
| [`v0.0.6.135`](README.md#v006135) | [#135](https://github.com/vixttha/README-HQ/issues/135) | Qualify the supported Python and Pillow dependency combination |
| [`v0.0.6.136`](README.md#v006136) | [#136](https://github.com/vixttha/README-HQ/issues/136) | Preserve canonical GitHub identity in learning receipts |
| [`v0.0.6.137`](README.md#v006137) | [#137](https://github.com/vixttha/README-HQ/issues/137) | Retain the matched learning source anchor |
| [`v0.0.6.138`](README.md#v006138) | [#138](https://github.com/vixttha/README-HQ/issues/138) | Verify the required local route behind a README Quickstart |
| [`v0.0.6.139`](README.md#v006139) | [#139](https://github.com/vixttha/README-HQ/issues/139) | Bind draft receipts to the checked media bytes |
| [`v0.0.6.140`](README.md#v006140) | [#140](https://github.com/vixttha/README-HQ/issues/140) | Honor accessible names in mixed Markdown and HTML image links |
