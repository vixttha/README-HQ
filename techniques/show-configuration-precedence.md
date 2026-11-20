<!-- catalog
{
  "title": "Show configuration precedence",
  "summary": "Explain which setting wins when flags, environment variables, configuration files, and defaults disagree.",
  "tasks": [
    "quickstart"
  ],
  "tags": [
    "onboarding",
    "configuration"
  ],
  "aliases": [
    "settings override order"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "The same setting can be supplied in multiple places."
}
-->

# Show configuration precedence

**Use when.** The same setting can be supplied in multiple places.

**Reader task.** Quickstart and adoption.

**Practice.** Explain which setting wins when flags, environment variables, configuration files, and defaults disagree. Give one concrete conflict example in the supporting reference. Terraform documents the order for root module input variables.

**Example (illustrative).** Command-line options override environment variables, which override the local config file.

**Result to check.** Set one option at three levels and check that the observed precedence matches the README.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Terraform variable precedence](https://developer.hashicorp.com/terraform/language/values/variables#variable-definition-precedence)
