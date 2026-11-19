# README HQ repair pipeline v0.0.6.78–v0.0.6.128

**Status** Active planning. Implementation awaits owner approval. The sequence continues after checkpoint `v0.0.6.77` is verified.

The plan covers 51 open GitHub issues at the planning snapshot. Checkpoint numbers match issues #78–#128 one to one, with a separate repair commit and a post-fix debug gate for each issue. The observed baseline is [draft PR #68 at `8d50cae`](https://github.com/vixttha/README-HQ/commit/8d50caec2bc6fcb998994a1fd302294a029325f9). [Checkpoints .1–.67](https://github.com/vixttha/README-HQ/blob/7f4562b8f44544bc9dd4b479fcd1bc30ca07ca94/plans/v0.0.6-repairs/README.md) · [Checkpoints .68–.77](https://github.com/vixttha/README-HQ/blob/ac07987cfe11d6592b8def2ff16b72a6b2c0a203/plans/v0.0.6.68-to-v0.0.6.77/README.md) · [Machine-readable ledger](checkpoints.json)

| Checkpoint | GitHub issue | Repair | Priority | Start after |
| --- | --- | --- | --- | --- |
| `v0.0.6.78` | [#78](https://github.com/vixttha/README-HQ/issues/78) | Bind audit receipts to the executing validator | High | `v0.0.6.77` |
| `v0.0.6.79` | [#79](https://github.com/vixttha/README-HQ/issues/79) | Hash the learning registry snapshot used for recommendations | High | `v0.0.6.78` |
| `v0.0.6.80` | [#80](https://github.com/vixttha/README-HQ/issues/80) | Use homepage precedence for repository-root fragments | Medium | `v0.0.6.79` |
| `v0.0.6.81` | [#81](https://github.com/vixttha/README-HQ/issues/81) | Handle malformed registry structure as a normal CLI failure | Medium | `v0.0.6.80` |
| `v0.0.6.82` | [#82](https://github.com/vixttha/README-HQ/issues/82) | Report the actual line of each broken link | Medium | `v0.0.6.81` |
| `v0.0.6.83` | [#83](https://github.com/vixttha/README-HQ/issues/83) | Handle Graphify references that resolve to one edge | Medium | `v0.0.6.82` |
| `v0.0.6.84` | [#84](https://github.com/vixttha/README-HQ/issues/84) | Run smoke checks in the selected package context | High | `v0.0.6.83` |
| `v0.0.6.85` | [#85](https://github.com/vixttha/README-HQ/issues/85) | Keep smoke output streams distinct | High | `v0.0.6.84` |
| `v0.0.6.86` | [#86](https://github.com/vixttha/README-HQ/issues/86) | Bind each repair-plan partition to its approved source inventory | High | `v0.0.6.85` |
| `v0.0.6.87` | [#87](https://github.com/vixttha/README-HQ/issues/87) | Resolve contradictory learning decisions for one observation | Medium | `v0.0.6.86` |
| `v0.0.6.88` | [#88](https://github.com/vixttha/README-HQ/issues/88) | Distinguish Git LFS pointers from corrupt media | Medium | `v0.0.6.87` |
| `v0.0.6.89` | [#89](https://github.com/vixttha/README-HQ/issues/89) | Account for rendered bare GFM URLs | Medium | `v0.0.6.88` |
| `v0.0.6.90` | [#90](https://github.com/vixttha/README-HQ/issues/90) | Resolve the publication root deterministically | Medium | `v0.0.6.89` |
| `v0.0.6.91` | [#91](https://github.com/vixttha/README-HQ/issues/91) | Document how CLI evidence becomes a reviewed technique receipt | Medium | `v0.0.6.90` |
| `v0.0.6.92` | [#92](https://github.com/vixttha/README-HQ/issues/92) | Check explicitly expected HTTP error bodies | Low | `v0.0.6.91` |
| `v0.0.6.93` | [#93](https://github.com/vixttha/README-HQ/issues/93) | Resolve published GitHub refs with published semantics | High | `v0.0.6.92` |
| `v0.0.6.94` | [#94](https://github.com/vixttha/README-HQ/issues/94) | Verify the repair plan’s acceptance text | High | `v0.0.6.93` |
| `v0.0.6.95` | [#95](https://github.com/vixttha/README-HQ/issues/95) | Check animation frames or report partial media coverage | Medium | `v0.0.6.94` |
| `v0.0.6.96` | [#96](https://github.com/vixttha/README-HQ/issues/96) | Record and verify the final destination of remote smoke requests | Medium | `v0.0.6.95` |
| `v0.0.6.97` | [#97](https://github.com/vixttha/README-HQ/issues/97) | Report unknown technique IDs explicitly | Medium | `v0.0.6.96` |
| `v0.0.6.98` | [#98](https://github.com/vixttha/README-HQ/issues/98) | Bind Graphify PR verification to the base ref and SHA | Medium | `v0.0.6.97` |
| `v0.0.6.99` | [#99](https://github.com/vixttha/README-HQ/issues/99) | Validate smoke mode and matcher types before execution | Medium | `v0.0.6.98` |
| `v0.0.6.100` | [#100](https://github.com/vixttha/README-HQ/issues/100) | Make Graphify binary inventory size behavior explicit | Low | `v0.0.6.99` |
| `v0.0.6.101` | [#101](https://github.com/vixttha/README-HQ/issues/101) | Isolate smoke commands from the audited Git repository | High | `v0.0.6.100` |
| `v0.0.6.102` | [#102](https://github.com/vixttha/README-HQ/issues/102) | Include audit scope in adopter receipts | Medium | `v0.0.6.101` |
| `v0.0.6.103` | [#103](https://github.com/vixttha/README-HQ/issues/103) | Distinguish GitHub run attempts and jobs in receipts | Medium | `v0.0.6.102` |
| `v0.0.6.104` | [#104](https://github.com/vixttha/README-HQ/issues/104) | Make partial-clone object fetching explicit | Medium | `v0.0.6.103` |
| `v0.0.6.105` | [#105](https://github.com/vixttha/README-HQ/issues/105) | Reject empty or separately label empty Graphify output | Medium | `v0.0.6.104` |
| `v0.0.6.106` | [#106](https://github.com/vixttha/README-HQ/issues/106) | Validate the SVG element namespace | Medium | `v0.0.6.105` |
| `v0.0.6.107` | [#107](https://github.com/vixttha/README-HQ/issues/107) | Parse GitHub plain-mode query parameters | Medium | `v0.0.6.106` |
| `v0.0.6.108` | [#108](https://github.com/vixttha/README-HQ/issues/108) | Require rendered checkpoint and version tables | High | `v0.0.6.107` |
| `v0.0.6.109` | [#109](https://github.com/vixttha/README-HQ/issues/109) | Reuse public GitHub metadata within one learning intake | Medium | `v0.0.6.108` |
| `v0.0.6.110` | [#110](https://github.com/vixttha/README-HQ/issues/110) | Distinguish raw GitHub files from rendered heading destinations | Medium | `v0.0.6.109` |
| `v0.0.6.111` | [#111](https://github.com/vixttha/README-HQ/issues/111) | Prevent draft reads through symlinked ancestors | Medium | `v0.0.6.110` |
| `v0.0.6.112` | [#112](https://github.com/vixttha/README-HQ/issues/112) | Keep validation errors visible when receipt writes fail | Low | `v0.0.6.111` |
| `v0.0.6.113` | [#113](https://github.com/vixttha/README-HQ/issues/113) | Detect missing HTML image alternatives | Medium | `v0.0.6.112` |
| `v0.0.6.114` | [#114](https://github.com/vixttha/README-HQ/issues/114) | Apply or reject adopter-only flags explicitly | Medium | `v0.0.6.113` |
| `v0.0.6.115` | [#115](https://github.com/vixttha/README-HQ/issues/115) | Validate the learning request structure before processing | Low | `v0.0.6.114` |
| `v0.0.6.116` | [#116](https://github.com/vixttha/README-HQ/issues/116) | Verify Graphify inventory relations over MCP | Medium | `v0.0.6.115` |
| `v0.0.6.117` | [#117](https://github.com/vixttha/README-HQ/issues/117) | Make Windows CI fail on the validator’s actual exit | High | `v0.0.6.116` |
| `v0.0.6.118` | [#118](https://github.com/vixttha/README-HQ/issues/118) | Recognize the repository’s actual Quickstart | High | `v0.0.6.117` |
| `v0.0.6.119` | [#119](https://github.com/vixttha/README-HQ/issues/119) | Make rich-text navigation coverage explicit | Medium | `v0.0.6.118` |
| `v0.0.6.120` | [#120](https://github.com/vixttha/README-HQ/issues/120) | Publish a copyable first-action proof guide | Medium | `v0.0.6.119` |
| `v0.0.6.121` | [#121](https://github.com/vixttha/README-HQ/issues/121) | Reuse parsed anchors for a pinned Markdown blob | Medium | `v0.0.6.120` |
| `v0.0.6.122` | [#122](https://github.com/vixttha/README-HQ/issues/122) | Prepare reader dependencies before the retained plan check | Medium | `v0.0.6.121` |
| `v0.0.6.123` | [#123](https://github.com/vixttha/README-HQ/issues/123) | Link Graphify rich-text evidence to physical source lines | Medium | `v0.0.6.122` |
| `v0.0.6.124` | [#124](https://github.com/vixttha/README-HQ/issues/124) | Retain real Graphify evidence after a failed CI attempt | High | `v0.0.6.123` |
| `v0.0.6.125` | [#125](https://github.com/vixttha/README-HQ/issues/125) | Publish plan partitions only after all staged manifests succeed | Medium | `v0.0.6.124` |
| `v0.0.6.126` | [#126](https://github.com/vixttha/README-HQ/issues/126) | Make required first-action verification distinguish skipped coverage | High | `v0.0.6.125` |
| `v0.0.6.127` | [#127](https://github.com/vixttha/README-HQ/issues/127) | Preserve actionable first-action failure diagnostics | Medium | `v0.0.6.126` |
| `v0.0.6.128` | [#128](https://github.com/vixttha/README-HQ/issues/128) | Distinguish retryable GitHub errors from invalid learning evidence | Medium | `v0.0.6.127` |

## Keeping the plan current

GitHub Issues is the source for new findings. On each refresh, reconcile newly opened or reopened issues and material changes to planned issues against this ledger. For a distinct, evidenced defect, append the next unused checkpoint, preserve existing assignments, and record the issue, exact affected revision, evidence, related checkpoints, baseline replay, post-fix acceptance and applicable public runner coverage. Issue numbers and checkpoint numbers happened to match for #78–#128. Future issue and checkpoint numbers may differ. Link duplicates and additional evidence to the existing checkpoint. If an issue closes, reconcile the reason and evidence before changing its planning disposition.

When work from an earlier checkpoint also resolves a later issue, replay the later issue’s original case and control on that exact SHA and record where the fix landed. Keep its checkpoint and acceptance history. When related issues share a fixture, keep a result for each distinct acceptance criterion.

## Related repair checkpoints

The pinned source and issue evidence show recurring gaps in scope, outcome and verification across several components. The groupings below identify shared regression coverage. Each issue still has its own acceptance criteria.

| Area | Related issues | Connection |
| --- | --- | --- |
| Scope and provenance | [#78](https://github.com/vixttha/README-HQ/issues/78), [#79](https://github.com/vixttha/README-HQ/issues/79), [#84](https://github.com/vixttha/README-HQ/issues/84), [#90](https://github.com/vixttha/README-HQ/issues/90), [#98](https://github.com/vixttha/README-HQ/issues/98), [#102](https://github.com/vixttha/README-HQ/issues/102), [#103](https://github.com/vixttha/README-HQ/issues/103), [#114](https://github.com/vixttha/README-HQ/issues/114) | The operation and its receipt need to agree on the selected repository, revision, profile, inputs and execution context. Several distinct paths currently lose one of those identifiers. [check_readme_hq.py](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/tools/check_readme_hq.py) · [intake.py](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/learning/intake.py) |
| Outcome and diagnostics | [#85](https://github.com/vixttha/README-HQ/issues/85), [#99](https://github.com/vixttha/README-HQ/issues/99), [#112](https://github.com/vixttha/README-HQ/issues/112), [#117](https://github.com/vixttha/README-HQ/issues/117), [#124](https://github.com/vixttha/README-HQ/issues/124), [#126](https://github.com/vixttha/README-HQ/issues/126), [#127](https://github.com/vixttha/README-HQ/issues/127), [#128](https://github.com/vixttha/README-HQ/issues/128) | The surrounding command, workflow or receipt can drop or misclassify an underlying result. #117, #124 and #126 demonstrate different mechanisms at the workflow, artifact and command boundaries. [hq_smoke.py](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/tools/hq_smoke.py) · [readme-hq.yml](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/.github/workflows/readme-hq.yml) |
| Graph and plan coverage | [#83](https://github.com/vixttha/README-HQ/issues/83), [#86](https://github.com/vixttha/README-HQ/issues/86), [#94](https://github.com/vixttha/README-HQ/issues/94), [#105](https://github.com/vixttha/README-HQ/issues/105), [#108](https://github.com/vixttha/README-HQ/issues/108), [#116](https://github.com/vixttha/README-HQ/issues/116), [#125](https://github.com/vixttha/README-HQ/issues/125) | A generated graph can be internally consistent while missing an intended relation or obligation. #125 adds a separate publication failure when the input spans several partitions. [verify_plan.py](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/tools/verify_plan.py) · [evidence_map.py](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/graphify-hq/template/v0.0.8/evidence_map.py) |
| Published reader path | [#80](https://github.com/vixttha/README-HQ/issues/80), [#89](https://github.com/vixttha/README-HQ/issues/89), [#93](https://github.com/vixttha/README-HQ/issues/93), [#107](https://github.com/vixttha/README-HQ/issues/107), [#110](https://github.com/vixttha/README-HQ/issues/110), [#118](https://github.com/vixttha/README-HQ/issues/118), [#119](https://github.com/vixttha/README-HQ/issues/119), [#120](https://github.com/vixttha/README-HQ/issues/120), [#121](https://github.com/vixttha/README-HQ/issues/121), [#123](https://github.com/vixttha/README-HQ/issues/123) | The validator, generated source links and published GitHub view can disagree about what a human or agent can actually open or run. [hq_navigation.py](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/tools/hq_navigation.py) · [check_readme_hq.py](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/tools/check_readme_hq.py) |
| Learning intake | [#79](https://github.com/vixttha/README-HQ/issues/79), [#81](https://github.com/vixttha/README-HQ/issues/81), [#87](https://github.com/vixttha/README-HQ/issues/87), [#91](https://github.com/vixttha/README-HQ/issues/91), [#97](https://github.com/vixttha/README-HQ/issues/97), [#109](https://github.com/vixttha/README-HQ/issues/109), [#115](https://github.com/vixttha/README-HQ/issues/115), [#128](https://github.com/vixttha/README-HQ/issues/128) | The intake must validate and deduplicate decisions, bind the inputs and separate external retryable errors from invalid evidence. #109 and #128 affect the same GitHub lookup path, with separate frequency and error-reporting regressions. [intake.py](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/learning/intake.py) · [audit_learning.py](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/learning/audit_learning.py) |

After the linked checkpoints qualify individually, use the same fixture sets to verify the combined candidate. For the first adopter walkthrough, start at the published README, run its documented first action, and trace the outcome from the command through the receipt and public job artifact on the same SHA. For Graphify, compare the intended inventory and plan with actual MCP readback and retain both success and failure evidence. For learning intake, verify that rerunning the same observation preserves the decision history and that an unavailable source is distinguishable from invalid evidence.

## Debug and verification gate for every repair

**Every repair gets a post-fix debug pass before it can advance or be considered for merge.**

1. **Confirm the baseline.** Reproduce the issue from the preceding verified revision using the linked fixture. Record the exact starting SHA, expected result, actual result, and diagnostic. If a preceding repair already resolves it, verify the same case on the new revision and record that disposition on the issue.
2. **Finish one scoped repair.** Keep its checkpoint commit distinct and link it to the issue. Run this step and the downstream checks only after implementation is approved.
3. **Debug after the repair.** Replay the original failing case against the repair SHA, also run the positive or unchanged control, and inspect the touched behavior for adjacent regressions. Compare actual outputs with the acceptance criteria, including code paths that should fail or report incomplete coverage. A failure or unexplained change keeps the checkpoint open. Investigate it and repeat the focused checks on the new SHA.
4. **Qualify the exact SHA.** Use standard public GitHub-hosted jobs for the focused case and relevant existing tests. Verify Graphify changes with the real compiler and MCP readback, including receipt and digest checks when they are relevant. Record the tested SHA, workflow run and attempt, job link, platform, invocation, expected and observed outputs, and the receipt or artifact on the issue. If a tool omits a field, record it from the hosted job. Treat skipped or unavailable coverage explicitly.
5. **Review before advancing or merging.** Re-read the patch and evidence and mark the checkpoint eligible for review only after its debug gate passes. Carry it forward on the draft branch. If the candidate or relevant base changes, refresh the applicable evidence. Verify the combined candidate at the exact proposed head and merge base, and retain owner approval for main, publication and release decisions.

The same post-fix debug requirement applies when executing the pending .68–.77 plan. Until [#117](https://github.com/vixttha/README-HQ/issues/117) qualifies, capture the Windows validator and test exits separately on the public audit job. A green combined step alone cannot establish the validator’s outcome. Use the pinned audit runner with reader and Graphify dependencies installed in the right order while [#122](https://github.com/vixttha/README-HQ/issues/122) remains open. Until [#124](https://github.com/vixttha/README-HQ/issues/124) qualifies, preserve Graphify failure evidence through the audit job’s observer artifact.

Keep the existing acceptance records for the 67-checkpoint candidate open until their own requirements are met. Later evidence for [#5 rollback](https://github.com/vixttha/README-HQ/issues/5#issuecomment-7024854146), [#13 homepage selection](https://github.com/vixttha/README-HQ/issues/13#issuecomment-7024183384), [#18 run proof](https://github.com/vixttha/README-HQ/issues/18#issuecomment-7024685050), [#19 source spans](https://github.com/vixttha/README-HQ/issues/19#issuecomment-7024685302), and [#65 prerelease anchoring](https://github.com/vixttha/README-HQ/issues/65#issuecomment-7024322470) belongs with the original issues. Checkpoint .99 includes the [late smoke matcher validation case](https://github.com/vixttha/README-HQ/issues/99#issuecomment-7024853858). The standalone reuse decision and live merge-queue verification remain tracked under [#24](https://github.com/vixttha/README-HQ/issues/24) and [#58](https://github.com/vixttha/README-HQ/issues/58).

## Acceptance by checkpoint

### v0.0.6.78

- **Replay** Put a harmless file at the validator’s relative path in an adopter tree, then repeat with that path missing.
- **After the repair** Both receipts identify the installed validator and revision or digest. They record adopter Git blobs separately.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#78](https://github.com/vixttha/README-HQ/issues/78) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44622391591/job/135907188784)

### v0.0.6.79

- **Replay** Simulate retiring a technique between reading the active registry and writing the receipt.
- **After the repair** The recorded hash belongs to the snapshot that governed the decision, or intake stops explicitly. Unchanged active and retired controls behave correctly.
- **Public runners** `ubuntu-latest`. [#79](https://github.com/vixttha/README-HQ/issues/79) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44622391591/job/135907188784)

### v0.0.6.80

- **Replay** Compete .github, root and docs README headings with a directory README control.
- **After the repair** Root links resolve against the effective homepage and reject fallback-only anchors. Subdirectory links still resolve against their own README.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#80](https://github.com/vixttha/README-HQ/issues/80) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44622391591/job/135907188784)

### v0.0.6.81

- **Replay** Use valid JSON arrays, null and invalid nested records, plus a valid registry.
- **After the repair** Failures return a normal diagnostic and a parseable failed receipt when requested. The valid registry still passes.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#81](https://github.com/vixttha/README-HQ/issues/81) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44622391591/job/135907188784)

### v0.0.6.82

- **Replay** Place two broken links on distinct lines of one paragraph, including repeated labels.
- **After the repair** Diagnostics identify both exact occurrence lines. Single-line and valid-link controls retain their behavior.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#82](https://github.com/vixttha/README-HQ/issues/82) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44622391591/job/135907188784)

### v0.0.6.83

- **Replay** Use implicit and explicit references that resolve to the same source line. Include separate lines and relations.
- **After the repair** Duplicates are rejected clearly or represented consistently as one resolved edge. Distinct edges survive export and MCP readback.
- **Public runners** `ubuntu-latest` and Graphify MCP. [#83](https://github.com/vixttha/README-HQ/issues/83) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44622391591/job/135907188784)

### v0.0.6.84

- **Replay** Use a package-only command and a similarly named root decoy, then repeat with an ordinary root project.
- **After the repair** The package action executes in the declared context, the receipt identifies the working directory, and the root decoy cannot satisfy the package check.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#84](https://github.com/vixttha/README-HQ/issues/84) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44630216828/job/135934528628)

### v0.0.6.85

- **Replay** Split the expected marker across stdout and stderr, then emit the full marker on each intended stream in controls.
- **After the repair** A cross-stream match fails. Valid per-stream checks pass and the observation identifies the stream used.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#85](https://github.com/vixttha/README-HQ/issues/85) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44630216828/job/135934528628)

### v0.0.6.86

- **Replay** Remove or add source files and regenerate a self-consistent graph and receipt.
- **After the repair** Verification catches both mutations with the expected inventory held fixed. The canonical graph and exact edges pass MCP readback.
- **Public runners** `ubuntu-latest` and Graphify MCP. [#86](https://github.com/vixttha/README-HQ/issues/86) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44630216828/job/135934528628)

### v0.0.6.87

- **Replay** Submit adopt and decline for one technique, target and source in the same request.
- **After the repair** Intake rejects or explicitly represents the conflict. A single decision and genuinely distinct evidence remain usable.
- **Public runners** `ubuntu-latest`. [#87](https://github.com/vixttha/README-HQ/issues/87) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44630216828/job/135934528628)

### v0.0.6.88

- **Replay** Use a valid pointer with and without a locally available verified object, plus a malformed pointer and a normal PNG.
- **After the repair** The checker distinguishes verified media, unavailable-object coverage and corruption. It respects the caller’s fetch policy.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#88](https://github.com/vixttha/README-HQ/issues/88) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44630216828/job/135934528628)

### v0.0.6.89

- **Replay** Use bare HTTPS and www routes, punctuation boundaries, and the same examples within code spans and fences.
- **After the repair** Live autolinks appear in the audit or explicit coverage gaps. Literal examples remain outside link counts.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#89](https://github.com/vixttha/README-HQ/issues/89) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44630216828/job/135934528628)

### v0.0.6.90

- **Replay** Run on the same fixture using its root, a child directory as --repo, and a deliberate --subproject.
- **After the repair** A child checkout path resolves to the actual root or produces a clear diagnostic. Explicit subproject selection behaves as documented.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#90](https://github.com/vixttha/README-HQ/issues/90) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44630216828/job/135934528628)

### v0.0.6.91

- **Replay** Follow the guide using a public run receipt, then try a raw or incomplete input.
- **After the repair** A reviewer can produce a valid record tied to the exact source, case and outcome. Raw or incomplete input cannot qualify as verified. Record attempt metadata manually until .103 lands.
- **Public runners** `ubuntu-latest`. [#91](https://github.com/vixttha/README-HQ/issues/91) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44630216828/job/135934528628)

### v0.0.6.92

- **Replay** Use matching and mismatching expected 404 bodies, plus success and gated-auth controls.
- **After the repair** Matches follow the documented bounded-body policy, or an unsupported specification fails before the probe. Authentication gating remains explicit.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#92](https://github.com/vixttha/README-HQ/issues/92) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44630216828/job/135934528628)

### v0.0.6.93

- **Replay** Use a local-only origin/main alias, a real published slash branch, and a public HEAD link while on a local topic branch.
- **After the repair** The alias cannot falsely verify, genuine fetched branches resolve, and HEAD uses the remote default. Retain .72’s fetched-ref controls.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#93](https://github.com/vixttha/README-HQ/issues/93) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44631303188/job/135938331014)

### v0.0.6.94

- **Replay** Remove an acceptance section, change one obligation, and compare with the approved or explicitly revised version.
- **After the repair** Unapproved drift fails while the approved text passes. Pin the selected plan revision and run Graphify MCP checks.
- **Public runners** `ubuntu-latest` and Graphify MCP. [#94](https://github.com/vixttha/README-HQ/issues/94) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44631303188/job/135938331014)

### v0.0.6.95

- **Replay** Use a GIF with a truncated later frame, a valid animation and a static control.
- **After the repair** Later-frame failure is detected or reported as partial coverage. Valid media follows the supported resource policy.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#95](https://github.com/vixttha/README-HQ/issues/95) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44631303188/job/135938331014)

### v0.0.6.96

- **Replay** Compare an expected redirect, an unexpected landing page with matching text, and a direct response.
- **After the repair** The receipt identifies the effective URL. When a destination is asserted, an unrelated landing page fails.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#96](https://github.com/vixttha/README-HQ/issues/96) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44631303188/job/135938331014)

### v0.0.6.97

- **Replay** Run unknown, active, retired and out-of-scope technique fixtures.
- **After the repair** The unknown ID reports a diagnostic. Active IDs produce valid output and intentional exclusions are distinguishable.
- **Public runners** `ubuntu-latest`. [#97](https://github.com/vixttha/README-HQ/issues/97) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44631303188/job/135938331014)

### v0.0.6.98

- **Replay** Retarget the PR between reads with the same head, then run a stable-base control.
- **After the repair** Retargeting prevents a coherent verified observation. The stable receipt identifies the exact base and head.
- **Public runners** `ubuntu-latest` and Graphify MCP. [#98](https://github.com/vixttha/README-HQ/issues/98) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44631303188/job/135938331014)

### v0.0.6.99

- **Replay** Exercise argv-only, URL-only, both, neither and a non-string contains matcher with a harmless action marker.
- **After the repair** Valid modes still work. Invalid specs stop before requests or command execution, with a structured diagnostic.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#99](https://github.com/vixttha/README-HQ/issues/99) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44631303188/job/135938331014)

### v0.0.6.100

- **Replay** Run valid inventory below and above the 1 MB cap, plus a text anchor boundary control.
- **After the repair** The published limits match observed behavior. Any larger inventory support remains bounded and preserves exact source digests.
- **Public runners** `ubuntu-latest` and Graphify MCP. [#100](https://github.com/vixttha/README-HQ/issues/100) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44631303188/job/135938331014)

### v0.0.6.101

- **Replay** Have a disposable action write a harmless local Git setting. Inspect the source configuration, refs and files afterward.
- **After the repair** The audited repository remains unchanged under the default smoke behavior. Ordinary output and exit checks still work.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#101](https://github.com/vixttha/README-HQ/issues/101) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44633049784/job/135944431011)

### v0.0.6.102

- **Replay** Compare the same commit across distinct repository labels, profiles and subprojects.
- **After the repair** The receipt makes the selected scope distinguishable and states which repository identity was inferred or verified.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#102](https://github.com/vixttha/README-HQ/issues/102) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44633049784/job/135944431011)

### v0.0.6.103

- **Replay** Use two attempts with one run ID, distinct jobs, and a standalone execution.
- **After the repair** Hosted receipts identify the actual attempt and job. Standalone output stays usable and labels unavailable CI metadata.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#103](https://github.com/vixttha/README-HQ/issues/103) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44633049784/job/135944431011)

### v0.0.6.104

- **Replay** Use a missing blob with the offline policy and an explicitly permitted fetch, plus a complete-clone control.
- **After the repair** Offline reads leave the blob unfetched and report the gap. Authorized fetches and complete clones record the actual coverage.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#104](https://github.com/vixttha/README-HQ/issues/104) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44633049784/job/135944431011)

### v0.0.6.105

- **Replay** Build zero-evidence, inventory-only and feature-bearing manifests.
- **After the repair** A root-only graph cannot qualify as evidence-bearing. Supported inventory and feature controls retain accurate MCP evidence and receipts.
- **Public runners** `ubuntu-latest` and Graphify MCP. [#105](https://github.com/vixttha/README-HQ/issues/105) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44633049784/job/135944431011)

### v0.0.6.106

- **Replay** Use valid default and prefixed SVG namespaces, a foreign namespace and malformed XML.
- **After the repair** Only supported SVG root identities pass. Wrong namespace and malformed XML retain meaningful diagnostics.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#106](https://github.com/vixttha/README-HQ/issues/106) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44633049784/job/135944431011)

### v0.0.6.107

- **Replay** Compare plain mode alone, extra parameters in either order, and an invalid line range.
- **After the repair** Valid plain links remain valid with extra query parameters. An invalid range still fails the line bounds check.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#107](https://github.com/vixttha/README-HQ/issues/107) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44633049784/job/135944431011)

### v0.0.6.108

- **Replay** Fence the approved-looking plan and version rows, then add table-looking examples beside a real rendered table.
- **After the repair** Hidden tables fail the appropriate reader or Graphify checks. Only the actual navigation table is counted.
- **Public runners** `ubuntu-latest`, `windows-latest` and Graphify MCP. [#108](https://github.com/vixttha/README-HQ/issues/108) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44634064022/job/135947933810)

### v0.0.6.109

- **Replay** Replay 32 distinct anchors at one commit with a bounded mock API budget, then vary the commit and simulate a genuine limit.
- **After the repair** Redundant metadata calls collapse while each anchor is independently checked. Distinct commits and rate-limit diagnostics remain accurate.
- **Public runners** `ubuntu-latest`. [#109](https://github.com/vixttha/README-HQ/issues/109) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44634064022/job/135947933810)

### v0.0.6.110

- **Replay** Compare a raw URL and a rendered blob URI for the same tracked Markdown and fragment.
- **After the repair** The raw file’s existence is tracked separately from unsupported fragment coverage. The real rendered heading still verifies.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#110](https://github.com/vixttha/README-HQ/issues/110) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44634064022/job/135947933810)

### v0.0.6.111

- **Replay** Replace a tracked directory with an internal symlink, then test an external target and a normal edited draft.
- **After the repair** Substituted bytes are rejected or explicitly marked outside tracked draft coverage. A regular draft still validates normally.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#111](https://github.com/vixttha/README-HQ/issues/111) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44634064022/job/135947933810)

### v0.0.6.112

- **Replay** Use an existing directory as the receipt path for a broken-link audit and a passing audit.
- **After the repair** The persistence issue is reported without dropping findings or emitting a traceback. A writable receipt path still produces valid JSON.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#112](https://github.com/vixttha/README-HQ/issues/112) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44634064022/job/135947933810)

### v0.0.6.113

- **Replay** Compare omitted alt, an explicitly decorative empty alt, and descriptive alt.
- **After the repair** Omission receives a meaningful diagnostic. Both valid accessibility controls retain their expected result.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#113](https://github.com/vixttha/README-HQ/issues/113) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44634204082/job/135948411631)

### v0.0.6.114

- **Replay** Run standalone defaults, adopter scope flags without a repository, and valid and invalid explicit adopter scopes.
- **After the repair** The CLI never silently validates README HQ when the user supplied a different scope. Valid standalone and adopter uses remain supported.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#114](https://github.com/vixttha/README-HQ/issues/114) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44634204082/job/135948411631)

### v0.0.6.115

- **Replay** Use an array, null, malformed nested source and target data, and a valid object.
- **After the repair** Malformed inputs receive stable CLI diagnostics without a traceback or receipt publication. Valid intake still writes its receipt.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#115](https://github.com/vixttha/README-HQ/issues/115) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44634204082/job/135948411631)

### v0.0.6.116

- **Replay** Use a count-preserving mutation of an inventory edge and the matching graph digest, with valid inventory and feature controls.
- **After the repair** Wrong inventory identities or destinations fail the real MCP readback. Correct feature and file relations still pass.
- **Public runners** `ubuntu-latest` and Graphify MCP. [#116](https://github.com/vixttha/README-HQ/issues/116) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44634204082/job/135948411631)

### v0.0.6.117

- **Replay** Force the validator to fail before a passing test command, then repeat with both commands passing.
- **After the repair** The public Windows job comes back red for validator failure and preserves its receipt. Ubuntu and clean Windows controls pass.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#117](https://github.com/vixttha/README-HQ/issues/117) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44634204082/job/135948412069)

### v0.0.6.118

- **Replay** Audit the candidate README, a valid action after a large navigation table, and a fake Quickstart with an unrelated link.
- **After the repair** The real first action passes. The invalid route fails and the validator still identifies the effective README.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#118](https://github.com/vixttha/README-HQ/issues/118) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44634440367/job/135949209668)

### v0.0.6.119

- **Replay** Use pinned reStructuredText and AsciiDoc files with good and broken links, anchors and first actions.
- **After the repair** Supported routes are checked and bad ones diagnosed. Unsupported coverage is explicit and cannot look like complete validation.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#119](https://github.com/vixttha/README-HQ/issues/119) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44634440367/job/135949209668)

### v0.0.6.120

- **Replay** Run documented command-mode examples from clean Ubuntu and Windows checkouts, then exercise the documented failure and URL behavior.
- **After the repair** The example binds the expected result to an exact SHA and working directory and yields inspectable pass and failure receipts.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#120](https://github.com/vixttha/README-HQ/issues/120) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44634440367/artifacts/14582678432)

### v0.0.6.121

- **Replay** Measure actual reads and parses for 64 links to one file, then include distinct refs and fragments and an edited draft.
- **After the repair** Redundant blob work falls while valid and broken links keep their exact outcomes. An updated draft cannot reuse stale anchors.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#121](https://github.com/vixttha/README-HQ/issues/121) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44635421690/job/135952553310)

### v0.0.6.122

- **Replay** Run the intended plan workflow against a clean interpreter and the pinned checkout without preinstalled packages.
- **After the repair** The hashed reader setup precedes validation, or the historical workflow runs against its declared original checkout. Reader and Graphify steps run in the intended order.
- **Public runners** `ubuntu-latest` and Graphify MCP. [#122](https://github.com/vixttha/README-HQ/issues/122) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44635421690/job/135952553310)

### v0.0.6.123

- **Replay** Generate Markdown, reStructuredText and AsciiDoc line links and open the pinned examples.
- **After the repair** Each supported link resolves to the exact source view and line. The changed map and receipt pass Graphify MCP verification.
- **Public runners** `ubuntu-latest` and Graphify MCP. [#123](https://github.com/vixttha/README-HQ/issues/123) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44635421690/job/135952553310)

### v0.0.6.124

- **Replay** Force a verification mismatch after an earlier artifact was produced. Repeat on a successful run.
- **After the repair** The failed job stays failed, and its attempt-specific diagnostic and available evidence remain downloadable. Prior and unchecked receipts are labeled separately.
- **Public runners** `ubuntu-latest` and Graphify MCP. [#124](https://github.com/vixttha/README-HQ/issues/124) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44635863502/job/135954070928)

### v0.0.6.125

- **Replay** Make a second partition fail in a 33-checkpoint plan, then correct it and retry at the same output path.
- **After the repair** The failed input leaves no partial published manifests. The corrected retry succeeds at the original destination and preserves complete partition coverage.
- **Public runners** `ubuntu-latest` and Graphify MCP. [#125](https://github.com/vixttha/README-HQ/issues/125) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44635863502/job/135954070600)

### v0.0.6.126

- **Replay** Request a pinned HTTPS probe without network permission. Compare blocked, unresolved and failing probes with a successful local action.
- **After the repair** A skipped or blocked required smoke check cannot look like a confirmed pass. Network access remains opt-in and the observed result is explicit.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#126](https://github.com/vixttha/README-HQ/issues/126) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44635863502/job/135954070600)

### v0.0.6.127

- **Replay** Run commands with the same exit code and distinct failure reasons, then exercise an output-marker mismatch and a missing file.
- **After the repair** The receipt distinguishes failure causes, retains reproducibility hashes and exposes bounded diagnostics under the documented redaction policy.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#127](https://github.com/vixttha/README-HQ/issues/127) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44635863502/job/135954070600)

### v0.0.6.128

- **Replay** Simulate HTTP 429 and a wrong pinned source anchor, then run the valid control.
- **After the repair** The CLI reports distinct structured error categories and retry timing when provided, with sanitized context. Valid intake still succeeds.
- **Public runners** `ubuntu-latest`, `windows-latest`. [#128](https://github.com/vixttha/README-HQ/issues/128) · [Existing audit evidence](https://github.com/vixttha/README-HQ/actions/runs/44635863502/job/135954070600)
