# README technique map

This map groups individual techniques by the job they do for a reader or maintainer. Linked techniques have a catalog record. Plain entries describe candidates for later research and may need stronger evidence before they get a record.

A technique belongs wherever its behavior helps. This map gives each one a primary home for browsing. The searchable catalog can list a single record under more than one task.

## Purpose and audience

Help readers decide whether they’re in the right place.

- [State the project’s purpose](techniques/project-purpose-statement.md) — Tell a new reader what the project does and what they can accomplish with it.
- **Audience and use cases** — Name the people and jobs the project serves.
- **Value proposition** — Explain the practical payoff or problem the project removes.
- **Project status and maturity** — Distinguish a preview, stable release, or archived project.
- **Capabilities at a glance** — Show the few important things readers can do today.
- **Scope boundaries** — Call out material limitations or environments outside the supported scope.
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
- **Captioned video walkthrough** — Demonstrate a longer workflow with captions or a transcript.
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
- [Write a copyable Quickstart](techniques/copyable-quickstart.md) — Give readers ordered commands they can paste into the supported shell.
- **Separate platform commands** — Label POSIX and PowerShell paths where their commands differ.
- **Installation methods** — Distinguish packages, installers, source builds, and other supported options.
- **Starting directory and checkout** — State where commands begin and which revision or project root they expect.
- **Safe configuration example** — Use labeled placeholders and explain where values belong.
- **Sample fixture or starter input** — Provide a small known input that readers can use immediately.
- **Guest or offline first run** — Offer a first-use path with minimal account or network dependencies when supported.
- **Prerequisite or installation check** — Show a fast way to check that the local environment is ready before the demo.
- **Copy-in or template adoption path** — Identify what to copy, where it goes, and how to check the resulting project.
- **Upgrade or migration route** — Name the starting version, intended destination, and relevant migration guide.
- **Cleanup or reset instructions** — Show how a reader can leave a temporary demo or restore a clean starting point.

[Google code-sample guidance](https://developers.google.com/style/code-samples) · [Pinned BART Quickstart](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/blob/3e7f9e02e61739825b56bcafecebbd0221cc9657/README.md) · [Pinned template adoption guide](https://github.com/vixttha/Brand-Identity-Template/blob/87d0f9aedbe69ca4b16815d6b3329efcf5889da9/README.md)

## First result and recovery

Help the reader recognize success and get unstuck.

- [Show a recognizable first result](techniques/first-success-milestone.md) — Tell the reader what success looks like immediately after the first real task.
- **Expected output contract** — Separate stable result fields from variable example values when exact comparison matters.
- **Save or persistence checkpoint** — Tell readers what should survive a restart and how to confirm it.
- **First successful result link** — Point to the file, page, or artifact the task created so it is easy to inspect.
- **Next action after success** — Offer a natural second task once the first one works.
- **Recovery beside the failed step** — Put a common failure and its recovery close to the command or action that produces it.
- **Diagnostic decision guide** — Route different symptoms to the relevant fix instead of listing generic troubleshooting.
- **Known limitations and workarounds** — State a known constraint and the currently supported path around it.

[Pinned Veraphify result example](https://github.com/vixttha/Veraphify/blob/88d5d08cd8c80de3927858685878e51b6d7c69b8/README.md) · [README HQ registry](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/techniques/registry.json)

## Navigation and accessibility

Get readers to the right information with minimal scanning.

- [Route by reader task](techniques/role-based-entry-points.md) — Give distinct reader goals clear routes from the same homepage.
- [Relative navigation](techniques/relative-navigation.md) — Link same-checkout guides and assets with paths relative to the Markdown file.
- **Descriptive link labels** — Use text that tells the reader where the link goes or what it does.
- **Clear heading hierarchy** — Organize sections in a predictable structure for visual scanning and assistive navigation.
- **Table of contents or jump links** — Expose major sections when the page is long enough to need them.
- **Section deep links** — Send the reader to the relevant part of a guide and recheck anchors when headings change.
- **Progressive disclosure** — Collapse optional details or move them to a clearly labeled supporting document.
- **Separate guide types** — Route readers to a tutorial, how-to, reference, or explanation according to their task.
- **Concise comparison table** — Present repeated choices in a table when readers need to compare the same attributes.
- **Language routing** — Link translated docs and make the expected language clear.
- **Task-local help link** — Put the relevant support path beside a high-friction step.
- **Consistent terms** — Use the same names for actions and objects as the code, UI, and linked instructions.

[GitHub README and section links](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) · [W3C accessible writing](https://www.w3.org/WAI/tips/writing/) · [Diátaxis documentation types](https://diataxis.fr/start-here/)

## Verification and trust

Make public claims traceable and scoped.

- [Execute the documented walkthrough](techniques/exact-revision-walkthrough.md) — Replay the reader’s published steps at the named revision and verify the result.
- [Permanent proof links](techniques/permanent-proof-links.md) — Keep verification traceable with a commit-pinned receipt and recorded run, attempt, artifact ID, and digest.
- [Label the scope of compatibility evidence](techniques/claim-scope-labels.md) — State the version, platform, capability, and checks that support a compatibility claim.
- **Declared versus observed checks** — Show which checks were required and which actually ran, passed, failed, or were skipped.
- **Published release link** — Give a direct path to the release named in the README and its release notes.
- **Artifact verification instructions** — Explain how to compare a downloaded artifact with its recorded digest.
- **Combined-commit proof** — Tie a merge-readiness claim to tests on the exact combined content.
- **Lightweight link verification** — Check that critical relative targets and anchors resolve at the claimed revision.
- **Publication-path verification** — Test links and assets from the path where the README will actually ship.
- **Rendered review at two widths** — Check the landing page on wide and narrow layouts for overflow or unreadable content.
- **Benchmark method and scope** — Describe the workload, environment, revision, and units beside a performance result.
- **Clean consumer adoption test** — Verify documented copy-in or install steps in a fresh consumer project.
- **Snapshot source identity** — Record the origin and digest of frozen README or asset bytes when exact archival identity matters.

[GitHub file permalinks](https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files) · [GitHub artifact validation](https://docs.github.com/en/actions/tutorials/store-and-share-data#validating-artifacts) · [Pinned audit receipt](https://github.com/vixttha/README-HQ/blob/2f66dd6aa23928716f645cfebdce462b7574c4b3/audit/evidence/v0.0.6.67-full-stack.json) · [README HQ registry](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/techniques/registry.json)

## Handoff and maintenance

Help the next owner, contributor, or agent take responsibility for the project.

- [Link authoritative agent instructions](techniques/agent-instruction-pointer.md) — Point an agent to the repository’s applicable instructions from the README.
- **Developer entry point** — Link the source layout, setup, and shortest routine development check.
- **Contribution route** — Point to contribution rules, issue templates, and where work is reviewed.
- **Support and issue route** — Tell readers where to report a bug or ask for help and what evidence to include.
- **License and reuse link** — Point to the actual terms and distinguish project assets with different terms.
- **Attribution and data provenance** — Link the source and terms for material external assets or datasets.
- **Security reporting route** — Link the project’s supported private disclosure process when applicable.
- **Citation instructions** — Point researchers to the maintained citation metadata where appropriate.
- **Changelog and version navigation** — Show where release history lives and which version the reader is viewing.
- **Human guide for a structured inventory** — Pair a machine-readable manifest with an explanation of its reader-facing purpose.
- **Independent version lines** — Name the product, README, or collection beside each version when their release lines differ.
- **Versioned section map** — Provide a path to find corresponding sections across archived READMEs.
- **Draft, archive, and publication stages** — Keep proposed text, frozen snapshots, and the published default-branch README distinguishable.

[GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) · [Pinned Brand Identity Template](https://github.com/vixttha/Brand-Identity-Template/blob/87d0f9aedbe69ca4b16815d6b3329efcf5889da9/README.md) · [README HQ registry](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/techniques/registry.json)

## Expand the map

Search titles and aliases before adding an entry. Reuse the existing record ID when the reader problem and the practice already match. Record a new technique when it does a distinct job. The [research guide](RESEARCH.md) explains how to move a candidate into the catalog.
