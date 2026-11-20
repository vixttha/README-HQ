<!-- catalog
{
  "title": "Offer an isolated trial command",
  "summary": "Give the reader a short way to try a tool without installing it into their project.",
  "tasks": [
    "quickstart"
  ],
  "tags": [
    "onboarding",
    "environment"
  ],
  "aliases": [
    "temporary test environment"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "A trial can be disposable while installation changes persistent state."
}
-->

# Offer an isolated trial command

**Use when.** A trial can be disposable while installation changes persistent state.

**Reader task.** Quickstart and adoption.

**Practice.** Give the reader a short way to try a tool without installing it into their project. State what runner is required and what can be cached. uv demonstrates a temporary tool environment with `uvx`.

**Example (illustrative).** Run the trial in a temporary directory or disposable container with the example input.

**Result to check.** The trial can be repeated and leaves the documented project state intact.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [uv README example](https://github.com/astral-sh/uv/blob/c99faeeeeb8318d874007b4c48635d009838c1a0/README.md#L147-L166) · [Environment and cache behavior](https://github.com/astral-sh/uv/blob/c99faeeeeb8318d874007b4c48635d009838c1a0/docs/concepts/tools.md#L10-L38)
