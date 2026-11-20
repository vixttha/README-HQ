<!-- catalog
{
  "title": "Show how to enable optional capabilities",
  "summary": "Identify what the base install enables and which feature flag or package extra enables each optional capability.",
  "tasks": [
    "quickstart"
  ],
  "tags": [
    "onboarding",
    "installation"
  ],
  "aliases": [
    "feature flags and extras"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "An example requires features or dependencies excluded from the base installation."
}
-->

# Show how to enable optional capabilities

**Use when.** An example requires features or dependencies excluded from the base installation.

**Reader task.** Quickstart and adoption.

**Practice.** Identify what the base install enables and which feature flag or package extra enables each optional capability. Put optional setup beside the example that requires it. Tokio documents the default and the features readers can select.

**Example (illustrative).** Show a small example with the optional image codec and the install flag that enables it.

**Result to check.** The default route works alone, and the feature route works with the documented extra.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Tokio feature flags](https://docs.rs/tokio/latest/tokio/#feature-flags) · [Python dependency extras](https://packaging.python.org/en/latest/specifications/dependency-specifiers/#extras) [npm’s optional dependency behavior](https://docs.npmjs.com/cli/v11/configuring-npm/package-json#optionaldependencies)
