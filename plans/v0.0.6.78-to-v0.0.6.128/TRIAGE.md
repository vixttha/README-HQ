# README HQ full-stack issue triage

This is the review snapshot for **139 open GitHub issues** through #140. Both pages of GitHub’s open-issue listing and the 22 comments then visible were reviewed. The snapshot has 52 High, 80 Medium, and 7 Low issues according to the filed priorities. Every issue below has one primary workstream. Cross-workstream dependencies stay with the original issue and checkpoint.

[Open issues](https://github.com/vixttha/README-HQ/issues?q=is%3Aopen+is%3Aissue) · [Combined draft PR #68](https://github.com/vixttha/README-HQ/pull/68) · [Active .78–.140 plan](README.md) · [Machine-readable checkpoints](checkpoints.json) · [Original .1–.67 plan](https://github.com/vixttha/README-HQ/blob/7f4562b8f44544bc9dd4b479fcd1bc30ca07ca94/plans/v0.0.6-repairs/README.md) · [First pending .68–.77 plan](https://github.com/vixttha/README-HQ/blob/ac07987cfe11d6592b8def2ff16b72a6b2c0a203/plans/v0.0.6.68-to-v0.0.6.77/README.md)

## Sequence for the next milestone

1. **Prepare Batch 1 for owner approval.** Start from the exact [combined candidate](https://github.com/vixttha/README-HQ/commit/8d50caec2bc6fcb998994a1fd302294a029325f9). [Batch 1](BATCHES.md#batch-1) covers .68–.82 in the existing order, beginning with agent onboarding, independently verified technique sources, and first-use file outcomes. Use the [batch schedule](BATCHES.md) when reviewing each batch head and its checkpoint evidence.
2. **Use focused qualification for each repair.** Replay the original failure, run a passing control, and check affected regressions on the exact repair SHA. Standard public GitHub-hosted runners are the execution target. Inspect individual validator and test exits until [#117](https://github.com/vixttha/README-HQ/issues/117) qualifies. Keep requested smoke checks explicit and tie a behavioral pass to the actual documented command or route as tracked in [#126](https://github.com/vixttha/README-HQ/issues/126), [#129](https://github.com/vixttha/README-HQ/issues/129), [#138](https://github.com/vixttha/README-HQ/issues/138). Preserve diagnostic evidence when Graphify fails under [#124](https://github.com/vixttha/README-HQ/issues/124) and bind the artifact to the actual attempt under [#103](https://github.com/vixttha/README-HQ/issues/103).
3. **Reconcile the original candidate by issue.** The combined .67 run and graph integrity results are retained. An original checkpoint can use focused proof at the combined candidate SHA if its documented case and control are covered. Keep any remaining criteria open and fix them when needed. Keep [#5](https://github.com/vixttha/README-HQ/issues/5) at both .5 and .77 because .77 is an already-planned follow-up for a distinct link case.
4. **Review publication separately after the relevant blockers qualify.** Preserve the owner's explicit merge and publication authority. [#132](https://github.com/vixttha/README-HQ/issues/132) needs an approved solo-maintainer branch-rule design and effective GitHub readback. [#135](https://github.com/vixttha/README-HQ/issues/135) needs a supported Python and Pillow decision plus hashed public-runner qualification. [#24](https://github.com/vixttha/README-HQ/issues/24) retains the standalone reuse decision. Recheck [#58](https://github.com/vixttha/README-HQ/issues/58) on a real merge-queue event if the publication path uses one.
5. **Keep the plan and product backlog traceable.** [#133](https://github.com/vixttha/README-HQ/issues/133) tracks ongoing validation of the active ledger, including automatically proposed updates. This reconciliation's structural checks apply to this snapshot. Keep technique combinations in [Provenistem](https://github.com/vixttha/README-HQ/blob/Provenistem/features/records/FEAT-000012.json), with the documented Veraphify trial available as evidence when the owner resumes it.

**Every repair gets a post-fix debug pass before it can advance or be considered for merge.** All newly added checkpoints await owner approval. Default branch, issue states, and release settings are outside this planning revision.

## Follow-up evidence to carry into acceptance

| Issue | Effect on the plan | Evidence |
| --- | --- | --- |
| [#4](https://github.com/vixttha/README-HQ/issues/4) | Check frozen directory membership and assets alongside direct file byte controls. | [Comment 1](https://github.com/vixttha/README-HQ/issues/4#issuecomment-7025327820) |
| [#5](https://github.com/vixttha/README-HQ/issues/5) | Replay the wrong guide under .77, synchronized current-version rollback, and the swapped destinations on the Graphify landing page. | [Comment 1](https://github.com/vixttha/README-HQ/issues/5#issuecomment-7011679375) · [Comment 2](https://github.com/vixttha/README-HQ/issues/5#issuecomment-7024854146) · [Comment 3](https://github.com/vixttha/README-HQ/issues/5#issuecomment-7025125458) |
| [#13](https://github.com/vixttha/README-HQ/issues/13) | Run homepage precedence controls in standalone publication CI as well as adopter mode. | [Comment 1](https://github.com/vixttha/README-HQ/issues/13#issuecomment-7024183384) · [Comment 2](https://github.com/vixttha/README-HQ/issues/13#issuecomment-7024754911) |
| [#14](https://github.com/vixttha/README-HQ/issues/14) | Require the first action to belong to its Quickstart section. Retain both the placeholder false pass and the valid Quickstart control. | [Comment 1](https://github.com/vixttha/README-HQ/issues/14#issuecomment-7024754604) |
| [#18](https://github.com/vixttha/README-HQ/issues/18) | Verify the hosted run actually resolves and matches the claim, revision and attempt. | [Comment 1](https://github.com/vixttha/README-HQ/issues/18#issuecomment-7024685050) |
| [#19](https://github.com/vixttha/README-HQ/issues/19) | Preserve disjoint spans from one pinned file while counting the file once for corroboration. | [Comment 1](https://github.com/vixttha/README-HQ/issues/19#issuecomment-7024685302) |
| [#24](https://github.com/vixttha/README-HQ/issues/24) | Keep the owner decision on standalone reuse with the publication review. | [Comment 1](https://github.com/vixttha/README-HQ/issues/24#issuecomment-7025327548) |
| [#50](https://github.com/vixttha/README-HQ/issues/50) | Keep the public checkpoint-to-evidence mutation fixture with the original acceptance case. | [Comment 1](https://github.com/vixttha/README-HQ/issues/50#issuecomment-7009316979) |
| [#51](https://github.com/vixttha/README-HQ/issues/51) | Retain the public dead plan-index link fixture and valid control. | [Comment 1](https://github.com/vixttha/README-HQ/issues/51#issuecomment-7009316221) |
| [#52](https://github.com/vixttha/README-HQ/issues/52) | Retain the public working-tree line-ending fixture with pinned archive bytes. | [Comment 1](https://github.com/vixttha/README-HQ/issues/52#issuecomment-7009316644) |
| [#65](https://github.com/vixttha/README-HQ/issues/65) | Add the stable-versus-prerelease match control to release-specific anchoring. | [Comment 1](https://github.com/vixttha/README-HQ/issues/65#issuecomment-7024322470) |
| [#67](https://github.com/vixttha/README-HQ/issues/67) | A focused named-anchor case passed on the candidate. Retain it while confirming the rest of the original acceptance. | [Comment 1](https://github.com/vixttha/README-HQ/issues/67#issuecomment-7011686656) |
| [#70](https://github.com/vixttha/README-HQ/issues/70) | The 21 pinned public documents were independently checked. The validator's normal admission path still needs to require independent evidence. | [Comment 1](https://github.com/vixttha/README-HQ/issues/70#issuecomment-7025722952) |
| [#77](https://github.com/vixttha/README-HQ/issues/77) | Keep the interrupted publication and same-path recovery controls alongside the concurrent-reader case. | [Comment 1](https://github.com/vixttha/README-HQ/issues/77#issuecomment-7024925366) |
| [#99](https://github.com/vixttha/README-HQ/issues/99) | Malformed matcher fields must fail before executing an action. | [Comment 1](https://github.com/vixttha/README-HQ/issues/99#issuecomment-7024853858) |
| [#103](https://github.com/vixttha/README-HQ/issues/103) | Retain attempt-specific artifact IDs and digests when runs reuse an artifact name. | [Comment 1](https://github.com/vixttha/README-HQ/issues/103#issuecomment-7024925069) |
| [#125](https://github.com/vixttha/README-HQ/issues/125) | Use the corrected cross-platform fixture for the late-failure and retry check. | [Comment 1](https://github.com/vixttha/README-HQ/issues/125#issuecomment-7024975085) |
| [#126](https://github.com/vixttha/README-HQ/issues/126) | Keep skipped, wrong-action and different blocked-request cases distinct in the receipt. | [Comment 1](https://github.com/vixttha/README-HQ/issues/126#issuecomment-7025125154) |
| [#135](https://github.com/vixttha/README-HQ/issues/135) | The advisory snapshot and ordinary regressions are retained. The dependency upgrade and runtime compatibility still need qualification. | [Comment 1](https://github.com/vixttha/README-HQ/issues/135#issuecomment-7025723273) |

## All open issues by workstream

| Workstream | Open issues | High priority |
| --- | --- | --- |
| Reader entry points and first-use execution | 20 | 13 |
| GitHub navigation, rendering, and repository paths | 23 | 6 |
| Media, accessibility, and decoder support | 9 | 1 |
| Technique registry and learning provenance | 26 | 8 |
| Graphify generation, source anchors, and MCP readback | 28 | 9 |
| Archive integrity and version navigation | 5 | 3 |
| CI evidence, GitHub provenance, and release authority | 21 | 7 |
| Repair-ledger validation | 7 | 5 |

`Candidate acceptance open` indicates the original plan and combined candidate exist and the open issue still needs its acceptance reconciled. `Planned` and `Added to plan` await owner approval. The batch schedule is ready for review.

### Reader entry points and first-use execution

Use the advertised repo and revision, then prove that the actual documented command or link delivers the expected result.

| Issue | Finding | Filed priority | Checkpoint | Planning status |
| --- | --- | --- | --- | --- |
| [#12](https://github.com/vixttha/README-HQ/issues/12) | Validator cannot target a normal adopter repository | High | `.12` | Candidate acceptance open |
| [#14](https://github.com/vixttha/README-HQ/issues/14) | The README validator reports success for missing meaningful content and truncation | High | `.14` | Candidate acceptance open |
| [#27](https://github.com/vixttha/README-HQ/issues/27) | A README passes validation when the documented first action fails | High | `.27` | Candidate acceptance open |
| [#45](https://github.com/vixttha/README-HQ/issues/45) | Broken external first-action links pass without a coverage diagnostic | High | `.45` | Candidate acceptance open |
| [#69](https://github.com/vixttha/README-HQ/issues/69) | The documented agent entry point loads the prerepair branch | High | `.68` | Planned |
| [#71](https://github.com/vixttha/README-HQ/issues/71) | First-use smoke passes when its expected file predates the command | High | `.70` | Planned |
| [#84](https://github.com/vixttha/README-HQ/issues/84) | Monorepo smoke checks execute in the repository root | High | `.84` | Planned |
| [#85](https://github.com/vixttha/README-HQ/issues/85) | A smoke check can pass an output marker that neither stream emitted | High | `.85` | Planned |
| [#92](https://github.com/vixttha/README-HQ/issues/92) | Remote smoke checks skip the body of explicitly expected HTTP errors | Low | `.92` | Planned |
| [#96](https://github.com/vixttha/README-HQ/issues/96) | Remote smoke receipts omit the final URL after a redirect | Medium | `.96` | Planned |
| [#99](https://github.com/vixttha/README-HQ/issues/99) | Smoke configuration with both argv and URL silently skips the command | Medium | `.99` | Planned |
| [#101](https://github.com/vixttha/README-HQ/issues/101) | First-action smoke can change the audited repository’s shared Git configuration | High | `.101` | Planned |
| [#114](https://github.com/vixttha/README-HQ/issues/114) | Adopter flags can silently validate README HQ instead of the requested scope | Medium | `.114` | Planned |
| [#118](https://github.com/vixttha/README-HQ/issues/118) | The adopter validator rejects README HQ’s own documented Quickstart | High | `.118` | Planned |
| [#120](https://github.com/vixttha/README-HQ/issues/120) | Adopter guides omit the format for proving the first successful action | Medium | `.120` | Planned |
| [#126](https://github.com/vixttha/README-HQ/issues/126) | An explicitly requested smoke check can exit green without running | High | `.126` | Planned |
| [#127](https://github.com/vixttha/README-HQ/issues/127) | First-action failures omit the diagnostic needed to distinguish causes | Medium | `.127` | Planned |
| [#129](https://github.com/vixttha/README-HQ/issues/129) | A passing smoke command can certify a different, failing README Quickstart | High | `.129` | Added to plan |
| [#130](https://github.com/vixttha/README-HQ/issues/130) | Unchecked smoke receipts drop the requested URL and cannot distinguish two probes | Medium | `.130` | Added to plan |
| [#138](https://github.com/vixttha/README-HQ/issues/138) | A passing homepage audit can miss a broken link in its Quickstart guide | High | `.138` | Added to plan |

### GitHub navigation, rendering, and repository paths

Check the effective homepage and intended published destinations, accurately report gaps, and keep parser and Git lookup behavior consistent.

| Issue | Finding | Filed priority | Checkpoint | Planning status |
| --- | --- | --- | --- | --- |
| [#1](https://github.com/vixttha/README-HQ/issues/1) | Default GitHub homepage has no route to README HQ v0.0.6 | High | `.1` | Candidate acceptance open |
| [#2](https://github.com/vixttha/README-HQ/issues/2) | Archived BART homepages expose broken local documentation links | High | `.2` | Candidate acceptance open |
| [#6](https://github.com/vixttha/README-HQ/issues/6) | Navigation checker misses valid GFM link forms and misreads headings and inline code | Medium | `.6` | Candidate acceptance open |
| [#13](https://github.com/vixttha/README-HQ/issues/13) | Validation ignores the effective GitHub README when .github or docs supplies it | High | `.13` | Candidate acceptance open |
| [#15](https://github.com/vixttha/README-HQ/issues/15) | Valid GitHub repository-root links fail as filesystem escapes | Medium | `.15` | Candidate acceptance open |
| [#16](https://github.com/vixttha/README-HQ/issues/16) | Link audits can pass paths absent from the published Git tree | High | `.16` | Candidate acceptance open |
| [#29](https://github.com/vixttha/README-HQ/issues/29) | One malformed URL hides other validation findings | Medium | `.29` | Candidate acceptance open |
| [#38](https://github.com/vixttha/README-HQ/issues/38) | README validation accepts nonexistent source line links | Medium | `.38` | Candidate acceptance open |
| [#66](https://github.com/vixttha/README-HQ/issues/66) | Missing README fragments pass on directory links and alternate Markdown extensions | High | `.66` | Candidate acceptance open |
| [#67](https://github.com/vixttha/README-HQ/issues/67) | GitHub-rendered HTML named anchors fail README HQ link validation | Medium | `.67` | Candidate acceptance open |
| [#73](https://github.com/vixttha/README-HQ/issues/73) | GitHub branch links go unchecked when only the fetched remote ref exists | Medium | `.72` | Planned |
| [#80](https://github.com/vixttha/README-HQ/issues/80) | Root fragments use a different README than the homepage selector | Medium | `.80` | Planned |
| [#82](https://github.com/vixttha/README-HQ/issues/82) | Broken-link diagnostics point to the paragraph start instead of the link line | Medium | `.82` | Planned |
| [#89](https://github.com/vixttha/README-HQ/issues/89) | Bare GFM autolinks disappear from validation coverage | Medium | `.89` | Planned |
| [#90](https://github.com/vixttha/README-HQ/issues/90) | Passing a Git subdirectory silently changes the audited publication root | Medium | `.90` | Planned |
| [#93](https://github.com/vixttha/README-HQ/issues/93) | GitHub blob links are validated using local-only ref meanings | High | `.93` | Planned |
| [#104](https://github.com/vixttha/README-HQ/issues/104) | Pinned README reads can fetch missing objects from a Git promisor remote | Medium | `.104` | Planned |
| [#107](https://github.com/vixttha/README-HQ/issues/107) | A second query parameter makes valid GitHub plain line links fail validation | Medium | `.107` | Planned |
| [#110](https://github.com/vixttha/README-HQ/issues/110) | README navigation accepts heading fragments on raw GitHub file URLs | Medium | `.110` | Planned |
| [#111](https://github.com/vixttha/README-HQ/issues/111) | Draft navigation reads a substituted file through a symlinked parent directory | Medium | `.111` | Planned |
| [#119](https://github.com/vixttha/README-HQ/issues/119) | GitHub-rendered reStructuredText and AsciiDoc READMEs skip navigation validation | Medium | `.119` | Planned |
| [#121](https://github.com/vixttha/README-HQ/issues/121) | Heading links repeatedly read and parse the same pinned Git blob | Medium | `.121` | Planned |
| [#131](https://github.com/vixttha/README-HQ/issues/131) | README HQ cannot identify a GitHub-rendered Org README as the homepage | Medium | `.131` | Added to plan |

### Media, accessibility, and decoder support

Validate the actual image and its accessible role, bind checked bytes to receipts, and qualify the supported decoder and Python runtime.

| Issue | Finding | Filed priority | Checkpoint | Planning status |
| --- | --- | --- | --- | --- |
| [#28](https://github.com/vixttha/README-HQ/issues/28) | Media validation misses corrupt images and unnamed image-only links | Medium | `.28` | Candidate acceptance open |
| [#74](https://github.com/vixttha/README-HQ/issues/74) | GitHub dark-mode README images can be missing with a clean audit | Medium | `.73` | Planned |
| [#88](https://github.com/vixttha/README-HQ/issues/88) | Git LFS pointers are reported as corrupt README images | Medium | `.88` | Planned |
| [#95](https://github.com/vixttha/README-HQ/issues/95) | The README image check passes an animation with a truncated second frame | Medium | `.95` | Planned |
| [#106](https://github.com/vixttha/README-HQ/issues/106) | README media validation accepts a non-SVG XML namespace as an SVG image | Medium | `.106` | Planned |
| [#113](https://github.com/vixttha/README-HQ/issues/113) | README media can pass without an HTML text alternative | Medium | `.113` | Planned |
| [#135](https://github.com/vixttha/README-HQ/issues/135) | Published advisories affect the README validator’s pinned Pillow version | High | `.135` | Added to plan |
| [#139](https://github.com/vixttha/README-HQ/issues/139) | Draft receipts stay identical after verified image content changes | Medium | `.139` | Added to plan |
| [#140](https://github.com/vixttha/README-HQ/issues/140) | Markdown links containing a named HTML image fail the accessible-name check | Medium | `.140` | Added to plan |

### Technique registry and learning provenance

Keep one canonical technique identity, admit independently checked public sources, record target-specific decisions, and make the receipts reproducible.

| Issue | Finding | Filed priority | Checkpoint | Planning status |
| --- | --- | --- | --- | --- |
| [#8](https://github.com/vixttha/README-HQ/issues/8) | Technique registry accepts malformed schema and alias types | Medium | `.8` | Candidate acceptance open |
| [#18](https://github.com/vixttha/README-HQ/issues/18) | Registry treats unsupported verification claims as verified evidence | High | `.18` | Candidate acceptance open |
| [#19](https://github.com/vixttha/README-HQ/issues/19) | Evidence URL aliases can count one source as multiple entries | Medium | `.19` | Candidate acceptance open |
| [#20](https://github.com/vixttha/README-HQ/issues/20) | A duplicate technique survives under alternate names and outcome wording | Medium | `.20` | Candidate acceptance open |
| [#21](https://github.com/vixttha/README-HQ/issues/21) | Source audits lack a durable intake and candidate history | High | `.21` | Candidate acceptance open |
| [#22](https://github.com/vixttha/README-HQ/issues/22) | Technique output lacks a project-specific recommendation record | High | `.22` | Candidate acceptance open |
| [#23](https://github.com/vixttha/README-HQ/issues/23) | Public catalog validation accepts evidence explicitly marked private | High | `.23` | Candidate acceptance open |
| [#30](https://github.com/vixttha/README-HQ/issues/30) | Learning pilot recommends techniques with nonexistent target evidence | High | `.30` | Candidate acceptance open |
| [#31](https://github.com/vixttha/README-HQ/issues/31) | Optimized Python silently removes the learning pilot's provenance gates | Medium | `.31` | Candidate acceptance open |
| [#46](https://github.com/vixttha/README-HQ/issues/46) | Learning evidence accepts line zero and an empty anchor | High | `.46` | Candidate acceptance open |
| [#47](https://github.com/vixttha/README-HQ/issues/47) | Learning recommendations ignore retired technique status | Medium | `.47` | Candidate acceptance open |
| [#55](https://github.com/vixttha/README-HQ/issues/55) | Learning records can claim exact evidence with a moving HEAD | Medium | `.55` | Candidate acceptance open |
| [#60](https://github.com/vixttha/README-HQ/issues/60) | The documented technique list crashes on an ASCII output stream | Medium | `.60` | Candidate acceptance open |
| [#61](https://github.com/vixttha/README-HQ/issues/61) | A technique outcome key can collide with another technique's stable ID | Medium | `.61` | Candidate acceptance open |
| [#70](https://github.com/vixttha/README-HQ/issues/70) | The technique source inventory can attest to its own unverified entries | High | `.69` | Planned |
| [#76](https://github.com/vixttha/README-HQ/issues/76) | Renaming a request-local source ID creates duplicate learning history | Medium | `.75` | Planned |
| [#79](https://github.com/vixttha/README-HQ/issues/79) | Learning receipts can cite registry bytes that did not govern the decision | High | `.79` | Planned |
| [#81](https://github.com/vixttha/README-HQ/issues/81) | Wrong-shaped registry JSON bypasses CLI diagnostics and failure receipts | Medium | `.81` | Planned |
| [#87](https://github.com/vixttha/README-HQ/issues/87) | Learning intake records opposite decisions for the same evidence | Medium | `.87` | Planned |
| [#91](https://github.com/vixttha/README-HQ/issues/91) | The technique guide omits how to turn CLI evidence into a reviewed receipt | Medium | `.91` | Planned |
| [#97](https://github.com/vixttha/README-HQ/issues/97) | Learning intake silently drops misspelled technique IDs | Medium | `.97` | Planned |
| [#109](https://github.com/vixttha/README-HQ/issues/109) | Learning intake repeats public GitHub verification for each anchor in the same commit | Medium | `.109` | Planned |
| [#115](https://github.com/vixttha/README-HQ/issues/115) | Learning intake raises a traceback for a wrong-shaped request | Low | `.115` | Planned |
| [#128](https://github.com/vixttha/README-HQ/issues/128) | Learning intake reports the same error for transient API limits and invalid source evidence | Medium | `.128` | Planned |
| [#136](https://github.com/vixttha/README-HQ/issues/136) | Learning receipts can lose GitHub’s canonical repository identity after a rename | Medium | `.136` | Added to plan |
| [#137](https://github.com/vixttha/README-HQ/issues/137) | Learning receipts omit the exact anchor text used to verify a source | Low | `.137` | Added to plan |

### Graphify generation, source anchors, and MCP readback

Compile complete maps from pinned sources, verify exact source relations, and recover reliably when a staged publication fails.

| Issue | Finding | Filed priority | Checkpoint | Planning status |
| --- | --- | --- | --- | --- |
| [#7](https://github.com/vixttha/README-HQ/issues/7) | Graphify attributes standalone version testing to the imported-history verifier | Medium | `.7` | Candidate acceptance open |
| [#9](https://github.com/vixttha/README-HQ/issues/9) | A failed version-map batch leaves partial output and blocks retry | Medium | `.9` | Candidate acceptance open |
| [#10](https://github.com/vixttha/README-HQ/issues/10) | Graphify outline breaks table columns when a catalog title contains a pipe | Low | `.10` | Candidate acceptance open |
| [#25](https://github.com/vixttha/README-HQ/issues/25) | Generated Graphify Markdown source links miss GitHub line mode | Medium | `.25` | Candidate acceptance open |
| [#26](https://github.com/vixttha/README-HQ/issues/26) | Graphify selects code examples as documentation and change evidence | Medium | `.26` | Candidate acceptance open |
| [#33](https://github.com/vixttha/README-HQ/issues/33) | A single Graphify plan stops at 32 checkpoints | Medium | `.33` | Candidate acceptance open |
| [#34](https://github.com/vixttha/README-HQ/issues/34) | Graphify MCP verifier accepts the wrong evidence target | High | `.34` | Candidate acceptance open |
| [#36](https://github.com/vixttha/README-HQ/issues/36) | Graphify uses Git symlink pointers as source evidence | Medium | `.36` | Candidate acceptance open |
| [#40](https://github.com/vixttha/README-HQ/issues/40) | Graphify marks a current release with zero records as verified | High | `.40` | Candidate acceptance open |
| [#41](https://github.com/vixttha/README-HQ/issues/41) | Graphify records the wrong source line after a Unicode separator | High | `.41` | Candidate acceptance open |
| [#42](https://github.com/vixttha/README-HQ/issues/42) | Graphify file inventory rejects tracked README media | Medium | `.42` | Candidate acceptance open |
| [#43](https://github.com/vixttha/README-HQ/issues/43) | Standalone Graphify can overwrite a graph before its receipt write fails | High | `.43` | Candidate acceptance open |
| [#48](https://github.com/vixttha/README-HQ/issues/48) | Graphify’s MCP verifier truncates a supported 48-reference feature | High | `.48` | Candidate acceptance open |
| [#52](https://github.com/vixttha/README-HQ/issues/52) | Graphify verification rejects a clean checkout with core.autocrlf enabled | Medium | `.52` | Candidate acceptance open |
| [#53](https://github.com/vixttha/README-HQ/issues/53) | Graphify receipts can describe replacement Git objects under a pinned SHA | High | `.53` | Candidate acceptance open |
| [#54](https://github.com/vixttha/README-HQ/issues/54) | Graphify miscounts a valid filename as an MCP relation | Medium | `.54` | Candidate acceptance open |
| [#56](https://github.com/vixttha/README-HQ/issues/56) | The shipped Graphify self-map cannot build in a README HQ checkout | High | `.56` | Candidate acceptance open |
| [#63](https://github.com/vixttha/README-HQ/issues/63) | Automatic Graphify anchoring fails on published non-Markdown READMEs | Medium | `.63` | Candidate acceptance open |
| [#64](https://github.com/vixttha/README-HQ/issues/64) | Graphify rejects an exact Markdown anchor containing a standard joined emoji | Medium | `.64` | Candidate acceptance open |
| [#65](https://github.com/vixttha/README-HQ/issues/65) | Graphify labels a changelog placeholder as evidence for a specific release | High | `.65` | Candidate acceptance open |
| [#72](https://github.com/vixttha/README-HQ/issues/72) | Plan partitioning emits manifests above Graphify's source-file limit | High | `.71` | Planned |
| [#77](https://github.com/vixttha/README-HQ/issues/77) | Graphify temporarily removes the published graph and receipt during a successful update | Medium | `.76` | Planned |
| [#83](https://github.com/vixttha/README-HQ/issues/83) | Graphify accepts two references that collapse to one evidence edge | Medium | `.83` | Planned |
| [#100](https://github.com/vixttha/README-HQ/issues/100) | Graphify rejects ordinary binary inventory above its undocumented blob cap | Low | `.100` | Planned |
| [#105](https://github.com/vixttha/README-HQ/issues/105) | Standalone Graphify emits an MCP-verified receipt for a graph with no evidence | Medium | `.105` | Planned |
| [#116](https://github.com/vixttha/README-HQ/issues/116) | Graphify MCP readback verifies feature relations but omits source inventory relations | Medium | `.116` | Planned |
| [#123](https://github.com/vixttha/README-HQ/issues/123) | Graphify omits source view from reStructuredText and AsciiDoc line links | Medium | `.123` | Planned |
| [#125](https://github.com/vixttha/README-HQ/issues/125) | A failed plan partition leaves partial output that blocks an in-place retry | Medium | `.125` | Planned |

### Archive integrity and version navigation

Keep frozen snapshots, archive membership, and version links tied to independently identified source and release records.

| Issue | Finding | Filed priority | Checkpoint | Planning status |
| --- | --- | --- | --- | --- |
| [#3](https://github.com/vixttha/README-HQ/issues/3) | Archive validation accepts nonexistent source commits and tracked-mode drift | High | `.3` | Candidate acceptance open |
| [#4](https://github.com/vixttha/README-HQ/issues/4) | Frozen standalone versions can change while archive and Graphify checks pass | High | `.4` | Candidate acceptance open |
| [#5](https://github.com/vixttha/README-HQ/issues/5) | Version navigation can point to the wrong map and current version without failing CI | Medium | `.5` and `.77` | Original qualification and follow-up |
| [#39](https://github.com/vixttha/README-HQ/issues/39) | Deleting an archived screenshot and its record passes validation | High | `.39` | Candidate acceptance open |
| [#57](https://github.com/vixttha/README-HQ/issues/57) | A duplicate version-index row passes both README and Graphify checks | Medium | `.57` | Candidate acceptance open |

### CI evidence, GitHub provenance, and release authority

Keep the runner and tested SHA explicit, retain diagnostic evidence, and represent release approval and review eligibility accurately.

| Issue | Finding | Filed priority | Checkpoint | Planning status |
| --- | --- | --- | --- | --- |
| [#11](https://github.com/vixttha/README-HQ/issues/11) | Hosted validation can schedule paid-capable private jobs and has no automatic mode selection | High | `.11` | Candidate acceptance open |
| [#17](https://github.com/vixttha/README-HQ/issues/17) | Public validation misses the default-branch push publication path | Medium | `.17` | Candidate acceptance open |
| [#24](https://github.com/vixttha/README-HQ/issues/24) | Standalone reuse and imported material have no explicit rights boundary | Medium | `.24` | Candidate acceptance open |
| [#32](https://github.com/vixttha/README-HQ/issues/32) | Acceptance outcomes rely on expiring logs without a stand-alone run receipt | Medium | `.32` | Candidate acceptance open |
| [#35](https://github.com/vixttha/README-HQ/issues/35) | Graphify receipts accept an unrelated repository label | High | `.35` | Candidate acceptance open |
| [#44](https://github.com/vixttha/README-HQ/issues/44) | Graphify rejects historical PR commits outside GitHub’s listed window | Medium | `.44` | Candidate acceptance open |
| [#49](https://github.com/vixttha/README-HQ/issues/49) | Graphify’s PR manifest rejects a Git-valid branch name | Medium | `.49` | Candidate acceptance open |
| [#58](https://github.com/vixttha/README-HQ/issues/58) | README HQ has no trigger for required GitHub merge-queue checks | Medium | `.58` | Candidate acceptance open |
| [#59](https://github.com/vixttha/README-HQ/issues/59) | A moving PR head can produce an inconsistent Graphify provenance observation | High | `.59` | Candidate acceptance open |
| [#62](https://github.com/vixttha/README-HQ/issues/62) | Graphify rejects a complete PR review list at exactly ten full pages | Low | `.62` | Candidate acceptance open |
| [#75](https://github.com/vixttha/README-HQ/issues/75) | Missing draft README crashes failure reporting and drops the receipt | Medium | `.74` | Planned |
| [#78](https://github.com/vixttha/README-HQ/issues/78) | Adopter receipts can attribute a target file’s digest to the running validator | High | `.78` | Planned |
| [#98](https://github.com/vixttha/README-HQ/issues/98) | Graphify treats a retargeted pull request as one coherent observation | Medium | `.98` | Planned |
| [#102](https://github.com/vixttha/README-HQ/issues/102) | Adopter receipts omit the selected repository and validation profile | Medium | `.102` | Planned |
| [#103](https://github.com/vixttha/README-HQ/issues/103) | GitHub audit receipts cannot distinguish workflow attempts or jobs | Medium | `.103` | Planned |
| [#112](https://github.com/vixttha/README-HQ/issues/112) | An invalid receipt destination hides the actual README validation error | Low | `.112` | Planned |
| [#117](https://github.com/vixttha/README-HQ/issues/117) | Windows CI can report success after the README validator fails | High | `.117` | Planned |
| [#122](https://github.com/vixttha/README-HQ/issues/122) | The retained plan workflow validates before installing its required reader dependencies | Medium | `.122` | Planned |
| [#124](https://github.com/vixttha/README-HQ/issues/124) | Graphify CI skips receipt retention when verification fails | High | `.124` | Planned |
| [#132](https://github.com/vixttha/README-HQ/issues/132) | The owner-only publication gate has no active protection on GitHub main | High | `.132` | Added to plan |
| [#134](https://github.com/vixttha/README-HQ/issues/134) | Graphify exact-commit approval counts leave reviewer authority unspecified | Medium | `.134` | Added to plan |

### Repair-ledger validation

Keep current plans, acceptance cases, and graph inventories aligned as new findings are added.

| Issue | Finding | Filed priority | Checkpoint | Planning status |
| --- | --- | --- | --- | --- |
| [#37](https://github.com/vixttha/README-HQ/issues/37) | Duplicate JSON keys silently override validation inputs | High | `.37` | Candidate acceptance open |
| [#50](https://github.com/vixttha/README-HQ/issues/50) | Repair-plan CI accepts an unrelated test, change, and title for a checkpoint | High | `.50` | Candidate acceptance open |
| [#51](https://github.com/vixttha/README-HQ/issues/51) | Repair-plan CI passes when the Graphify evidence index has a dead link | Medium | `.51` | Candidate acceptance open |
| [#86](https://github.com/vixttha/README-HQ/issues/86) | Repair-plan validation passes after an entire source inventory is removed | High | `.86` | Planned |
| [#94](https://github.com/vixttha/README-HQ/issues/94) | Plan verification passes after a checkpoint’s acceptance criteria are deleted | High | `.94` | Planned |
| [#108](https://github.com/vixttha/README-HQ/issues/108) | Plan and version checks pass when navigation tables are hidden in fenced code | High | `.108` | Planned |
| [#133](https://github.com/vixttha/README-HQ/issues/133) | Automated planning updates are outside the active repair-ledger verification scope | Medium | `.133` | Added to plan |
