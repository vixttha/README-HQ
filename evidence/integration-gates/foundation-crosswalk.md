# Foundation acceptance evidence crosswalk

Status: **WORKING EVIDENCE INDEX — NOT ACCEPTANCE OR RELEASE AUTHORIZATION**

Reviewed 2026-11-24. Exact qualified repair head: [d12d5c6bd82fe448f64adb3ae48024296b8e6db4](https://github.com/vixttha/README-HQ/commit/d12d5c6bd82fe448f64adb3ae48024296b8e6db4). Source: [original 67-checkpoint plan](https://github.com/vixttha/README-HQ/blob/7f4562b8f44544bc9dd4b479fcd1bc30ca07ca94/plans/v0.0.6-repairs/README.md). All 67 original issues remain open (GitHub open-issue query). The shared foundation implementation in draft #68 is preserved unchanged.

This is a first-pass mapping from plan topics to named related tests observed in the existing exact-candidate public runner logs, not a proof that the original failure was reproduced or that all acceptance clauses passed. Reader references were observed in both Ubuntu and Windows proposed-merge logs; graph references were observed in the Graphify log. Every mapped test name requires source/fixture review against the original issue criteria before acceptance. Combined graph coverage does not establish checkpoint acceptance. Do not backdate or fabricate per-checkpoint commits. Where historical commit granularity cannot be met without rewriting, obtain an explicit owner decision on alternate evidence.

Evidence: [Ubuntu](https://github.com/vixttha/README-HQ/actions/runs/44688891185/job/136129680512), [Windows](https://github.com/vixttha/README-HQ/actions/runs/44688891185/job/136129680539), [Graphify](https://github.com/vixttha/README-HQ/actions/runs/44688891185/job/136129680274), [original foundation evidence](https://github.com/vixttha/README-HQ/tree/c8a70ad2e1a06cad5f058fcc691c21860eb51915/evidence/repair-v0.0.6), [integration gate #156](https://github.com/vixttha/README-HQ/issues/156).

## Status counts

- 1 owner publication pending
- 57 related passing regression; full criterion not yet reviewed
- 3 combined Graphify evidence only; checkpoint-specific review pending
- 4 specific evidence not located in this crosswalk
- 1 owner license decision pending
- 1 live merge-group proof pending

## Checkpoint index

| Checkpoint | Issue | Plan topic | Candidate evidence pointer | Review status |
| --- | --- | --- | --- | --- |
| v0.0.6.1 | [#1](https://github.com/vixttha/README-HQ/issues/1) | Default homepage discovery | draft root README; main unchanged | owner publication pending |
| v0.0.6.2 | [#2](https://github.com/vixttha/README-HQ/issues/2) | Archived BART homepage links | `test_fragments_and_rendered_link_forms` | related passing regression; full criterion not yet reviewed |
| v0.0.6.3 | [#3](https://github.com/vixttha/README-HQ/issues/3) | Source provenance and tracked modes | `test_registry_and_inventory_cannot_vouch_for_each_other` | related passing regression; full criterion not yet reviewed |
| v0.0.6.4 | [#4](https://github.com/vixttha/README-HQ/issues/4) | Frozen standalone version integrity | `test_version_rows_and_current_label_are_bound_to_archives` | related passing regression; full criterion not yet reviewed |
| v0.0.6.5 | [#5](https://github.com/vixttha/README-HQ/issues/5) | Version-to-map and homepage mapping | `test_version_rows_and_current_label_are_bound_to_archives` | related passing regression; full criterion not yet reviewed |
| v0.0.6.6 | [#6](https://github.com/vixttha/README-HQ/issues/6) | GitHub Markdown navigation | `test_fragments_and_rendered_link_forms` | related passing regression; full criterion not yet reviewed |
| v0.0.6.7 | [#7](https://github.com/vixttha/README-HQ/issues/7) | Record-specific Graphify evidence | MCP combined run | combined Graphify evidence only; checkpoint-specific review pending |
| v0.0.6.8 | [#8](https://github.com/vixttha/README-HQ/issues/8) | Technique registry field types | `test_wrong_registry_shapes_fail_without_a_traceback_and_write_a_receipt` | related passing regression; full criterion not yet reviewed |
| v0.0.6.9 | [#9](https://github.com/vixttha/README-HQ/issues/9) | Failed batch recovery | `test_partition_late_write_failure_leaves_destination_available_for_retry` | related passing regression; full criterion not yet reviewed |
| v0.0.6.10 | [#10](https://github.com/vixttha/README-HQ/issues/10) | Graphify table escaping | `test_rendered_tables_ignore_fenced_rows_and_reject_missing_navigation` | related passing regression; full criterion not yet reviewed |
| v0.0.6.11 | [#11](https://github.com/vixttha/README-HQ/issues/11) | Automatic repository mode and runner safety | `test_public_reader_workflow_preserves_the_validator_exit` | related passing regression; full criterion not yet reviewed |
| v0.0.6.12 | [#12](https://github.com/vixttha/README-HQ/issues/12) | Portable adopter target and ref | `test_repo_cli_requires_root_and_supports_explicit_subproject`, `test_pinned_readme_and_monorepo_routes` | related passing regression; full criterion not yet reviewed |
| v0.0.6.13 | [#13](https://github.com/vixttha/README-HQ/issues/13) | GitHub-visible README discovery | `test_root_fragments_follow_the_effective_homepage`, `test_adopter_detects_an_org_homepage_as_incomplete` | related passing regression; full criterion not yet reviewed |
| v0.0.6.14 | [#14](https://github.com/vixttha/README-HQ/issues/14) | Mechanical README quality gates | `test_quality_and_smoke_have_separate_outcomes` | related passing regression; full criterion not yet reviewed |
| v0.0.6.15 | [#15](https://github.com/vixttha/README-HQ/issues/15) | Repository-root-relative links | `test_pinned_readme_and_monorepo_routes` | related passing regression; full criterion not yet reviewed |
| v0.0.6.16 | [#16](https://github.com/vixttha/README-HQ/issues/16) | Published Git tree link verification | `test_fetched_repository_refs_are_resolved_without_a_local_branch`, `test_partial_clone_blob_fetch_requires_explicit_permission` | related passing regression; full criterion not yet reviewed |
| v0.0.6.17 | [#17](https://github.com/vixttha/README-HQ/issues/17) | Default-branch publication coverage | — | specific evidence not located in this crosswalk |
| v0.0.6.18 | [#18](https://github.com/vixttha/README-HQ/issues/18) | Verified source and run binding | `test_documented_review_receipt_passes_and_raw_or_incomplete_receipts_fail` | related passing regression; full criterion not yet reviewed |
| v0.0.6.19 | [#19](https://github.com/vixttha/README-HQ/issues/19) | Canonical evidence identity | `test_json_duplicates_and_canonical_evidence`, `test_learning_records_verified_canonical_repository_identity` | related passing regression; full criterion not yet reviewed |
| v0.0.6.20 | [#20](https://github.com/vixttha/README-HQ/issues/20) | Duplicate mechanism detection | `test_learning_conflicting_decisions_at_same_source_are_rejected` | related passing regression; full criterion not yet reviewed |
| v0.0.6.21 | [#21](https://github.com/vixttha/README-HQ/issues/21) | Durable source-learning intake | `test_learning_receipt_is_pinned_and_idempotent` | related passing regression; full criterion not yet reviewed |
| v0.0.6.22 | [#22](https://github.com/vixttha/README-HQ/issues/22) | Project-specific recommendation receipts | `test_learning_distinguishes_unknown_retired_and_unselected_ids` | related passing regression; full criterion not yet reviewed |
| v0.0.6.23 | [#23](https://github.com/vixttha/README-HQ/issues/23) | Public and private learning separation | `test_public_learning_refusal_writes_nothing` | related passing regression; full criterion not yet reviewed |
| v0.0.6.24 | [#24](https://github.com/vixttha/README-HQ/issues/24) | Reuse and attribution boundary | REUSE.md; no approved license | owner license decision pending |
| v0.0.6.25 | [#25](https://github.com/vixttha/README-HQ/issues/25) | Exact Markdown evidence permalinks | `test_graphify_evidence_line_links_use_source_mode_for_rendered_formats` | related passing regression; full criterion not yet reviewed |
| v0.0.6.26 | [#26](https://github.com/vixttha/README-HQ/issues/26) | Rendered Graphify source anchors | `test_exact_anchors_and_explicit_line` | related passing regression; full criterion not yet reviewed |
| v0.0.6.27 | [#27](https://github.com/vixttha/README-HQ/issues/27) | Behavioral first-use validation | `test_required_smoke_distinguishes_pass_failure_and_incomplete_coverage`, `test_required_smoke_needs_a_matching_documented_action` | related passing regression; full criterion not yet reviewed |
| v0.0.6.28 | [#28](https://github.com/vixttha/README-HQ/issues/28) | Media and accessible image links | `test_bad_image_and_unnamed_image_link_are_separate`, `test_mixed_markdown_html_image_link_names_keep_both_targets` | related passing regression; full criterion not yet reviewed |
| v0.0.6.29 | [#29](https://github.com/vixttha/README-HQ/issues/29) | Complete diagnostics | `test_broken_inline_links_reference_the_exact_occurrence_line`, `test_receipt_persistence_failure_preserves_audit_diagnostics` | related passing regression; full criterion not yet reviewed |
| v0.0.6.30 | [#30](https://github.com/vixttha/README-HQ/issues/30) | Target evidence binding | `test_adopter_receipt_distinguishes_scope_at_one_commit`, `test_learning_receipt_is_pinned_and_idempotent` | related passing regression; full criterion not yet reviewed |
| v0.0.6.31 | [#31](https://github.com/vixttha/README-HQ/issues/31) | Optimization-safe verification | — | specific evidence not located in this crosswalk |
| v0.0.6.32 | [#32](https://github.com/vixttha/README-HQ/issues/32) | Durable acceptance receipts | `test_receipt_distinguishes_actions_attempts_jobs_and_standalone`, `test_receipt_identifies_executing_validator_separately_from_target_bytes` | related passing regression; full criterion not yet reviewed |
| v0.0.6.33 | [#33](https://github.com/vixttha/README-HQ/issues/33) | Graphify roadmap capacity | `test_partition_capacity_preserves_order`, `test_partition_writer_handles_more_than_three_partitions` | related passing regression; full criterion not yet reviewed |
| v0.0.6.34 | [#34](https://github.com/vixttha/README-HQ/issues/34) | MCP evidence destinations | `test_mcp_inventory_rejects_a_count_preserving_wrong_edge` | related passing regression; full criterion not yet reviewed |
| v0.0.6.35 | [#35](https://github.com/vixttha/README-HQ/issues/35) | Repository provenance | `test_unrelated_repository_or_branch_is_rejected` | related passing regression; full criterion not yet reviewed |
| v0.0.6.36 | [#36](https://github.com/vixttha/README-HQ/issues/36) | Git source file modes | `test_source_path_must_stay_inside_commit` | related passing regression; full criterion not yet reviewed |
| v0.0.6.37 | [#37](https://github.com/vixttha/README-HQ/issues/37) | Unambiguous JSON inputs | `test_json_duplicates_and_canonical_evidence` | related passing regression; full criterion not yet reviewed |
| v0.0.6.38 | [#38](https://github.com/vixttha/README-HQ/issues/38) | Source line bounds | `test_anchor_resolves_to_one_exact_line` | related passing regression; full criterion not yet reviewed |
| v0.0.6.39 | [#39](https://github.com/vixttha/README-HQ/issues/39) | Archive inventory completeness | `test_registry_and_inventory_cannot_vouch_for_each_other` | related passing regression; full criterion not yet reviewed |
| v0.0.6.40 | [#40](https://github.com/vixttha/README-HQ/issues/40) | Version map coverage | `test_coverage_and_duplicate_manifest_keys` | related passing regression; full criterion not yet reviewed |
| v0.0.6.41 | [#41](https://github.com/vixttha/README-HQ/issues/41) | Exact Git line coordinates | `test_review_followup_rendered_rows_normalize_line_endings` | related passing regression; full criterion not yet reviewed |
| v0.0.6.42 | [#42](https://github.com/vixttha/README-HQ/issues/42) | Binary media inventory | `test_inventory_blob_cap_and_text_anchor_boundary` | related passing regression; full criterion not yet reviewed |
| v0.0.6.43 | [#43](https://github.com/vixttha/README-HQ/issues/43) | Graph and receipt publication | `test_atomic_pair_preserves_prior_graph_on_conflict`, `test_graphify_reader_and_writer_recover_an_interrupted_publication` | related passing regression; full criterion not yet reviewed |
| v0.0.6.44 | [#44](https://github.com/vixttha/README-HQ/issues/44) | Bounded GitHub PR history | `test_historical_commit_requires_github_membership` | related passing regression; full criterion not yet reviewed |
| v0.0.6.45 | [#45](https://github.com/vixttha/README-HQ/issues/45) | External reader entry points | `test_http_smoke_checks_expected_error_bodies_and_preserves_auth_gates`, `test_http_smoke_records_and_can_require_the_effective_url` | related passing regression; full criterion not yet reviewed |
| v0.0.6.46 | [#46](https://github.com/vixttha/README-HQ/issues/46) | Learning source coordinates | `test_learning_structured_rate_limit_and_invalid_anchor_diagnostics` | related passing regression; full criterion not yet reviewed |
| v0.0.6.47 | [#47](https://github.com/vixttha/README-HQ/issues/47) | Technique retirement in recommendations | `test_learning_distinguishes_unknown_retired_and_unselected_ids` | related passing regression; full criterion not yet reviewed |
| v0.0.6.48 | [#48](https://github.com/vixttha/README-HQ/issues/48) | Complete MCP readback at supported limits | MCP combined run | combined Graphify evidence only; checkpoint-specific review pending |
| v0.0.6.49 | [#49](https://github.com/vixttha/README-HQ/issues/49) | Git branch-name compatibility | `test_batch5_review_publication_rule_pages_classic_branch_protection_and_branch_syntax` | related passing regression; full criterion not yet reviewed |
| v0.0.6.50 | [#50](https://github.com/vixttha/README-HQ/issues/50) | Checkpoint label and fixture ownership | `test_plan_acceptance_checks_reject_missing_or_changed_obligations`, `test_plan_file_inventory_is_bound_to_approved_partition` | related passing regression; full criterion not yet reviewed |
| v0.0.6.51 | [#51](https://github.com/vixttha/README-HQ/issues/51) | Graphify plan index links | `test_rendered_tables_ignore_fenced_rows_and_reject_missing_navigation` | related passing regression; full criterion not yet reviewed |
| v0.0.6.52 | [#52](https://github.com/vixttha/README-HQ/issues/52) | Clean checkout line-ending compatibility | `test_review_followup_rendered_rows_normalize_line_endings` | related passing regression; full criterion not yet reviewed |
| v0.0.6.53 | [#53](https://github.com/vixttha/README-HQ/issues/53) | Immutable Git object reads | — | specific evidence not located in this crosswalk |
| v0.0.6.54 | [#54](https://github.com/vixttha/README-HQ/issues/54) | Exact MCP relation fields | `test_mcp_inventory_rejects_a_count_preserving_wrong_edge` | related passing regression; full criterion not yet reviewed |
| v0.0.6.55 | [#55](https://github.com/vixttha/README-HQ/issues/55) | Immutable learning-source commits | `test_learning_receipt_is_pinned_and_idempotent` | related passing regression; full criterion not yet reviewed |
| v0.0.6.56 | [#56](https://github.com/vixttha/README-HQ/issues/56) | Packaged Graphify self-map | MCP combined run | combined Graphify evidence only; checkpoint-specific review pending |
| v0.0.6.57 | [#57](https://github.com/vixttha/README-HQ/issues/57) | Version-index row uniqueness | `test_version_rows_and_current_label_are_bound_to_archives` | related passing regression; full criterion not yet reviewed |
| v0.0.6.58 | [#58](https://github.com/vixttha/README-HQ/issues/58) | Merge-queue validation | workflow declares merge_group | live merge-group proof pending |
| v0.0.6.59 | [#59](https://github.com/vixttha/README-HQ/issues/59) | Consistent PR head observation | `test_base_provenance_rejects_retargeting_with_the_same_head`, `test_merge_sha_is_distinct_from_source_sha` | related passing regression; full criterion not yet reviewed |
| v0.0.6.60 | [#60](https://github.com/vixttha/README-HQ/issues/60) | Technique list output encoding | `test_ascii_technique_listing` | related passing regression; full criterion not yet reviewed |
| v0.0.6.61 | [#61](https://github.com/vixttha/README-HQ/issues/61) | Technique lookup key collisions | `test_json_duplicates_and_canonical_evidence` | related passing regression; full criterion not yet reviewed |
| v0.0.6.62 | [#62](https://github.com/vixttha/README-HQ/issues/62) | Exact review pagination boundary | — | specific evidence not located in this crosswalk |
| v0.0.6.63 | [#63](https://github.com/vixttha/README-HQ/issues/63) | GitHub README markup coverage | `test_rich_text_navigation_reports_explicit_incomplete_status`, `test_adopter_detects_an_org_homepage_as_incomplete` | related passing regression; full criterion not yet reviewed |
| v0.0.6.64 | [#64](https://github.com/vixttha/README-HQ/issues/64) | Joined Unicode emoji in exact anchors | `test_exact_anchors_and_explicit_line` | related passing regression; full criterion not yet reviewed |
| v0.0.6.65 | [#65](https://github.com/vixttha/README-HQ/issues/65) | Release-specific change anchoring | `test_release_heading_beats_a_draft_placeholder` | related passing regression; full criterion not yet reviewed |
| v0.0.6.66 | [#66](https://github.com/vixttha/README-HQ/issues/66) | Rendered fragment destinations | `test_root_fragments_follow_the_effective_homepage`, `test_fragments_and_rendered_link_forms` | related passing regression; full criterion not yet reviewed |
| v0.0.6.67 | [#67](https://github.com/vixttha/README-HQ/issues/67) | Custom named anchor navigation | `test_fragments_and_rendered_link_forms` | related passing regression; full criterion not yet reviewed |

## Navigation evidence

[Run 45395209099](https://github.com/vixttha/README-HQ/actions/runs/45395209099), attempt 1, [artifact 14920702366](https://github.com/vixttha/README-HQ/actions/runs/45395209099/artifacts/14920702366) SHA-256 `ecbf11eceafd7e98bf1f132b98fef2db58cb785c460a90441cdb6c205dad5aa1` independently matched after download. 89 observations: 82 GitHub routes responded (58 unique requests), five historical local examples intentionally not probed, two official Pillow sources outside runner probe scope but separately retrieved on 2026-11-24: [release notes](https://pillow.readthedocs.io/en/stable/releasenotes/13.0.0.html) and [PyPI metadata](https://pypi.org/pypi/Pillow/13.0.0/json). HTTP route availability is not semantic, rendered anchor, or behavior verification. Preserve historical imports.

## Next gate

First review the unlocated specific controls (#17 publication branches, #31 optimized interpreter, #53 replacement refs, #62 pagination boundary), then read the mapped test bodies and reproduce missing acceptance clauses on public runners. Owner decisions #1, #24, #58, #132 remain separate. Do not merge, tag or establish the proposed next release without owner approval.
