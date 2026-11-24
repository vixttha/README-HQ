# Foundation criterion reconciliation addendum

Status: **working acceptance register — NOT all 67 accepted**

The original crosswalk is preserved. This addendum attaches all 67 original plan criteria and records reviewed evidence and specific limitations. All original issue states remain open. No one-commit-per-checkpoint history was manufactured. The two replayed technical controls for #31 and #62 satisfy the tested original technical criteria, while #17 and #53 retain live scheduler/full MCP limits. The remaining criteria still require clause-by-clause verification or an explicit owner-approved alternate acceptance record.

Sources: [original plan](https://github.com/vixttha/README-HQ/blob/7f4562b8f44544bc9dd4b479fcd1bc30ca07ca94/plans/v0.0.6-repairs/README.md), [crosswalk](https://github.com/vixttha/README-HQ/blob/70d208a2539d77b1bfa5e0d596074cd609158851/evidence/integration-gates/foundation-crosswalk.md), [targeted run](https://github.com/vixttha/README-HQ/actions/runs/45396565680), [repeat run](https://github.com/vixttha/README-HQ/actions/runs/45397558792), [integration rehearsal and adoption](https://github.com/vixttha/README-HQ/actions/runs/45397558620). Frozen original candidate: `d12d5c6bd82fe448f64adb3ae48024296b8e6db4`. Rehearsal plus two-document correction: `95a54600184d7b95235fc401eb26797cf4ab5b57`.

## Per-checkpoint criteria and current evidence

### v0.0.6.1 — [#1](https://github.com/vixttha/README-HQ/issues/1) — Default homepage discovery

- Add a clear route from the default GitHub landing page to the active README HQ version, version index, and Graphify index.
- Open the default repo page or plain clone and follow every advertised link to its expected target.

Evidence pointer: draft root README; main unchanged.  
Status: publication or owner/scope dependency.  
Review: Root homepage and discovery routes staged; main unchanged. Publication not accepted.

### v0.0.6.2 — [#2](https://github.com/vixttha/README-HQ/issues/2) — Archived BART homepage links

- Restore navigable documentation links for the BART v0.0.3 and v0.0.4 homepage snapshots while preserving the frozen README bytes.
- Verify both indexed reading paths and all reported relative destinations. Compare archived README hashes with the audited copies.

Evidence pointer: `test_fragments_and_rendered_link_forms`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.3 — [#3](https://github.com/vixttha/README-HQ/issues/3) — Source provenance and tracked modes

- Verify the archive's source repository, commit, path, blob, and tracked mode against independently pinned evidence.
- Reject an unrelated or nonexistent source commit and a mode-only change. Verify valid imported snapshots still pass.

Evidence pointer: `test_registry_and_inventory_cannot_vouch_for_each_other`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.4 — [#4](https://github.com/vixttha/README-HQ/issues/4) — Frozen standalone version integrity

- Bind accepted standalone README and changelog bytes to source evidence used by archive validation and Graphify.
- Change a frozen changelog in a disposable checkout and confirm the candidate checks reject the drift. Verify the unchanged snapshot passes.

Evidence pointer: `test_version_rows_and_current_label_are_bound_to_archives`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.5 — [#5](https://github.com/vixttha/README-HQ/issues/5) — Version-to-map and homepage mapping

- Require each version row to link to its own map and make the homepage current version agree with the canonical index.
- Retarget the v0.0.6 row to the v0.0.5 map and the homepage to v0.0.1. Confirm both valid-but-wrong targets are rejected.

Evidence pointer: `test_version_rows_and_current_label_are_bound_to_archives`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Reviewed test_version_rows_and_current_label_are_bound_to_archives: wrong graph-index destination and rolled-back current label rejected; original version-row map retarget case still needs explicit clause-by-clause review.

### v0.0.6.6 — [#6](https://github.com/vixttha/README-HQ/issues/6) — GitHub Markdown navigation

- Check rendered Markdown link forms and GitHub heading anchors while ignoring inline code and other literal examples.
- Reject missing targets in titled, reference-style, and supported HTML links. Accept the Setext anchor and inline-code example.

Evidence pointer: `test_fragments_and_rendered_link_forms`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.7 — [#7](https://github.com/vixttha/README-HQ/issues/7) — Record-specific Graphify evidence

- Give each Graphify record the correct verification reference for its own artifact.
- Query the standalone and imported version nodes over MCP and verify they cite the validators that cover their respective artifacts.

Evidence pointer: MCP combined run.  
Status: combined Graphify evidence only; checkpoint-specific review pending.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.8 — [#8](https://github.com/vixttha/README-HQ/issues/8) — Technique registry field types

- Enforce the registry schema and explicit field types before normalizing IDs or aliases.
- Reject a Boolean schema and a string in place of the aliases array. Preserve the valid catalog and the public list command.

Evidence pointer: `test_wrong_registry_shapes_fail_without_a_traceback_and_write_a_receipt`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Reviewed malformed registry test: null/array/invalid item fail with receipt. Boolean schema and string aliases not separately demonstrated by this named test.

### v0.0.6.9 — [#9](https://github.com/vixttha/README-HQ/issues/9) — Failed batch recovery

- Publish a complete Graphify batch only after all maps and receipts pass, with a safe retry path.
- Force the second map build to fail. Confirm the destination remains safe and rerunning the same output succeeds when the fault is removed.

Evidence pointer: `test_partition_late_write_failure_leaves_destination_available_for_retry`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Reviewed partition write failure/retry test; it is a manifest staging test, not proof of second Graphify map-build failure. Need full build failure control.

### v0.0.6.10 — [#10](https://github.com/vixttha/README-HQ/issues/10) — Graphify table escaping

- Escape delimiters in catalog titles and summaries before rendering Markdown table cells.
- Generate a row with pipe characters and verify it renders as exactly three cells with the original readable text.

Evidence pointer: `test_rendered_tables_ignore_fenced_rows_and_reject_missing_navigation`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Reviewed Graphify table_cell pipe escape assertion; rendered catalog three-cell outcome not independently demonstrated in this pass.

### v0.0.6.11 — [#11](https://github.com/vixttha/README-HQ/issues/11) — Automatic repository mode and runner safety

- Classify the trusted hosting repository before any jobs are scheduled. Verify public, private, internal, unknown, and fork-PR metadata. Only verified public mode may schedule standard hosted validation. Use offline validation or an explicitly configured private environment for private/internal mode, and keep evidence private.

Evidence pointer: `test_public_reader_workflow_preserves_the_validator_exit`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.12 — [#12](https://github.com/vixttha/README-HQ/issues/12) — Portable adopter target and ref

- Run an explicit target/ref for a plain project and a monorepo without requiring HQ's history, registry, or version folders. Report the selected repo, entry point, Git tree, applicable checks, and verification gaps.

Evidence pointer: `test_repo_cli_requires_root_and_supports_explicit_subproject`, `test_pinned_readme_and_monorepo_routes`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.13 — [#13](https://github.com/vixttha/README-HQ/issues/13) — GitHub-visible README discovery

- Resolve the GitHub-visible README using .github, root, and docs precedence. Run link checks relative to the selected file. Cover competing files, a docs-only README, and a reportable missing README.

Evidence pointer: `test_root_fragments_follow_the_effective_homepage`, `test_adopter_detects_an_org_homepage_as_incomplete`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.14 — [#14](https://github.com/vixttha/README-HQ/issues/14) — Mechanical README quality gates

- Add a profile-aware quality check for empty and placeholder content, visible first action, justified prerequisites, and verifiable material claims. Detect GitHub display truncation and keep qualitative review as a separate result.

Evidence pointer: `test_quality_and_smoke_have_separate_outcomes`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.15 — [#15](https://github.com/vixttha/README-HQ/issues/15) — Repository-root-relative links

- Resolve leading-slash GitHub paths from the repository root and ordinary relative paths from the README location. Test both forms in nested folders and continue rejecting references outside the selected repository tree.

Evidence pointer: `test_pinned_readme_and_monorepo_routes`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.16 — [#16](https://github.com/vixttha/README-HQ/issues/16) — Published Git tree link verification

- Validate checkout-relative and recognized same-repository links against the exact tracked publication tree and ref. Exercise untracked paths, wrong-case paths, explicit refs, and existing links on both Linux and Windows. Report any ref that cannot be resolved.

Evidence pointer: `test_fetched_repository_refs_are_resolved_without_a_local_branch`, `test_partial_clone_blob_fetch_requires_explicit_permission`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.17 — [#17](https://github.com/vixttha/README-HQ/issues/17) — Default-branch publication coverage

- Validate the adopter's configured publication branch on supported push and PR events while preserving the pre-scheduling visibility gate. Test at least main, master, trunk, and a custom branch.

Evidence pointer: —.  
Status: new targeted controls passed; scope limitation remains.  
Review: Two public runner replays passed actual guard-source comparison plus 48 synthetic branch input cases and 8 nonpublic controls per platform. Live custom/fork scheduling not exercised.

### v0.0.6.18 — [#18](https://github.com/vixttha/README-HQ/issues/18) — Verified source and run binding

- Bind each finding to a source repository, full commit, path or artifact digest, and anchor. Use observed for a documented pattern. Require outcome, environment, and exact execution evidence before marking a behavioral claim verified.

Evidence pointer: `test_documented_review_receipt_passes_and_raw_or_incomplete_receipts_fail`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.19 — [#19](https://github.com/vixttha/README-HQ/issues/19) — Canonical evidence identity

- Normalize evidence identity to repository, commit, path, and evidence span while grouping same-file observations under the same source. Preserve relevant source lines and keep aliases or mirrors from inflating independent corroboration.

Evidence pointer: `test_json_duplicates_and_canonical_evidence`, `test_learning_records_verified_canonical_repository_identity`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Reviewed canonical evidence test: same-file normalization and duplicate JSON check; independent span/mirror inflation needs additional criterion proof.

### v0.0.6.20 — [#20](https://github.com/vixttha/README-HQ/issues/20) — Duplicate mechanism detection

- Detect exact repeated mechanisms with a canonical signature, flag semantic overlap for review, and retain one stable ID with aliases and corroborating evidence. Test against both active and retired techniques.

Evidence pointer: `test_learning_conflicting_decisions_at_same_source_are_rejected`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.21 — [#21](https://github.com/vixttha/README-HQ/issues/21) — Durable source-learning intake

- Create an idempotent learning intake for supplied source repositories and in-flight discoveries. Persist source revision, candidate identity, disposition, and provenance. Demonstrate that repeated intake records new evidence once and retains versioned history.

Evidence pointer: `test_learning_receipt_is_pinned_and_idempotent`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Reviewed pinned/idempotent receipt test: identical request and renamed source ID reuse one receipt; selection change yields distinct receipt. New source revision history needs separate explicit proof.

### v0.0.6.22 — [#22](https://github.com/vixttha/README-HQ/issues/22) — Project-specific recommendation receipts

- Bind recommendations to a target tree, owner-selected references, actual audience and capabilities, and the matching technique record. Record adopt, adapt, already present, declined, irrelevant, or insufficient evidence. Test that changing target facts or allowed sources changes the applicable recommendations.

Evidence pointer: `test_learning_distinguishes_unknown_retired_and_unselected_ids`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.23 — [#23](https://github.com/vixttha/README-HQ/issues/23) — Public and private learning separation

- Keep public shared learning and private project receipts isolated. Require independently resolved visibility and provenance before public admission. Verify using a synthetic private marker that public outputs and logs contain no private identifiers, links, or excerpts.

Evidence pointer: `test_public_learning_refusal_writes_nothing`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Reviewed private input refusal: output directory not created. Full log and synthetic private marker leakage control still needed.

### v0.0.6.24 — [#24](https://github.com/vixttha/README-HQ/issues/24) — Reuse and attribution boundary

- Record an owner decision on the HQ template's own reuse terms. For learning from an external example, cite the evidence and store an original abstraction. Require explicit license and attribution metadata before including copied material. Keep unresolved rights visible.

Evidence pointer: REUSE.md; no approved license.  
Status: publication or owner/scope dependency.  
Review: No approved standalone reuse license. Four BART snapshot roots have identical retained MIT license; six roots have no root license entry. Root absence not full rights clearance.

### v0.0.6.25 — [#25](https://github.com/vixttha/README-HQ/issues/25) — Exact Markdown evidence permalinks

- Generate immutable Markdown source links with the commit, file path, plain-file mode, and accurate line fragment. Verify at least one public source link opens with its exact line highlighted.

Evidence pointer: `test_graphify_evidence_line_links_use_source_mode_for_rendered_formats`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.26 — [#26](https://github.com/vixttha/README-HQ/issues/26) — Rendered Graphify source anchors

- Select source anchors from rendered source structure or explicit reviewed line anchors. Ignore fenced and indented code for heading and changelog detection. Report an ambiguous or absent anchor.

Evidence pointer: `test_exact_anchors_and_explicit_line`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.27 — [#27](https://github.com/vixttha/README-HQ/issues/27) — Behavioral first-use validation

- Support explicitly declared, authorized first-use smoke checks with exact revision, environment, invocation, and expected result. Fail on unsuccessful exit and on successful exit with the wrong outcome. Record unsupported, skipped, and unverified scenarios clearly.

Evidence pointer: `test_required_smoke_distinguishes_pass_failure_and_incomplete_coverage`, `test_required_smoke_needs_a_matching_documented_action`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.28 — [#28](https://github.com/vixttha/README-HQ/issues/28) — Media and accessible image links

- Verify local media against the published blob using supported format checks. Require a meaningful accessible name for image-only controls and links. Preserve decorative empty alt text where adjacent accessible content already describes the action.

Evidence pointer: `test_bad_image_and_unnamed_image_link_are_separate`, `test_mixed_markdown_html_image_link_names_keep_both_targets`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.29 — [#29](https://github.com/vixttha/README-HQ/issues/29) — Complete diagnostics

- Collect file and line diagnostics per URL, continue across independent validation cases, and return a failing result with each observed defect. Keep explicit reporting for sections the validator cannot inspect.

Evidence pointer: `test_broken_inline_links_reference_the_exact_occurrence_line`, `test_receipt_persistence_failure_preserves_audit_diagnostics`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.30 — [#30](https://github.com/vixttha/README-HQ/issues/30) — Target evidence binding

- Require a resolved target evidence receipt for applicable claims. Verify target facts against a pinned tree, report unresolved evidence, and abstain or mark the recommendation preliminary when the target match cannot be established. Link this pilot defect to the broader project-specific recommendation work in #22.

Evidence pointer: `test_adopter_receipt_distinguishes_scope_at_one_commit`, `test_learning_receipt_is_pinned_and_idempotent`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.31 — [#31](https://github.com/vixttha/README-HQ/issues/31) — Optimization-safe verification

- Use explicit conditional failures for provenance and pass/fail reporting, or fail clearly before verification in unsupported execution modes. Test identical malformed evidence under normal and optimized interpreter settings.

Evidence pointer: —.  
Status: technical criterion supported; historical acceptance remains open.  
Review: Technical criterion supported: on both platforms normal valid evidence succeeds; wrong hash, wrong anchor and zero line fail; optimized historical audit explicitly refuses before verification, which the original acceptance allows. Two exact-candidate public runner replays and downloaded ZIP digests verified. Historical checkpoint granularity not retrospectively accepted.

### v0.0.6.32 — [#32](https://github.com/vixttha/README-HQ/issues/32) — Durable acceptance receipts

- Generate an exact-SHA, machine-readable acceptance receipt with expected cases, outcomes, skips, source hashes, tool versions, and run references. Preserve accepted public receipts in a durable location and keep private evidence isolated.

Evidence pointer: `test_receipt_distinguishes_actions_attempts_jobs_and_standalone`, `test_receipt_identifies_executing_validator_separately_from_target_bytes`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.33 — [#33](https://github.com/vixttha/README-HQ/issues/33) — Graphify roadmap capacity

- Generalize Graphify plan partitioning for arbitrary checkpoint counts and verify that no checkpoint is dropped, duplicated, or disconnected across maps.

Evidence pointer: `test_partition_capacity_preserves_order`, `test_partition_writer_handles_more_than_three_partitions`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Reviewed 100-item partition/order and 100-item writer tests; live Graphify verified 67 nodes across three partitions. Combined evidence is strong for partition coverage, but not a distinct historical checkpoint receipt.

### v0.0.6.34 — [#34](https://github.com/vixttha/README-HQ/issues/34) — MCP evidence destinations

- Verify each outgoing edge against its expected target ID, relation, pinned path, and source range. Reject changed destinations even when totals match.

Evidence pointer: `test_mcp_inventory_rejects_a_count_preserving_wrong_edge`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Reviewed actual MCP count-preserving wrong-edge rejection; original full target/relation/path/range matrix needs separate confirmation.

### v0.0.6.35 — [#35](https://github.com/vixttha/README-HQ/issues/35) — Repository provenance

- Bind repository identity to independently established source provenance. Report local graph verification and remote provenance as distinct results and reject an unrelated repository label when provenance is claimed.

Evidence pointer: `test_unrelated_repository_or_branch_is_rejected`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.36 — [#36](https://github.com/vixttha/README-HQ/issues/36) — Git source file modes

- Inspect the pinned Git tree entry mode. Reject symlink evidence with a path diagnostic or resolve it inside the same pinned tree with explicit path and mode records.

Evidence pointer: `test_source_path_must_stay_inside_commit`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.37 — [#37](https://github.com/vixttha/README-HQ/issues/37) — Unambiguous JSON inputs

- Reject repeated JSON object keys at any depth before schema validation in registry, archive, version catalog, and Graphify manifest inputs. Include the input path and duplicate key in the diagnostic.

Evidence pointer: `test_json_duplicates_and_canonical_evidence`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Reviewed nested repeated-key rejection in parser; full registry/archive/catalog/manifest path-specific matrix remains to review.

### v0.0.6.38 — [#38](https://github.com/vixttha/README-HQ/issues/38) — Source line bounds

- Validate positive inline source line and line-range fragments against the target file, with tests for reversed and out-of-bounds ranges as well as valid last-line references.

Evidence pointer: `test_anchor_resolves_to_one_exact_line`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.39 — [#39](https://github.com/vixttha/README-HQ/issues/39) — Archive inventory completeness

- Validate the retained import inventory against an independent pinned listing and check archived README links against the imported tree. Fail on coordinated deletion of required files and manifest entries.

Evidence pointer: `test_registry_and_inventory_cannot_vouch_for_each_other`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.40 — [#40](https://github.com/vixttha/README-HQ/issues/40) — Version map coverage

- Require independently defined coverage for every advertised version. Reject empty or incomplete record sets and identify missing versions and record IDs before publishing verified artifacts.

Evidence pointer: `test_coverage_and_duplicate_manifest_keys`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.41 — [#41](https://github.com/vixttha/README-HQ/issues/41) — Exact Git line coordinates

- Use one explicit Git-compatible line model for locating evidence and generating source links. Test embedded Unicode separators and CRLF against pinned physical line numbers.

Evidence pointer: `test_review_followup_rendered_rows_normalize_line_endings`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.42 — [#42](https://github.com/vixttha/README-HQ/issues/42) — Binary media inventory

- Hash and inventory supported binary blobs without decoding them. Require text decoding only for line anchors, and report unsupported anchor types clearly.

Evidence pointer: `test_inventory_blob_cap_and_text_anchor_boundary`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.43 — [#43](https://github.com/vixttha/README-HQ/issues/43) — Graph and receipt publication

- Stage and validate the graph and receipt as a pair. Preserve the prior accepted pair on a publication failure and test recovery and repeat builds.

Evidence pointer: `test_atomic_pair_preserves_prior_graph_on_conflict`, `test_graphify_reader_and_writer_recover_an_interrupted_publication`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Reviewed publication conflict preservation test; full recovery and repeat build criterion still needs evidence review.

### v0.0.6.44 — [#44](https://github.com/vixttha/README-HQ/issues/44) — Bounded GitHub PR history

- Check for a capped commit listing. Resolve membership through a complete supported evidence route or report that membership could not be verified from the bounded response.

Evidence pointer: `test_historical_commit_requires_github_membership`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.45 — [#45](https://github.com/vixttha/README-HQ/issues/45) — External reader entry points

- Verify explicitly declared, authorized remote first-action URLs against an expected result when supported. Record unchecked, unresolved, gated, and broken routes distinctly in offline and online checks.

Evidence pointer: `test_http_smoke_checks_expected_error_bodies_and_preserves_auth_gates`, `test_http_smoke_records_and_can_require_the_effective_url`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.46 — [#46](https://github.com/vixttha/README-HQ/issues/46) — Learning source coordinates

- Require a positive in-range integer coordinate and a meaningful nonempty anchor before comparing the pinned contents. Cover zero, negative, empty, and valid first/last-line evidence.

Evidence pointer: `test_learning_structured_rate_limit_and_invalid_anchor_diagnostics`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.47 — [#47](https://github.com/vixttha/README-HQ/issues/47) — Technique retirement in recommendations

- Resolve existing recommendations against the canonical technique state and applicable registry revision. Exclude retired IDs from active recommendations and preserve prior decision history.

Evidence pointer: `test_learning_distinguishes_unknown_retired_and_unselected_ids`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Reviewed unknown/retired/unselected/active cases; canonical decision registry hash separately covered. Prior decision history criterion remains to review.

### v0.0.6.48 — [#48](https://github.com/vixttha/README-HQ/issues/48) — Complete MCP readback at supported limits

- Verify complete relationship readback for every supported manifest. Query by relation or page results, detect truncation explicitly, and test long valid paths at the documented limits.

Evidence pointer: MCP combined run.  
Status: combined Graphify evidence only; checkpoint-specific review pending.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.49 — [#49](https://github.com/vixttha/README-HQ/issues/49) — Git branch-name compatibility

- Validate source branch names with Git-compatible rules and compare the literal name to the API response. Exercise leading underscores, nested ref names, and invalid refs.

Evidence pointer: `test_batch5_review_publication_rule_pages_classic_branch_protection_and_branch_syntax`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.50 — [#50](https://github.com/vixttha/README-HQ/issues/50) — Checkpoint label and fixture ownership

- Bind the checkpoint label, planned change anchor, and reproduction fixture to the corresponding issue. Reject each independently when the manifest, graph, and receipt agree on unrelated evidence.

Evidence pointer: `test_plan_acceptance_checks_reject_missing_or_changed_obligations`, `test_plan_file_inventory_is_bound_to_approved_partition`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.51 — [#51](https://github.com/vixttha/README-HQ/issues/51) — Graphify plan index links

- Validate each repair-plan index link against the exact partition and artifact in the checked-out tree. Cover missing and existing-but-wrong graph, manifest, and receipt destinations.

Evidence pointer: `test_rendered_tables_ignore_fenced_rows_and_reject_missing_navigation`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.52 — [#52](https://github.com/vixttha/README-HQ/issues/52) — Clean checkout line-ending compatibility

- Preserve the bytes of Graphify inputs and generated files across supported checkout settings or compare authoritative Git blobs. Verify default and autocrlf checkouts with real input drift still failing.

Evidence pointer: `test_review_followup_rendered_rows_normalize_line_endings`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.53 — [#53](https://github.com/vixttha/README-HQ/issues/53) — Immutable Git object reads

- Ensure every pinned evidence read uses the original Git object regardless of local replacement refs. Verify the reported line coordinates and digest against that object in both the compiler and version-map builder.

Evidence pointer: —.  
Status: new targeted controls passed; scope limitation remains.  
Review: Two public runner replays used real replacement refs; Ubuntu compiler original digest and L1 anchor plus version-builder original bytes, Windows reader original bytes. Full MCP regeneration in presence of replacement refs not yet reproduced by this control.

### v0.0.6.54 — [#54](https://github.com/vixttha/README-HQ/issues/54) — Exact MCP relation fields

- Verify typed graph relationship fields or parse an unambiguous MCP representation. Accept valid paths with bracketed text while counting and checking only actual relationship fields.

Evidence pointer: `test_mcp_inventory_rejects_a_count_preserving_wrong_edge`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.55 — [#55](https://github.com/vixttha/README-HQ/issues/55) — Immutable learning-source commits

- Resolve each requested source revision to a full immutable commit before verifying and recording a source observation. Require receipt provenance to retain the resolved SHA and test that moving input refs cannot change a saved observation.

Evidence pointer: `test_learning_receipt_is_pinned_and_idempotent`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.56 — [#56](https://github.com/vixttha/README-HQ/issues/56) — Packaged Graphify self-map

- Provide and test a self-map for the actual vendored layout, or route the example explicitly to the working upstream tree. Verify the documented command from a clean checkout and check its graph over MCP.

Evidence pointer: MCP combined run.  
Status: combined Graphify evidence only; checkpoint-specific review pending.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.57 — [#57](https://github.com/vixttha/README-HQ/issues/57) — Version-index row uniqueness

- Require exactly one row per advertised version in the canonical version table. Reject duplicate labels even when their destinations and other columns are identical.

Evidence pointer: `test_version_rows_and_current_label_are_bound_to_archives`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.58 — [#58](https://github.com/vixttha/README-HQ/issues/58) — Merge-queue validation

- Support checks_requested for adopters that use a merge queue. Verify a queued synthetic merge candidate reports the README and Graphify statuses against the queue SHA under the intended runner policy.

Evidence pointer: workflow declares merge_group.  
Status: publication or owner/scope dependency.  
Review: Personal-owned repository; GitHub documented live queue feature unavailable. Workflow declares merge_group checks_requested; live queue adopter scope remains for owner acceptance.

### v0.0.6.59 — [#59](https://github.com/vixttha/README-HQ/issues/59) — Consistent PR head observation

- Bind the PR observation to coherent head metadata. Recheck the head across dependent evidence reads and retry or report an unstable observation when it changes. Keep historical member and current head results distinct.

Evidence pointer: `test_base_provenance_rejects_retargeting_with_the_same_head`, `test_merge_sha_is_distinct_from_source_sha`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Reviewed same-head base retargeting negative control; original changing-head race and historical membership distinction need explicit criterion review.

### v0.0.6.60 — [#60](https://github.com/vixttha/README-HQ/issues/60) — Technique list output encoding

- Make technique list output safe and explicit across supported stream encodings. Keep output and exit status consistent when rendering fails, and test redirected ASCII and UTF-8 output.

Evidence pointer: `test_ascii_technique_listing`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Reviewed redirected ASCII output success; UTF-8 plus rendering failure outcome still needs explicit criterion proof.

### v0.0.6.61 — [#61](https://github.com/vixttha/README-HQ/issues/61) — Technique lookup key collisions

- Reject cross-record exact collisions across the lookup fields promised by the technique guide, or define an explicit disambiguation rule and use it consistently for lookup. Test IDs, aliases, and outcome keys.

Evidence pointer: `test_json_duplicates_and_canonical_evidence`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.62 — [#62](https://github.com/vixttha/README-HQ/issues/62) — Exact review pagination boundary

- Use the review endpoint pagination metadata to distinguish complete results from an intentionally bounded observation. Test 999, 1,000, and more than 1,000 reviews and never represent a partial count as exact.

Evidence pointer: —.  
Status: technical criterion supported; historical acceptance remains open.  
Review: Technical criterion supported: 999, 1000, 1001 reviews return exact counts with 10,10,11 pages; explicit observation cap fails closed. Both platforms, two replays; downloaded artifact hashes verified. No historical checkpoint granularity claim.

### v0.0.6.63 — [#63](https://github.com/vixttha/README-HQ/issues/63) — GitHub README markup coverage

- Recognize headings in supported non-Markdown README formats or require a reviewed explicit anchor with a clear unsupported-format result. Test the three pinned README formats and compare the chosen anchor with the actual document heading.

Evidence pointer: `test_rich_text_navigation_reports_explicit_incomplete_status`, `test_adopter_detects_an_org_homepage_as_incomplete`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Reviewed RST and AsciiDoc fixture anchor recognition; original three pinned format documents still need exact source comparison.

### v0.0.6.64 — [#64](https://github.com/vixttha/README-HQ/issues/64) — Joined Unicode emoji in exact anchors

- Permit supported well-formed emoji joiner sequences in exact source anchors and preserve their original text and line coordinates. Test a joined emoji and a plain heading in the same pinned file.

Evidence pointer: `test_exact_anchors_and_explicit_line`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.65 — [#65](https://github.com/vixttha/README-HQ/issues/65) — Release-specific change anchoring

- Bind the changelog anchor to the requested release section or a reviewed explicit source line. Reject draft placeholders as release evidence and test a newer unreleased section above the requested release.

Evidence pointer: `test_release_heading_beats_a_draft_placeholder`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Reviewed release heading above unreleased draft placeholder; negative case with absent requested release still needs explicit proof.

### v0.0.6.66 — [#66](https://github.com/vixttha/README-HQ/issues/66) — Rendered fragment destinations

- Resolve a directory route to the GitHub-rendered README before checking its fragment. Validate supported Markdown extensions and distinguish a missing fragment from an unchecked target.

Evidence pointer: `test_root_fragments_follow_the_effective_homepage`, `test_fragments_and_rendered_link_forms`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.

### v0.0.6.67 — [#67](https://github.com/vixttha/README-HQ/issues/67) — Custom named anchor navigation

- Recognize documented custom anchor destinations alongside generated heading anchors, while retaining missing-target diagnostics. Verify the fixture against GitHub-rendered HTML and the offline checker.

Evidence pointer: `test_fragments_and_rendered_link_forms`.  
Status: related passing regression; full criterion not yet reviewed.  
Review: Related evidence retained; individual source/fixture/criterion review not completed in this pass.
