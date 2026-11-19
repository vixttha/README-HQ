"""Compare the offline navigator with rendered GitHub README destinations."""

import argparse
from contextlib import contextmanager
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
BASE = "f50e3749dab90ddfe35894284d1660097a1fb1a8"
REPO = "vixttha/README-HQ"
FIXTURES = Path("audit/fixtures")
CHECKER = "tools/check_readme_hq.py"
COMPILER = "graphify-hq/template/v0.0.8/evidence_map.py"
CUSTOM_ANCHOR = "owner-reviewed-quick-start"


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def execute(directory, *args):
    return subprocess.run(args, cwd=directory, capture_output=True, encoding="utf-8")


def run(directory, *args):
    result = execute(directory, *args)
    require(result.returncode == 0, result.stdout + result.stderr)
    return result.stdout


@contextmanager
def worktree(directory):
    run(ROOT, "git", "worktree", "add", "--quiet", "--detach", str(directory), BASE)
    try:
        yield directory
    finally:
        run(ROOT, "git", "worktree", "remove", "--force", str(directory))


def with_link(directory, path):
    entrypoint = directory / "README.md"
    original = entrypoint.read_bytes()
    try:
        entrypoint.write_bytes(original + f"\n[Navigation fixture]({path})\n".encode())
        return execute(directory, sys.executable, CHECKER)
    finally:
        entrypoint.write_bytes(original)


def check_fragment_coverage(directory):
    existing = with_link(directory, "audits/#inspect-a-repository")
    require(existing.returncode == 0 and "Validated" in existing.stdout, existing.stderr)
    missing = with_link(directory, "audits/#audit-fixture-heading-absent")
    require(missing.returncode == 0 and "Validated" in missing.stdout, missing.stderr)
    control = with_link(directory, "audits/README.md#audit-fixture-heading-absent")
    require(control.returncode == 1 and "missing local heading" in control.stderr, control.stderr)

    alternate = FIXTURES / "alternate.markdown"
    expected = with_link(directory, f"{alternate}#available-section")
    require(expected.returncode == 0, expected.stderr)
    missing = with_link(directory, f"{alternate}#audit-fixture-heading-absent")
    require(missing.returncode == 0 and "Validated" in missing.stdout, missing.stderr)
    print("N66: Missing fragments pass on a rendered directory and a .markdown link, while the direct .md control rejects the same absent heading.", flush=True)


def check_named_anchor(directory):
    document = FIXTURES / "named-anchor.md"
    text = (directory / document).read_text(encoding="utf-8")
    require(text.count(f'<a name="{CUSTOM_ANCHOR}"></a>') == 1, "Named anchor fixture missing")
    control = with_link(directory, f"{document}#generated-section")
    require(control.returncode == 0 and "Validated" in control.stdout, control.stderr)
    custom = with_link(directory, f"{document}#{CUSTOM_ANCHOR}")
    require(custom.returncode == 1 and f"missing local heading {document}#{CUSTOM_ANCHOR}" in custom.stderr,
            custom.stdout + custom.stderr)
    print("N67: A GitHub-style named anchor fails the offline checker; a generated heading in the same file passes.", flush=True)


class PageAnchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.identifiers = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        for key in ("id", "name"):
            if key in attributes:
                self.identifiers.add(attributes[key])


def fetch(url):
    request = Request(url, headers={"User-Agent": "README-HQ-public-navigation-audit"})
    with urlopen(request, timeout=35) as response:
        return response.read().decode("utf-8")


def rendered_anchors(url):
    parser = PageAnchors()
    parser.feed(fetch(url))
    return parser.identifiers


def check_rendered_targets(audit_sha):
    api = f"https://api.github.com/repos/{REPO}/readme/audits?ref={BASE}"
    info = json.loads(fetch(api))
    require(info["path"] == "audits/README.md", str(info.get("path")))
    actual = run(ROOT, "git", "rev-parse", f"{BASE}:audits/README.md").strip()
    require(info["sha"] == actual, "GitHub directory README blob differs from the pinned one")

    base_url = f"https://github.com/{REPO}"
    group = rendered_anchors(f"{base_url}/tree/{BASE}/audits")
    require("user-content-inspect-a-repository" in group and
            "user-content-audit-fixture-heading-absent" not in group, "Unexpected directory HTML anchors")
    alternate = rendered_anchors(f"{base_url}/blob/{audit_sha}/{FIXTURES}/alternate.markdown")
    require("user-content-available-section" in alternate and
            "user-content-audit-fixture-heading-absent" not in alternate, "Unexpected alternate file HTML anchors")
    named = rendered_anchors(f"{base_url}/blob/{audit_sha}/{FIXTURES}/named-anchor.md")
    require(f"user-content-{CUSTOM_ANCHOR}" in named and "user-content-generated-section" in named,
            "GitHub did not render both fixture anchors")
    print("Rendered control: GitHub's API returns the expected directory README blob, and GitHub HTML confirms the valid and missing anchors.", flush=True)


def reference(path, anchor):
    return {"path": str(path), "anchor": anchor}


def verify_graphify_targets(temporary, audit_sha):
    payload = {
        "repository": REPO, "source_commit": audit_sha, "title": "Rendered navigation audit evidence",
        "features": [
            {
                "id": "directory-and-markdown-fragments", "label": "Rendered README destination evidence",
                "documented_in": [reference("audits/README.md", "## Inspect a repository"),
                                  reference(FIXTURES / "alternate.markdown", "## Available section")],
                "changed_in": [reference("audits/README.md", "## Audit record")],
                "tested_by": [reference("audit/audit_navigation.py", "def check_fragment_coverage(directory):")],
            },
            {
                "id": "named-anchor", "label": "GitHub named anchor evidence",
                "documented_in": [reference(FIXTURES / "named-anchor.md", f'<a name="{CUSTOM_ANCHOR}"></a>')],
                "changed_in": [reference(FIXTURES / "named-anchor.md", "## Generated section")],
                "tested_by": [reference("audit/audit_navigation.py", "def check_named_anchor(directory):")],
            },
        ],
    }
    manifest = temporary / "navigation.json"
    manifest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    output = temporary / "graph"
    verified = run(ROOT, sys.executable, COMPILER, str(manifest), str(output))
    require("Graphify MCP verified" in verified, verified)
    receipt = json.loads((output / "receipt.json").read_bytes())
    require(receipt["source_commit"] == audit_sha and receipt["mcp_verified"], str(receipt))
    print("Graphify control: Both finding nodes, including the exact named-anchor source, passed Graphify MCP.", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-sha", help="Run rendered and Graphify checks against the exact public audit commit")
    args = parser.parse_args()
    with TemporaryDirectory(prefix="readme-hq-rendered-fixtures-") as directory:
        temporary = Path(directory)
        with worktree(temporary / "baseline") as checkout:
            (checkout / FIXTURES).mkdir(parents=True)
            for name in ("alternate.markdown", "named-anchor.md"):
                (checkout / FIXTURES / name).write_bytes((ROOT / FIXTURES / name).read_bytes())
            check_fragment_coverage(checkout)
            check_named_anchor(checkout)
        if args.audit_sha:
            check_rendered_targets(args.audit_sha)
            verify_graphify_targets(temporary, args.audit_sha)


if __name__ == "__main__":
    main()
