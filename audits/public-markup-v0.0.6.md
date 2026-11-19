# README HQ public source markup audit

This audit uses the shipped Graphify compiler and version-map anchor selector at [README HQ v0.0.6](https://github.com/vixttha/README-HQ/commit/f50e3749dab90ddfe35894284d1660097a1fb1a8). It reads public Git objects at pinned commits. The probe points the existing selector at each source repository and supplies explicit anchors as a control for the same Graphify CLI. It reads source test definitions without running the projects' tests.

| Shipped README source | Automatic README anchor | Explicit anchors over Graphify MCP |
| --- | --- | --- |
| [Requests Markdown](https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/README.md) | Found | Passed |
| [Sphinx reStructuredText](https://github.com/sphinx-doc/sphinx/blob/035a07c32c3241fd3356f4d827800c1f88525272/README.rst) | No anchor found | Passed |
| [Asciidoctor AsciiDoc](https://github.com/asciidoctor/asciidoctor/blob/743f47d5e4d12049744e6d5236ad16cdfb6dca3d/README.adoc) | Selected a Gemfile comment | Passed |

- C63 compares common README formats in three public projects outside the README HQ learning pilot. GitHub's markup library lists all three formats. [GitHub markup support](https://github.com/github/markup#markups)
- C64 compares two exact headings in the same synthetic Markdown file. The heading with a Unicode emoji zero-width joiner is rejected, while the plain heading passes Graphify MCP. [Unicode emoji specification](https://www.unicode.org/reports/tr51/#Emoji_ZWJ_Sequences)
- C65 requests Requests v2.34.2 and observes the built-in selector preferring the unreleased placeholder on line 7 over the requested release section beginning at line 10. The normal compiler and MCP verifier accept the graph and the outline links to the placeholder. [Requests history](https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/HISTORY.md)

The sample was chosen to cover distinct formats. It measures anchor discovery and Graphify compilation. It cannot estimate overall README HQ adoption success or the editorial quality of generated READMEs.
