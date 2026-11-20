<!-- catalog
{
  "title": "Give a readiness check before the first request",
  "summary": "After the startup command, show what indicates the dependency can accept traffic and how the reader can check it.",
  "tasks": [
    "first-result"
  ],
  "tags": [
    "success-checks"
  ],
  "aliases": [
    "service health check"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "Process startup can finish before the service can accept work."
}
-->

# Give a readiness check before the first request

**Use when.** Process startup can finish before the service can accept work.

**Reader task.** First result and recovery.

**Practice.** After the startup command, show what indicates the dependency can accept traffic and how the reader can check it. A service may be running before its dependencies are ready.

**Example (illustrative).** Wait for the readiness endpoint to report ready before sending the example request.

**Result to check.** The check distinguishes slow startup from a service ready to handle the request.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Docker Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/) · [Kubernetes readiness probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/)
