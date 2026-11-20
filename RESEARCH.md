# Research guide

Start with the [technique map](TECHNIQUE-MAP.md) and search the [existing catalog](catalog/search.md). Use this process when someone supplies repositories to research or when the library needs more evidence for a particular reader task.

1. **Define the reader task.** Record the intended audience and the outcome you want to see. Review the supplied repositories for that task.
2. **Pin each source.** Resolve the repository and revision. Record the actual README or guide, its file path, and the section or lines. Link to the commit-specific source. Record inaccessible or unavailable sources in the review log.
3. **Extract the practice.** Describe the reader problem, what the README does, and the outcome it aims for. Include project type and limits. Prefer a brief original example or a source link.
4. **Check what you can.** A source inspection supports an observed practice. An execution or navigation check supports only the result you actually observed. Record discovery, execution, and handoff separately when they apply. For execution, record the revision, environment, exact reader action, expected and observed result, and evidence link. A failed check is evidence of a failure and cannot support a success claim. Preserve the workflow run, attempt, artifact ID, and digest when they are available.
5. **Deduplicate and publish the finding.** Compare the reader problem, practice, and expected outcome with the [existing records](catalog/search.md). Add a source or alias to a matching technique. Use a [new record](TEMPLATES.md#technique-record) for a distinct practice. Use a [combination record](TEMPLATES.md#combination-record) when several techniques support one reader task.

When bringing over an existing README HQ technique, keep its registry ID and link to the source revision used. To retire a record, set its status to `retired` and update or retire any active combinations that depend on it. The next successful catalog refresh moves the retired entry into its archive. Use paths relative to this branch for its own documents. Use immutable links for claims about other revisions. Share only sources and evidence that can be published in this public repository.

## Research batch log template

**Reader task** [Task and audience]  
**Scope** [Repositories requested, date, and selection rationale]  
**Coverage** [Repositories requested, inspected, checked for the task, and unavailable. Report the counts independently.]

| Repository and revision | README or guide | Technique or combination ID | Finding and evidence status |
| --- | --- | --- | --- |
| [Repo and SHA] | [Pinned file and section] | [Existing or proposed ID] | [Observation, verified result, or reason review was incomplete] |

**Gaps and disagreements.** [Platforms, project types, unavailable sources, inconsistent outcomes, and checks still needed.]

## Research coverage

One cross-domain pass broadened the [technique map](TECHNIQUE-MAP.md) from 86 to 108 practices. It compared public examples and primary guidance across onboarding, configuration, recovery, verification, publishing, accessibility, localization, governance, and research data.

- Later searches for captions, page headings, collapsible sections, artifact retention, and executable examples confirmed existing practices. The map links relevant sources under those entries.
- The final search across research repositories added a data dictionary and host-readable discovery metadata. That search also surfaced reproducibility and attribution guidance already covered by earlier entries.
- The new entries describe observed documentation mechanisms and how to adapt them. Separate execution checks establish whether a practice works in a specific project.

For future saturation reviews, record which source families were searched, which plausible additions matched existing entries, and any areas left open. This approach shows what the pass covered and makes later research easier to target.

### Hardware, games, integrations, and research artifacts

A specialist pass expanded the [technique map](TECHNIQUE-MAP.md) from 108 to 120 practices. It compared OSHWA and QMK guidance, game READMEs and control accessibility guidance, service sandboxes, GitHub Actions documentation, teaching material, and scientific artifact evaluation guides.

- The hardware and games sources contributed parts lists, revision-specific firmware, editable design files, control mapping, separately distributed assets, and saved-data compatibility.
- Service and automation documentation contributed sandbox setup, caller permissions, and examples of downstream consumers. Research and teaching sources contributed separate smoke and full runs, reproducible claim mapping, and exercises with worked solutions.
- The closing cross-check revisited keyboard setup, game launch, action inputs and outputs, lesson structure, and Markdown rendering. Those examples fit techniques already in the map. The map retains useful source links under those entries.

The result records qualitative coverage of the public sources surveyed. A statistical completeness estimate would require a defined corpus and independent classification.

### APIs, service startup, file conversion, and accessible examples

A focused pass expanded the [technique map](TECHNIQUE-MAP.md) from 120 to 134 practices. The sources included API standards and consumer guides, container quickstarts, extension activation reference, file-conversion documentation, asset inventories, notebook hosts, and accessibility testing guidance.

- The API sources covered versioned interface contracts, reusable request collections, page traversal, automatic retries, event delivery, and replacement timelines for deprecated interfaces.
- The other sources covered local service addresses and readiness, extension activation, conversion fidelity, published asset names, notebook preview and execution links, labels that communicate without color, and keyboard checks on rendered READMEs.
- Closing checks in Microsoft’s API docs, Docker labs, Material Icons, W3C accessibility guidance, and GitHub notebook documentation produced further examples of these mechanisms. The map records concrete examples under the relevant entries.

This pass used source comparison and deduplication. The count describes documented practices in the map and supports a qualitative judgment about diminishing returns within the sampled source families.
