<!-- catalog
{
  "title": "Give each public package its own README entry point",
  "summary": "Put a short orientation in the package directory so someone entering through a deep link can find its purpose, setup, and supporting docs.",
  "tasks": [
    "navigation",
    "quickstart"
  ],
  "tags": [
    "navigation"
  ],
  "aliases": [
    "monorepo package readmes"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "A repository contains multiple independently used packages."
}
-->

# Give each public package its own README entry point

**Use when.** A repository contains multiple independently used packages.

**Reader task.** Navigation and accessibility.

**Practice.** Put a short orientation in the package directory so someone entering through a deep link can find its purpose, setup, and supporting docs. Google’s README guide calls this out for package directories.

**Example (illustrative).** The root points to the CLI and SDK directories, each with its own installation and first result.

**Result to check.** A reader can reach and follow the correct instructions for either package.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Google’s package README guidance](https://github.com/google/styleguide/blob/8bdadbb0732b387aaa26f553dd9033484d1a2071/docguide/READMEs.md#L30-L55)
