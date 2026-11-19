# README HQ source and plan audit

The fixtures use the [v0.0.6 baseline](https://github.com/vixttha/README-HQ/commit/f50e3749dab90ddfe35894284d1660097a1fb1a8), the [learning pilot](https://github.com/vixttha/README-HQ/commit/a8d97d0559853538d4d814edf5c998e42cfec3d2), and the [49-checkpoint plan](https://github.com/vixttha/README-HQ/commit/7b3cf8b569f20474152e134f23c5d56f538f089d). The audit runs the shipped CLI, the Graphify compiler and MCP service, the learning verifier, and the exact plan workflow command in disposable repositories.

| Fixture | Baseline behavior |
| --- | --- |
| I50 | The 49-checkpoint workflow passes after an unrelated checkpoint label, change anchor, and test fixture are written into matching Graphify artifacts. |
| I51 | The README checker and plan verification pass when the plan index links to a nonexistent graph. |
| I52 | A clean checkout with core.autocrlf enabled passes README validation and fails the Graphify catalog comparison. [Git working-tree conversion](https://git-scm.com/docs/gitattributes#_end_of_line_conversion) |
| I53 | A local Git replacement ref changes the cited document and digest while the standalone Graphify receipt still reports the original commit and a successful MCP result. [Git replacement behavior](https://git-scm.com/docs/git-replace) |
| I54 | Graphify accepts a plain path and rejects an otherwise equivalent legal path containing bracketed relation text. |
| I55 | The learning verifier accepts symbolic HEAD as exact evidence before and after it moves to a different source commit with unchanged README contents. [Git revision syntax](https://git-scm.com/docs/gitrevisions) |

A successful audit run means the listed failures were reproduced. Each repair requires its own candidate verification. These fixtures measure evidence and plan integrity. Cross-project reliability and README quality still require held-out evaluation.
