<!-- catalog
{
  "title": "Show a recognizable first result",
  "summary": "Tell the reader what success looks like immediately after the first real task.",
  "tasks": [
    "first-result",
    "quickstart",
    "demo"
  ],
  "tags": [
    "expected-output",
    "onboarding"
  ],
  "aliases": [
    "first-use milestone",
    "expected first output"
  ],
  "evidence": "observed",
  "status": "active",
  "use_when": "A quickstart produces output the reader must recognize before continuing."
}
-->

# Show a recognizable first result

**Use when.** A quickstart produces output the reader must recognize before continuing.

**Problem.** A setup or demo can finish without giving the reader a clear way to tell whether the project worked.

**Practice.** Put a concrete success signal directly after the first real action. Use a recognizable output line, file, screen, or milestone. Describe the stable part if IDs, files, or metrics can vary.

**Example.** Veraphify says that the CLI help lists `import`, `verify`, and `lookup`. The two-version example also provides recognizable file-and-line results.

**Limits.** For browser tasks, use a visible state such as a page heading or a saved result. For commands that create files, name or describe the file rather than relying only on exit status.

**Result to check.** Ask a first-time reader to identify the first successful outcome without being told what to look for.

**Evidence.** Observed in the cited guidance or example. [Pinned Veraphify README](https://github.com/vixttha/Veraphify/blob/88d5d08cd8c80de3927858685878e51b6d7c69b8/README.md#quickstart) · [Original README HQ registry](https://github.com/vixttha/README-HQ/blob/8d50caec2bc6fcb998994a1fd302294a029325f9/techniques/registry.json)
