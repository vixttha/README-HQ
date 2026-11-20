<!-- catalog
{
  "title": "Show how to prepare an offline install",
  "summary": "Separate gathering dependencies on a connected machine from installing the staged set on the offline target.",
  "tasks": [
    "quickstart"
  ],
  "tags": [
    "onboarding",
    "environment"
  ],
  "aliases": [
    "offline dependency bundle"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "Installation targets cannot access the package registry during setup."
}
-->

# Show how to prepare an offline install

**Use when.** Installation targets cannot access the package registry during setup.

**Reader task.** Quickstart and adoption.

**Practice.** Separate gathering dependencies on a connected machine from installing the staged set on the offline target. State which platform and runtime the bundle must match. pip documents both stages.

**Example (illustrative).** Stage wheels for the target Python version, then install from the bundle on the offline machine.

**Result to check.** A clean disconnected target installs and passes the first-use check.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [pip download](https://pip.pypa.io/en/stable/cli/pip_download/) · [Installing from local packages](https://pip.pypa.io/en/stable/user_guide/#installing-from-local-packages)
