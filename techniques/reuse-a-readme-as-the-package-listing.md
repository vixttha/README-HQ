<!-- catalog
{
  "title": "Reuse a README as the package listing",
  "summary": "Wire the maintained README into package metadata so package users see the same introduction in their registry.",
  "tasks": [
    "handoff"
  ],
  "tags": [
    "publication"
  ],
  "aliases": [
    "package registry readme"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "The same README is consumed by a package or registry landing page."
}
-->

# Reuse a README as the package listing

**Use when.** The same README is consumed by a package or registry landing page.

**Reader task.** Handoff and maintenance.

**Practice.** Wire the maintained README into package metadata so package users see the same introduction in their registry. Check the description from the built package and resolve links in the target renderer.

**Example (illustrative).** Use the project README as the package description and check its links in the package preview.

**Result to check.** The packaged preview renders the intended README and the linked resources resolve.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [PyPI packaging guide](https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/) · [Cargo manifest README field](https://doc.rust-lang.org/cargo/reference/manifest.html#the-readme-field)
