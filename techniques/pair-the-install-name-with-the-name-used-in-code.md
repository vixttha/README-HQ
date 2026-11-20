<!-- catalog
{
  "title": "Pair the install name with the name used in code",
  "summary": "When distribution, import, or executable names differ, show the exact names together so readers can connect the installation step to the first use.",
  "tasks": [
    "quickstart"
  ],
  "tags": [
    "onboarding",
    "installation"
  ],
  "aliases": [
    "package and import names"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "The package manager name differs from the executable or import identifier."
}
-->

# Pair the install name with the name used in code

**Use when.** The package manager name differs from the executable or import identifier.

**Reader task.** Quickstart and adoption.

**Practice.** When distribution, import, or executable names differ, show the exact names together so readers can connect the installation step to the first use. The Python Packaging User Guide illustrates this with the Pillow distribution and its PIL import.

**Example (illustrative).** Put the package manager’s distribution name beside the import or executable name.

**Result to check.** A new reader can install the package, then import or execute the correct identifier.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Python packaging names](https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/)
