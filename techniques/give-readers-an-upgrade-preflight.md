<!-- catalog
{
  "title": "Give readers an upgrade preflight",
  "summary": "Link a compatibility check readers can run before an upgrade changes their existing installation.",
  "tasks": [
    "quickstart"
  ],
  "tags": [
    "maintenance"
  ],
  "aliases": [
    "upgrade dry check"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "Compatibility can be checked before an upgrade changes state."
}
-->

# Give readers an upgrade preflight

**Use when.** Compatibility can be checked before an upgrade changes state.

**Reader task.** Quickstart and adoption.

**Practice.** Link a compatibility check readers can run before an upgrade changes their existing installation. Explain which findings block the upgrade and where to resolve them. PostgreSQL documents a check-only path for pg_upgrade.

**Example (illustrative).** Run the tool’s compatibility-only check and link the remedies for blocking findings.

**Result to check.** A supported fixture passes, and an incompatible fixture surfaces an actionable finding before changes.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [PostgreSQL upgrade compatibility check](https://www.postgresql.org/docs/current/pgupgrade.html)
