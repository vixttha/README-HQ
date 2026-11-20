# Learn from verified public sources

Run the [intake command](intake.py) with a JSON specification and an output directory for public receipts. Each source supplies a unique id, a local Git checkout, a GitHub repository, a ref, a path, a positive line, an anchor, and public visibility. The target uses the same evidence fields plus an audience and capability. Select source IDs and record a decision and rationale for each applicable existing technique. A new candidate provides its own problem, practice, and outcome.

The intake verifies public visibility and exact commit against GitHub and verifies the anchor against the pinned Git blob. Submitting identical evidence and decisions yields the same receipt. Changed source or target commits yield distinct history. Only active technique IDs with selected sources can produce recommendations. A receipt lists known exclusions with their reason, such as a retired technique or an unselected source. An unknown ID stops intake so a typo cannot silently discard a recommendation. Keep private inputs outside shared intake.

Reuse decisions and source attribution are recorded under [project and imported material terms](../REUSE.md). The earlier [learning pilot](https://github.com/vixttha/README-HQ/tree/a8d97d0559853538d4d814edf5c998e42cfec3d2/learning) documents the historical experiments.

The intake receipt retains the requested and canonical GitHub repository names, the API repository ID, and the exact matched anchor and line. A canonical rename is accepted only when the canonical metadata confirms the same public repository ID. Different anchors on one line can represent distinct evidence.
