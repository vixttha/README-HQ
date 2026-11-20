# README Technique Library

A field guide to reusable README techniques. Find a technique for a reader task, see where it was observed or verified, and compare combinations that solve a larger problem.

## v0.0.1 baseline

The [frozen 144-technique map](https://github.com/vixttha/README-HQ/blob/059f5fb4d1c0c738736f9050a016dc8e46b46178/TECHNIQUE-MAP.md) defines the v0.0.1 roster. The [version manifest](versions/v0.0.1.json) lists those 144 stable IDs and the original commit. The records on this branch provide expanded learning material for the same roster. The map also shows later research candidates awaiting learning records.

## Find and learn a technique

1. Start with a reader task or use-case phrase. Use the [JSON index](catalog/index.json), [task pages](catalog/README.md), or offline search below. The JSON index lists titles, IDs, aliases, tags, use cases, evidence status, and paths relative to this branch’s root.
2. Open the linked Markdown record. Read **Use when**, **Practice**, and **Example** to decide what applies to the project.
3. Use **Result to check** to verify the adaptation against the target project. Read **Evidence** for the limits of what the library establishes.

## Browse or search

- [Explore the full technique map](TECHNIQUE-MAP.md) for individual practices and later research candidates.
- [Browse by reader task](catalog/README.md) to see techniques and ordered combinations. The JSON index distinguishes their `kind` values.
- [Find a title, alias, ID, or tag](catalog/search.md) using your browser’s Find command. Large lists show page links. [Retired records](catalog/retired.md) have their own finder.
- Search a checkout with Python 3.12 or newer. Add `--json` for structured output.

```sh
python tools/catalog.py search "proof links" --task verification
python tools/catalog.py search "backup restore test" --kind technique --limit 5 --json
python tools/catalog.py search --kind combination --tag quickstart --limit 25 --offset 25 --json
```

Search matches word prefixes across titles, IDs, aliases, tags, summaries, and use cases, without regard to case or accents. All query words must match. Exact titles, IDs, and aliases rank first. Filter by task, kind, tag, evidence, or status. Search defaults to active records, and `--status all` includes retired entries.

## Maintain the catalog

Use the [research guide](RESEARCH.md) to gather evidence and the [record templates](TEMPLATES.md) to add or update an entry. Each technique or combination has one Markdown record. The generated indexes list it under every relevant reader task.

Commit the record files. GitHub Actions validates them and refreshes the browser indexes on this branch automatically. The record files are the source for search, and the generated index commit follows when the checks pass.

For a local preview, run `python tools/catalog.py build`. Run `python tools/catalog.py check` to detect invalid metadata, duplicate IDs or search names, missing technique steps, and stale indexes.

## How to read the evidence

| Status | Meaning |
| --- | --- |
| Observed | The technique appears in a pinned source. Its effect on the reader task still needs a check. |
| Verified | A named check was run at a stated revision and, where relevant, environment. Read the record for the result and whether it passed. |
| Unverified | The research or check is incomplete. The record says what is missing. |

Use the scope and limitations in each record to judge whether it transfers to your project.
