<!-- catalog
{
  "title": "Generate repetitive README sections from their source",
  "summary": "Generate sections such as configuration inputs or outputs from their authoritative definitions.",
  "tasks": [
    "handoff"
  ],
  "tags": [
    "publication"
  ],
  "aliases": [
    "readme generation from source"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "A README table, list, or example repeats facts maintained elsewhere."
}
-->

# Generate repetitive README sections from their source

**Use when.** A README table, list, or example repeats facts maintained elsewhere.

**Reader task.** Handoff and maintenance.

**Practice.** Generate sections such as configuration inputs or outputs from their authoritative definitions. Bound generation with file markers so authored explanations stay editable. terraform-docs documents an injected section between comments.

**Example (illustrative).** Generate the options table from the CLI help and show the command that updates the section.

**Result to check.** Changing the source updates the generated section and the freshness check detects drift.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [terraform-docs output injection](https://terraform-docs.io/user-guide/configuration/output/#inject)
