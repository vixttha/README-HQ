<!-- catalog
{
  "title": "Guide readers through a pinned walkthrough with evidence",
  "summary": "Pair a task link and recognizable output with a pinned walkthrough and evidence of the checks that ran.",
  "tasks": ["quickstart", "first-result", "verification", "handoff"],
  "tags": ["onboarding", "proof-links", "release-evidence"],
  "aliases": ["two-version walkthrough", "first-use evidence path"],
  "evidence": "verified",
  "status": "active",
  "steps": [
    "role-based-entry-points",
    "first-success-milestone",
    "exact-revision-walkthrough",
    "claim-scope-labels",
    "declared-versus-observed-evidence"
  ]
}
-->

# Guide readers through a pinned walkthrough with evidence

**Reader task.** Find an example, recognize its result, and trace the result to a check at the advertised revision.

**Use when.** The project has a repeatable first action and a safe fixture, demo, or sample input. An agent can offer this combination to the adopter and explain which steps fit the project.

| Step | Technique | Contribution | When to adapt |
| --- | --- | --- | --- |
| 1 | [Route by reader task](../techniques/role-based-entry-points.md) | Surface the walkthrough from the homepage. | Use the equivalent first action for a game, library, or template. |
| 2 | [Show a recognizable first result](../techniques/first-success-milestone.md) | Tell the reader what success looks like. | Use a visible milestone or generated file if there is no terminal output. |
| 3 | [Execute the documented walkthrough](../techniques/exact-revision-walkthrough.md) | Exercise the advertised action at the pinned revision. | State explicitly when an environment or fixture prevents execution. |
| 4 | [Label the scope of compatibility evidence](../techniques/claim-scope-labels.md) | Tie the claim to the tested revision, task, and platform. | Include only distinctions that affect the reader. |
| 5 | [Distinguish intended checks from results](../techniques/declared-versus-observed-evidence.md) | Show discovery, execution, and handoff outcomes separately. | Record skipped or pending checks with their scope. |

**Result to check.** Start at the candidate README, find the walkthrough, run the documented example, recognize the expected output, and reach the corresponding evidence. Start a separate handoff check from the adopter workspace.

**Evidence.** The Veraphify pilot found the walkthrough and evidence links in the rendered draft. The public Ubuntu job ran the pinned walkthrough and returned the two expected citations. The clean adopter checkout recovered the task and README HQ revision, while locating the draft and product revisions required a separate PR lookup. [Pinned pilot](https://github.com/vixttha/README-HQ/blob/f6bc7b41af8dca7b7bf0671c851d041a55d77e71/trials/veraphify-two-version-lookup.md) · [Public walkthrough job](https://github.com/vixttha/Veraphify/actions/runs/44640005952/job/135968332305)

**Limits.** The verified outcome covers discovery and execution at the pilot's cited revisions. The independent fresh-agent handoff remains pending in the pinned pilot.
