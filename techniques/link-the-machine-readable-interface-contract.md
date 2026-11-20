<!-- catalog
{
  "title": "Link the machine-readable interface contract",
  "summary": "Point to the specification or schema for the interface addressed by the README and identify its version.",
  "tasks": [
    "handoff",
    "verification"
  ],
  "tags": [
    "interfaces"
  ],
  "aliases": [
    "openapi or schema link"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "A schema or contract is the authoritative definition for a versioned interface."
}
-->

# Link the machine-readable interface contract

**Use when.** A schema or contract is the authoritative definition for a versioned interface.

**Reader task.** Handoff and maintenance.

**Practice.** Point to the specification or schema for the interface addressed by the README and identify its version. Integrators can inspect operations and field requirements in the contract while following the short example in the README.

**Example (illustrative).** Link a versioned API contract and label which release implements it.

**Result to check.** A consumer can open a parseable definition whose version matches the described endpoint.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [OpenAPI interface description](https://spec.openapis.org/oas/v3.2.1.html) [Microsoft’s OpenAPI generation guide](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/openapi)
