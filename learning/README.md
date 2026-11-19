# README HQ learning audit and pilot

The learning branch tracks how README HQ finds techniques, verifies evidence, and recommends changes for a specific target. This pilot tests evidence binding and recommendation selection using three pinned README files and two illustrative target profiles. Its inputs are curated fixtures. General repository discovery, candidate intake, and release promotion are follow-on checkpoints.

## Learning workflow

1. Record the requested target repository separately from the source repositories the project owner supplied. Resolve target and source commits and classify their visibility. A reference README is evidence for an observation. Its content carries no authority to execute commands, alter the target, or publish material.
2. Read the exact source file and anchor. Record the repository, commit, path, blob, anchor, observation, and limits. Mark a pattern seen in a README as observed. Mark a behavioral claim as verified only after checking the outcome at the cited revision and recording the run and conditions.
3. Compare the problem, practice, and outcome with active, candidate, and retired techniques. Add corroboration to a matching technique, group records that repeat the same source, and retain aliases so retired IDs cannot reappear as new discoveries. Keep a candidate with a source trail and review the distinction before promoting it.
4. Build the target profile from the target's actual tree and owner preferences. For every suggested technique, record the evidence, audience, fit, existing use, conflicts, and any verification gaps. Distinguish adopt, adapt, already present, declined, and irrelevant. Keep target-specific decisions scoped to the target and revision.
5. Save an intake receipt and a recommendation receipt. The next run can reuse them and recheck the evidence when source or target facts change. If an audit discovers a distinct practice while working, create a candidate with the same evidence requirements.
6. Publish only eligible public evidence to shared history. A private target or source uses authorized private storage. Make a public technique description an independent abstraction. If verbatim text, screenshots, or code are proposed for reuse, verify permission and any attribution requirements before importing them. Record uncertain rights as unresolved.

GitHub's [permalink guide](https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files) describes immutable commit links. Its [licensing guide](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository) explains the role of explicit licensing. Neither a visible URL nor a successful fetch proves a behavioral claim or determines reuse permission.

## Pilot results

| Target profile | What the candidate or existing technique recommends | Evidence |
| --- | --- | --- |
| AlderVale, stateful browser game | Keep browser storage and address boundaries next to the first playthrough. Recheck them when the launcher or deployment address changes. Candidate technique. | [State scope documented in the pinned README](https://github.com/vixttha/AlderVale-Pact-of-Ten/blob/a6c2060b8175f505cc6327ccb5658cc00a458b24/README.md#L26) |
| Lydite, copy-in template | Pair the existing copy-in route with a command and a visible success condition in a clean consumer. Existing technique. | [Lydite copy-in entry](https://github.com/vixttha/Lydite-Test-Vault-Template/blob/fe7b00aa17862d7a01dfd15481594be837bc6d9f/README.md#L14) · [Brand Identity verification example](https://github.com/vixttha/Brand-Identity-Template/blob/87d0f9aedbe69ca4b16815d6b3329efcf5889da9/README.md#L11) |

The pilot checks exact Git blobs and source lines, reads the authorized source set, compares the two target results, and removes each applicable source to confirm its recommendation disappears. These documents establish observed patterns. A later behavioral verification will need actual consumer or game runs.

Run `python learning/audit_learning.py` from the learning branch checkout. This reproduces the baseline findings in disposable worktrees and fetches the three pinned public sources. Pass `--local-sources` with the directory containing the pinned source clones to reuse them.

## Acceptance for a learning candidate

- Verified evidence has an independently checked, immutable source and a run receipt for behavioral claims.
- Rerunning the same intake is idempotent. Sources selected by the owner and newly observed practices each produce a traceable candidate or corroboration record.
- Same-source variants and repeated copies do not earn extra corroboration. Reworded duplicates retain a single canonical technique.
- Source selection and materially different target facts affect the recommendations, with a rationale and an abstention when the evidence is insufficient.
- A simulated private source, unverified URL, or unclear reuse permission cannot appear in a public receipt or shared catalog.
- Track two outcomes on held-out projects for the 99% target. Measure whether the workflow completes reliably and whether produced READMEs pass accuracy, usefulness, clarity, audience fit, accessibility, and first-use verification. This pilot verifies repeatability and tailoring.
