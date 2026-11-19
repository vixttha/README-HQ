# README HQ v0.0.6 repair plan graph

The [repair pipeline](../../../plans/v0.0.6-repairs/README.md) lists the seventeen checkpoints in order. Each Graphify node links to its issue row, planned change, and baseline reproduction. Nodes after the first also link to their predecessor row. The reproduction links identify evidence of the original defects. Each future repair needs its own passing regression result.

[Graph JSON](graph.json) · [Source manifest](manifest.json) · [Verification receipt](receipt.json)

The map uses pinned Git source and the [Graphify HQ v0.0.8 template](../../template/v0.0.8/README.md). Query a node such as `feature:v0-0-6-1` with Graphify MCP to trace its references.
