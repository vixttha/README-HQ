# README Technique Library

A field guide to reusable README techniques. Find a technique for a reader task, see where it was observed or verified, and compare combinations that solve a larger problem.

## Browse or search

- [Browse by reader task](catalog/README.md) to see techniques and ordered combinations.
- [Find a title, alias, ID, or tag](catalog/search.md) using your browser’s Find command. Large lists show page links. [Retired records](catalog/retired.md) have their own finder.
- Search a checkout with Python 3.12 or newer. Add `--json` for structured output.

```sh
python tools/catalog.py search "proof links" --task verification
python tools/catalog.py search --kind combination --tag quickstart --limit 25 --offset 25 --json
```

Search matches word prefixes across titles, IDs, aliases, tags, and summaries, without regard to case or accents. All query words must match. Exact titles, IDs, and aliases rank first. Filter by task, kind, tag, evidence, or status. Search defaults to active records, and `--status all` includes retired entries.

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
