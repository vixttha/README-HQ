# Learn from verified public sources

Run the [intake command](intake.py) with a JSON specification and an output directory for public receipts. Each source supplies a unique id, a local Git checkout, a GitHub repository, a ref, a path, a positive line, an anchor, and public visibility. The target uses the same evidence fields plus an audience and capability.

Use [README-Technique-Library](https://github.com/vixttha/README-HQ/tree/README-Technique-Library) to find techniques and combinations that fit the adopter's reader task. Record the owner's selection and rationale. Supply a top-level `catalog` object with a local `checkout` of that repository and its full library `commit`. The intake checks that GitHub confirms the commit is on the library branch and reads records from that commit's Git tree. Set either `technique` or `combination` to the selected record ID in a finding. The record and every step in a selected combination must be active at that commit. A new candidate provides its own problem, practice, and outcome.

The intake verifies public visibility and exact commit against GitHub and verifies the anchor against the pinned Git blob. Schema 2 receipts record the external catalog revision, record path, and ordered combination steps when applicable. Identical inputs yield the same receipt. Changed source, target, or catalog commits yield distinct history. The original schema 1 receipts remain historical records. Keep private inputs outside shared intake.

Reuse decisions and source attribution are recorded under [project and imported material terms](../REUSE.md). The earlier [learning pilot](https://github.com/vixttha/README-HQ/tree/a8d97d0559853538d4d814edf5c998e42cfec3d2/learning) documents the historical experiments.
