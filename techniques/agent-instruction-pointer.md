<!-- catalog
{
  "title": "Link authoritative agent instructions",
  "summary": "Point an agent to the repository’s applicable instructions from the README.",
  "tasks": [
    "handoff",
    "navigation"
  ],
  "tags": [
    "agents",
    "onboarding"
  ],
  "aliases": [
    "agent entry point",
    "agent instruction link"
  ],
  "evidence": "observed",
  "status": "active"
}
-->

# Link authoritative agent instructions

**Problem.** An agent can find general product instructions before it finds the repository’s rules for editing, validating, or handing off work.

**Practice.** Link to the applicable tracked `AGENTS.md` or project equivalent. For a monorepo, name the project or directory covered when the route would otherwise be ambiguous.

**Example.** AlderVale keeps agent workflow instructions in its tracked agent file. Brand Identity Template’s README explains how a consuming project can connect the kit to existing agent instructions.

**Limits.** Keep the actual instructions in their authoritative file so linked summaries do not drift. Check that the intended agent can read the target at the ref it is using.

**Result to check.** Give an agent the README and target path. Verify that it locates the applicable instructions before making a change.

**Evidence.** Observed in the cited guidance or example. [Pinned AlderVale agent instructions](https://github.com/vixttha/AlderVale-Pact-of-Ten/blob/a6c2060b8175f505cc6327ccb5658cc00a458b24/AGENTS.md) · [Pinned Brand Identity Template README](https://github.com/vixttha/Brand-Identity-Template/blob/87d0f9aedbe69ca4b16815d6b3329efcf5889da9/README.md) · [Original README HQ registry](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/techniques/registry.json)
