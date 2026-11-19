# README HQ v0.0.6 repair pipeline

Baseline [`v0.0.6` at `f50e374`](https://github.com/vixttha/README-HQ/commit/f50e3749dab90ddfe35894284d1660097a1fb1a8). The [public audit](https://github.com/vixttha/README-HQ/actions/runs/44510897511) reproduced the initial ten findings. The [portability audit](https://github.com/vixttha/README-HQ/actions/runs/44513298531) added seven checkpoints. The [learning audit](https://github.com/vixttha/README-HQ/actions/runs/44515197237) adds seven through `v0.0.6.24`. The [assurance audit](https://github.com/vixttha/README-HQ/actions/runs/44516410470) and Graphify capacity check add nine through `v0.0.6.33`. Each issue owns one cumulative repair checkpoint. The first checkpoint is ready to implement and the later checkpoints follow it in order.

[Graphify plan](../../graphify-hq/plans/v0.0.6-repairs/README.md)

## Checkpoints

| Checkpoint | GitHub issue | Repair | Priority | Start after |
| --- | --- | --- | --- | --- |
| `v0.0.6.1` | [#1](https://github.com/vixttha/README-HQ/issues/1) | Default homepage discovery | High | Audited `v0.0.6` |
| `v0.0.6.2` | [#2](https://github.com/vixttha/README-HQ/issues/2) | Archived BART homepage links | High | `v0.0.6.1` |
| `v0.0.6.3` | [#3](https://github.com/vixttha/README-HQ/issues/3) | Source provenance and tracked modes | High | `v0.0.6.2` |
| `v0.0.6.4` | [#4](https://github.com/vixttha/README-HQ/issues/4) | Frozen standalone version integrity | High | `v0.0.6.3` |
| `v0.0.6.5` | [#5](https://github.com/vixttha/README-HQ/issues/5) | Version-to-map and homepage mapping | Medium | `v0.0.6.4` |
| `v0.0.6.6` | [#6](https://github.com/vixttha/README-HQ/issues/6) | GitHub Markdown navigation | Medium | `v0.0.6.5` |
| `v0.0.6.7` | [#7](https://github.com/vixttha/README-HQ/issues/7) | Record-specific Graphify evidence | Medium | `v0.0.6.6` |
| `v0.0.6.8` | [#8](https://github.com/vixttha/README-HQ/issues/8) | Technique registry field types | Medium | `v0.0.6.7` |
| `v0.0.6.9` | [#9](https://github.com/vixttha/README-HQ/issues/9) | Failed batch recovery | Medium | `v0.0.6.8` |
| `v0.0.6.10` | [#10](https://github.com/vixttha/README-HQ/issues/10) | Graphify table escaping | Low | `v0.0.6.9` |
| `v0.0.6.11` | [#11](https://github.com/vixttha/README-HQ/issues/11) | Automatic repository mode and runner safety | High | `v0.0.6.10` |
| `v0.0.6.12` | [#12](https://github.com/vixttha/README-HQ/issues/12) | Portable adopter target and ref | High | `v0.0.6.11` |
| `v0.0.6.13` | [#13](https://github.com/vixttha/README-HQ/issues/13) | GitHub-visible README discovery | High | `v0.0.6.12` |
| `v0.0.6.14` | [#14](https://github.com/vixttha/README-HQ/issues/14) | Mechanical README quality gates | High | `v0.0.6.13` |
| `v0.0.6.15` | [#15](https://github.com/vixttha/README-HQ/issues/15) | Repository-root-relative links | Medium | `v0.0.6.14` |
| `v0.0.6.16` | [#16](https://github.com/vixttha/README-HQ/issues/16) | Published Git tree link verification | High | `v0.0.6.15` |
| `v0.0.6.17` | [#17](https://github.com/vixttha/README-HQ/issues/17) | Default-branch publication coverage | Medium | `v0.0.6.16` |
| `v0.0.6.18` | [#18](https://github.com/vixttha/README-HQ/issues/18) | Verified source and run binding | High | `v0.0.6.17` |
| `v0.0.6.19` | [#19](https://github.com/vixttha/README-HQ/issues/19) | Canonical evidence identity | Medium | `v0.0.6.18` |
| `v0.0.6.20` | [#20](https://github.com/vixttha/README-HQ/issues/20) | Duplicate mechanism detection | Medium | `v0.0.6.19` |
| `v0.0.6.21` | [#21](https://github.com/vixttha/README-HQ/issues/21) | Durable source-learning intake | High | `v0.0.6.20` |
| `v0.0.6.22` | [#22](https://github.com/vixttha/README-HQ/issues/22) | Project-specific recommendation receipts | High | `v0.0.6.21` |
| `v0.0.6.23` | [#23](https://github.com/vixttha/README-HQ/issues/23) | Public and private learning separation | High | `v0.0.6.22` |
| `v0.0.6.24` | [#24](https://github.com/vixttha/README-HQ/issues/24) | Reuse and attribution boundary | Medium | `v0.0.6.23` |
| `v0.0.6.25` | [#25](https://github.com/vixttha/README-HQ/issues/25) | Exact Markdown evidence permalinks | Medium | `v0.0.6.24` |
| `v0.0.6.26` | [#26](https://github.com/vixttha/README-HQ/issues/26) | Rendered Graphify source anchors | Medium | `v0.0.6.25` |
| `v0.0.6.27` | [#27](https://github.com/vixttha/README-HQ/issues/27) | Behavioral first-use validation | High | `v0.0.6.26` |
| `v0.0.6.28` | [#28](https://github.com/vixttha/README-HQ/issues/28) | Media and accessible image links | Medium | `v0.0.6.27` |
| `v0.0.6.29` | [#29](https://github.com/vixttha/README-HQ/issues/29) | Complete diagnostics | Medium | `v0.0.6.28` |
| `v0.0.6.30` | [#30](https://github.com/vixttha/README-HQ/issues/30) | Target evidence binding | High | `v0.0.6.29` |
| `v0.0.6.31` | [#31](https://github.com/vixttha/README-HQ/issues/31) | Optimization-safe verification | Medium | `v0.0.6.30` |
| `v0.0.6.32` | [#32](https://github.com/vixttha/README-HQ/issues/32) | Durable acceptance receipts | Medium | `v0.0.6.31` |
| `v0.0.6.33` | [#33](https://github.com/vixttha/README-HQ/issues/33) | Graphify roadmap capacity | Medium | `v0.0.6.32` |

## Checkpoint workflow

1. Reproduce the linked issue on the last verified revision. Record that revision and the audit fixture or test.
2. Make the scoped repair as its own checkpoint. Preserve a distinct commit and link it to the issue.
3. Run the checkpoint regression and applicable existing checks on standard public GitHub-hosted runners. Rebuild Graphify and query MCP for any change to graph generation, source evidence, or the version index.
4. Review the combined candidate against the intended base. Record the exact tested SHA, public runner links, Graphify evidence when relevant, and any unresolved conflicts on the issue before advancing to the next checkpoint.
5. Review the combined series after `v0.0.6.33`. Homepage publication and release decisions stay with the owner.

## Verification by checkpoint

### v0.0.6.1

- Add a clear route from the default GitHub landing page to the active README HQ version, version index, and Graphify index.
- Open the default repo page or plain clone and follow every advertised link to its expected target.

### v0.0.6.2

- Restore navigable documentation links for the BART v0.0.3 and v0.0.4 homepage snapshots while preserving the frozen README bytes.
- Verify both indexed reading paths and all reported relative destinations. Compare archived README hashes with the audited copies.

### v0.0.6.3

- Verify the archive's source repository, commit, path, blob, and tracked mode against independently pinned evidence.
- Reject an unrelated or nonexistent source commit and a mode-only change. Verify valid imported snapshots still pass.

### v0.0.6.4

- Bind accepted standalone README and changelog bytes to source evidence used by archive validation and Graphify.
- Change a frozen changelog in a disposable checkout and confirm the candidate checks reject the drift. Verify the unchanged snapshot passes.

### v0.0.6.5

- Require each version row to link to its own map and make the homepage current version agree with the canonical index.
- Retarget the v0.0.6 row to the v0.0.5 map and the homepage to v0.0.1. Confirm both valid-but-wrong targets are rejected.

### v0.0.6.6

- Check rendered Markdown link forms and GitHub heading anchors while ignoring inline code and other literal examples.
- Reject missing targets in titled, reference-style, and supported HTML links. Accept the Setext anchor and inline-code example.

### v0.0.6.7

- Give each Graphify record the correct verification reference for its own artifact.
- Query the standalone and imported version nodes over MCP and verify they cite the validators that cover their respective artifacts.

### v0.0.6.8

- Enforce the registry schema and explicit field types before normalizing IDs or aliases.
- Reject a Boolean schema and a string in place of the aliases array. Preserve the valid catalog and the public list command.

### v0.0.6.9

- Publish a complete Graphify batch only after all maps and receipts pass, with a safe retry path.
- Force the second map build to fail. Confirm the destination remains safe and rerunning the same output succeeds when the fault is removed.

### v0.0.6.10

- Escape delimiters in catalog titles and summaries before rendering Markdown table cells.
- Generate a row with pipe characters and verify it renders as exactly three cells with the original readable text.

### v0.0.6.11

- Classify the trusted hosting repository before any jobs are scheduled. Verify public, private, internal, unknown, and fork-PR metadata. Only verified public mode may schedule standard hosted validation. Use offline validation or an explicitly configured private environment for private/internal mode, and keep evidence private.

### v0.0.6.12

- Run an explicit target/ref for a plain project and a monorepo without requiring HQ's history, registry, or version folders. Report the selected repo, entry point, Git tree, applicable checks, and verification gaps.

### v0.0.6.13

- Resolve the GitHub-visible README using .github, root, and docs precedence. Run link checks relative to the selected file. Cover competing files, a docs-only README, and a reportable missing README.

### v0.0.6.14

- Add a profile-aware quality check for empty and placeholder content, visible first action, justified prerequisites, and verifiable material claims. Detect GitHub display truncation and keep qualitative review as a separate result.

### v0.0.6.15

- Resolve leading-slash GitHub paths from the repository root and ordinary relative paths from the README location. Test both forms in nested folders and continue rejecting references outside the selected repository tree.

### v0.0.6.16

- Validate checkout-relative and recognized same-repository links against the exact tracked publication tree and ref. Exercise untracked paths, wrong-case paths, explicit refs, and existing links on both Linux and Windows. Report any ref that cannot be resolved.

### v0.0.6.17

- Validate the adopter's configured publication branch on supported push and PR events while preserving the pre-scheduling visibility gate. Test at least main, master, trunk, and a custom branch.

## Portability and quality acceptance

[Acceptance matrix](https://github.com/vixttha/README-HQ/blob/97037dfb94241182b2471bcb33e7dc9a21557019/audits/portability-and-quality.md) · [Public audit](https://github.com/vixttha/README-HQ/actions/runs/44513298531)

## Learning and project-specific outputs

[Learning workflow and pilot](https://github.com/vixttha/README-HQ/blob/a8d97d0559853538d4d814edf5c998e42cfec3d2/learning/README.md) · [Public learning audit](https://github.com/vixttha/README-HQ/actions/runs/44515197237)

### v0.0.6.18

- Bind each finding to a source repository, full commit, path or artifact digest, and anchor. Use observed for a documented pattern. Require outcome, environment, and exact execution evidence before marking a behavioral claim verified.

### v0.0.6.19

- Normalize evidence identity to repository, commit, path, and evidence span while grouping same-file observations under the same source. Preserve relevant source lines and keep aliases or mirrors from inflating independent corroboration.

### v0.0.6.20

- Detect exact repeated mechanisms with a canonical signature, flag semantic overlap for review, and retain one stable ID with aliases and corroborating evidence. Test against both active and retired techniques.

### v0.0.6.21

- Create an idempotent learning intake for supplied source repositories and in-flight discoveries. Persist source revision, candidate identity, disposition, and provenance. Demonstrate that repeated intake records new evidence once and retains versioned history.

### v0.0.6.22

- Bind recommendations to a target tree, owner-selected references, actual audience and capabilities, and the matching technique record. Record adopt, adapt, already present, declined, irrelevant, or insufficient evidence. Test that changing target facts or allowed sources changes the applicable recommendations.

### v0.0.6.23

- Keep public shared learning and private project receipts isolated. Require independently resolved visibility and provenance before public admission. Verify using a synthetic private marker that public outputs and logs contain no private identifiers, links, or excerpts.

### v0.0.6.24

- Record an owner decision on the HQ template's own reuse terms. For learning from an external example, cite the evidence and store an original abstraction. Require explicit license and attribution metadata before including copied material. Keep unresolved rights visible.

## Assurance and regression verification

[Audit findings and acceptance rubric](https://github.com/vixttha/README-HQ/blob/ef4648eefd09dad06f6901fe81e81f493aef4ef7/audits/assurance-v0.0.6.md) · [Public reproduction](https://github.com/vixttha/README-HQ/actions/runs/44516410470)

The installed Graphify template accepts at most 32 feature nodes per manifest. The [evidence map index](../../graphify-hq/plans/v0.0.6-repairs/README.md) groups the same ordered pipeline into two compilable maps.

### v0.0.6.25

- Generate immutable Markdown source links with the commit, file path, plain-file mode, and accurate line fragment. Verify at least one public source link opens with its exact line highlighted.

### v0.0.6.26

- Select source anchors from rendered source structure or explicit reviewed line anchors. Ignore fenced and indented code for heading and changelog detection. Report an ambiguous or absent anchor.

### v0.0.6.27

- Support explicitly declared, authorized first-use smoke checks with exact revision, environment, invocation, and expected result. Fail on unsuccessful exit and on successful exit with the wrong outcome. Record unsupported, skipped, and unverified scenarios clearly.

### v0.0.6.28

- Verify local media against the published blob using supported format checks. Require a meaningful accessible name for image-only controls and links. Preserve decorative empty alt text where adjacent accessible content already describes the action.

### v0.0.6.29

- Collect file and line diagnostics per URL, continue across independent validation cases, and return a failing result with each observed defect. Keep explicit reporting for sections the validator cannot inspect.

### v0.0.6.30

- Require a resolved target evidence receipt for applicable claims. Verify target facts against a pinned tree, report unresolved evidence, and abstain or mark the recommendation preliminary when the target match cannot be established. Link this pilot defect to the broader project-specific recommendation work in #22.

### v0.0.6.31

- Use explicit conditional failures for provenance and pass/fail reporting, or fail clearly before verification in unsupported execution modes. Test identical malformed evidence under normal and optimized interpreter settings.

### v0.0.6.32

- Generate an exact-SHA, machine-readable acceptance receipt with expected cases, outcomes, skips, source hashes, tool versions, and run references. Preserve accepted public receipts in a durable location and keep private evidence isolated.

### v0.0.6.33

- Generalize Graphify plan partitioning for arbitrary checkpoint counts and verify that no checkpoint is dropped, duplicated, or disconnected across maps.
