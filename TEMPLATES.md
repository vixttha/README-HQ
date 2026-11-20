# Record templates

Copy the relevant section into a Markdown file under `techniques/<stable-id>.md` or `combinations/<stable-id>.md`. Reuse an existing ID when adding evidence for the same practice. Link the new record from the [library index](README.md).

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
| [Repository, commit, file, and section or lines] | [Observed practice or claim] | [Method, expected and observed result, scope, and evidence link if available] | [Observed, verified, or unverified] |

## Combination record

### Combination title

**ID** `stable-slug`  
**Reader task** [What the reader wants to accomplish]  
**Use when** [Audience, prerequisites, and applicable project types]

| Step | Linked technique ID | What it contributes | When to adapt or skip |
| --- | --- | --- | --- |
| 1 | [Technique ID] | [Contribution to the reader outcome] | [Condition] |

**Result to check.** [The exact reader path, starting point, and expected outcome.]

**Evidence.** [Pinned sources for the whole route, observed result, scope, and CI run or retained receipt if available.]

**Limits.** [What was unchecked and where the combination has yet to be tried.]
