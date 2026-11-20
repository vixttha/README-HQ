<!-- catalog
{
  "title": "Execute the documented walkthrough",
  "summary": "Replay the reader’s published steps at the named revision and verify the result.",
  "tasks": [
    "verification",
    "quickstart",
    "first-result"
  ],
  "tags": [
    "ci",
    "commands",
    "onboarding"
  ],
  "aliases": [
    "copy-and-run test",
    "walkthrough replay"
  ],
  "evidence": "verified",
  "status": "active"
}
-->

# Execute the documented walkthrough

**Problem.** A passing build or smoke test can exercise a different route from the one the README gives a reader.

**Practice.** Run the actual documented steps in a clean checkout. Record the README commit, target product revision, prerequisites, platform, invocation, and observed result. Check the actual output or artifact the reader expects.

**Example.** Veraphify’s public job explicitly ran the Quickstart and pinned two-version example using README commit `88d5d08` and product commit `91ccf6b`. The run log records both full SHAs, and the replay reported the expected version-specific citations.

**Limits.** The verification here covers that named job and tested preview path. Repeat the check when the instructions, tested revision, or supported environment changes.

**Result to check.** Rerun the published commands and compare the result with what the README promises. A missing or skipped run provides no execution result.

**Evidence.** Verified for the cited check. [Pinned Veraphify README](https://github.com/vixttha/Veraphify/blob/88d5d08cd8c80de3927858685878e51b6d7c69b8/README.md#quickstart) · [Passing README replay job](https://github.com/vixttha/Veraphify/actions/runs/44642589173/job/135977116342) · [Original README HQ registry](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/techniques/registry.json)
