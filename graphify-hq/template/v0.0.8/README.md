# Graphify HQ v0.0.8

Graphify HQ maps feature evidence at a full Git commit. It reads source directly
from Git objects and records the commit, Graphify version, graph SHA-256 and
each cited source file's SHA-256 in the receipt.

## Source and pull request provenance

Set `repository` to the GitHub owner and repository and `source_commit` to the
full SHA already fetched into the checkout. For a same-repository pull request,
add `pull_request` with its `number` and `source_branch`. Running with
`--verify-pr` queries GitHub for commit membership and exact-SHA reviews. The
live observation is printed separately from the deterministic receipt.

## Feature evidence links

Each feature has a unique lowercase ID, a label, and `documented_in`,
`changed_in`, and `tested_by` lists. Add `implemented_in` to link code or
workflow definitions. A reference has a repository-relative `path` and one
unique, exact source line as its `anchor`, with outer whitespace removed.
The optional `source_files` list adds file nodes for the source SHA and
connects matching evidence anchors to their files.

Test links identify definitions. The associated runner job records the
execution result. The [self-map manifest](self-map.json) supplies feature
links and inventory for this kit. Run the [self-map preparer](self_map.py) to fill the repository and exact commit from this checkout. Use the same manifest shape in your project
and replace the paths and anchors with yours.

## Reproducible build and MCP verification

Copy this version's Python files and lockfile. On a GitHub-hosted Linux x86-64
runner using Python 3.12, fetch the pinned commit and run from the repository
root. Adjust `kit`, the manifest and the output folder to match your project.

```bash
kit=graphify-hq/template/v0.0.8
python -m pip install --require-hashes --no-cache-dir --only-binary=:all: --no-deps -r "$kit/requirements.txt"
python -m pip check
python -m unittest discover -s "$kit" -p 'test_*.py' -v
python "$kit/self_map.py" /tmp/readme-hq-self-map.json
PYTHONHASHSEED=0 python "$kit/evidence_map.py" /tmp/readme-hq-self-map.json /tmp/readme-hq-self-map
PYTHONHASHSEED=0 python "$kit/evidence_map.py" /tmp/readme-hq-self-map.json /tmp/readme-hq-self-map --check
```

The build uses Graphify to export the map and verifies its source SHA and
counts using `graph_stats`, then reads each feature's links using
`get_neighbors`. With `--check`, it compares both rebuilt files byte for byte.
For saved maps, start an MCP server with
`python -m graphify.serve evidence/graph.json`. The kit runs from a manifest
and pinned Git blobs without credentials. Optional PR provenance can use a
read-only `GH_TOKEN`.
