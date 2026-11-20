<!-- catalog
{
  "title": "Clean consumer adoption test",
  "summary": "Verify documented copy-in or install steps in a fresh consumer project.",
  "tasks": [
    "verification",
    "quickstart"
  ],
  "tags": [
    "verification",
    "reproduction"
  ],
  "aliases": [
    "fresh adopter smoke test"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "Producer-local files or caches may hide problems in consumer adoption."
}
-->

# Clean consumer adoption test

**Use when.** Producer-local files or caches may hide problems in consumer adoption.

**Reader task.** Verification and trust.

**Practice.** Verify documented copy-in or install steps in a fresh consumer project.

**Example (illustrative).** Run the published install instructions in a clean checkout of a separate consumer project.

**Result to check.** The consumer reaches the first result without depending on producer-only files or caches.

**Evidence.** Illustrative practice. Add a project example or test result when this technique is evaluated.
