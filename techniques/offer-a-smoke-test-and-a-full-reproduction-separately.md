<!-- catalog
{
  "title": "Offer a smoke test and a full reproduction separately",
  "summary": "Use a small run to establish that setup works and a separate run to reproduce the full result.",
  "tasks": [
    "verification"
  ],
  "tags": [
    "verification",
    "reproduction"
  ],
  "aliases": [
    "small demo and full reproduction"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "The complete reproduction is too costly for a first setup check."
}
-->

# Offer a smoke test and a full reproduction separately

**Use when.** The complete reproduction is too costly for a first setup check.

**Reader task.** Verification and trust.

**Practice.** Use a small run to establish that setup works and a separate run to reproduce the full result. State the inputs, expected outputs, and resource needs for each.

**Example (illustrative).** Use a two-row fixture for setup and a separate command for the full study.

**Result to check.** Each route has independent prerequisites, runtime expectations, and a visible success check.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [SPIN artifact README guidance](https://spin-web.github.io/SPIN2026/artifacts) · [DistServe’s two evaluation paths](https://github.com/LLMServe/DistServe/blob/82831f1604cc6b10bebd360f6c437a07790dde9f/evaluation/docs/README-AE.md#L3-L8)
