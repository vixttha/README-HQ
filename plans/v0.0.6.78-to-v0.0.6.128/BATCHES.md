# README HQ repair batches

**Status** Batches 1–4 are verified on public runners in [draft PR #141](https://github.com/vixttha/README-HQ/pull/141), [draft PR #142](https://github.com/vixttha/README-HQ/pull/142), [draft PR #144](https://github.com/vixttha/README-HQ/pull/144), and [draft PR #145](https://github.com/vixttha/README-HQ/pull/145). Batch 5 remains planned. The pending sequence follows the combined [v0.0.6.67 candidate](https://github.com/vixttha/README-HQ/commit/8d50caec2bc6fcb998994a1fd302294a029325f9) in [draft PR #68](https://github.com/vixttha/README-HQ/pull/68).

Work on one batch at a time, with up to 15 sequential checkpoints per batch. This schedule covers the 73 checkpoints from `v0.0.6.68` through `v0.0.6.140`. The original [v0.0.6.1–v0.0.6.67 plan](https://github.com/vixttha/README-HQ/blob/7f4562b8f44544bc9dd4b479fcd1bc30ca07ca94/plans/v0.0.6-repairs/README.md) remains the record for qualifying its open criteria. The already-planned .77 follow-up stays with [issue #5](https://github.com/vixttha/README-HQ/issues/5).

| Batch | Checkpoints | Count | Start after |
| --- | --- | ---: | --- |
| [Batch 1](#batch-1) | `v0.0.6.68`–`v0.0.6.82` | 15 | Public runner evidence recorded in draft PR #141 |
| [Batch 2](#batch-2) | `v0.0.6.83`–`v0.0.6.97` | 15 | Public runner evidence recorded in draft PR #142 |
| [Batch 3](#batch-3) | `v0.0.6.98`–`v0.0.6.112` | 15 | Public runner evidence recorded in draft PR #144 |
| [Batch 4](#batch-4) | `v0.0.6.113`–`v0.0.6.127` | 15 | Public runner evidence recorded in draft PR #145 |
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

[Draft PR #141](https://github.com/vixttha/README-HQ/pull/141) records all 15 repair SHAs and the CodeRabbit follow-up at batch head [`774bf78`](https://github.com/vixttha/README-HQ/commit/774bf783850162f731f3e38aff0f52b99a5202fc). [Exact checkpoint verification](https://github.com/vixttha/README-HQ/actions/runs/44647908856/attempts/1) passed 15 checks on Ubuntu and 14 applicable checks on Windows. The Graphify recovery check (.76) used Ubuntu. The [batch push](https://github.com/vixttha/README-HQ/actions/runs/44647859983/attempts/1) and [proposed merge](https://github.com/vixttha/README-HQ/actions/runs/44647866459/attempts/1) passed the combined Ubuntu, Windows, and Graphify jobs.

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

[Draft PR #142](https://github.com/vixttha/README-HQ/pull/142) records 15 checkpoint commits and three follow-ups at [`941f6b49`](https://github.com/vixttha/README-HQ/commit/941f6b49aac6ab78076f088ad6b58a00e9f03477). [Exact checkpoint verification](https://github.com/vixttha/README-HQ/actions/runs/44657221341/attempts/1) passed all 15 checkpoints on Ubuntu and all 14 applicable checkpoints on Windows. Graphify .83 ran on Ubuntu. Both platforms passed all three follow-ups and reproduced the GIF error on the predecessor. The [batch push](https://github.com/vixttha/README-HQ/actions/runs/44657160697/attempts/1) and [proposed merge](https://github.com/vixttha/README-HQ/actions/runs/44657168441/attempts/1) passed Ubuntu, Windows, and Graphify MCP.

[CodeRabbit](https://github.com/vixttha/README-HQ/pull/142#pullrequestreview-5986271037) found a fenced Markdown heading could hide an acceptance obligation. The fix and regression are in [`0009e519`](https://github.com/vixttha/README-HQ/commit/0009e51957713dde538ffc8d1ee0f7aae9bbf2ad). CodeRabbit marked the [thread](https://github.com/vixttha/README-HQ/pull/142#discussion_r4637469492) addressed and it is resolved. The earlier [navigation follow-up](https://github.com/vixttha/README-HQ/commit/cd3cc3c07e528b3222c9b1da4579191e6920d7a3) validates LFS pointer extension syntax and bounds bare URL scanning.

[CodeRabbit found a truncated GIF descriptor could stop the audit](https://github.com/vixttha/README-HQ/pull/142#pullrequestreview-5986366981). The [repair](https://github.com/vixttha/README-HQ/commit/941f6b49aac6ab78076f088ad6b58a00e9f03477) reports the image error, retains a failure receipt, and continues checking later links. [CodeRabbit check for the repair](https://github.com/vixttha/README-HQ/runs/136027206662).

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

[Draft PR #144](https://github.com/vixttha/README-HQ/pull/144) records 15 checkpoint commits and three follow-ups at [`dc8ef217`](https://github.com/vixttha/README-HQ/commit/dc8ef21763240168227d67445f02fc4a05ea071c). The [checkpoint run](https://github.com/vixttha/README-HQ/actions/runs/44662359197/attempts/1) reproduced and passed all 15 checks on Ubuntu and all 12 applicable checks on Windows. Graphify checkpoints .98, .100, and .105 ran on Ubuntu. Both platforms passed the follow-up checks. The [batch push](https://github.com/vixttha/README-HQ/actions/runs/44662322632/attempts/1) and [proposed merge](https://github.com/vixttha/README-HQ/actions/runs/44662329172/attempts/1) passed Ubuntu, Windows, and Graphify MCP.

[CodeRabbit’s first review](https://github.com/vixttha/README-HQ/pull/144#pullrequestreview-5986613884) found five problems in PR fixtures, missing Git blobs, partial-clone smoke preparation, Markdown line endings, and qualified raw refs. The [first review follow-up](https://github.com/vixttha/README-HQ/commit/393487e218a4f0cb9475a87189601ef9241636eb) addressed them. The [next review](https://github.com/vixttha/README-HQ/pull/144#pullrequestreview-5986678859) found a missed GitHub secondary-rate-limit response. The [rate-limit follow-up](https://github.com/vixttha/README-HQ/commit/dc8ef21763240168227d67445f02fc4a05ea071c) distinguishes it from an ordinary forbidden response. [Final CodeRabbit check](https://github.com/vixttha/README-HQ/runs/136043447764).

The [Ubuntu rerun](https://github.com/vixttha/README-HQ/actions/runs/44662322632/attempts/2) produced a distinct attempt-2 ZIP under the same run ID. The downloaded [attempt-1 ZIP](https://github.com/vixttha/README-HQ/actions/runs/44662322632/artifacts/14594984768) and [attempt-2 ZIP](https://github.com/vixttha/README-HQ/actions/runs/44662322632/artifacts/14596153023) match GitHub’s published digests.

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

[Draft PR #145](https://github.com/vixttha/README-HQ/pull/145) records 15 repair commits and six follow-ups at [`921609e7`](https://github.com/vixttha/README-HQ/commit/921609e7a037d0ca37c66d8ef6438642cbeb17ea). [Exact checkpoint run](https://github.com/vixttha/README-HQ/actions/runs/44673218112/attempts/1) reproduced and passed all 15 checkpoints on Ubuntu and all 11 applicable checkpoints on Windows. Graphify checkpoints .116 and .122–.124 ran on Ubuntu. Both systems passed all six follow-ups and replayed the CodeRabbit findings on the predecessor. The [batch push](https://github.com/vixttha/README-HQ/actions/runs/44673187407/attempts/1) and [proposed merge](https://github.com/vixttha/README-HQ/actions/runs/44673195360/attempts/1) passed Ubuntu, Windows, and Graphify MCP.

[The clean retained-plan job](https://github.com/vixttha/README-HQ/actions/runs/44673218112/job/136078814812) installed the hashed reader dependencies before validating the candidate and running Graphify MCP. The workflow accepted the published plan byte for byte and rejected a prose-only change outside the checkpoint table. In the intentional failure controls, [Windows retained the failed validator receipt](https://github.com/vixttha/README-HQ/actions/runs/44673218127/artifacts/14599849742) and skipped the next command. The [Graphify failure archive](https://github.com/vixttha/README-HQ/actions/runs/44673218127/artifacts/14600828501) retains the diagnostic for the injected plan mismatch and six previously verified maps from that attempt. Both control jobs kept their failed status.

[CodeRabbit](https://github.com/vixttha/README-HQ/pull/145#pullrequestreview-5987209395) found three Quickstart edge cases and raised an HTML image naming case separately. The [first follow-up](https://github.com/vixttha/README-HQ/commit/bd393f5e023178a89ff36c4fda803590b5d5fbac) handles Usage, formatted headings, nested action sections, and nonblank `aria-label` for images. The [second review](https://github.com/vixttha/README-HQ/pull/145#pullrequestreview-5987282066) found a linked image could still be unnamed when it used only `srcset`. The [responsive-image follow-up](https://github.com/vixttha/README-HQ/commit/9236e5ee294feee4f9b7e69e12758da0ab1db322) covers that case. The [third review](https://github.com/vixttha/README-HQ/pull/145#pullrequestreview-5987342693) found that hidden images could still name links and called out the missing full-file plan comparison. The [next follow-up](https://github.com/vixttha/README-HQ/commit/fed6ae338df9d984ce9fe767cd1f0857c89a770f) covers both. The [last finding](https://github.com/vixttha/README-HQ/pull/145#pullrequestreview-5987394078) showed that hidden containers could still contribute image names. The [final follow-up](https://github.com/vixttha/README-HQ/commit/921609e7a037d0ca37c66d8ef6438642cbeb17ea) checks ancestor visibility. All six review threads are resolved. The [exact-head CodeRabbit check](https://github.com/vixttha/README-HQ/runs/136080253566) passed at `921609e7` with no new actionable findings.

All 10 downloaded evidence ZIPs matched GitHub’s SHA-256 digests. The checkpoint receipts match all 21 Git commit, parent, and tree records. [Ubuntu receipt](https://github.com/vixttha/README-HQ/actions/runs/44673218112/artifacts/14601265274) · [Windows receipt](https://github.com/vixttha/README-HQ/actions/runs/44673218112/artifacts/14601071769).

<details>
<summary>Verified artifact ZIPs and SHA-256 digests</summary>

| Evidence | Artifact ID | SHA-256 |
| --- | --- | --- |
| Checkpoint replay, Ubuntu | [14601265274](https://github.com/vixttha/README-HQ/actions/runs/44673218112/artifacts/14601265274) | `a79c1d1a897cb2fa7e2200b24cbe4171631f3efd5dcf22e27fd4ab9a243bc068` |
| Checkpoint replay, Windows | [14601071769](https://github.com/vixttha/README-HQ/actions/runs/44673218112/artifacts/14601071769) | `41037147eed6104835910c3809ab6620b7cc5298a8163c02049fa06fa1727972` |
| Branch reader, Ubuntu | [14600908072](https://github.com/vixttha/README-HQ/actions/runs/44673187407/artifacts/14600908072) | `88e36ac7ee48be2efc96af7f765948d04319efcc5a15e7a3d2377089eb0bdfc4` |
| Branch reader, Windows | [14601425348](https://github.com/vixttha/README-HQ/actions/runs/44673187407/artifacts/14601425348) | `d14e92504c574b624df21cacee6ceee73fced4bbc3b30a728457a6d555190a2a` |
| Branch Graphify MCP | [14600074188](https://github.com/vixttha/README-HQ/actions/runs/44673187407/artifacts/14600074188) | `88cff924b5b2b20b4435b240b2144080872e9880ef4226ccba65d0acdc913388` |
| Proposed merge reader, Ubuntu | [14600808104](https://github.com/vixttha/README-HQ/actions/runs/44673195360/artifacts/14600808104) | `4e0a6a7da7424c172cf176dff61601a462f8fe164f737049212779a02636efd4` |
| Proposed merge reader, Windows | [14601130962](https://github.com/vixttha/README-HQ/actions/runs/44673195360/artifacts/14601130962) | `10c055c6621e17dad237d7b261cffd0f5f1317c6457dd1c0c65bba35fb62e874` |
| Proposed merge Graphify MCP | [14600533487](https://github.com/vixttha/README-HQ/actions/runs/44673195360/artifacts/14600533487) | `c0d5429fd45de0c484a97cc0b42f79622844bfc617805628304dea479292f760` |
| Windows failure control | [14599849742](https://github.com/vixttha/README-HQ/actions/runs/44673218127/artifacts/14599849742) | `c32b0757af033c1a5119c23be567e0aba298dde141e98d99bd85e5e62f25017f` |
| Graphify failure control | [14600828501](https://github.com/vixttha/README-HQ/actions/runs/44673218127/artifacts/14600828501) | `5876f0d5dcccbff26fe3e55e45eda6cbf96cb68e918150a747902ffa8c204762` |

</details>

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

[Draft PR #151](https://github.com/vixttha/README-HQ/pull/151) contains 13 checkpoint commits and three follow-ups at [`aa07e7ab`](https://github.com/vixttha/README-HQ/commit/aa07e7ab89e4bb2d3d28c9d0a5302394b9b1839b), stacked on verified Batch 4 at `921609e7`.

The [exact checkpoint replay](https://github.com/vixttha/README-HQ/actions/runs/44685725350/attempts/1) passed 13/13 on Ubuntu and 9/9 applicable checkpoints on Windows. Checkpoints .132, .133, .136, and .137 ran on Ubuntu. Both systems passed all three follow-ups. Both receipts match all 16 commits, their parents, and their Git trees.

The [branch run](https://github.com/vixttha/README-HQ/actions/runs/44685722539/attempts/1) and [proposed merge run](https://github.com/vixttha/README-HQ/actions/runs/44685729266/attempts/1) each passed 91 reader tests per OS, 15 Graphify template tests, and 11 Graphify integration tests. Graphify MCP verified ten maps on each revision. The [proposed merge](https://github.com/vixttha/README-HQ/commit/ae460cb3658401e181a06148926bf5f58f2737da) and the draft head have the same tree.

Pillow 13.0.0 passed hashed wheel installation and reader tests on public Ubuntu and Windows with Python 3.11 through 3.15. The [live controls ZIP](https://github.com/vixttha/README-HQ/actions/runs/44685725350/artifacts/14606297122) records GitHub’s selected Org homepage and the readback for `main`. The [active planning branch workflow](https://github.com/vixttha/README-HQ/actions/runs/44685215438/attempts/1) verified the 63-checkpoint ledger after the visibility repair.

The publication policy fixture passed. The live readback at `a7a989ff` reports that `main` is unprotected and has none of the three proposed required check contexts. Live settings and the owner’s exact-SHA publication decision remain separate under [#132](https://github.com/vixttha/README-HQ/issues/132#issuecomment-7031938898).

CodeRabbit reported [eight initial findings](https://github.com/vixttha/README-HQ/pull/151#pullrequestreview-5988216302) and [two findings on the first follow-up](https://github.com/vixttha/README-HQ/pull/151#pullrequestreview-5988277263). The final replay covered the corrections and confirmed the timeout and quoted-literal cases. The [exact-head CodeRabbit check](https://github.com/vixttha/README-HQ/runs/136119772280) is in progress.

<details>
<summary>Verified artifact ZIPs and SHA-256 digests</summary>

| Evidence | Artifact ID | SHA-256 |
| --- | --- | --- |
| Ubuntu checkpoint replay | [14606770742](https://github.com/vixttha/README-HQ/actions/runs/44685725350/artifacts/14606770742) | `827e6082c377ac2a77376c08c5f8649ab9e28a61fed5f80c5833a773705fbe61` |
| Windows checkpoint replay | [14606127780](https://github.com/vixttha/README-HQ/actions/runs/44685725350/artifacts/14606127780) | `c0f2faafc8793ebb6656408014b0e0e9e5392211a7c7b780ee3bb454afae7966` |
| Branch reader, Ubuntu | [14606596699](https://github.com/vixttha/README-HQ/actions/runs/44685722539/artifacts/14606596699) | `b66ff2900f85da415ae81c83485c5e897ec0b1f224537a82bc96b8c3047c9922` |
| Branch reader, Windows | [14606547176](https://github.com/vixttha/README-HQ/actions/runs/44685722539/artifacts/14606547176) | `77df4212e8c9c1d9bf39d2dec9a2c3113d2cd922480d11320485f0e046f13b19` |
| Branch Graphify MCP | [14605784035](https://github.com/vixttha/README-HQ/actions/runs/44685722539/artifacts/14605784035) | `126a8eb397e37c1bb72ac1a3d41bbe6b3f27d9ee78f81e0ea2c70eaa209e9256` |
| Proposed merge reader, Ubuntu | [14606611339](https://github.com/vixttha/README-HQ/actions/runs/44685729266/artifacts/14606611339) | `7b84e0da16c4c577a34485c43f6b9a0dacf9ef30676ff1b1d872df3a5bd4e6fc` |
| Proposed merge reader, Windows | [14606920596](https://github.com/vixttha/README-HQ/actions/runs/44685729266/artifacts/14606920596) | `74f11a0128bcec2a2b494fc20f805f1b75af8beeaa105db80af5ec84676af019` |
| Proposed merge Graphify MCP | [14606556783](https://github.com/vixttha/README-HQ/actions/runs/44685729266/artifacts/14606556783) | `e8015af6f1c28638e3fa5fe622e0775ecc2a55fc731ebf7f5251ca25294ae6a2` |
| Org homepage, active plan, and publication rules | [14606297122](https://github.com/vixttha/README-HQ/actions/runs/44685725350/artifacts/14606297122) | `7b028085125590a2b799f0923ac83642494674d9f14055ffd492499ff73d67c1` |
| Pillow, Ubuntu, Python 3.11 | [14605977811](https://github.com/vixttha/README-HQ/actions/runs/44685725350/artifacts/14605977811) | `223120b15fe694b9fef79b40ffbbbaccf1b553cd1c684cae391bd49e6c321863` |
| Pillow, Ubuntu, Python 3.13 | [14605798791](https://github.com/vixttha/README-HQ/actions/runs/44685725350/artifacts/14605798791) | `0d366fab87bafa85cb831a3869797c3056744e1b74905e4baf502f963bde8f54` |
| Pillow, Ubuntu, Python 3.14 | [14606840565](https://github.com/vixttha/README-HQ/actions/runs/44685725350/artifacts/14606840565) | `20bbd632ca870cc4ec13dbc7b2bf8582a5fa8ab63cf825c638648a5e55d765bc` |
| Pillow, Ubuntu, Python 3.15 | [14606940017](https://github.com/vixttha/README-HQ/actions/runs/44685725350/artifacts/14606940017) | `1e63f3ebfe6b1514a7a9a0ea0a3659cd5adc12b9f4c6b0e057f7130834c667f5` |
| Pillow, Windows, Python 3.11 | [14605958670](https://github.com/vixttha/README-HQ/actions/runs/44685725350/artifacts/14605958670) | `dfef8d5bd7dcaed1acd92cedc5ef2de88af3f4d06aab9779b6ce895b8650e0a3` |
| Pillow, Windows, Python 3.13 | [14606771134](https://github.com/vixttha/README-HQ/actions/runs/44685725350/artifacts/14606771134) | `1c24dad96b0f1685bcd5d70e4262d333ef8c6cec86fadce415ee59346a35f82c` |
| Pillow, Windows, Python 3.14 | [14606905671](https://github.com/vixttha/README-HQ/actions/runs/44685725350/artifacts/14606905671) | `21aa3dc3392f251c0f9eff3697e61d57e18b33085023ef45eab28a00309e4f47` |
| Pillow, Windows, Python 3.15 | [14605784463](https://github.com/vixttha/README-HQ/actions/runs/44685725350/artifacts/14605784463) | `9e8672c6789fb5256dd64688df67b8c340c7128329b84bc35d6a7ff87df3ecd2` |

</details>

| Checkpoint | Issue | Planned repair |
| --- | --- | --- |
| [`v0.0.6.128`](README.md#v006128) | [#128](https://github.com/vixttha/README-HQ/issues/128#issuecomment-7031939204) | Distinguish retryable GitHub errors from invalid learning evidence |
| [`v0.0.6.129`](README.md#v006129) | [#129](https://github.com/vixttha/README-HQ/issues/129#issuecomment-7031935946) | Bind smoke results to the documented first action |
| [`v0.0.6.130`](README.md#v006130) | [#130](https://github.com/vixttha/README-HQ/issues/130#issuecomment-7031935673) | Record the identity of a required probe before it is skipped |
| [`v0.0.6.131`](README.md#v006131) | [#131](https://github.com/vixttha/README-HQ/issues/131#issuecomment-7031937685) | Identify GitHub-selected Org homepages |
| [`v0.0.6.132`](README.md#v006132) | [#132](https://github.com/vixttha/README-HQ/issues/132#issuecomment-7031938898) | Qualify the owner-controlled publication gate |
| [`v0.0.6.133`](README.md#v006133) | [#133](https://github.com/vixttha/README-HQ/issues/133#issuecomment-7031936880) | Verify every published revision of the active repair ledger |
| [`v0.0.6.134`](README.md#v006134) | [#134](https://github.com/vixttha/README-HQ/issues/134#issuecomment-7031938484) | Separate observed reviews from qualifying approvals |
| [`v0.0.6.135`](README.md#v006135) | [#135](https://github.com/vixttha/README-HQ/issues/135#issuecomment-7031937418) | Qualify the supported Python and Pillow dependency combination |
| [`v0.0.6.136`](README.md#v006136) | [#136](https://github.com/vixttha/README-HQ/issues/136#issuecomment-7031937933) | Preserve canonical GitHub identity in learning receipts |
| [`v0.0.6.137`](README.md#v006137) | [#137](https://github.com/vixttha/README-HQ/issues/137#issuecomment-7031936577) | Retain the matched learning source anchor |
| [`v0.0.6.138`](README.md#v006138) | [#138](https://github.com/vixttha/README-HQ/issues/138#issuecomment-7031936329) | Verify the required local route behind a README Quickstart |
| [`v0.0.6.139`](README.md#v006139) | [#139](https://github.com/vixttha/README-HQ/issues/139#issuecomment-7031938195) | Bind draft receipts to the checked media bytes |
| [`v0.0.6.140`](README.md#v006140) | [#140](https://github.com/vixttha/README-HQ/issues/140#issuecomment-7031937163) | Honor accessible names in mixed Markdown and HTML image links |
