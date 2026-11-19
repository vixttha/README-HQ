# README HQ v0.0.6 repair pipeline

Baseline [`v0.0.6` at `f50e374`](https://github.com/vixttha/README-HQ/commit/f50e3749dab90ddfe35894284d1660097a1fb1a8). The [public audit](https://github.com/vixttha/README-HQ/actions/runs/44510897511) reproduced the initial ten findings. The [portability audit](https://github.com/vixttha/README-HQ/actions/runs/44513298531) added seven checkpoints. Each issue owns one cumulative repair checkpoint. The first checkpoint is ready to implement and the later checkpoints follow it in order.

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

## Checkpoint workflow

1. Reproduce the linked issue on the last verified revision. Record that revision and the audit fixture or test.
2. Make the scoped repair as its own checkpoint. Preserve a distinct commit and link it to the issue.
3. Run the checkpoint regression and applicable existing checks on standard public GitHub-hosted runners. Rebuild Graphify and query MCP for any change to graph generation, source evidence, or the version index.
4. Review the combined candidate against the intended base. Record the exact tested SHA, public runner links, Graphify evidence when relevant, and any unresolved conflicts on the issue before advancing to the next checkpoint.
5. Review the combined series after `v0.0.6.17`. Homepage publication and release decisions stay with the owner.

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
