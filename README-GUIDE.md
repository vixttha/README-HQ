# Write a README for people and agents

Start by identifying the project, what works now, and the first useful action. Choose the route that matches the product. A game might begin with **Play**, a CLI with **Install and run**, and a template with **Copy and verify**.

| Section | What readers should be able to determine | Source to check |
| --- | --- | --- |
| Overview and status | What the project does, who can use it, and its current maturity | Release notes, product docs, default branch |
| First success | Prerequisites, exact commands, and a recognizable result | Package metadata, launcher or CLI, smoke checks |
| Common tasks | Supported usage, optional configuration, and how to recover from common failures | Configuration examples, docs, tested workflows |
| Development | How to find the code, run the normal checks, and report problems | Package scripts, CI, issue templates |
| Agent navigation | Where rules, source entry points, and validation instructions live | `AGENTS.md` or repository equivalent, source and workflow files |
| Project terms | License or reuse terms and relevant data or artwork provenance | License, attribution and provenance records |

Put role-specific links near the corresponding task. Keep durable repository instructions in the appropriate agent instruction file and link to it when the README needs to route an agent. Write descriptive link text, use one clear heading hierarchy, and describe informative images with meaningful alt text.

## Verify the first useful action

Run the documented commands from a clean checkout with the advertised prerequisites. Record the tested ref or release, commit, platform, invocation, expected result, and observed outcome. For an example that creates a file, verify that file or structure. Mark unavailable environments as unverified. If a route works only on the development branch or a specific release, put that boundary beside the route.

Review how the README renders at standard desktop and narrow widths. Check relative assets, links, anchors, long code blocks, and the accessibility of the text and images. Inspect the exact copy and image paths as they will appear on the target homepage.

### Run the first-action example

From the README HQ checkout, install the [locked reader requirements](tools/requirements.txt) and run the [example](examples/first_action_demo.py) with Python. Use `python3` or `py -3` if that is how your system exposes Python.

```sh
python -m pip install --require-hashes -r tools/requirements.txt
python examples/first_action_demo.py first-action-evidence
```

The example creates a disposable repository and pins its exact commit. It runs `python run.py` inside `packages/demo` and writes `passing.json`, `failing.json`, and `url-unchecked.json`. Open `cases.first_action` for each actual outcome. The two command specs share the same invocation and differ in their expected output.

To adapt a spec, set its `commit` to the full SHA selected by `--ref`. Pass it with `--repo`, `--smoke`, and `--receipt`. A local spec uses an `argv` array and `expected.exit` plus an output marker or file outcome. Arguments and expected files use the selected subproject in a temporary shallow checkout. An HTTPS spec uses `url` and `expected.http_status`. Only add `--allow-network` for a URL you intend to probe. The example leaves its URL probe unchecked. Add `--require-smoke` when the audit must prove a passing first action. A skipped, gated, or unresolved required check produces an incomplete receipt and exits 2. A failed expectation exits 1 and lists structured mismatch codes in the receipt. Command stdout and stderr stay out of receipts by default. For a private failure receipt, `--include-smoke-output` retains the first 512 bytes of each stream with a truncation flag. This opt-in copies raw output without secret detection. Keep those receipts out of public artifacts.

## Choose an authorized validation environment

Standard hosted workflow jobs are public-only. Use GitHub's trusted hosting repository metadata: visibility must be public and the private flag must be an actual Boolean false. Missing, conflicting, private or internal metadata does not authorize standard hosted execution. For a fork pull request, the hosting/base repository controls runner policy, not a fork's claimed visibility; separately record the PR head and tested merge checkout. Read-only permissions and ordinary pull-request events do not authorize access to private material.

For private, internal, unknown or inaccessible targets, use an authorized offline checkout (or a separately owner-configured private environment). Run the reader with `--repo`, `--ref` and a receipt path in private storage, without network or Git-fetch opt-ins. Do not upload its output, identifiers, receipts or artifacts to public locations. Report unresolved visibility and coverage to the owner. No private hosted jobs are required by README HQ.

## Install on a dedicated target branch

Use the reviewed full source SHA, not a moving branch tip. Before copying or publishing files, confirm that applicable reuse terms authorize the installation. A trial or review-only licensing draft grants no additional rights. Until then, use the separate source checkout for read-only consumer audits.

For an authorized fresh installation, start at the root of a clean target clone. Record its current branch and HEAD. Check the local and remote `readme-hq` branch first; if either exists, stop and review an upgrade rather than replacing it. Fetch the approved source commit into the target clone and create the dedicated branch directly from that commit, not from the product branch. This installs the complete reviewed tree (AGENTS.md, guides, tools, locked requirements, version records and tests) without mixing it into product history.

```sh
git status --short
git rev-parse HEAD
git branch --list readme-hq
git ls-remote --heads origin refs/heads/readme-hq
# Stop if dirty, if either branch exists, or if a check failed.
approved_sha=REPLACE_WITH_APPROVED_40_CHARACTER_SHA
case "$approved_sha" in
  *[!0-9a-f]*|'') exit 1 ;;
esac
test "${#approved_sha}" -eq 40 &&
git fetch --no-tags https://github.com/vixttha/README-HQ.git "$approved_sha" &&
test "$(git rev-parse FETCH_HEAD)" = "$approved_sha" &&
git branch readme-hq "$approved_sha" &&
git rev-parse readme-hq
```

Confirm the branch SHA exactly matches the reviewed source. Record the original product HEAD, installed SHA, target branch, authorization and verification receipt. The commands leave the product checkout on its original branch. Use a separate worktree to inspect or validate the installed branch; do not merge it into the product branch. Push the dedicated branch only with explicit owner permission and applicable distribution rights. Keep local records during upgrades and do not force-push.

## Draft, archive, and publish

1. Record the target project, docs version, target ref and full SHA, and current homepage status. Decide the first reader task and who needs additional routes.
2. Work in a per-version workspace. Record the intended changes, the draft, any images, and the proof for each claim. Link to the matching canonical source of each platform or compatibility statement.
3. When the owner accepts a draft, freeze the exact README and associated assets, record their origin and evidence, and add the version to the index.
4. Use a distinct publication change to promote the accepted README to the homepage when authorized. Recheck relative paths in that destination. Record the resulting commit, public status, and CI evidence if run.
5. Link to the frozen copy when answering a request for a specific version. Report a working draft, an accepted archive, and a published homepage with their observed statuses.

Use [the audit workflow](audits/README.md) to examine an existing repository before drafting. Browse the [README Technique Library](https://github.com/vixttha/README-HQ/tree/README-Technique-Library) for techniques and combinations; record selected IDs, the exact library commit, owner rationale and target verification.

A local smoke check with an expected file requires new or changed bytes by default. Use `expected.file_mode` to require `created` or `updated` specifically, or specify `exists` when existence alone is the intended result. Use `expected.file_sha256` for an exact expected digest.

A required smoke result must match a rendered Quickstart action in the pinned README. The receipt records the README path, line, and digest for a match. Simple POSIX, cmd, and PowerShell arguments are supported. Shell pipelines, redirects, and expansions stay supplemental.

HTTP smoke receipts include a digest of the validated specification and an origin and digest for each recorded URL. Paths, query strings, fragments, and content markers stay in the spec.

## Inspect the publication gate

```bash
python tools/check_publication_rules.py vixttha/README-HQ main \
  --require-check 'README HQ on ubuntu-latest' \
  --require-check 'README HQ on windows-latest' \
  --require-check 'Recoverable Graphify evidence and plan'
```

The read-only report records branch rulesets and classic branch protection when available. Set `GH_TOKEN` with read access to repository administration to inspect restricted protection settings. The solo maintainer records the publication decision separately with the exact candidate SHA.

The reader requires Python 3.11 or newer with Pillow 13.0.0 pinned in `tools/requirements.txt`. Pillow 13 removes Python 3.10 and includes security fixes. Graphify MCP uses its own pinned Python 3.12 environment. [Pillow 13.0.0 release notes](https://pillow.readthedocs.io/en/stable/releasenotes/13.0.0.html) · [PyPI release and wheel hashes](https://pypi.org/pypi/Pillow/13.0.0/json).
