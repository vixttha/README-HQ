<!-- catalog
{
  "title": "Verify which README appears on the repository homepage",
  "summary": "When multiple eligible README files exist, check which one the host surfaces and publish the expected content there.",
  "tasks": [
    "verification"
  ],
  "tags": [
    "verification",
    "publication"
  ],
  "aliases": [
    "github readme selection"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "More than one tracked README or ref could become the GitHub homepage."
}
-->

# Verify which README appears on the repository homepage

**Use when.** More than one tracked README or ref could become the GitHub homepage.

**Reader task.** Verification and trust.

**Practice.** When multiple eligible README files exist, check which one the host surfaces and publish the expected content there. GitHub checks `.github/`, the repository root, and `docs/` in that order.

**Example (illustrative).** Check the repository homepage and identify which README location and branch GitHub rendered.

**Result to check.** The rendered introduction matches the intended file and default revision.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [GitHub README display order](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
