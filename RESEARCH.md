# Research guide

Start with the [library index](README.md). Use this process when someone supplies repositories to research or when the library needs more evidence for a particular reader task.

1. **Define the reader task.** Record the intended audience and the outcome you want to see. Review the supplied repositories for that task.
2. **Pin each source.** Resolve the repository and revision. Record the actual README or guide, its file path, and the section or lines. Link to the commit-specific source. Record inaccessible or unavailable sources in the review log.
3. **Extract the practice.** Describe the reader problem, what the README does, and the outcome it aims for. Include project type and limits. Prefer a brief original example or a source link.
4. **Check what you can.** A source inspection supports an observed practice. An execution or navigation check supports only the result you actually observed. For an execution check, record the revision, environment, exact reader action, expected and observed result, and evidence link. Preserve the workflow run, attempt, artifact ID, and digest when they are available.
5. **Deduplicate and publish the finding.** Compare the reader problem, practice, and expected outcome with the [existing records](README.md#techniques-by-reader-task). Add a source or alias to a matching technique. Use a [new record](TEMPLATES.md#technique-record) for a distinct practice. Use a [combination record](TEMPLATES.md#combination-record) when several techniques support one reader task.

When bringing over an existing README HQ technique, keep its registry ID and link to the source revision used. Use paths relative to this branch for its own documents. Use immutable links for claims about other revisions. Share only sources and evidence that can be published in this public repository.

## Research batch log template

**Reader task** [Task and audience]  
**Scope** [Repositories requested, date, and selection rationale]  
**Coverage** [Repositories requested, inspected, checked for the task, and unavailable. Report the counts independently.]

| Repository and revision | README or guide | Technique or combination ID | Finding and evidence status |
| --- | --- | --- | --- |
| [Repo and SHA] | [Pinned file and section] | [Existing or proposed ID] | [Observation, verified result, or reason review was incomplete] |

**Gaps and disagreements.** [Platforms, project types, unavailable sources, inconsistent outcomes, and checks still needed.]
