<!-- catalog
{
  "title": "Document what happens with concurrent writers",
  "summary": "Say which shared state is protected, when writers wait or fail, and whether the behavior depends on the storage backend or deployment mode.",
  "tasks": [
    "first-result"
  ],
  "tags": [
    "troubleshooting"
  ],
  "aliases": [
    "simultaneous writes"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "Several processes can change the same state or use the same workspace."
}
-->

# Document what happens with concurrent writers

**Use when.** Several processes can change the same state or use the same workspace.

**Reader task.** First result and recovery.

**Practice.** Say which shared state is protected, when writers wait or fail, and whether the behavior depends on the storage backend or deployment mode. Terraform scopes locking to supported backends. SQLite distinguishes concurrent readers from writers in WAL mode.

**Example (illustrative).** A second process waits for the workspace lock. The backend table explains which storage supports locking.

**Result to check.** A two-writer test matches the documented wait, rejection, or serialization behavior.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Terraform state locking](https://developer.hashicorp.com/terraform/language/state/locking) · [SQLite WAL concurrency](https://sqlite.org/wal.html#concurrency)
