# Veraphify two-version lookup trial

The first pilot for [reusable README technique combinations](../features/records/FEAT-000012.json) asked whether a reader could start at the preview homepage, compare two versions of a feature, and trace the result to its evidence.

| Surface | Pinned revision |
| --- | --- |
| README HQ trial and technique registry | [`8d50caec2bc6fcb998994a1fd302294a029325f9`](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/techniques/registry.json) |
| Veraphify adopter workspace | [`1065e52c7924628c3402b63265124391b5f3c46e`](https://github.com/vixttha/Veraphify/tree/1065e52c7924628c3402b63265124391b5f3c46e) |
| Veraphify draft homepage | [`c0a03f7e40b115c51fbc4be2a45f50ce1dee46f7`](https://github.com/vixttha/Veraphify/tree/c0a03f7e40b115c51fbc4be2a45f50ce1dee46f7) · [Draft PR #55](https://github.com/vixttha/Veraphify/pull/55) |
| Veraphify executable preview and walkthrough | [`91ccf6bdc4ac4645006151d68605c2b77239d651`](https://github.com/vixttha/Veraphify/blob/91ccf6bdc4ac4645006151d68605c2b77239d651/docs/adopter-walkthrough.md) |

## Techniques exercised

1. **Find the task.** Use `role-based-entry-points` to give the two-version walkthrough a prominent link on the homepage.
2. **Recognize success.** Use `first-success-milestone` and `exact-revision-walkthrough` to show both expected citations and execute the documented walkthrough at the pinned preview.
3. **Trace the evidence.** Use `claim-scope-labels` and `declared-versus-observed-evidence` to distinguish the Ubuntu build-and-lookup walkthrough from independent replay coverage. The verification guide uses a relative link within the docs checkout. The walkthrough uses a commit permalink for the separately pinned product checkout.

This trial covers a runnable preview with fixtures and public evidence. A repository with no runnable preview can document its first feasible reader action and leave execution unverified. Save persistence and archive merge review require their own checks when relevant.

## Results

| Check | Result | Evidence |
| --- | --- | --- |
| Homepage discovery | **Passed at the draft revision.** Both task and evidence links appeared in GitHub's rendered README. The two-version walkthrough at the product revision and the verification guide at the docs revision both loaded. | [Rendered draft](https://github.com/vixttha/Veraphify/tree/c0a03f7e40b115c51fbc4be2a45f50ce1dee46f7) · [Verification guide](https://github.com/vixttha/Veraphify/blob/c0a03f7e40b115c51fbc4be2a45f50ce1dee46f7/docs/verification.md) |
| Run the documented action | **Passed at the pinned product revision.** The published Ubuntu job extracted the Bash block from the linked walkthrough and ran it. Its assertions checked two distinct source commits, both expected citations, and preservation of the earlier archive. | [Exact push run, attempt 1](https://github.com/vixttha/Veraphify/actions/runs/44640005952/attempts/1) · [Walkthrough job](https://github.com/vixttha/Veraphify/actions/runs/44640005952/job/135968332305) |
| Recover the task from the adopter branch | **Partial.** A clean checkout starting at the adopter README recovered the pinned README HQ revision, learning log, and two-version task. The linked plan cites the earlier `35c463c` product walkthrough. The entry point, plan, and learning log had no pointer to draft PR #55, so the tested draft and its product revision required separate GitHub lookup. An independent agent-session trial is pending. | [Adopter README](https://github.com/vixttha/Veraphify/blob/1065e52c7924628c3402b63265124391b5f3c46e/README.md) · [Adopter plan](https://github.com/vixttha/Veraphify/blob/1065e52c7924628c3402b63265124391b5f3c46e/VERAPHIFY-MAIN-PLAN.md) |

### Retained result

The documented job reported these fixture results. Each fixture SHA identifies source generated during that run.

```text
v1.0.0 verified at c1440bf1ce3e3c8c81c40761d8fcb8056a15a8b0, citation src/feature.py:3
v1.1.0 verified at 843a8223a89f4893bceea4b51e21052161f5ff60, citation src/feature.py:4
```

The run also had independent Ubuntu and Windows archive-replay jobs. The producer's handoff was artifact ID `14585449238`, with ZIP SHA-256 `cd0cc04a7937dd168919beab05556b64a522e2188e3c285cfe5724abf28ab0a1`, as reported by GitHub. [Run and jobs](https://github.com/vixttha/Veraphify/actions/runs/44640005952/attempts/1) · [Artifact](https://github.com/vixttha/Veraphify/actions/runs/44640005952/artifacts/14585449238)

The remaining handoff check is whether someone starting from the adopter README can reach the current homepage candidate, its distinct product pin, and this evidence without an additional PR search.
