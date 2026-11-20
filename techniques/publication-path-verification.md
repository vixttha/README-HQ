<!-- catalog
{
  "title": "Publication-path verification",
  "summary": "Test links and assets from the path where the README will actually ship.",
  "tasks": [
    "verification"
  ],
  "tags": [
    "verification",
    "publication"
  ],
  "aliases": [
    "published page verification"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "Content is served from a publication surface distinct from its source file."
}
-->

# Publication-path verification

**Use when.** Content is served from a publication surface distinct from its source file.

**Reader task.** Verification and trust.

**Practice.** Test links and assets from the path where the README will actually ship. The Python Packaging User Guide also runs this check against the built distribution.

**Example (illustrative).** After publishing, open the public release documentation route and follow its onboarding links.

**Result to check.** An unauthenticated reader can reach the published content and its target links at that revision.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [PyPI rendering check](https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/)
