<!-- catalog
{
  "title": "Show how to verify the artifact’s producer",
  "summary": "Where a release provides a signed attestation, show how to verify it against the expected repository or workflow.",
  "tasks": [
    "verification"
  ],
  "tags": [
    "verification",
    "release-evidence"
  ],
  "aliases": [
    "signed build provenance"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "Readers need to check who built an artifact and where it was built."
}
-->

# Show how to verify the artifact’s producer

**Use when.** Readers need to check who built an artifact and where it was built.

**Reader task.** Verification and trust.

**Practice.** Where a release provides a signed attestation, show how to verify it against the expected repository or workflow. This lets readers check build origin as well as artifact identity.

**Example (illustrative).** Verify a release artifact against the expected repository and workflow identity.

**Result to check.** A valid artifact matches the expected producer and a mismatched identity fails verification.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [GitHub build provenance and verification](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations#verifying-artifact-attestations-with-the-github-cli)
