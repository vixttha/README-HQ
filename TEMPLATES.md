# Record templates

Copy the relevant section into a Markdown file under `techniques/<stable-id>.md` or `combinations/<stable-id>.md`. Use a lowercase slug with hyphens for the filename and ID. Reuse the technique ID when adding evidence for the same practice. Identify the kind by its directory. Link each reviewed record from the [library index](README.md).

From the root index, link to a technique with `[Relative navigation](techniques/relative-navigation.md)`. From a combination record, link to that same technique with `[Relative navigation](../techniques/relative-navigation.md)`. These paths are examples to adapt once the record exists.

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
