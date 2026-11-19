# README HQ v0.0.6 repair plan graphs

The [repair pipeline](../../../plans/v0.0.6-repairs/README.md) sequences all 59 checkpoints. Each Graphify node links a plan row, the planned change, and its baseline reproduction or inspection. The preceding row connects the ordering across the three manifests.

| Checkpoints | Graphify evidence |
| --- | --- |
| 1–24 | [Graph JSON](graph.json) · [Manifest](manifest.json) · [Receipt](receipt.json) |
| 25–55 | [Graph JSON](assurance/graph.json) · [Manifest](assurance/manifest.json) · [Receipt](assurance/receipt.json) |
| 56–59 | [Graph JSON](entrypoints/graph.json) · [Manifest](entrypoints/manifest.json) · [Receipt](entrypoints/receipt.json) |

The [pinned Graphify template](../../template/v0.0.8/README.md) accepts at most 32 features per manifest. The public plan workflow checks exact source, complete unique coverage, predecessor links, and a byte-for-byte rebuild of all three maps with MCP readback. Fixture links reproduce the observed baseline. Repair receipts will use each future candidate revision.
