# README HQ rendered navigation audit

The offline tests run the original checker at [README HQ v0.0.6](https://github.com/vixttha/README-HQ/commit/f50e3749dab90ddfe35894284d1660097a1fb1a8). The rendering check compares GitHub's directory README API and actual rendered HTML with the pinned source file and fixture blobs. Graphify compiles exact document, change, and test references for both findings and verifies them over MCP.

| Fixture | Observed behavior |
| --- | --- |
| N66 | The offline checker passes nonexistent fragments on a directory landing page and a .markdown file. It rejects the same absent fragment on a direct .md link. GitHub renders the existing directory and alternate-file anchors. [Directory README API](https://docs.github.com/en/rest/repos/contents#get-a-repository-readme-for-a-directory) · [GitHub markup types](https://github.com/github/markup#markups) |
| N67 | The checker rejects GitHub's documented HTML named-anchor syntax as a destination. GitHub renders that target, and an ordinary generated heading in the same file passes the checker. [GitHub custom anchors](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#custom-anchors) |

The controls compare specific GitHub navigation targets and exact evidence lines. The audit does not score end-to-end adoption or README editorial quality.
