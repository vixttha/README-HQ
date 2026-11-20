# README HQ

README HQ helps people understand a GitHub project and take their first useful step. It gives coding agents the same starting point, with links to repository instructions, test commands, and the evidence behind version and compatibility claims.

**Current version** · [README HQ v0.0.6](versions/v0.0.6/README.md)

| If you want to | Start here |
| --- | --- |
| Find a current or historical README | [Version index](versions/README.md) |
| Explore changes and evidence by version | [Graphify HQ](graphify-hq/README.md) |
| Improve a README in your own repository | [README guide](README-GUIDE.md) |
| Request a detailed repository review | [Repository audit](audits/README.md) |
| Browse techniques learned from reviews | [Technique library](techniques/README.md) |
| Invoke README HQ from an agent | [Agent entry point](AGENTS.md) |

## Use README HQ

For the current repair trial, ask your agent to use `vixttha/README-HQ` at `repair/v0.0.6-batch-1` and name the target repository. The agent records the exact trial commit and reads the target repository’s own instructions. Use `readme-hq` for the published version archive.

To check a README HQ checkout, use Python 3.10 or newer.

```sh
git clone --branch repair/v0.0.6-batch-1 https://github.com/vixttha/README-HQ.git
cd README-HQ
python3 -m pip install --require-hashes -r tools/requirements.txt
python3 tools/check_readme_hq.py
```

To audit a consumer, run `python3 tools/check_readme_hq.py --repo /path/to/project --ref HEAD --receipt audit.json`. Point `--repo` at the Git root. Use `--subproject` for a monorepo package or `--profile reference` for reference-only documentation. The receipt records the selected scope and identifies an origin-derived repository name as inferred. Git blob reads are offline by default. Use `--allow-git-fetch` for a partial clone when its promisor may supply missing blobs. The receipt lists blobs retrieved under that option.

Pass `--smoke smoke.json` to check a documented first action at the selected commit. A local spec uses `commit`, `argv`, and `expected.exit` with an output marker (`expected.contains`) or a file outcome (`expected.file`). Commands and expected files use the selected subproject in a temporary shallow Git checkout with independent metadata. The command runs with the caller’s privileges. A marker can select `expected.stream` as `stdout` or `stderr`. The default, `either`, matches within a single stream.

A remote spec uses `commit`, an HTTPS `url`, and `expected.http_status`. With `--allow-network`, the receipt includes the effective URL and can require an exact `expected.final_url`. Use `expected.contains` for a marker in the first 1,000,000 bytes of the response body. HTTP 401, 403, and 429 are reported as gated.

On Windows, install the same requirements with `py -3 -m pip install --require-hashes -r tools/requirements.txt` and use `py -3 tools/check_readme_hq.py`. A passing check prints counts for the version index, technique catalog, local navigation, and archived source files.

The branch keeps versions and audit findings available between sessions. An authorized human or agent starts each audit, records each new finding, and reviews any resulting project changes.

See the [learning intake](learning/README.md) and [reuse and attribution terms](REUSE.md).
