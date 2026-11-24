# Archived README HQ technique registry

Use the [README Technique Library](https://github.com/vixttha/README-HQ/tree/README-Technique-Library) for current technique and combination selection. The bundled registry and the historical verification instructions below remain for reproducible archival checks, not new recommendation intake. Changes to maintained techniques belong on the dedicated library branch and require review.

[Open the technique registry](registry.json) or print its index from a checkout.

```sh
python3 tools/check_readme_hq.py --list
```

The catalog can grow with each audit. Every technique has one canonical record and persistent ID. An audit can cite IDs without repeating their definitions.

## Historical registry record format

Compare the improvement against the registry, including retired records. Search for the same reader problem, intervention, and result under alternate wording. Use an existing record when those match. Add an alias for a common alternate name or an evidence link for a new example. Keep project advice in the relevant audit.

For a distinct technique, add an entry in `registry.json` with a stable slug ID, a short title, the problem, the practice, the observable outcome, a normalized outcome key, any aliases, a status, and one or more public evidence URLs. Mark static observations as `observed` and demonstrated checks as `verified` after following the receipt review below. Retire a record without freeing its ID or alternate names. Resolve semantic overlap in review and let the checker reject exact collisions across IDs, titles, aliases, outcome keys, and normalized outcomes.

Before changing the approved public inventory, independently check repository visibility, the pinned commit and path, the Git blob ID, SHA-256, and the physical line count against the public source. Record the review evidence with the inventory change and update the pinned digest in the validator.


## Review and record demonstrated evidence

1. Run the applicable check on the exact source commit and preserve the raw CLI receipt or job artifact. In GitHub Actions, open the run and its job. Record the run attempt, the runner OS and runtime version, the tested commit, the tool revision, and where the raw artifact can be retrieved.
2. Verify independently that the repository and run are public, the job actually checked that commit, and the claimed check passed without a skip or coverage gap. Compare the raw observation with the expected result. If the sources, environment, or result cannot be confirmed, keep the technique evidence at `observed`.
3. Open the exact GitHub blob and its physical line span. Compare its SHA-256 and line count with the independently reviewed source inventory. The URL fragment and the receipt's `source_span` must match.
4. Save a reviewed JSON record at `evidence/public/<name>.json`. In the registry evidence item, use `"status": "verified"`, the immutable blob URL with its line span, and a `"receipt"` value pointing to that tracked record. Run `python3 tools/check_readme_hq.py --list` and have a reviewer trace the new record back to the run. A raw `--receipt` file has a different schema and cannot be used as this record.

The following example uses fixture identities. Replace them with the values verified for your run. The `expected` and `observed` strings record the same outcome as established by the review. Keep the detailed observation in the source artifact.

```json
{
  "visibility": "public",
  "result": "pass",
  "source_repository": "example/project",
  "source_commit": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "source_path": "README.md",
  "source_span": "L1",
  "source_sha256": "bc553ffe57e544498b12a9865dbf3abc2004c474e349c52c378eaa402287424b",
  "environment": "Ubuntu, Python 3.12, validator commit bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "run_url": "https://github.com/example/project/actions/runs/123/job/456",
  "run_attempt": 1,
  "expected": "First command prints ready",
  "observed": "First command prints ready"
}
```
