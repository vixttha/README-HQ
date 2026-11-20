<!-- catalog
{
  "title": "State what event consumers can assume about delivery",
  "summary": "Say whether event delivery can repeat or arrive out of order and where to find the identifier needed to recognize a repeat.",
  "tasks": [
    "handoff"
  ],
  "tags": [
    "interfaces"
  ],
  "aliases": [
    "event delivery guarantees"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "A subscriber needs to handle duplicates, ordering changes, or retries."
}
-->

# State what event consumers can assume about delivery

**Use when.** A subscriber needs to handle duplicates, ordering changes, or retries.

**Reader task.** Handoff and maintenance.

**Practice.** Say whether event delivery can repeat or arrive out of order and where to find the identifier needed to recognize a repeat. Stripe’s webhook guidance documents both cases.

**Example (illustrative).** State that events may arrive more than once and name the identifier used to detect duplicates.

**Result to check.** A consumer can process the sample duplicate events according to the documented contract.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Stripe webhook event order and duplicates](https://docs.stripe.com/webhooks#event-ordering)
