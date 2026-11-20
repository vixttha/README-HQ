<!-- catalog
{
  "title": "Show the permissions automation needs",
  "summary": "Name the caller permissions the example needs and what each one allows.",
  "tasks": [
    "quickstart",
    "verification"
  ],
  "tags": [
    "onboarding",
    "prerequisites"
  ],
  "aliases": [
    "required automation permissions"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "A workflow fails with defaults or requires deliberate access to perform a step."
}
-->

# Show the permissions automation needs

**Use when.** A workflow fails with defaults or requires deliberate access to perform a step.

**Reader task.** Quickstart and adoption.

**Practice.** Name the caller permissions the example needs and what each one allows. For reusable workflows, state where those permissions must be granted.

**Example (illustrative).** List read access for checkout and write access for the reporting step in the workflow example.

**Result to check.** A least-privilege fixture can run the documented path with exactly those grants.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [actions/checkout recommended permissions](https://github.com/actions/checkout/blob/f548e57e544e1ff5a4c46bf1e1b8685f8e4a348a/README.md#L377-L384) · [GitHub nested workflow permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations#access-and-permissions-for-nested-workflows)
