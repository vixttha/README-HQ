"""Prepare the checked-in Graphify self-map for the current README HQ checkout."""

import argparse
import json
from pathlib import Path
import subprocess

from evidence_map import origin_repository, read_manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    manifest = read_manifest(Path(__file__).with_name("self-map.json"))
    manifest["repository"] = origin_repository() or "vixttha/README-HQ"
    manifest["source_commit"] = subprocess.check_output(
        ["git", "--no-replace-objects", "rev-parse", "HEAD"], text=True
    ).strip()
    args.output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
