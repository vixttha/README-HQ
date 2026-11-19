# README HQ Ideas and Features

Use this branch to capture improvements to README HQ and track their progress. The records follow the Provenistem v0.0.2 Ideas and Features format and can be edited directly on GitHub.

- [Ideas](ideas/INDEX.md) records questions, possible improvements, benefits, and tradeoffs.
- [Features](features/INDEX.md) records capabilities, acceptance criteria, implementation status, and evidence.

Start with [self-use for the README HQ homepage](ideas/records/IDEA-000001.json), [the v0.0.6.67 draft validation record](features/records/FEAT-000003.json), or [the checkpoint plan awaiting approval](features/records/FEAT-000008.json).

## Add a record

1. Copy the [idea starter](templates/idea.json) or [feature starter](templates/feature.json) into the matching `records/` folder. Use the next unused six-digit ID and match the filename to the ID.
2. Replace the starter text with project facts. Link a feature to its related ideas through `idea_ids`, and pin evidence to the source commit and repository path.
3. Update the corresponding index in the same commit. JSON records are the source for the index.
4. Keep defects in [GitHub Issues](https://github.com/vixttha/README-HQ/issues), implementation and checks in GitHub pull requests and Actions, and publication status in the [README HQ version archive](../versions/README.md). Use tracking states and test outcomes only when their evidence supports them.

The first seed uses the public README HQ v0.0.6 branch as its baseline and cites [draft PR #68](https://github.com/vixttha/README-HQ/pull/68) for candidate work.
