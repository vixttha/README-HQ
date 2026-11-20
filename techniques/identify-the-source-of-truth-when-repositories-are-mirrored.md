<!-- catalog
{
  "title": "Identify the source of truth when repositories are mirrored",
  "summary": "Name the canonical repository and explain which revision identifiers to cite from a mirror.",
  "tasks": [
    "handoff"
  ],
  "tags": [
    "lifecycle"
  ],
  "aliases": [
    "canonical repo for mirrors"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "A mirror exposes code and directs decisions or contributions elsewhere."
}
-->

# Identify the source of truth when repositories are mirrored

**Use when.** A mirror exposes code and directs decisions or contributions elsewhere.

**Reader task.** Handoff and maintenance.

**Practice.** Name the canonical repository and explain which revision identifiers to cite from a mirror. SQLite’s GitHub README points to Fossil and tells readers where to find the official check-in name.

**Example (illustrative).** State that the primary repository owns issues and show how to translate a mirror revision for citations.

**Result to check.** A reader starting from the mirror can find the canonical source revision.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [SQLite mirror guidance](https://github.com/sqlite/sqlite/blob/28c1e4669d7649506c5bf640f62ce3abfc0114fa/README.md#L15-L29) [Kubernetes’s published staging repositories](https://github.com/kubernetes/kubernetes/blob/dee14a0ede00099d6441a8991ad6137b938d2a9d/staging/README.md#L1-L16)
