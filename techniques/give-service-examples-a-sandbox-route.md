<!-- catalog
{
  "title": "Give service examples a sandbox route",
  "summary": "Name the sandbox or mock used by the example and state what effects it simulates.",
  "tasks": [
    "quickstart"
  ],
  "tags": [
    "onboarding",
    "configuration"
  ],
  "aliases": [
    "api sandbox"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "The first service request should run without changing production state."
}
-->

# Give service examples a sandbox route

**Use when.** The first service request should run without changing production state.

**Reader task.** Quickstart and adoption.

**Practice.** Name the sandbox or mock used by the example and state what effects it simulates. Label the difference from live operation so readers know where the example can be run.

**Example (illustrative).** Run the request against a service-provided sandbox using its test account and endpoint.

**Result to check.** The example produces the documented result without touching production data.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Stripe testing environments](https://docs.stripe.com/testing-use-cases) · [Stripe Sandboxes](https://docs.stripe.com/sandboxes)
