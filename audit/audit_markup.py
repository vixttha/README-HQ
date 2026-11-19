"""Probe exact public README sources and Graphify's handling of text evidence."""

from dataclasses import dataclass
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
COMPILER = ROOT / "graphify-hq/template/v0.0.8/evidence_map.py"


@dataclass(frozen=True)
class Source:
    repo: str
    commit: str
    document: tuple[str, str]
    change: tuple[str, str]
    test: tuple[str, str]


SOURCES = (
    Source("psf/requests", "3c7baaa05ab4aa49cc819ce3a819d260de19c157",
           ("README.md", "# Requests"), ("HISTORY.md", "2.34.2 (2026-05-14)"),
           ("tests/test_requests.py", "def test_entry_points(self):")),
    Source("sphinx-doc/sphinx", "035a07c32c3241fd3356f4d827800c1f88525272",
           ("README.rst", "Sphinx"), ("CHANGES.rst", "Release 9.3.0 (in development)"),
           (".github/workflows/main.yml", "run: python -m pytest -n logical --dist=worksteal -vv")),
    Source("asciidoctor/asciidoctor", "743f47d5e4d12049744e6d5236ad16cdfb6dca3d",
           ("README.adoc", "= Asciidoctor"), ("CHANGELOG.adoc", "= Asciidoctor Changelog"),
           ("test/test_helper.rb", "class Minitest::Test")),
)


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def execute(directory, *args):
    return subprocess.run(args, cwd=directory, capture_output=True, encoding="utf-8")


def run(directory, *args):
    result = execute(directory, *args)
    require(result.returncode == 0, result.stdout + result.stderr)
    return result.stdout


def initialize(directory):
    directory.mkdir()
    run(directory, "git", "init", "--quiet")


def fetch_source(directory, source):
    initialize(directory)
    url = f"https://github.com/{source.repo}.git"
    run(directory, "git", "fetch", "--quiet", "--no-tags", "--depth=1", url, source.commit)
    resolved = run(directory, "git", "rev-parse", "FETCH_HEAD").strip()
    require(resolved == source.commit, f"Expected {source.commit}, saw {resolved}")


def read_json(path):
    return json.loads(path.read_bytes())


def compile_graph(directory, temporary, name, manifest):
    path = temporary / f"{name}.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False) + "\n", encoding="utf-8")
    output = temporary / name
    return execute(directory, sys.executable, str(COMPILER), str(path), str(output)), output


def evidence(source_reference):
    path, anchor = source_reference
    return {"path": path, "anchor": anchor}


def explicit_manifest(source):
    return {
        "repository": source.repo,
        "source_commit": source.commit,
        "title": "README evidence portability probe",
        "features": [{
            "id": "readme-evidence", "label": "Public README evidence",
            "documented_in": [evidence(source.document)],
            "changed_in": [evidence(source.change)],
            "tested_by": [evidence(source.test)],
        }],
    }


def check_real_readme_formats(temporary, version_maps):
    auto = []
    manual = []
    checkouts = {}
    for source in SOURCES:
        name = source.repo.rsplit("/", 1)[-1]
        directory = temporary / name
        fetch_source(directory, source)
        checkouts[source.repo] = directory
        version_maps.ROOT = directory
        path = source.document[0]
        try:
            chosen, _ = version_maps.reference(source.commit, path)
        except ValueError as exc:
            require(path.endswith(".rst") and "No unique source anchor" in str(exc), str(exc))
            print(f"C63 sample {source.repo}: automatic heading discovery found no anchor in {path}.", flush=True)
        else:
            if chosen == evidence(source.document):
                auto.append(source.repo)
            else:
                require(path.endswith(".adoc") and chosen["anchor"] == "# or specify the version explicitly",
                        str(chosen))
                print(f"C63 sample {source.repo}: automatic discovery selected a Gemfile comment in {path}.",
                      flush=True)
        result, output = compile_graph(directory, temporary, f"explicit-{name}", explicit_manifest(source))
        require(result.returncode == 0, result.stdout + result.stderr)
        receipt = read_json(output / "receipt.json")
        require(receipt["mcp_verified"] and receipt["source_commit"] == source.commit, str(receipt))
        manual.append(source.repo)
    require(auto == ["psf/requests"] and len(manual) == 3, str((auto, manual)))
    print("C63: Real source probes found the intended README anchor automatically in 1/3 projects. Explicit anchors compiled and passed real Graphify MCP in 3/3.", flush=True)
    return checkouts["psf/requests"]


def check_exact_emoji_anchor(temporary):
    directory = temporary / "emoji"
    initialize(directory)
    plain = "# Maintainer guide"
    emoji = "# \U0001f469\u200d\U0001f4bb Setup guide"
    (directory / "README.md").write_text(f"{plain}\n\n{emoji}\n", encoding="utf-8")
    (directory / "CHANGELOG.md").write_text("- Add the setup guide.\n", encoding="utf-8")
    (directory / "test.py").write_text("def test_setup():\n    return True\n", encoding="utf-8")
    run(directory, "git", "add", "-A")
    run(directory, "git", "-c", "user.name=Audit fixture", "-c", "user.email=audit@example.invalid",
        "commit", "--quiet", "-m", "Add both source headings")
    commit = run(directory, "git", "rev-parse", "HEAD").strip()
    source = Source("vixttha/README-HQ", commit, ("README.md", plain),
                    ("CHANGELOG.md", "- Add the setup guide."), ("test.py", "def test_setup():"))
    control, output = compile_graph(directory, temporary, "plain-anchor", explicit_manifest(source))
    require(control.returncode == 0 and read_json(output / "receipt.json")["mcp_verified"], control.stderr)
    fixture = explicit_manifest(source)
    fixture["features"][0]["documented_in"][0]["anchor"] = emoji
    require(emoji in run(directory, "git", "show", f"{commit}:README.md"), "Emoji heading absent from the pinned blob")
    result, _ = compile_graph(directory, temporary, "joined-emoji-anchor", fixture)
    require(result.returncode != 0 and "Invalid or duplicate source link" in result.stderr, result.stdout + result.stderr)
    print("C64: On the same pinned README, a plain anchor compiled and passed MCP while the exact valid emoji-joined heading was rejected.", flush=True)


def check_release_change_placeholder(temporary, directory, version_maps):
    source = SOURCES[0]
    version_maps.ROOT = directory
    records = [{
        "id": "release-history", "title": "Requests release history probe",
        "summary": "Locate the version-specific changelog entry.",
        "documented_in": [source.document[0]], "changed_in": source.change[0],
    }]
    manifest, outline = version_maps.version_manifest(source.repo, source.commit, "v2.34.2", records)
    actual = manifest["features"][0]["changed_in"][0]
    expected = version_maps.source_bytes(source.commit, source.change[0]).decode("utf-8").splitlines()
    chosen = next(number for number, line in enumerate(expected, 1) if line.strip() == actual["anchor"])
    requested = expected.index(source.change[1]) + 1
    require(chosen < requested and "Short description of non-trivial change" in actual["anchor"], str(actual))
    # Supply a source test reference in this consumer. The release selection above remains intact.
    manifest["features"][0]["tested_by"] = [evidence(source.test)]
    manifest["source_files"].remove(version_maps.CHECKER)
    manifest["source_files"].append(source.test[0])
    result, output = compile_graph(directory, temporary, "release-change-auto", manifest)
    require(result.returncode == 0, result.stdout + result.stderr)
    receipt = read_json(output / "receipt.json")
    rendered = version_maps.render_outline("v2.34.2", source.repo, receipt, outline)
    require(receipt["mcp_verified"] and f"HISTORY.md#L{chosen}" in rendered, rendered)
    print(f"C65: Requests v2.34.2 selects the unreleased placeholder at line {chosen}, before the release heading at line {requested}; Graphify MCP passes.", flush=True)


def main():
    module_path = ROOT / "graphify-hq/version_maps.py"
    spec = importlib.util.spec_from_file_location("version_maps", module_path)
    version_maps = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(version_maps)
    with TemporaryDirectory(prefix="readme-hq-markup-probes-") as temp:
        temporary = Path(temp)
        requests = check_real_readme_formats(temporary, version_maps)
        check_exact_emoji_anchor(temporary)
        check_release_change_placeholder(temporary, requests, version_maps)


if __name__ == "__main__":
    main()
