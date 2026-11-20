<!-- catalog
{
  "title": "Document automatic retry boundaries",
  "summary": "Tell automated readers which responses allow another attempt, which server signal controls the delay, and when retries should stop.",
  "tasks": [
    "first-result"
  ],
  "tags": [
    "troubleshooting"
  ],
  "aliases": [
    "retry policy"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "Transient failures are retried automatically and behavior depends on operation type."
}
-->

# Document automatic retry boundaries

**Use when.** Transient failures are retried automatically and behavior depends on operation type.

**Reader task.** First result and recovery.

**Practice.** Tell automated readers which responses allow another attempt, which server signal controls the delay, and when retries should stop. GitHub’s REST guidance distinguishes waiting according to response headers from persisting after repeated failures.

**Example (illustrative).** The client retries transient reads up to three times. Write operations require documented retry conditions.

**Result to check.** A test can distinguish requests the client retries from requests it returns immediately.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [GitHub REST retry guidance](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api#handle-rate-limit-errors-appropriately)
