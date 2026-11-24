"""Demonstrate Graphify HQ's per-manifest capacity using synthetic data."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def check_graphify_capacity():
    sys.path.insert(0, str(ROOT / "graphify-hq/template/v0.0.8"))
    from evidence_map import validate_manifest

    ref = {"path": "README.md", "anchor": "# README HQ"}
    features = [
        {"id": f"checkpoint-{i}", "label": f"Checkpoint {i}",
         "documented_in": [ref], "changed_in": [ref], "tested_by": [ref]}
        for i in range(1, 34)
    ]
    data = {
        "repository": "vixttha/README-HQ",
        "source_commit": "f50e3749dab90ddfe35894284d1660097a1fb1a8",
        "title": "Synthetic manifest capacity fixture",
        "features": features[:32],
    }
    validate_manifest(data)
    try:
        validate_manifest({**data, "features": features})
    except ValueError as exc:
        if str(exc) != "Expected at most 32 features":
            raise
    else:
        raise ValueError("The reference template unexpectedly accepted 33 features")
    print("Q33: Graphify HQ v0.0.8 accepted 32 checkpoint nodes and rejected 33 in a single manifest.")


if __name__ == "__main__":
    check_graphify_capacity()
