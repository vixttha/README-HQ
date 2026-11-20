# Technique library

[Open the technique registry](registry.json) or print its index from a checkout.

```sh
python3 tools/check_readme_hq.py --list
```

The catalog can grow with each audit. Every technique has one canonical record and persistent ID. An audit can cite IDs without repeating their definitions.

## Record a discovery

Compare the improvement against the registry, including retired records. Search for the same reader problem, intervention, and result under alternate wording. Use an existing record when those match. Add an alias for a common alternate name or an evidence link for a new example. Keep project advice in the relevant audit.

For a distinct technique, add an entry in `registry.json` with a stable slug ID, a short title, the problem, the practice, the observable outcome, a normalized outcome key, any aliases, a status, and one or more public evidence URLs. Mark static observations as `observed` and demonstrated checks as `verified` when an exact result is available. Retire a record without freeing its ID or alternate names. Resolve semantic overlap in review and let the checker reject exact collisions across IDs, titles, aliases, outcome keys, and normalized outcomes.

Before changing the approved public inventory, independently check repository visibility, the pinned commit and path, the Git blob ID, SHA-256, and the physical line count against the public source. Record the review evidence with the inventory change and update the pinned digest in the validator.
