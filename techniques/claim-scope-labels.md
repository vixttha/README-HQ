<!-- catalog
{
  "title": "Label the scope of compatibility evidence",
  "summary": "State the version, platform, capability, and checks that support a compatibility claim.",
  "tasks": [
    "verification",
    "overview"
  ],
  "tags": [
    "compatibility",
    "release-evidence"
  ],
  "aliases": [
    "release and development evidence",
    "scoped compatibility claims"
  ],
  "evidence": "observed",
  "status": "active"
}
-->

# Label the scope of compatibility evidence

**Problem.** Readers can mistake a check of one command or preview commit for support on every platform or in a released build.

**Practice.** Put the scope beside the claim. Name the relevant release or revision, platform, runtime, and feature. Use a small matrix only when it helps readers compare supported choices.

**Example.** BART separates Python-only inspection from capabilities that require Blender and provides platform-specific setup steps at the cited revision.

**Limits.** Record unknown or untested environments when they affect a reader’s decision. State release and development coverage separately if those results differ.

**Result to check.** Pick a capability and environment from the table or paragraph and trace the claim to the evidence for that exact combination.

**Evidence.** Observed in the cited guidance or example. [Pinned BART README](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/blob/3e7f9e02e61739825b56bcafecebbd0221cc9657/README.md#compatibility) · [Original README HQ registry](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/techniques/registry.json)
