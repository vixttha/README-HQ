<!-- catalog
{
  "title": "Show a benchmark case that changes the takeaway",
  "summary": "Beside a favorable result, include a reproducible workload or flag change that reduces the advantage or changes performance.",
  "tasks": [
    "verification"
  ],
  "tags": [
    "verification",
    "reproduction"
  ],
  "aliases": [
    "benchmark counterexample"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "A benchmark advantage depends heavily on data or workload shape."
}
-->

# Show a benchmark case that changes the takeaway

**Use when.** A benchmark advantage depends heavily on data or workload shape.

**Reader task.** Verification and trust.

**Practice.** Beside a favorable result, include a reproducible workload or flag change that reduces the advantage or changes performance. ripgrep shows performance cliffs and cases with many matches.

**Example (illustrative).** Show both the sparse dataset and a dense dataset on which the speed advantage shrinks.

**Result to check.** The second workload is reproducible and its result qualifies the headline claim.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [ripgrep performance caveats](https://github.com/BurntSushi/ripgrep/blob/16f9b2e64a42c43a469f72260226a6c65a4c88b9/README.md#L77-L114)
