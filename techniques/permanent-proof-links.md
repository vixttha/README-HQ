<!-- catalog
{
  "title": "Permanent proof links",
  "summary": "Keep verification traceable with a commit-pinned receipt and recorded run, attempt, artifact ID, and digest.",
  "tasks": [
    "verification",
    "handoff"
  ],
  "tags": [
    "ci",
    "git",
    "release-evidence"
  ],
  "aliases": [
    "durable verification receipt",
    "pinned proof links"
  ],
  "evidence": "verified",
  "status": "active",
  "use_when": "A public claim needs evidence that can be traced back to the exact run and revision."
}
-->

# Permanent proof links

**Use when.** A public claim needs evidence that can be traced back to the exact run and revision.

**Problem.** Run and artifact links can expire. A future reviewer may be unable to identify what revision was tested or what evidence the run produced.

**Practice.** Link to a receipt committed in Git and pin that link to a full commit SHA. In the receipt, record the tested revision, workflow or job, run ID, attempt, outcome, and the artifact ID and digest when available.

**Example.** README HQ’s full-stack audit receipt preserves the run and attempt, exact tested revision, per-platform job IDs, and archive IDs and SHA-256 digests. Those digests were checked during the audit.

**Limits.** A digest establishes identity when you have the original bytes. Preserve any report that must stay readable in public-safe, durable storage. The receipt records what was checked if the artifact expires.

**Result to check.** Starting from the receipt alone, identify the exact revision and run attempt. If the artifact is still available, download it and compare its digest to the receipt.

**Evidence.** Verified for the cited check. [Pinned README HQ audit receipt](https://github.com/vixttha/README-HQ/blob/2f66dd6aa23928716f645cfebdce462b7574c4b3/audit/evidence/v0.0.6.67-full-stack.json) · [GitHub file permalinks](https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files) · [GitHub artifact validation](https://docs.github.com/en/actions/tutorials/store-and-share-data#validating-artifacts)
