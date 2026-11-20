<!-- catalog
{
  "title": "Save or persistence checkpoint",
  "summary": "Tell readers what should survive a restart and how to confirm it.",
  "tasks": [
    "first-result"
  ],
  "tags": [
    "stored-state"
  ],
  "aliases": [
    "save and reload checkpoint"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "The first task writes state that the reader expects to retain."
}
-->

# Save or persistence checkpoint

**Use when.** The first task writes state that the reader expects to retain.

**Reader task.** First result and recovery.

**Practice.** Tell readers what should survive a restart and how to confirm it.

**Example (illustrative).** Save the example workspace, reopen it, and inspect the item just created.

**Result to check.** The named change survives a fresh session in the supported environment.

**Evidence.** Illustrative practice. Add a project example or test result when this technique is evaluated.
