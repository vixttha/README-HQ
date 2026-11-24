# README HQ

README HQ helps people understand a GitHub project and take their first useful step. It gives coding agents the same starting point, with links to repository instructions, test commands, and the evidence behind version and compatibility claims.

**Current version** · [README HQ v0.0.6](versions/v0.0.6/README.md)

| If you want to | Start here |
| --- | --- |
| Find a current or historical README | [Version index](versions/README.md) |
| Explore changes and evidence by version | [Graphify HQ](graphify-hq/README.md) |
| Improve a README in your own repository | [README guide](README-GUIDE.md) |
| Request a detailed repository review | [Repository audit](audits/README.md) |
| Browse techniques learned from reviews | [README Technique Library](https://github.com/vixttha/README-HQ/tree/README-Technique-Library) |
| Invoke README HQ from an agent | [Agent entry point](AGENTS.md) |

## Use README HQ

For the current repair trial, ask your agent to use `vixttha/README-HQ` at `repair/v0.0.6-integration-candidate` (the combined v0.0.6 repair draft, not a published release) and name the target repository. Resolve the branch to an exact SHA and confirm it against the approved review evidence before use. The agent records the exact trial commit and reads the target repository’s own instructions. Use `readme-hq` for the published version archive.

To check a README HQ checkout, use Python 3.11 or newer.

```sh
git clone --branch repair/v0.0.6-integration-candidate https://github.com/vixttha/README-HQ.git
cd README-HQ
# Replace with the full commit SHA from the accepted review, not a branch tip.
approved_sha=REPLACE_WITH_APPROVED_40_CHARACTER_SHA
case "$approved_sha" in
  *[!0-9a-f]*|'') exit 1 ;;
esac
test "${#approved_sha}" -eq 40 &&
git checkout --detach "$approved_sha" &&
test "$(git rev-parse HEAD)" = "$approved_sha" &&
python3 -m pip install --require-hashes -r tools/requirements.txt &&
python3 tools/check_readme_hq.py
```

To audit a consumer, run `python3 tools/check_readme_hq.py --repo /path/to/project --ref HEAD --receipt audit.json`. Point `--repo` at the Git root. Use `--subproject` for a monorepo package or `--profile reference` for reference-only documentation. A rich-text README whose navigation cannot be checked produces an incomplete receipt and exits 2. The receipt records the selected scope and identifies an origin-derived repository name as inferred. Git blob reads are offline by default. Use `--allow-git-fetch` for a partial clone when its promisor may supply missing blobs. The receipt lists blobs retrieved under that option.

Follow the [first-action receipt example](README-GUIDE.md#run-the-first-action-example), or pass `--smoke smoke.json` to check a documented first action at the selected commit. A local spec uses `commit`, `argv`, and `expected.exit` with an output marker (`expected.contains`) or a file outcome (`expected.file`). Commands and expected files use the selected subproject in a temporary shallow Git checkout with independent metadata. The command runs with the caller’s privileges. A marker can select `expected.stream` as `stdout` or `stderr`. The default, `either`, matches within a single stream.

A remote spec uses `commit`, an HTTPS `url`, and `expected.http_status`. With `--allow-network`, the receipt records the effective URL’s origin and SHA-256 digest. You can require an exact match with `expected.final_url`. Use `expected.contains` for a marker in the first 1,000,000 bytes of the response body. HTTP 401, 403, and 429 are reported as gated.

On Windows, install the same requirements with `py -3 -m pip install --require-hashes -r tools/requirements.txt` and use `py -3 tools/check_readme_hq.py`. A passing check prints counts for the version index, archived technique registry, local navigation, and archived source files.

The branch keeps versions and audit findings available between sessions. An authorized human or agent starts each audit, records each new finding, and reviews any resulting project changes.

See the [learning intake](learning/README.md) and [reuse and attribution terms](REUSE.md).

## Engineering ecosystem

[Owner-approved six architectural laws](ENGINEERING-LAWS.md) apply to this product. Standalone operation and owner authority remain unchanged. The product has no mandatory coordination-tool dependency.

## Agent capability discovery — v1

<!-- agent-capability:v1
{"schema_version":1,"id":"readme-hq","branch":"readme-hq","entrypoint":"AGENTS.md","scope":"Documentation authoring and version history","required_ecosystem_tools":[],"authority":"owner","discovery":"read-only","versioning":"independent"}
-->

A compatible agent may enumerate the target repository's branch refs, resolve this branch to a commit, and read its entry point at that exact commit. Read-only discovery confers no execution, write, integration or release authority. If this branch or marker is absent, the tool is absent or legacy/unverified; continue independently. Check the target's own instructions and owner scope before any action. The marker describes a capability, not a required registry or package version.

Installation convention: human or agent selects a reviewed exact source SHA, checks the dedicated target branch and collisions, follows [this product's own installation guide](#use-readme-hq), and records source/target SHA and preserved product state. Never merge a template workspace wholesale into product source. Existing installations require explicit reviewed upgrades; preserve local records and prior receipts. Optional evidence links do not authorize writes. No mandatory coordinator or other ecosystem tool.
