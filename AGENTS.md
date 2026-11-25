# README HQ agent entry point

For the current repair trial, use `repair/v0.0.6-integration-candidate` in `vixttha/README-HQ` (combined v0.0.6 repair draft, not a published release). Resolve the branch to a full commit and confirm it against reviewed evidence before using the adopter CLI and learning intake. Use `readme-hq` to look up published versions and history. Resolve the target repository's ref independently. Read the target's applicable instructions, version metadata, and repository rules at the selected ref.

| Request | Work |
| --- | --- |
| Show the versions | Read [the version index](versions/README.md). Return the requested project's HQ and homepage versions with status and pinned links. |
| Inspect a repository | Follow [the audit workflow](audits/README.md). Give ranked findings with source and validation status, then record a reusable discovery with source evidence; external catalog changes require separate review. |
| Draft or update a README | Use [the README guide](README-GUIDE.md). Draft on a working branch and verify changes against the target's entry points. |
| Archive or publish a README | Use the guide's version workflow and the target repository's acceptance rules. Return the approved archive and homepage publication evidence independently. |

For each audit, read [README Technique Library](https://github.com/vixttha/README-HQ/tree/README-Technique-Library) at a pinned commit before recording discoveries. Record the chosen technique or combination, applicability and catalog SHA. Compare the problem, intervention, and outcome with active and retired records. Add evidence and aliases to an existing record when the mechanism matches. Use new IDs for distinct techniques, and cite source commits in the catalog. Keep repo-specific recommendations in the audit.

Use the public branch for public-safe evidence and general techniques. Keep private repository identities, original files, and private evidence with the owner. Verify changes with `python3 tools/check_readme_hq.py` and report what was actually tested. The owner decides homepage publication and releases.

## Owner-approved engineering ecosystem laws

Decision ENGINEERING-ECOSYSTEM-LAWS-001 (2026-11-24). Mission: Build a toolkit that gives compatible LLM agents a structured engineering environment, rather than building another AI model.

<!-- engineering-laws:start -->
1. **Independence:** Every tool must remain independently installable, usable, versioned and maintained.
2. **Composability:** Installing additional tools expands the agent's capabilities without creating mandatory dependencies.
3. **Portability:** No mandatory AI provider, model, agent harness or paid execution service.
4. **Persistence:** Project knowledge, decisions, progress and evidence survive the termination of an AI session.
5. **Verification:** Development claims must be supported by reproducible, revision-bound evidence.
6. **Owner authority:** The human retains control over scope, architectural decisions, integration and releases.
<!-- engineering-laws:end -->

Remain standalone. Other tools are optional; their absence must not block normal operation. Preserve project-local authority and evidence; never automatically install, merge, synchronize or write to another tool's branch. No mandatory seventh coordinator, paid service or AI provider. Existing product scope remains authoritative. Change these laws only by explicit owner approval.

## Agent capability discovery — v1

<!-- agent-capability:v1
{"schema_version":1,"id":"readme-hq","branch":"readme-hq","entrypoint":"AGENTS.md","scope":"Documentation authoring and version history","required_ecosystem_tools":[],"authority":"owner","discovery":"read-only","versioning":"independent"}
-->

A compatible agent may enumerate the target repository's branch refs, resolve this branch to a commit, and read its entry point at that exact commit. Read-only discovery confers no execution, write, integration or release authority. If this branch or marker is absent, the tool is absent or legacy/unverified; continue independently. Check the target's own instructions and owner scope before any action. The marker describes a capability, not a required registry or package version.

Installation convention: human or agent selects a reviewed exact source SHA, checks the dedicated target branch and collisions, follows [this product's own installation guide](README.md#use-readme-hq), and records source/target SHA and preserved product state. Never merge a template workspace wholesale into product source. Existing installations require explicit reviewed upgrades; preserve local records and prior receipts. Optional evidence links do not authorize writes. No mandatory coordinator or other ecosystem tool.
