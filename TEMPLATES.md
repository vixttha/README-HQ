# Record templates

Save one record per lowercase, hyphenated ID as `techniques/<id>.md` or `combinations/<id>.md`. IDs, titles, and aliases must identify one record across both directories. Use tags for terms shared across records. Keep IDs stable when editing titles or adding evidence.

Start the file with the metadata comment below, then write the matching Markdown section. Set `tasks` to one or more IDs from the [task index](catalog/README.md). Use `observed`, `verified`, or `unverified` for evidence and `active` or `retired` for status.

```markdown
<!-- catalog
{
  "title": "Relative navigation",
  "summary": "Link readers to a guide shipped in the same checkout.",
  "tasks": ["navigation", "quickstart"],
  "tags": ["links", "onboarding"],
  "aliases": ["same-checkout links"],
  "evidence": "observed",
  "status": "active"
}
-->
```

For a combination, add a `"steps"` field to the same metadata object. For example, `"steps": ["relative-navigation", "expected-first-output"]` lists two technique IDs in reading order. Save both technique files before adding the combination. The generated task page links each step automatically.

From a combination record, link to a technique with `[Relative navigation](../techniques/relative-navigation.md)`. Change the filename to the technique’s real ID. The indexes refresh when the record reaches the library branch. See [catalog maintenance](README.md#maintain-the-catalog) for local preview commands.

## Technique record

### Technique title

**ID** `stable-slug`  
**Reader task** [What the reader wants to accomplish]  
**Use when** [Project types, prerequisites, or signals that make this useful]  
**Evidence summary** [Observed, verified, or unverified, with its scope]

**Problem.** [What slows down or misleads the reader?]

**Practice.** [What to change, in enough detail to reuse the technique.]

**Example.** [A small original example or a pinned source with a short explanation.]

**Limits and alternatives.** [When to adapt or skip it, and which audience, platform, or project type was covered.]

**Result to check.** [What the reader should be able to do after the change.]

| Source repository and pinned location | What it shows | Check and result | Status |
| --- | --- | --- | --- |
| [Repository, commit, file, and section or lines] | [Observed practice or claim] | [Method, expected and observed result, pass or fail, scope, and available evidence link] | [Observed, verified, or unverified for this claim] |

## Combination record

### Combination title

**ID** `stable-slug`  
**Reader task** [What the reader wants to accomplish]  
**Use when** [Audience, prerequisites, and applicable project types]

| Step | Linked technique ID | What it contributes | When to adapt or skip |
| --- | --- | --- | --- |
| 1 | [Technique ID] | [Contribution to the reader outcome] | [Condition] |

**Result to check.** [The exact reader path, starting point, and expected outcome.]

**Evidence.** [Catalog revision used, pinned sources for the whole route, observed result and scope, and CI run or retained receipt if available.]

**Limits.** [What was unchecked and where the combination has yet to be tried.]
