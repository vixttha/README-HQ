<!-- catalog
{
  "title": "Turn examples into regression tests",
  "summary": "Generate test cases from examples in the maintained documentation source so changing an example also changes what gets tested.",
  "tasks": [
    "verification"
  ],
  "tags": [
    "verification"
  ],
  "aliases": [
    "tested documentation examples"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "An example can break when code, flags, or fixtures change."
}
-->

# Turn examples into regression tests

**Use when.** An example can break when code, flags, or fixtures change.

**Reader task.** Verification and trust.

**Practice.** Generate test cases from examples in the maintained documentation source so changing an example also changes what gets tested. jq’s docs README describes the process and its Makefile connects manual examples to the test suite.

**Example (illustrative).** Run the quickstart command against the fixture whenever examples or CLI behavior change.

**Result to check.** An intentional mismatch in the example makes the documentation test report the error.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [jq docs README](https://github.com/jqlang/jq/blob/5c001b18d7237cce1fdba63608732163f978dd23/docs/README.md#L1-L22) · [jq test-generation rule](https://github.com/jqlang/jq/blob/5c001b18d7237cce1fdba63608732163f978dd23/Makefile.am#L154-L170) [Python doctest documentation](https://docs.python.org/3/library/doctest.html)
