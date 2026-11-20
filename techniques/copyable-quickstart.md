<!-- catalog
{
  "title": "Write a copyable Quickstart",
  "summary": "Give readers ordered commands they can paste into the supported shell.",
  "tasks": [
    "quickstart"
  ],
  "tags": [
    "commands",
    "onboarding"
  ],
  "aliases": [
    "copy-paste quickstart",
    "runnable command block"
  ],
  "evidence": "observed",
  "status": "active"
}
-->

# Write a copyable Quickstart

**Problem.** Readers can mistake shell prompts, expected output, and descriptive placeholders for commands.

**Practice.** State prerequisites and the starting directory before the block. Put executable input in a fenced block with the right language. Place example output separately and explain any placeholders the reader must replace.

**Example.** The pinned BART README gives common clone and setup steps, then separate executable blocks for PowerShell and POSIX shells.

**Limits.** Test each advertised shell separately. An interactive example may need one step per block when a reader has to respond between commands.

**Result to check.** Copy the block exactly into the documented shell and confirm the action runs from the declared starting directory.

**Evidence.** Observed in the cited guidance or example. [Google’s code-sample guidance](https://developers.google.com/style/code-samples) · [Pinned BART Quickstart](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/blob/3e7f9e02e61739825b56bcafecebbd0221cc9657/README.md#quick-start)
