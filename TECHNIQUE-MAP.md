# README technique map

This map groups individual techniques by the job they do for a reader or maintainer. Linked techniques have a catalog record. Plain entries describe candidates for later research and may need stronger evidence before they get a record.

A technique belongs wherever its behavior helps. This map gives each one a primary home for browsing. The searchable catalog can list a single record under more than one task.

## Purpose and audience

Help readers decide whether they’re in the right place.

- [State the project’s purpose](techniques/project-purpose-statement.md) — Tell a new reader what the project does and what they can accomplish with it.
- **Audience and use cases** — Name the people and jobs the project serves.
- **Value proposition** — Explain the practical payoff or problem the project removes.
- **Project status and maturity** — Distinguish a preview, stable release, or archived project.
- **Explain how to choose an update channel** — When multiple release streams are offered, state the differences in stability, update cadence, and what the reader should install. nginx labels mainline, stable, and legacy downloads. [nginx release channels](https://nginx.org/en/download.html)
- **Distinguish source from the shipped product** — Explain what readers are browsing, which product or distribution it produces, and where each set of terms applies. VS Code does this for Code - OSS and Microsoft’s Visual Studio Code distribution. [VS Code source and distribution](https://github.com/microsoft/vscode/blob/f26893c248aa2b2ef1f3dba2134d9d1806559186/README.md#L9-L15)
- **Capabilities at a glance** — Show the few important things readers can do today.
- **Scope boundaries** — Call out material limitations or environments outside the supported scope.
- **Disclose telemetry defaults and controls** — Name the data a tool collects, the default participation state, and how to view or change the setting. Next.js documents the data collected and its opt-out control. [Next.js telemetry documentation](https://nextjs.org/telemetry)
- **Alternatives and tradeoffs** — Explain when a related tool or approach fits a reader better.
- **Roadmap pointer** — Link planned work to a maintained roadmap and distinguish it from available features.
- **Status badges** — Surface meaningful build, release, or license signals and link each badge to its source.

[GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) · [Pinned BART introduction](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/blob/3e7f9e02e61739825b56bcafecebbd0221cc9657/README.md)

## Demos and visuals

Show what using the project looks like.

- **Live demo or playground** — Link directly to a usable experience and state access requirements.
- **Screenshot or result preview** — Show the key product screen or output readers should recognize.
- **Annotated screenshot** — Identify the controls or evidence a reader needs to notice.
- **Animated micro-demo** — Show a short interaction sequence that needs no narration.
- **Captioned video walkthrough** — Demonstrate a longer workflow with captions or a transcript. [Google accessible media guidance](https://developers.google.com/style/accessibility)
- **Minimal working example** — Show the smallest realistic input and operation that demonstrate the capability.
- **Architecture or flow diagram** — Show component relationships or the order of steps.
- **Asset caption and provenance** — Name what a visual shows and identify its source or build where relevant.
- [Write image alternatives for their purpose](techniques/purpose-specific-image-alternatives.md) — Give informative, decorative, functional, and complex visuals the text treatment their roles require.
- **Theme-aware images** — Check readability against light and dark backgrounds and provide variants when needed.
- **Text equivalent for a chart or diagram** — Put essential values, conclusions, or relationships in surrounding text.

[GitHub diagram support](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) · [W3C WAI image guidance](https://www.w3.org/WAI/tutorials/images/) · [Pinned AlderVale visual example](https://github.com/vixttha/AlderVale-Pact-of-Ten/blob/a6c2060b8175f505cc6327ccb5658cc00a458b24/README.md)

## Quickstart and adoption

Get a reader to a first meaningful action.

- **One prominent first action** — Lead with a recognizable task such as play, try, install, or adopt.
- **Prerequisites next to the task** — Name tools, versions, access, and prior setup before any commands depend on them.
- **Set a time and cost expectation before setup** — State how long the example usually takes and whether it can create billable resources, with a link to current terms when pricing depends on an account or provider. AWS examples show [an estimated duration](https://docs.aws.amazon.com/hands-on/latest/setup-environment/setup-environment.html) and [a cost label](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/tutorial-launch-my-first-ec2-instance.html).
- [Write a copyable Quickstart](techniques/copyable-quickstart.md) — Give readers ordered commands they can paste into the supported shell.
- **Separate platform commands** — Label POSIX and PowerShell paths where their commands differ.
- **Installation methods** — Distinguish packages, installers, source builds, and other supported options.
- **Describe what the installer changes** — Tell readers where binaries or files are installed, which persistent user settings change, and what supported option controls those changes. uv documents its installation directory and shell-profile behavior. [uv installer options](https://docs.astral.sh/uv/reference/installer/)
- **Label ownership of installation channels** — Identify who maintains and supports each package or installer so readers know where to report installation problems. GitHub CLI links community-supported routes separately. [GitHub CLI installation links](https://github.com/cli/cli/blob/f24a94ffcb8c344ed5db0e4fb9a4d1fffd42c256/README.md#L33-L58) · [Linux package maintainers](https://github.com/cli/cli/blob/f24a94ffcb8c344ed5db0e4fb9a4d1fffd42c256/docs/install_linux.md#L186-L222)
- **Starting directory and checkout** — State where commands begin and which revision or project root they expect.
- **Safe configuration example** — Use labeled placeholders and explain where values belong.
- **Show configuration precedence** — Explain which setting wins when flags, environment variables, configuration files, and defaults disagree. Give one concrete conflict example in the supporting reference. Terraform documents the order for root module input variables. [Terraform variable precedence](https://developer.hashicorp.com/terraform/language/values/variables#variable-definition-precedence)
- **Sample fixture or starter input** — Provide a small known input that readers can use immediately.
- **Guest or offline first run** — Offer a first-use path with minimal account or network dependencies when supported.
- **Offer an isolated trial command** — Give the reader a short way to try a tool without installing it into their project. State what runner is required and what can be cached. uv demonstrates a temporary tool environment with `uvx`. [uv README example](https://github.com/astral-sh/uv/blob/c99faeeeeb8318d874007b4c48635d009838c1a0/README.md#L147-L166) · [Environment and cache behavior](https://github.com/astral-sh/uv/blob/c99faeeeeb8318d874007b4c48635d009838c1a0/docs/concepts/tools.md#L10-L38)
- **Link directly to a project-configured workspace** — Point readers to a preconfigured development workspace tied to the repository and intended branch. State what account or local tooling it needs. GitHub Codespaces and VS Code Dev Containers document repository links for this. [Codespaces deep links](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/setting-up-your-repository/facilitating-quick-creation-and-resumption-of-codespaces) · [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/create-dev-container)
- **Prerequisite or installation check** — Show a fast way to check that the local environment is ready before the demo.
- **Copy-in or template adoption path** — Identify what to copy, where it goes, and how to check the resulting project.
- **Upgrade or migration route** — Name the starting version, intended destination, and relevant migration guide.
- **Cleanup or reset instructions** — Show how a reader can leave a temporary demo or restore a clean starting point.
- **Preview changes before applying them** — When a workflow changes state and offers a preview, give the preview and apply steps distinct labels. Explain which changes the preview can predict. Terraform documents its plan separately from apply. [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan) · [Ansible check mode limits](https://docs.ansible.com/projects/ansible/latest/playbooks_checkmode.html)

[Google code-sample guidance](https://developers.google.com/style/code-samples) · [Pinned BART Quickstart](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/blob/3e7f9e02e61739825b56bcafecebbd0221cc9657/README.md) · [Pinned template adoption guide](https://github.com/vixttha/Brand-Identity-Template/blob/87d0f9aedbe69ca4b16815d6b3329efcf5889da9/README.md)

## First result and recovery

Help the reader recognize success and get unstuck.

- [Show a recognizable first result](techniques/first-success-milestone.md) — Tell the reader what success looks like immediately after the first real task.
- **Expected output contract** — Separate stable result fields from variable example values when exact comparison matters.
- **Document the scripting interface** — Show where scripts can find structured output and which outcomes return which exit codes. Include command-specific exceptions when they affect automation. GitHub CLI documents both formatting and exit behavior. [GitHub CLI output formatting](https://cli.github.com/manual/gh_help_formatting) · [Exit codes](https://cli.github.com/manual/gh_help_exit-codes) · [Authentication status exception](https://cli.github.com/manual/gh_auth_status)
- **Save or persistence checkpoint** — Tell readers what should survive a restart and how to confirm it.
- **First successful result link** — Point to the file, page, or artifact the task created so it is easy to inspect.
- **Next action after success** — Offer a natural second task once the first one works.
- **Recovery beside the failed step** — Put a common failure and its recovery close to the command or action that produces it.
- **Explain what happens when a step is repeated** — State whether repeating a command converges on the same result, resumes work, or creates another copy. Ansible’s module guide describes idempotency as a behavior that module authors should provide. Check the actual commands before promising it. [Ansible module behavior](https://docs.ansible.com/projects/ansible/latest/module_plugin_guide/modules_intro.html)
- **Diagnostic decision guide** — Route different symptoms to the relevant fix instead of listing generic troubleshooting.
- **Known limitations and workarounds** — State a known constraint and the currently supported path around it.
- **Explain defaults that change what readers see** — Name the input the tool omits or transforms by default, what a reader may miss, and how to change the behavior. ripgrep puts its default exclusions near its opening description. [ripgrep default search scope](https://github.com/BurntSushi/ripgrep/blob/16f9b2e64a42c43a469f72260226a6c65a4c88b9/README.md#L1-L9)

[Pinned Veraphify result example](https://github.com/vixttha/Veraphify/blob/88d5d08cd8c80de3927858685878e51b6d7c69b8/README.md) · [README HQ registry](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/techniques/registry.json)

## Navigation and accessibility

Get readers to the right information with minimal scanning.

- [Route by reader task](techniques/role-based-entry-points.md) — Give distinct reader goals clear routes from the same homepage.
- [Relative navigation](techniques/relative-navigation.md) — Link same-checkout guides and assets with paths relative to the Markdown file.
- **Descriptive link labels** — Use text that tells the reader where the link goes or what it does.
- **Clear heading hierarchy** — Organize sections in a predictable structure for visual scanning and assistive navigation. [Google heading structure guidance](https://developers.google.com/style/headings)
- **Table of contents or jump links** — Expose major sections when the page is long enough to need them.
- **Section deep links** — Send the reader to the relevant part of a guide and recheck anchors when headings change.
- **Send readers to docs for their installed version** — Label stable and development docs links so readers can match them to the version they are using. A branch README can link multiple editions if its audience spans supported releases. [Read the Docs version routing](https://docs.readthedocs.com/platform/stable/versions.html) · [Godot’s development docs notice](https://docs.godotengine.org/en/latest/getting_started/step_by_step/index.html)
- **Progressive disclosure** — Collapse optional details or move them to a clearly labeled supporting document. [GitHub collapsed sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections)
- **Use labeled callouts at the point of action** — Use short labeled notices for important context or consequences beside the relevant step. Keep essential information readable in plain text when the renderer handles callouts differently. [GitHub alerts](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts) · [Google’s notice guidance](https://developers.google.com/style/notices)
- **Separate guide types** — Route readers to a tutorial, how-to, reference, or explanation according to their task.
- **Give each public package its own README entry point** — Put a short orientation in the package directory so someone entering through a deep link can find its purpose, setup, and supporting docs. Google’s README guide calls this out for package directories. [Google’s package README guidance](https://github.com/google/styleguide/blob/8bdadbb0732b387aaa26f553dd9033484d1a2071/docguide/READMEs.md#L30-L55)
- **Concise comparison table** — Present repeated choices in a table when readers need to compare the same attributes.
- **Language routing** — Link translated docs and make the expected language clear.
- **Track the source revision of translations** — Link a translated README to its original and record which revision or release it follows. This lets maintainers identify what needs updating and readers find the source text when needed. Kubernetes documents its upstream-first translation workflow. [Kubernetes localization workflow](https://kubernetes.io/docs/contribute/localization/)
- **Task-local help link** — Put the relevant support path beside a high-friction step.
- **Consistent terms** — Use the same names for actions and objects as the code, UI, and linked instructions.

[GitHub README and section links](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) · [W3C accessible writing](https://www.w3.org/WAI/tips/writing/) · [Diátaxis documentation types](https://diataxis.fr/start-here/)

## Verification and trust

Make public claims traceable and scoped.

- [Execute the documented walkthrough](techniques/exact-revision-walkthrough.md) — Replay the reader’s published steps at the named revision and verify the result.
- **Turn examples into regression tests** — Generate test cases from examples in the maintained documentation source so changing an example also changes what gets tested. jq’s docs README describes the process and its Makefile connects manual examples to the test suite. [jq docs README](https://github.com/jqlang/jq/blob/5c001b18d7237cce1fdba63608732163f978dd23/docs/README.md#L1-L22) · [jq test-generation rule](https://github.com/jqlang/jq/blob/5c001b18d7237cce1fdba63608732163f978dd23/Makefile.am#L154-L170) [Python doctest documentation](https://docs.python.org/3/library/doctest.html)
- [Permanent proof links](techniques/permanent-proof-links.md) — Keep verification traceable with a commit-pinned receipt and recorded run, attempt, artifact ID, and digest.
- [Label the scope of compatibility evidence](techniques/claim-scope-labels.md) — State the version, platform, capability, and checks that support a compatibility claim.
- **Declared versus observed checks** — Show which checks were required and which actually ran, passed, failed, or were skipped.
- **Published release link** — Give a direct path to the release named in the README and its release notes.
- **Artifact verification instructions** — Explain how to compare a downloaded artifact with its recorded digest.
- **Show how to verify the artifact’s producer** — Where a release provides a signed attestation, show how to verify it against the expected repository or workflow. This lets readers check build origin as well as artifact identity. [GitHub build provenance and verification](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations#verifying-artifact-attestations-with-the-github-cli)
- **Combined-commit proof** — Tie a merge-readiness claim to tests on the exact combined content.
- **Lightweight link verification** — Check that critical relative targets and anchors resolve at the claimed revision.
- **Publication-path verification** — Test links and assets from the path where the README will actually ship. The Python Packaging User Guide also runs this check against the built distribution. [PyPI rendering check](https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/)
- **Verify which README appears on the repository homepage** — When multiple eligible README files exist, check which one the host surfaces and publish the expected content there. GitHub checks `.github/`, the repository root, and `docs/` in that order. [GitHub README display order](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- **Rendered review at two widths** — Check the landing page on wide and narrow layouts for overflow or unreadable content.
- **Benchmark method and scope** — Describe the workload, environment, revision, and units beside a performance result.
- **Show a benchmark case that changes the takeaway** — Beside a favorable result, include a reproducible workload or flag change that reduces the advantage or changes performance. ripgrep shows performance cliffs and cases with many matches. [ripgrep performance caveats](https://github.com/BurntSushi/ripgrep/blob/16f9b2e64a42c43a469f72260226a6c65a4c88b9/README.md#L77-L114)
- **Clean consumer adoption test** — Verify documented copy-in or install steps in a fresh consumer project.
- **Snapshot source identity** — Record the origin and digest of frozen README or asset bytes when exact archival identity matters.

[GitHub file permalinks](https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files) · [GitHub artifact validation](https://docs.github.com/en/actions/tutorials/store-and-share-data#validating-artifacts) · [Pinned audit receipt](https://github.com/vixttha/README-HQ/blob/2f66dd6aa23928716f645cfebdce462b7574c4b3/audit/evidence/v0.0.6.67-full-stack.json) · [README HQ registry](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/techniques/registry.json)

## Handoff and maintenance

Help the next owner, contributor, or agent take responsibility for the project.

- [Link authoritative agent instructions](techniques/agent-instruction-pointer.md) — Point an agent to the repository’s applicable instructions from the README.
- **Developer entry point** — Link the source layout, setup, and shortest routine development check.
- **Contribution route** — Point to contribution rules, issue templates, and where work is reviewed. [Open Source Guides](https://opensource.guide/starting-a-project/)
- **Recognize contribution types beyond code** — Label what people contributed, such as documentation, design, translation, or testing, in the README or linked credits. The All Contributors specification describes these recognitions and a generated contributor table. [All Contributors specification](https://allcontributors.org/en/project/specification/requirements/)
- **Explain where project decisions are made** — Link a project’s governance and identify who makes major decisions. Give proposals a route when that route differs from submitting a patch. Kubernetes’s steering README describes its decision-making scope and links its charter. [Pinned Kubernetes steering README](https://github.com/kubernetes/community/blob/e1963fc0dd9debd04690163f50a6178e278b9779/committee-steering/README.md#L9-L15)
- **Support and issue route** — Tell readers where to report a bug or ask for help and what evidence to include.
- **License and reuse link** — Point to the actual terms and distinguish project assets with different terms.
- **Attribution and data provenance** — Link the source and terms for material external assets or datasets.
- **Include a data dictionary for shared datasets** — Explain file relationships, field names, units, and missing-value codes so another person can interpret the data. Link the full dictionary when it needs its own file. [Cornell’s research-data README guide](https://data.research.cornell.edu/data-management/sharing/readme/)
- **Security reporting route** — Link the project’s supported private disclosure process when applicable.
- **Citation instructions** — Point researchers to the maintained citation metadata where appropriate.
- **Changelog and version navigation** — Show where release history lives and which version the reader is viewing.
- **Identify the source of truth when repositories are mirrored** — Name the canonical repository and explain which revision identifiers to cite from a mirror. SQLite’s GitHub README points to Fossil and tells readers where to find the official check-in name. [SQLite mirror guidance](https://github.com/sqlite/sqlite/blob/28c1e4669d7649506c5bf640f62ce3abfc0114fa/README.md#L15-L29) [Kubernetes’s published staging repositories](https://github.com/kubernetes/kubernetes/blob/dee14a0ede00099d6441a8991ad6137b938d2a9d/staging/README.md#L1-L16)
- **Turn an archived README into a handoff** — Put the maintained successor and new project name, if any, at the top of the archive. State what remains accessible at the old location. Prisma Next explains its move and archive status before its historical README content. [Prisma Next archive handoff](https://github.com/prisma/prisma-next/blob/55458c441d2cf452028c22eed21370447720840a/README.md#L1-L10)
- **Human guide for a structured inventory** — Pair a machine-readable manifest with an explanation of its reader-facing purpose.
- **Generate repetitive README sections from their source** — Generate sections such as configuration inputs or outputs from their authoritative definitions. Bound generation with file markers so authored explanations stay editable. terraform-docs documents an injected section between comments. [terraform-docs output injection](https://terraform-docs.io/user-guide/configuration/output/#inject)
- **Reuse a README as the package listing** — Wire the maintained README into package metadata so package users see the same introduction in their registry. Check the description from the built package and resolve links in the target renderer. [PyPI packaging guide](https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/) · [Cargo manifest README field](https://doc.rust-lang.org/cargo/reference/manifest.html#the-readme-field)
- **Expose discovery metadata through the README** — Use host-supported metadata for fields such as dataset language, license, tags, and file layout. Hugging Face renders a dataset README as a card and uses its YAML fields for discovery and configuration. [Hugging Face dataset cards](https://huggingface.co/docs/hub/datasets-cards)
- **Independent version lines** — Name the product, README, or collection beside each version when their release lines differ.
- **Versioned section map** — Provide a path to find corresponding sections across archived READMEs.
- **Draft, archive, and publication stages** — Keep proposed text, frozen snapshots, and the published default-branch README distinguishable.

[GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) · [Pinned Brand Identity Template](https://github.com/vixttha/Brand-Identity-Template/blob/87d0f9aedbe69ca4b16815d6b3329efcf5889da9/README.md) · [README HQ registry](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/techniques/registry.json)

## Expand the map

Search titles and aliases before adding an entry. Reuse the existing record ID when the reader problem and the practice already match. Record a new technique when it does a distinct job. The [research guide](RESEARCH.md) explains how to move a candidate into the catalog.
