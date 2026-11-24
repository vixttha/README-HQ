# Publication gate proposal — not applied

This is an administration proposal for #132, not a declaration that main is protected. The current repository is public and owned by an individual. GitHub readback on 2026-11-24 reported main unprotected at a7a989ffb6b664df86aae0ea01053ea2fc0a4405, no repository rulesets, and the classic protection endpoint returned HTTP 403 to the connected app. No administration write action is available.

## Proposed settings
- Target only refs/heads/main; require a PR, current base and three GitHub Actions status contexts from app 15368.
- Require zero approving reviewers for solo operation; the owner records a separate exact-SHA decision. Require conversation resolution; disallow force pushes and deletion; allow merge commits, not squash or rebase, to preserve checkpoint ancestry.
- No automatic merge, bypass actor, paid runner or required self-review. Do not enable this until the owner can review the consequences and the required checks are selectable.
- [Ruleset API documentation](https://docs.github.com/en/rest/repos/rules) and [repository rulesets](https://github.com/vixttha/README-HQ/settings/rules). The adjacent JSON is a proposed GitHub repository ruleset creation payload, not an active rule or a verified UI import.

## Queue scope (#58)
GitHub's [merge queue availability](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) is organization-owned public repos and eligible organization-owned private repos. Keep merge_group: checks_requested in the portable workflow. Use direct PR integration and strict status checks for this personal repository. Actual queue behavior for adopters is unverified and needs separate scoped validation on an eligible public organization repository. No repo transfer or organization creation authorized.

## Reuse (#24)
Existing REUSE.md remains unchanged. No standalone reuse license has been selected by the owner. Preserve imported source terms, original abstractions and review permission/attribution before copying. Publication review does not grant a license. No permission change is inferred from a request to fix defects.

## Readback
After owner application, run the existing read-only tools/check_publication_rules.py with the three exact status check names. Require protected=true, requires_pull_request=true, no missing required checks, and mechanical_gate=observed. Independently verify no bypass and merge-commit policy in GitHub settings. Retain exact-SHA owner authorization separately in #156. Do not merge or release while these controls are unresolved.
