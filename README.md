# Provenistem

Provenistem is a project tracker for **what exists today** and **what you might build next**. Use the permanent `Provenistem` branch to capture an idea while it's fresh, then find its context and status in a later session. You can read and edit the records directly on GitHub.

- [**Features**](features/INDEX.md) starts with capabilities available on README HQ today and links to their source. It labels draft implementations and links to a separate [proposals and plans](features/PLANNED.md) page.
- [**Ideas**](ideas/INDEX.md) holds possibilities, design questions, tradeoffs, and the context that led to them.

## Pick up where you left off

1. Open [Ideas](ideas/INDEX.md) and find the ID or title you remember. Each record explains the idea, its origin, and its current state. Try [IDEA-000008](ideas/records/IDEA-000008.json) to see a dated example.
2. Open [Features](features/INDEX.md) to see which capabilities currently exist. Follow the source and test links in the record. Try [FEAT-000001](features/records/FEAT-000001.json) for the version archive.
3. If an idea led to a capability, follow the idea IDs in the feature's `idea_ids` field. Keep the original idea for its context and use the feature record for implementation progress.

## Capture and update records

**Capture an idea.** Copy the [idea starter](templates/idea.json) into `ideas/records/`. Use the next unused `IDEA-000000` style ID for both the filename and the record. In `origin.source`, include the date and where the idea came from. Use the summary and tradeoffs to capture enough context to make sense in a fresh session. Link the new record from the Ideas index.

**Record a feature.** Copy the [feature starter](templates/feature.json) into `features/records/`. Give it a `FEAT-000000` style ID and write the behavior a reviewer can observe. Link supporting ideas and pin implementation and test evidence to the source revision. Link available and draft implementations from the Features index. Use the proposals and plans page for work still under consideration.

JSON records hold the details. Keep their indexes in sync and preserve IDs when titles or status change. Use [GitHub Issues](https://github.com/vixttha/README-HQ/issues) for defects and the [README HQ version archive](https://github.com/vixttha/README-HQ/blob/readme-hq/versions/README.md) for publication status.

## Use the layout in another repository

Create a dedicated branch or folder for the tracker. Start from the two starter forms and use that repository's own records, evidence links, and indexes. The sample records on this branch describe README HQ.

[README HQ trial notes](TRIAL.md)
