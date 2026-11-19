# README HQ portability and quality acceptance

Audit baseline [README HQ v0.0.6 at f50e374](https://github.com/vixttha/README-HQ/commit/f50e3749dab90ddfe35894284d1660097a1fb1a8). The portability fixtures exercise known gaps. The acceptance cases below describe the behavior a candidate needs to prove.

## Repository and runner detection

| Detected repository visibility | Execution approach | Evidence to record |
| --- | --- | --- |
| Verified public GitHub | Standard public GitHub-hosted runners | Hosting repository, visibility source, tested SHA, workflow and jobs |
| Verified private or internal GitHub | Offline validation or an explicitly configured private runner | Visibility, authorized execution environment, and private receipt location |
| Unknown or inaccessible | Local inspection of available material, with scheduling blocked until visibility and execution policy are known | Missing metadata, affected checks, and coverage |
| Non-GitHub or offline checkout | Inspect the local tree and report the available checks | Ref, origin when known, and GitHub-only checks skipped |

Use GitHub's repository metadata for the authorized target. For an Actions job, the workflow's hosting repository determines runner policy. For PRs, identify the target project and the candidate's tree separately, including fork heads. Missing metadata, an inaccessible remote, or conflicting signals should produce an actionable unresolved result. A private or internal repository uses private receipt storage and avoids public artifact uploads.

Relevant GitHub rules cover [Actions billing](https://docs.github.com/en/actions/concepts/billing-and-usage), [repository metadata](https://docs.github.com/en/rest/repos/repos#get-a-repository), and [README precedence and rendering](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes).

## Representative acceptance cases

| Test case | What it should prove |
| --- | --- |
| Public, private, internal, missing metadata, offline remote, and fork PR | Mode and runner policy match the authorized repository. Use simulated events for non-public scheduling until an approved private environment exists. |
| Default branches named main, master, trunk, and release/main | Detect the default branch and test the intended PR candidate and final commit when a documented publication path uses either. |
| Root, docs, and .github READMEs, including multiple competing files | Match GitHub's visible entry, resolve links relative to that file, support repository-root links, and report competing candidates. |
| Python CLI, JS application, compiled utility, browser game, and starter template | Resolve the advertised entry point from the project's actual manifest or source. Run a declared first-use smoke test when an approved execution path exists. |
| Monorepo, documentation-only repo, empty repo, or unknown stack | Select a first action that matches the repo. Use a docs route for docs-only projects. Report ambiguous or missing entry points. |
| Missing asset, wrong-case link, untracked file, redirected URL, and separately pinned ref | Check links and images against the published Git tree, then report failures or explicitly unverified external destinations. |
| Valid titled and reference links, Setext headings, inline literals, and GFM tables | Match GitHub's rendered links and anchors, and preserve text in the expected columns. |
| Empty README, generic placeholder, over-display-size entry, stale setup examples, and undocumented platform claims | Reject active placeholders and missing first actions. Flag truncation and require source evidence for setup, prerequisites, result, and material claims. |
| Archived, gated, or platform-specific project | State supported scope and the verified reader path. Preserve historical claims as versioned evidence. |
| Private or internal fixture with a synthetic sensitive marker | No private repository content or evidence is exported to public reports, logs, or artifact storage. Run the fixture against the defined local or approved private path. |

For external evaluation, use frozen, independent public repositories held out from the development fixtures. Cover several kinds of project, different README layouts, repository sizes, missing evidence, and different documented targets. Record the eligible repositories and the reasons any are blocked so they remain visible in the report.

## Quality criteria

Mechanical checks can prove the correct README was selected, links and media resolve on the intended revision, accepted examples produce their documented output, and relevant claims point to evidence. Score the remainder separately with a reviewer who sees the target repository and the draft. Review audience fit, accuracy, clarity, first-use usefulness, and accessibility of prose and layout. Require clear supporting evidence for material statements. A successful validator exit alone is insufficient evidence of README quality.

For a measured 99% target, track two outcomes independently. One is whether the workflow completes reliably on supported repositories. The second is whether produced READMEs pass the quality rubric. Under an independent binomial sampling model, 299 successes with zero failures give a one-sided 95% lower confidence bound just above 99% for one outcome. This calculation depends on the sampling design. The current fixtures are diagnostic cases and do not estimate either rate.
