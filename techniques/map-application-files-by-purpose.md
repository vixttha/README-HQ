<!-- catalog
{
  "title": "Map application files by purpose",
  "summary": "List the locations for user data, configuration, runtime state, and cache on supported platforms.",
  "tasks": [
    "first-result"
  ],
  "tags": [
    "stored-state"
  ],
  "aliases": [
    "config and cache locations"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "Files have different persistence, cleanup, or migration needs."
}
-->

# Map application files by purpose

**Use when.** Files have different persistence, cleanup, or migration needs.

**Reader task.** First result and recovery.

**Practice.** List the locations for user data, configuration, runtime state, and cache on supported platforms. Identify overrides and distinguish files a reader needs to preserve from data the application can rebuild.

**Example (illustrative).** List settings, database, and cache in separate rows with their paths and overrides.

**Result to check.** A user can find each file and identify which ones they need to preserve.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Syncthing configuration and database locations](https://docs.syncthing.net/users/config.html) · [XDG data and cache conventions](https://specifications.freedesktop.org/basedir/)
