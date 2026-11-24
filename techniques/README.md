# Archived README HQ technique registry

Use the [README Technique Library](https://github.com/vixttha/README-HQ/tree/README-Technique-Library) for current technique and combination selection. The bundled registry and the historical verification instructions below remain for reproducible archival checks, not new recommendation intake. Changes to maintained techniques belong on the dedicated library branch and require review.

[Open the technique registry](registry.json) or print its index from a checkout.

```sh
python3 tools/check_readme_hq.py --list
```

The historical catalog records one canonical record and persistent ID per technique. Current discoveries belong in the external library.

## Historical registry record format

The archived registry represents active and retired records, alternate names and evidence links. For current discoveries, compare the problem, intervention and result with the external library; keep project-specific advice in the audit.

Historical `registry.json` entries contain a stable slug ID, title, problem, practice, observable outcome, normalized outcome key, aliases, status and public evidence URLs. Static observations use `observed`; demonstrated checks use `verified`. Retired IDs and aliases remain reserved. The checker rejects exact lookup and mechanism collisions; semantic overlap requires review. Do not add current discoveries to this archive.

The approved historical inventory binds repository visibility, commit, path, Git blob ID, SHA-256 and physical line count to independently reviewed public sources. Preserve the inventory and its validator digest.


## Historical demonstrated-evidence format

1. Run the applicable check on the exact source commit and preserve the raw CLI receipt or job artifact. In GitHub Actions, open the run and its job. Record the run attempt, the runner OS and runtime version, the tested commit, the tool revision, and where the raw artifact can be retrieved.
2. Verify independently that the repository and run are public, the job actually checked that commit, and the claimed check passed without a skip or coverage gap. Compare the raw observation with the expected result. If the sources, environment, or result cannot be confirmed, keep the technique evidence at `observed`.
3. Open the exact GitHub blob and its physical line span. Compare its SHA-256 and line count with the independently reviewed source inventory. The URL fragment and the receipt's `source_span` must match.
4. A historical verified item points to a tracked reviewed JSON record under `evidence/public/`, an immutable blob URL with its line span, and `"status": "verified"`. Reviewers can trace existing records with `python3 tools/check_readme_hq.py --list`. A raw `--receipt` file has a different schema. New evidence belongs in the current library workflow, not this archive.

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
