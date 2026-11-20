<!-- catalog
{
  "title": "Explain what uninstall removes and retains",
  "summary": "State which commands or files uninstall removes and what happens to data, configuration, caches, or installed components.",
  "tasks": [
    "quickstart",
    "handoff"
  ],
  "tags": [
    "maintenance"
  ],
  "aliases": [
    "uninstall data retention"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "Uninstall removes a program and has separate effects on user data or settings."
}
-->

# Explain what uninstall removes and retains

**Use when.** Uninstall removes a program and has separate effects on user data or settings.

**Reader task.** Quickstart and adoption.

**Practice.** State which commands or files uninstall removes and what happens to data, configuration, caches, or installed components. Point to the data-preservation path when it matters. Docker Desktop distinguishes uninstall effects from backup and restore.

**Example (illustrative).** List removed binaries separately from retained user settings and link the backup procedure.

**Result to check.** A test uninstall leaves or removes each listed item as documented.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Docker Desktop uninstall effects](https://docs.docker.com/desktop/uninstall/) · [Docker Desktop backup and restore](https://docs.docker.com/desktop/settings-and-maintenance/backup-and-restore/)
