<!-- catalog
{
  "title": "Show the order for upgrading multiple components",
  "summary": "When components evolve independently, show the upgrade sequence and which version combinations can coexist during the transition.",
  "tasks": [
    "quickstart"
  ],
  "tags": [
    "maintenance"
  ],
  "aliases": [
    "component upgrade order"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "An upgrade crosses independently versioned services, nodes, or clients."
}
-->

# Show the order for upgrading multiple components

**Use when.** An upgrade crosses independently versioned services, nodes, or clients.

**Reader task.** Quickstart and adoption.

**Practice.** When components evolve independently, show the upgrade sequence and which version combinations can coexist during the transition. Kubernetes documents both the skew limits and the supported component order.

**Example (illustrative).** Upgrade the controller first, then workers in batches within the documented version-skew window.

**Result to check.** Every intermediate state uses a supported version combination.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Kubernetes version skew and upgrade order](https://kubernetes.io/releases/version-skew-policy/)
