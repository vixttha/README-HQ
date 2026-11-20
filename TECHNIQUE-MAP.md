# README technique map

This map groups individual techniques by the job they do for a reader or maintainer. Each linked technique has a learning record. Plain entries are later research candidates awaiting a learning record.

A technique belongs wherever its behavior helps. This map gives each one a primary home for browsing. The searchable catalog can list a single record under more than one task.

## Purpose and audience

Help readers decide whether they’re in the right place.

- [State the project’s purpose](techniques/project-purpose-statement.md) — Tell a new reader what the project does and what they can accomplish with it.
- [Audience and use cases](techniques/audience-and-use-cases.md) — Name the people and jobs the project serves.
- [Value proposition](techniques/value-proposition.md) — Explain the practical payoff or problem the project removes.
- [Project status and maturity](techniques/project-status-and-maturity.md) — Distinguish a preview, stable release, or archived project.
- [Explain how to choose an update channel](techniques/explain-how-to-choose-an-update-channel.md) — When multiple release streams are offered, state the differences in stability, update cadence, and what the reader should install. nginx labels mainline, stable, and legacy downloads.
- [Distinguish source from the shipped product](techniques/distinguish-source-from-the-shipped-product.md) — Explain what readers are browsing, which product or distribution it produces, and where each set of terms applies. VS Code does this for Code - OSS and Microsoft’s Visual Studio Code distribution.
- **Match model variants to their files and runtime** — List the exact variants readers can obtain and show how the base or instruction-tuned version, weight format, and precision affect runtime compatibility and resource needs. Point to the matching model card and example for each supported option. For derived weights, link the base model and name the relationship. [Gemma variant and memory guide](https://gemma.ai/models/gemma-4/) · [Gemma GGUF model card](https://huggingface.co/google/gemma-3-12b-pt-qat-q4_0-gguf)
- [Capabilities at a glance](techniques/capabilities-at-a-glance.md) — Show the few important things readers can do today.
- [Scope boundaries](techniques/scope-boundaries.md) — Call out material limitations or environments outside the supported scope.
- **State what the dataset represents** — Describe the unit of observation, collection period, geographic or population coverage, and material exclusions. Name the release the coverage applies to and distinguish sampled records from the population they represent by labeling each explicitly. [U.S. Census ACS microdata coverage](https://api.census.gov/data/2024/acs/acs5/pums.html) · [W3C DCAT coverage properties](https://www.w3.org/TR/vocab-dcat-3/)
- [List what each format can read, write, and preserve](techniques/list-what-each-format-can-read-write-and-preserve.md) — Separate input and output support. State which content or formatting a named conversion may lose, and how to check a result that needs fidelity. Pandoc distinguishes its readers and writers and explains lossy conversions.
- [Disclose telemetry defaults and controls](techniques/disclose-telemetry-defaults-and-controls.md) — Name the data a tool collects, the default participation state, and how to view or change the setting. Next.js documents the data collected and its opt-out control.
- [Alternatives and tradeoffs](techniques/alternatives-and-tradeoffs.md) — Explain when a related tool or approach fits a reader better.
- [Roadmap pointer](techniques/roadmap-pointer.md) — Link planned work to a maintained roadmap and distinguish it from available features.
- [Status badges](techniques/status-badges.md) — Surface meaningful build, release, or license signals and link each badge to its source.

[GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) · [Pinned BART introduction](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/blob/3e7f9e02e61739825b56bcafecebbd0221cc9657/README.md)

## Demos and visuals

Show what using the project looks like.

- [Live demo or playground](techniques/live-demo-or-playground.md) — Link directly to a usable experience and state access requirements.
- [Link both a notebook preview and a runnable notebook](techniques/link-both-a-notebook-preview-and-a-runnable-notebook.md) — Label the link for inspecting saved results and the link for launching the notebook at the corresponding revision. GitHub renders notebooks statically, while Binder can open a particular notebook for execution.
- [Screenshot or result preview](techniques/screenshot-or-result-preview.md) — Show the key product screen or output readers should recognize.
- [Annotated screenshot](techniques/annotated-screenshot.md) — Identify the controls or evidence a reader needs to notice.
- [Animated micro-demo](techniques/animated-micro-demo.md) — Show a short interaction sequence that needs no narration.
- [Captioned video walkthrough](techniques/captioned-video-walkthrough.md) — Demonstrate a longer workflow with captions or a transcript.
- [Minimal working example](techniques/minimal-working-example.md) — Show the smallest realistic input and operation that demonstrate the capability.
- [Architecture or flow diagram](techniques/architecture-or-flow-diagram.md) — Show component relationships or the order of steps.
- [Asset caption and provenance](techniques/asset-caption-and-provenance.md) — Name what a visual shows and identify its source or build where relevant.
- [Show how asset variants map to published files](techniques/show-how-asset-variants-map-to-published-files.md) — Give the file naming pattern, label the dimensions or styles that change the filename, and show where to check whether a combination exists. Fluent UI’s SVG README specifies the names and which file inventory determines availability.
- [Write image alternatives for their purpose](techniques/purpose-specific-image-alternatives.md) — Give informative, decorative, functional, and complex visuals the text treatment their roles require.
- [Theme-aware images](techniques/theme-aware-images.md) — Check readability against light and dark backgrounds and provide variants when needed.
- [Text equivalent for a chart or diagram](techniques/text-equivalent-for-a-chart-or-diagram.md) — Put essential values, conclusions, or relationships in surrounding text.

[GitHub diagram support](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) · [W3C WAI image guidance](https://www.w3.org/WAI/tutorials/images/) · [Pinned AlderVale visual example](https://github.com/vixttha/AlderVale-Pact-of-Ten/blob/a6c2060b8175f505cc6327ccb5658cc00a458b24/README.md)

## Quickstart and adoption

Get a reader to a first meaningful action.

- [One prominent first action](techniques/one-prominent-first-action.md) — Lead with a recognizable task such as play, try, install, or adopt.
- [Provide a starter control map](techniques/provide-a-starter-control-map.md) — List the actions a player needs in the first minute and map them to each supported input type. Point to remapping settings where they exist.
- [Prerequisites next to the task](techniques/prerequisites-next-to-the-task.md) — Name tools, versions, access, and prior setup before any commands depend on them.
- [Show the permissions automation needs](techniques/show-the-permissions-automation-needs.md) — Name the caller permissions the example needs and what each one allows. For reusable workflows, state where those permissions must be granted.
- [Link a parts list for the hardware revision](techniques/link-a-parts-list-for-the-hardware-revision.md) — Give builders a bill of materials that matches the design they are assembling. Include part identifiers, quantities, and any documented substitutions, with a way to map each item to the design.
- [Match firmware to the physical hardware revision](techniques/match-firmware-to-the-physical-hardware-revision.md) — Help readers identify the device revision and map it to the correct build or download target. QMK distinguishes buildable keyboard revisions and documents target selection.
- [Set a time and cost expectation before setup](techniques/set-a-time-and-cost-expectation-before-setup.md) — State how long the example usually takes and whether it can create billable resources, with a link to current terms when pricing depends on an account or provider. AWS examples show
- [Write a copyable Quickstart](techniques/copyable-quickstart.md) — Give readers ordered commands they can paste into the supported shell.
- [Separate platform commands](techniques/separate-platform-commands.md) — Label POSIX and PowerShell paths where their commands differ.
- [Installation methods](techniques/installation-methods.md) — Distinguish packages, installers, source builds, and other supported options.
- [Show how to enable optional capabilities](techniques/show-how-to-enable-optional-capabilities.md) — Identify what the base install enables and which feature flag or package extra enables each optional capability. Put optional setup beside the example that requires it. Tokio documents the default and the features readers can select.
- [Pair the install name with the name used in code](techniques/pair-the-install-name-with-the-name-used-in-code.md) — When distribution, import, or executable names differ, show the exact names together so readers can connect the installation step to the first use. The Python Packaging User Guide illustrates this with the Pillow distribution and its PIL import.
- [Identify required assets distributed separately](techniques/identify-required-assets-distributed-separately.md) — State which graphics, sound, models, or other runtime assets the checkout needs. Link their maintained source and say which installation routes fetch them automatically.
- **Explain how to obtain restricted inputs** — Give each restricted input an authorized acquisition route and name the eligibility, training, agreement, or approved environment that applies. Identify affected steps and the role or provider that handles access requests. [Social Science Data Editors README template](https://github.com/social-science-data-editors/template_README/blob/development/template-README.md) · [UK Data Service controlled access](https://ukdataservice.ac.uk/find-data/access-conditions/secure-application-requirements/)
- [Describe what the installer changes](techniques/describe-what-the-installer-changes.md) — Tell readers where binaries or files are installed, which persistent user settings change, and what supported option controls those changes. uv documents its installation directory and shell-profile behavior.
- [Label ownership of installation channels](techniques/label-ownership-of-installation-channels.md) — Identify who maintains and supports each package or installer so readers know where to report installation problems. GitHub CLI links community-supported routes separately.
- [Starting directory and checkout](techniques/starting-directory-and-checkout.md) — State where commands begin and which revision or project root they expect.
- [List the local service URLs by purpose](techniques/list-the-local-service-urls-by-purpose.md) — When setup starts several services, tell readers which address opens the app, dashboard, API, or other local tool. Supabase CLI labels the addresses it prints for its development stack.
- [Safe configuration example](techniques/safe-configuration-example.md) — Use labeled placeholders and explain where values belong.
- [Give service examples a sandbox route](techniques/give-service-examples-a-sandbox-route.md) — Name the sandbox or mock used by the example and state what effects it simulates. Label the difference from live operation so readers know where the example can be run.
- [Offer an importable API request collection](techniques/offer-an-importable-api-request-collection.md) — Link a reusable request collection so readers can run the same requests in their API client. Identify the target environment and show which values they need to supply locally.
- [Show configuration precedence](techniques/show-configuration-precedence.md) — Explain which setting wins when flags, environment variables, configuration files, and defaults disagree. Give one concrete conflict example in the supporting reference. Terraform documents the order for root module input variables.
- [Sample fixture or starter input](techniques/sample-fixture-or-starter-input.md) — Provide a small known input that readers can use immediately.
- **Provide a shareable substitute for restricted data** — Offer a documented, structurally compatible sample when real inputs cannot be distributed. Tell readers which checks the sample supports and which findings require the authorized inputs. Keep the sample path clearly labeled in the run instructions. [World Bank synthetic-data verification guidance](https://github.com/worldbank/wb-reproducible-research-repository/blob/main/guidance_note_wb.md#packages-with-restricted-or-confidential-data)
- [Guest or offline first run](techniques/guest-or-offline-first-run.md) — Offer a first-use path with minimal account or network dependencies when supported.
- [Show how to prepare an offline install](techniques/show-how-to-prepare-an-offline-install.md) — Separate gathering dependencies on a connected machine from installing the staged set on the offline target. State which platform and runtime the bundle must match. pip documents both stages.
- [Offer an isolated trial command](techniques/offer-an-isolated-trial-command.md) — Give the reader a short way to try a tool without installing it into their project. State what runner is required and what can be cached. uv demonstrates a temporary tool environment with `uvx`.
- [Link directly to a project-configured workspace](techniques/link-directly-to-a-project-configured-workspace.md) — Point readers to a preconfigured development workspace tied to the repository and intended branch. State what account or local tooling it needs. GitHub Codespaces and VS Code Dev Containers document repository links for this.
- [Prerequisite or installation check](techniques/prerequisite-or-installation-check.md) — Show a fast way to check that the local environment is ready before the demo.
- [Copy-in or template adoption path](techniques/copy-in-or-template-adoption-path.md) — Identify what to copy, where it goes, and how to check the resulting project.
- [Upgrade or migration route](techniques/upgrade-or-migration-route.md) — Name the starting version, intended destination, and relevant migration guide.
- [Show the order for upgrading multiple components](techniques/show-the-order-for-upgrading-multiple-components.md) — When components evolve independently, show the upgrade sequence and which version combinations can coexist during the transition. Kubernetes documents both the skew limits and the supported component order.
- [Give readers an upgrade preflight](techniques/give-readers-an-upgrade-preflight.md) — Link a compatibility check readers can run before an upgrade changes their existing installation. Explain which findings block the upgrade and where to resolve them. PostgreSQL documents a check-only path for pg_upgrade.
- [Cleanup or reset instructions](techniques/cleanup-or-reset-instructions.md) — Show how a reader can leave a temporary demo or restore a clean starting point.
- [Explain what uninstall removes and retains](techniques/explain-what-uninstall-removes-and-retains.md) — State which commands or files uninstall removes and what happens to data, configuration, caches, or installed components. Point to the data-preservation path when it matters. Docker Desktop distinguishes uninstall effects from backup and restore.
- [Preview changes before applying them](techniques/preview-changes-before-applying-them.md) — When a workflow changes state and offers a preview, give the preview and apply steps distinct labels. Explain which changes the preview can predict. Terraform documents its plan separately from apply.

[Google code-sample guidance](https://developers.google.com/style/code-samples) · [Pinned BART Quickstart](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/blob/3e7f9e02e61739825b56bcafecebbd0221cc9657/README.md) · [Pinned template adoption guide](https://github.com/vixttha/Brand-Identity-Template/blob/87d0f9aedbe69ca4b16815d6b3329efcf5889da9/README.md)

## First result and recovery

Help the reader recognize success and get unstuck.

- [Show a recognizable first result](techniques/first-success-milestone.md) — Tell the reader what success looks like immediately after the first real task.
- [Expected output contract](techniques/expected-output-contract.md) — Separate stable result fields from variable example values when exact comparison matters.
- [Give a readiness check before the first request](techniques/give-a-readiness-check-before-the-first-request.md) — After the startup command, show what indicates the dependency can accept traffic and how the reader can check it. A service may be running before its dependencies are ready.
- [Document the scripting interface](techniques/document-the-scripting-interface.md) — Show where scripts can find structured output and which outcomes return which exit codes. Include command-specific exceptions when they affect automation. GitHub CLI documents both formatting and exit behavior.
- [Show how to retrieve every page of results](techniques/show-how-to-retrieve-every-page-of-results.md) — Give an example that spans multiple pages, follows the continuation link or cursor, and states when to stop. GitHub’s REST guide demonstrates following the next-page link until it is absent.
- [Save or persistence checkpoint](techniques/save-or-persistence-checkpoint.md) — Tell readers what should survive a restart and how to confirm it.
- [Map application files by purpose](techniques/map-application-files-by-purpose.md) — List the locations for user data, configuration, runtime state, and cache on supported platforms. Identify overrides and distinguish files a reader needs to preserve from data the application can rebuild.
- [State which saved data a release can open](techniques/state-which-saved-data-a-release-can-open.md) — Name which older saves, archives, or project files the new version can read, and describe rollback separately where supported. OpenTTD documents loading saves from older revisions.
- [Show a restore check against a separate destination](techniques/show-a-restore-check-against-a-separate-destination.md) — Pair a backup path with a small restore exercise into a separate destination and show what to inspect in the restored copy. The restic restore guide explains selecting the snapshot and destination.
- [First successful result link](techniques/first-successful-result-link.md) — Point to the file, page, or artifact the task created so it is easy to inspect.
- [Next action after success](techniques/next-action-after-success.md) — Offer a natural second task once the first one works.
- [Put a practice task before its worked solution](techniques/put-a-practice-task-before-its-worked-solution.md) — When the README is also a learning guide, give readers a short task and a way to check their attempt. Put the worked answer behind a labeled section or link. The Carpentries uses separate challenge and solution blocks.
- [Recovery beside the failed step](techniques/recovery-beside-the-failed-step.md) — Put a common failure and its recovery close to the command or action that produces it.
- [Explain what happens when a step is repeated](techniques/explain-what-happens-when-a-step-is-repeated.md) — State whether repeating a command converges on the same result, resumes work, or creates another copy. Ansible’s module guide describes idempotency as a behavior that module authors should provide. Check the actual commands before promising it.
- [Document what happens with concurrent writers](techniques/document-what-happens-with-concurrent-writers.md) — Say which shared state is protected, when writers wait or fail, and whether the behavior depends on the storage backend or deployment mode. Terraform scopes locking to supported backends. SQLite distinguishes concurrent readers from writers in WAL mode.
- [Document automatic retry boundaries](techniques/document-automatic-retry-boundaries.md) — Tell automated readers which responses allow another attempt, which server signal controls the delay, and when retries should stop. GitHub’s REST guidance distinguishes waiting according to response headers from persisting after repeated failures.
- [Diagnostic decision guide](techniques/diagnostic-decision-guide.md) — Route different symptoms to the relevant fix instead of listing generic troubleshooting.
- [Separate diagnostic capture from sharing](techniques/separate-diagnostic-capture-from-sharing.md) — Tell readers how to capture relevant evidence, where the resulting bundle lands, and how to inspect or anonymize it before sending it through the support route. Docker distinguishes diagnostic capture and upload. Atlassian documents support-bundle anonymization.
- [Show how to activate an installed extension](techniques/show-how-to-activate-an-installed-extension.md) — Name the first command, view, or event that activates the extension and the behavior a reader should see. VS Code distinguishes installing an extension from activating it on a matching event.
- [Known limitations and workarounds](techniques/known-limitations-and-workarounds.md) — State a known constraint and the currently supported path around it.
- [Explain defaults that change what readers see](techniques/explain-defaults-that-change-what-readers-see.md) — Name the input the tool omits or transforms by default, what a reader may miss, and how to change the behavior. ripgrep puts its default exclusions near its opening description.

[Pinned Veraphify result example](https://github.com/vixttha/Veraphify/blob/88d5d08cd8c80de3927858685878e51b6d7c69b8/README.md) · [README HQ registry](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/techniques/registry.json)

## Navigation and accessibility

Get readers to the right information with minimal scanning.

- [Route by reader task](techniques/role-based-entry-points.md) — Give distinct reader goals clear routes from the same homepage.
- [Relative navigation](techniques/relative-navigation.md) — Link same-checkout guides and assets with paths relative to the Markdown file.
- [Descriptive link labels](techniques/descriptive-link-labels.md) — Use text that tells the reader where the link goes or what it does.
- [Clear heading hierarchy](techniques/clear-heading-hierarchy.md) — Organize sections in a predictable structure for visual scanning and assistive navigation.
- [Table of contents or jump links](techniques/table-of-contents-or-jump-links.md) — Expose major sections when the page is long enough to need them.
- [Section deep links](techniques/section-deep-links.md) — Send the reader to the relevant part of a guide and recheck anchors when headings change.
- [Send readers to docs for their installed version](techniques/send-readers-to-docs-for-their-installed-version.md) — Label stable and development docs links so readers can match them to the version they are using. A branch README can link multiple editions if its audience spans supported releases.
- [Progressive disclosure](techniques/progressive-disclosure.md) — Collapse optional details or move them to a clearly labeled supporting document.
- [Use labeled callouts at the point of action](techniques/use-labeled-callouts-at-the-point-of-action.md) — Use short labeled notices for important context or consequences beside the relevant step. Keep essential information readable in plain text when the renderer handles callouts differently.
- [Give color-coded information a text label](techniques/give-color-coded-information-a-text-label.md) — Label states, branches, or series in words when color conveys their meaning. Readers should still understand a status table or diagram with the colors removed.
- [Separate guide types](techniques/separate-guide-types.md) — Route readers to a tutorial, how-to, reference, or explanation according to their task.
- [Give each public package its own README entry point](techniques/give-each-public-package-its-own-readme-entry-point.md) — Put a short orientation in the package directory so someone entering through a deep link can find its purpose, setup, and supporting docs. Google’s README guide calls this out for package directories.
- [Concise comparison table](techniques/concise-comparison-table.md) — Present repeated choices in a table when readers need to compare the same attributes.
- [Language routing](techniques/language-routing.md) — Link translated docs and make the expected language clear.
- [Track the source revision of translations](techniques/track-the-source-revision-of-translations.md) — Link a translated README to its original and record which revision or release it follows. This lets maintainers identify what needs updating and readers find the source text when needed. Kubernetes documents its upstream-first translation workflow.
- [Task-local help link](techniques/task-local-help-link.md) — Put the relevant support path beside a high-friction step.
- [Consistent terms](techniques/consistent-terms.md) — Use the same names for actions and objects as the code, UI, and linked instructions.

[GitHub README and section links](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) · [W3C accessible writing](https://www.w3.org/WAI/tips/writing/) · [Diátaxis documentation types](https://diataxis.fr/start-here/)

## Verification and trust

Make public claims traceable and scoped.

- [Execute the documented walkthrough](techniques/exact-revision-walkthrough.md) — Replay the reader’s published steps at the named revision and verify the result.
- [Turn examples into regression tests](techniques/turn-examples-into-regression-tests.md) — Generate test cases from examples in the maintained documentation source so changing an example also changes what gets tested. jq’s docs README describes the process and its Makefile connects manual examples to the test suite.
- [Permanent proof links](techniques/permanent-proof-links.md) — Keep verification traceable with a commit-pinned receipt and recorded run, attempt, artifact ID, and digest.
- [Label the scope of compatibility evidence](techniques/claim-scope-labels.md) — State the version, platform, capability, and checks that support a compatibility claim. [Kubernetes client and server compatibility example](https://github.com/kubernetes-client/python/blob/92f5111c5b27dcc3004314552165d5da2190d73e/README.md#L112-L151)
- [Declared versus observed checks](techniques/declared-versus-observed-evidence.md) — Show which checks were required and which actually ran, passed, failed, or were skipped.
- [Map each claim to the check that can reproduce it](techniques/map-each-claim-to-the-check-that-can-reproduce-it.md) — Pair the claim or reported result with its command, expected outcome, and the data it produces. Label claims that fall outside the reproduction instructions.
- **State how close a rerun must get** — Define the acceptance threshold for numerical or stochastic outputs. Specify the metric, comparison rule, and tolerance, and explain which exact outputs or invariants still need to match. [ACM CCS artifact evaluation](https://sigsac.org/ccs/CCS2025/call-for-artifacts/) · [Computational reproduction package guidance](https://pmc.ncbi.nlm.nih.gov/articles/PMC8059663/)
- [Published release link](techniques/published-release-link.md) — Give a direct path to the release named in the README and its release notes.
- [Artifact verification instructions](techniques/artifact-verification-instructions.md) — Explain how to compare a downloaded artifact with its recorded digest.
- [Show how to verify the artifact’s producer](techniques/show-how-to-verify-the-artifact-s-producer.md) — Where a release provides a signed attestation, show how to verify it against the expected repository or workflow. This lets readers check build origin as well as artifact identity.
- [Combined-commit proof](techniques/combined-commit-proof.md) — Tie a merge-readiness claim to tests on the exact combined content.
- [Lightweight link verification](techniques/lightweight-link-verification.md) — Check that critical relative targets and anchors resolve at the claimed revision.
- [Publication-path verification](techniques/publication-path-verification.md) — Test links and assets from the path where the README will actually ship. The Python Packaging User Guide also runs this check against the built distribution.
- [Verify which README appears on the repository homepage](techniques/verify-which-readme-appears-on-the-repository-homepage.md) — When multiple eligible README files exist, check which one the host surfaces and publish the expected content there. GitHub checks `.github/`, the repository root, and `docs/` in that order.
- [Rendered review at two widths](techniques/rendered-review-at-two-widths.md) — Check the landing page on wide and narrow layouts for overflow or unreadable content.
- [Check keyboard navigation on the rendered README](techniques/check-keyboard-navigation-on-the-rendered-readme.md) — Use the keyboard on the published view to reach the primary links and any collapsible controls. Check for visible focus and an order that follows the content. W3C includes these in its preliminary accessibility checks.
- [Benchmark method and scope](techniques/benchmark-method-and-scope.md) — Describe the workload, environment, revision, and units beside a performance result.
- **Label which benchmark results can be compared** — Group results by evaluation rules and explain what each group holds constant and what it permits entrants to change. Identify the reference baseline or quality target where it determines whether two results belong together. [MLPerf Training divisions](https://mlcommons.org/benchmarks/training/#divisions) · [MLPerf Endpoints divisions and scenarios](https://docs.mlcommons.org/endpoints-submission-docs/understand/divisions-and-scenarios/)
- **Report how much repeated measurements vary** — Accompany a headline number with the number of runs, the summary statistic, and a suitable measure of spread or uncertainty. Name what changed across runs so readers can interpret the variation. [NeurIPS reporting checklist](https://neurips.cc/public/guides/PaperChecklist) · [MLPerf Training measurement rules](https://mlcommons.org/benchmarks/training/)
- **Disclose checks for training and evaluation overlap** — State what training or tuning sources were checked for overlap with the evaluation set, how matches were handled, and which inputs were unavailable for checking. Link the underlying protocol when it affects how readers interpret reported scores. [Phi-4-mini-instruct model card](https://huggingface.co/microsoft/Phi-4-mini-instruct/blob/main/README.md)
- [Show a benchmark case that changes the takeaway](techniques/show-a-benchmark-case-that-changes-the-takeaway.md) — Beside a favorable result, include a reproducible workload or flag change that reduces the advantage or changes performance. ripgrep shows performance cliffs and cases with many matches.
- **Break down evaluation results by meaningful groups** — Show comparable metrics for relevant populations, languages, or operating conditions alongside aggregate results. Identify the slices actually evaluated and provide the sample sizes or coverage limits readers need to interpret the scores. [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993) · [Google evaluation guidance](https://developers.google.com/machine-learning/crash-course/fairness/evaluating-for-bias)
- [Clean consumer adoption test](techniques/clean-consumer-adoption-test.md) — Verify documented copy-in or install steps in a fresh consumer project.
- [Offer a smoke test and a full reproduction separately](techniques/offer-a-smoke-test-and-a-full-reproduction-separately.md) — Use a small run to establish that setup works and a separate run to reproduce the full result. State the inputs, expected outputs, and resource needs for each.
- **Provide a way to verify saved results without rerunning everything** — Link precomputed outputs or intermediate results, their integrity checks, and the scripts or inputs that produced them. State what readers can check using the saved artifacts and which claims still require a fresh run. [World Bank guidance for computationally intensive packages](https://github.com/worldbank/wb-reproducible-research-repository/blob/main/guidance_note_wb.md#computationally-intensive-packages)
- [Snapshot source identity](techniques/snapshot-source-identity.md) — Record the origin and digest of frozen README or asset bytes when exact archival identity matters.

[GitHub file permalinks](https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files) · [GitHub artifact validation](https://docs.github.com/en/actions/tutorials/store-and-share-data#validating-artifacts) · [Pinned audit receipt](https://github.com/vixttha/README-HQ/blob/2f66dd6aa23928716f645cfebdce462b7574c4b3/audit/evidence/v0.0.6.67-full-stack.json) · [README HQ registry](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/techniques/registry.json)

## Handoff and maintenance

Help the next owner, contributor, or agent take responsibility for the project.

- [Link authoritative agent instructions](techniques/agent-instruction-pointer.md) — Point an agent to the repository’s applicable instructions from the README.
- [Developer entry point](techniques/developer-entry-point.md) — Link the source layout, setup, and shortest routine development check.
- [Contribution route](techniques/contribution-route.md) — Point to contribution rules, issue templates, and where work is reviewed.
- [Recognize contribution types beyond code](techniques/recognize-contribution-types-beyond-code.md) — Label what people contributed, such as documentation, design, translation, or testing, in the README or linked credits. The All Contributors specification describes these recognitions and a generated contributor table.
- [Explain where project decisions are made](techniques/explain-where-project-decisions-are-made.md) — Link a project’s governance and identify who makes major decisions. Give proposals a route when that route differs from submitting a patch. Kubernetes’s steering README describes its decision-making scope and links its charter.
- [Support and issue route](techniques/support-and-issue-route.md) — Tell readers where to report a bug or ask for help and what evidence to include.
- [License and reuse link](techniques/license-and-reuse-link.md) — Point to the actual terms and distinguish project assets with different terms.
- [Attribution and data provenance](techniques/attribution-and-data-provenance.md) — Link the source and terms for material external assets or datasets.
- [Route readers to editable designs and manufacturing exports](techniques/route-readers-to-editable-designs-and-manufacturing-exports.md) — Give separate links to the preferred files for modifying the design, files prepared for fabrication, and human-readable drawings where provided. Label the toolchain and revision that produced the exports.
- [Include a data dictionary for shared datasets](techniques/include-a-data-dictionary-for-shared-datasets.md) — Explain file relationships, field names, units, and missing-value codes so another person can interpret the data. Link the full dictionary when it needs its own file.
- **Show how source data becomes published files** — Trace each important derived file to its source inputs and the processing stage that produced it. Link the scripts or workflow and call out filtering, aggregation, or normalization decisions that affect reuse. [Dryad data documentation](https://datadryad.org/help/guides/best_practices) · [DVC pipeline dependencies and outputs](https://doc.dvc.org/user-guide/pipelines/defining-pipelines)
- **Explain how dataset splits were made** — Name the purpose, size, and construction rule for each partition. State which unit is kept together within a single partition, such as a speaker or account, and show readers how to select the intended split. [Samrómur speech dataset README](https://huggingface.co/datasets/language-and-voice-lab/samromur_asr) · [scikit-learn grouped splits](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html)
- **Explain how dataset labels were assigned** — Document the annotation task and label rules. Link annotator instructions and describe how disagreement was handled or measured at the level readers will use, such as records, spans, or tokens. [RefRESD dataset README](https://huggingface.co/datasets/eleftheria/refresd/blob/33c084dafbec95b939fdd16be527d74fcefdc406/README.md) · [Hugging Face dataset card template](https://huggingface.co/datasets/templates/dataset-card-example/blob/main/README.md?code=true)
- **Explain uncertainty in published measurements** — Identify the fields or derived values affected by measurement uncertainty. Define the error or confidence quantities, their units and interpretation, and the method used to estimate them where these details affect reuse. [USGS data-quality guidance](https://www.usgs.gov/data-management/documenting-data-quality-considerations) · [NIST guidance on reporting measurement uncertainty](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-7-reporting-uncertainty)
- [Security reporting route](techniques/security-reporting-route.md) — Link the project’s supported private disclosure process when applicable.
- [Citation instructions](techniques/citation-instructions.md) — Point researchers to the maintained citation metadata where appropriate.
- **Cite the exact subset of changing data** — When a result depends on a filtered subset of a changing data source, record the query or selection rules and the data version or timestamp. Link a persistent identifier for the versioned query or a frozen subset when available. [Research Data Alliance dynamic data citation recommendations](https://doi.org/10.15497/RDA00132)
- [Changelog and version navigation](techniques/changelog-and-version-navigation.md) — Show where release history lives and which version the reader is viewing.
- [Give a deprecation notice a replacement and timeline](techniques/give-a-deprecation-notice-a-replacement-and-timeline.md) — Name the affected interface, link the replacement or migration route, and distinguish the deprecation date from any planned retirement date. Link the authoritative policy when it governs multiple interfaces.
- [Identify the source of truth when repositories are mirrored](techniques/identify-the-source-of-truth-when-repositories-are-mirrored.md) — Name the canonical repository and explain which revision identifiers to cite from a mirror. SQLite’s GitHub README points to Fossil and tells readers where to find the official check-in name.
- [Turn an archived README into a handoff](techniques/turn-an-archived-readme-into-a-handoff.md) — Put the maintained successor and new project name, if any, at the top of the archive. State what remains accessible at the old location. Prisma Next explains its move and archive status before its historical README content.
- [Human guide for a structured inventory](techniques/human-guide-for-a-structured-inventory.md) — Pair a machine-readable manifest with an explanation of its reader-facing purpose.
- [Link the machine-readable interface contract](techniques/link-the-machine-readable-interface-contract.md) — Point to the specification or schema for the interface addressed by the README and identify its version. Integrators can inspect operations and field requirements in the contract while following the short example in the README.
- [Show how another workflow consumes an output](techniques/show-how-another-workflow-consumes-an-output.md) — Document output names and show a caller reading one of those outputs. Demonstrate the boundary between steps or jobs when it changes the syntax.
- [State what event consumers can assume about delivery](techniques/state-what-event-consumers-can-assume-about-delivery.md) — Say whether event delivery can repeat or arrive out of order and where to find the identifier needed to recognize a repeat. Stripe’s webhook guidance documents both cases.
- [Generate repetitive README sections from their source](techniques/generate-repetitive-readme-sections-from-their-source.md) — Generate sections such as configuration inputs or outputs from their authoritative definitions. Bound generation with file markers so authored explanations stay editable. terraform-docs documents an injected section between comments.
- [Reuse a README as the package listing](techniques/reuse-a-readme-as-the-package-listing.md) — Wire the maintained README into package metadata so package users see the same introduction in their registry. Check the description from the built package and resolve links in the target renderer.
- [Expose discovery metadata through the README](techniques/expose-discovery-metadata-through-the-readme.md) — Use host-supported metadata for fields such as dataset language, license, tags, and file layout. Hugging Face renders a dataset README as a card and uses its YAML fields for discovery and configuration.
- [Independent version lines](techniques/independent-version-lines.md) — Name the product, README, or collection beside each version when their release lines differ.
- [Versioned section map](techniques/versioned-section-map.md) — Provide a path to find corresponding sections across archived READMEs.
- [Draft, archive, and publication stages](techniques/draft-archive-and-publication-stages.md) — Keep proposed text, frozen snapshots, and the published default-branch README distinguishable.

[GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) · [Pinned Brand Identity Template](https://github.com/vixttha/Brand-Identity-Template/blob/87d0f9aedbe69ca4b16815d6b3329efcf5889da9/README.md) · [README HQ registry](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/techniques/registry.json)

## Expand the map

Search titles and aliases before adding an entry. Reuse the existing record ID when the reader problem and the practice already match. Record a new technique when it does a distinct job. The [research guide](RESEARCH.md) explains how to move a candidate into the catalog.
