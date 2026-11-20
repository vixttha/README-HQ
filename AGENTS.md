# README HQ agent entry point

For the current repair trial, resolve `repair/v0.0.6-batch-1` in `vixttha/README-HQ` to an exact commit before using the adopter CLI and learning intake. Use `readme-hq` to look up published versions and history. Resolve the target repository's ref independently. Read the target's applicable instructions, version metadata, and repository rules at the selected ref.

| Request | Work |
| --- | --- |
| Show the versions | Read [the version index](versions/README.md). Return the requested project's HQ and homepage versions with status and pinned links. |
| Inspect a repository | Follow [the audit workflow](audits/README.md). Give ranked findings with source and validation status, then update the technique catalog when the review uncovers a genuinely new reusable practice. |
| Draft or update a README | Use [the README guide](README-GUIDE.md). Draft on a working branch and verify changes against the target's entry points. |
| Archive or publish a README | Use the guide's version workflow and the target repository's acceptance rules. Return the approved archive and homepage publication evidence independently. |

For each audit, read [the technique catalog](techniques/registry.json) before recording discoveries. Compare the problem, intervention, and outcome with active and retired records. Add evidence and aliases to an existing record when the mechanism matches. Use new IDs for distinct techniques, and cite source commits in the catalog. Keep repo-specific recommendations in the audit.

Use the public branch for public-safe evidence and general techniques. Keep private repository identities, original files, and private evidence with the owner. Verify changes with `python3 tools/check_readme_hq.py` and report what was actually tested. The owner decides homepage publication and releases.
