<!-- catalog
{
  "title": "Distinguish intended checks from results",
  "summary": "Show which checks were planned and which actually ran, with a scoped outcome for each.",
  "tasks": ["verification", "first-result", "handoff"],
  "tags": ["coverage", "release-evidence"],
  "aliases": ["planned versus executed checks"],
  "evidence": "verified",
  "status": "active"
}
-->

# Distinguish intended checks from results

**Problem.** A workflow declaration or passing job can be mistaken for proof that every advertised check actually ran.

**Practice.** For each reader task, name the revision and action. Record the outcome separately from intended coverage, including skipped or unsupported checks. Link to the run attempt, job, or retained result that shows what executed.

**Example.** Veraphify records the Ubuntu build and lookup separately from independent archive replay. The README HQ trial records homepage discovery and walkthrough execution as passed at their tested revisions and the adopter handoff as partial.

**Limits.** Replay evidence covers archive replay. A reader journey and a fresh agent handoff each need their own result.

**Result to check.** Follow a claim to the exact job or retained outcome and identify what was executed and what still needs checking.

**Evidence.** [Original technique ID](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/techniques/registry.json) · [Pinned verification guide](https://github.com/vixttha/Veraphify/blob/c0a03f7e40b115c51fbc4be2a45f50ce1dee46f7/docs/verification.md) · [Scoped trial outcomes](https://github.com/vixttha/README-HQ/blob/f6bc7b41af8dca7b7bf0671c851d041a55d77e71/trials/veraphify-two-version-lookup.md#results)
