<!-- catalog
{
  "title": "Explain defaults that change what readers see",
  "summary": "Name the input the tool omits or transforms by default, what a reader may miss, and how to change the behavior.",
  "tasks": [
    "first-result"
  ],
  "tags": [
    "configuration"
  ],
  "aliases": [
    "hidden by default"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "Defaults filter, hide, or transform the output a reader expects to see."
}
-->

# Explain defaults that change what readers see

**Use when.** Defaults filter, hide, or transform the output a reader expects to see.

**Reader task.** First result and recovery.

**Practice.** Name the input the tool omits or transforms by default, what a reader may miss, and how to change the behavior. ripgrep puts its default exclusions near its opening description.

**Example (illustrative).** The default list shows only active projects. Select All to include archived entries.

**Result to check.** A fixture with both statuses displays the documented counts under both filters.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [ripgrep default search scope](https://github.com/BurntSushi/ripgrep/blob/16f9b2e64a42c43a469f72260226a6c65a4c88b9/README.md#L1-L9)
