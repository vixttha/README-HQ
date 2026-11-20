<!-- catalog
{
  "title": "Show a restore check against a separate destination",
  "summary": "Pair a backup path with a small restore exercise into a separate destination and show what to inspect in the restored copy.",
  "tasks": [
    "first-result",
    "verification"
  ],
  "tags": [
    "stored-state"
  ],
  "aliases": [
    "backup restore test"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "The project stores important state and has a documented backup path."
}
-->

# Show a restore check against a separate destination

**Use when.** The project stores important state and has a documented backup path.

**Reader task.** First result and recovery.

**Practice.** Pair a backup path with a small restore exercise into a separate destination and show what to inspect in the restored copy. The restic restore guide explains selecting the snapshot and destination.

**Example (illustrative).** Restore a named snapshot into a temporary directory and inspect two expected files.

**Result to check.** The restored data matches the checks while the live location stays unchanged.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [restic restore guide](https://restic.readthedocs.io/en/stable/050_restore.html) · [Borg restore quickstart](https://borgbackup.readthedocs.io/en/master/quickstart.html)
