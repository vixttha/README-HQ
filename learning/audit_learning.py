"""Reproduce v0.0.6 learning gaps and verify a source-backed tailoring pilot."""

import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


if not __debug__:
    raise RuntimeError("The historical learning audit requires assertions enabled. Use learning/intake.py for current receipts.")


BASELINE = "f50e3749dab90ddfe35894284d1660097a1fb1a8"
ROOT = Path(__file__).resolve().parents[1]


def git(directory, *args):
    return subprocess.check_output(["git", "-C", str(directory), *args], stderr=subprocess.PIPE)


def checker(directory, cwd=None):
    result = subprocess.run(
        [sys.executable, str(directory / "tools/check_readme_hq.py"), "--list"],
        cwd=cwd or directory, text=True, capture_output=True,
        env={**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"},
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


def check_evidence_binding(worktree, registry, original):
    trial = deepcopy(original)
    trial["techniques"][0]["evidence"] = [{
        "url": "https://example.invalid/nonexistent-source",
        "status": "verified",
    }]
    registry.write_text(json.dumps(trial), encoding="utf-8")
    checker(worktree)
    print("L18: A nonexistent URL asserted as verified passed the registry gate.")


def check_evidence_identity(worktree, registry, original):
    trial = deepcopy(original)
    evidence = trial["techniques"][0]["evidence"]
    same_file = evidence[0]["url"]
    evidence.extend([
        {"url": same_file + "#L1", "status": "observed"},
        {"url": same_file + "?view=1", "status": "observed"},
    ])
    registry.write_text(json.dumps(trial), encoding="utf-8")
    checker(worktree)
    print("L19: Fragment and query variants of one evidence file passed as separate entries.")


def check_duplicate_mechanism(worktree, registry, original):
    trial = deepcopy(original)
    duplicate = deepcopy(trial["techniques"][0])
    duplicate.update({
        "id": "alternate-audit-technique",
        "title": "Different audit label",
        "aliases": [],
        "outcome_key": "different-audit-key",
        "outcome": "Alternate wording for the same reader action.",
    })
    trial["techniques"].append(duplicate)
    registry.write_text(json.dumps(trial), encoding="utf-8")
    checker(worktree)
    print("L20: Identical problem, practice, and evidence passed under new record names and outcome wording.")


def check_public_scope(worktree, registry, original):
    trial = deepcopy(original)
    trial["techniques"][0]["evidence"] = [{
        "url": "https://example.invalid/synthetic-private-learning-marker",
        "status": "observed",
        "visibility": "private",
    }]
    registry.write_text(json.dumps(trial), encoding="utf-8")
    checker(worktree)
    print("L23: The public registry gate accepted an evidence fixture explicitly marked private.")


def check_workflow_gaps(worktree, temporary):
    help_output = subprocess.check_output(
        [sys.executable, str(worktree / "tools/check_readme_hq.py"), "--help"], text=True,
    )
    assert "--list" in help_output
    assert all(x not in help_output for x in ("--intake", "--source", "--target", "--learn"))
    assert not (worktree / "learning").exists()
    print("L21: The baseline has a guide and registry but no learning intake or promotion record.")
    first, second = temporary / "game", temporary / "template"
    first.mkdir()
    second.mkdir()
    assert checker(worktree, first) == checker(worktree, second)
    print("L22: The public technique listing carries no target context or scoped recommendation receipt.")
    names = {p.name.upper() for p in worktree.iterdir() if p.is_file()}
    assert not any(x.startswith(("LICENSE", "LICENCE", "COPYING", "NOTICE")) for x in names)
    assert (worktree / "history/bart/published-v0.0.3/LICENSE").is_file()
    print("L24: The standalone branch has no top-level license or reuse notice. A license under history belongs to an imported source.")


def audit_baseline():
    with TemporaryDirectory(prefix="readme-hq-learning-audit-") as tmp:
        temporary = Path(tmp)
        worktree = temporary / "baseline"
        git(ROOT, "--no-replace-objects", "worktree", "add", "--quiet", "--detach", str(worktree), BASELINE)
        try:
            registry = worktree / "techniques/registry.json"
            original_bytes = registry.read_bytes()
            original = json.loads(original_bytes)
            checker(worktree)
            check_evidence_binding(worktree, registry, original)
            check_evidence_identity(worktree, registry, original)
            check_duplicate_mechanism(worktree, registry, original)
            check_public_scope(worktree, registry, original)
            registry.write_bytes(original_bytes)
            check_workflow_gaps(worktree, temporary)
        finally:
            git(ROOT, "worktree", "remove", "--force", str(worktree))


def verify_sources(sources, directory=None):
    local = directory is not None
    with TemporaryDirectory(prefix="readme-hq-learning-sources-") as temp:
        base = directory if local else Path(temp)
        for source in sources.values():
            name, commit = source["repository"], source["commit"]
            if len(commit) != 40 or any(char not in "0123456789abcdef" for char in commit):
                raise ValueError("learning evidence needs an exact source commit")
            line, anchor = source["line"], source["anchor"]
            if type(line) is not int or line < 1 or not isinstance(anchor, str) or not anchor.strip():
                raise ValueError("learning evidence needs a positive line and nonempty anchor")
            project = base / name
            if not local:
                project.mkdir()
                git(project, "init", "--quiet")
                git(project, "fetch", "--quiet", "--depth=1", f"https://github.com/vixttha/{name}.git", commit)
            actual = git(project, "--no-replace-objects", "rev-parse", f"{commit}:README.md").decode().strip()
            if actual != source["blob"]:
                raise ValueError("learning source blob does not match the pinned evidence")
            lines = git(project, "--no-replace-objects", "show", f"{commit}:README.md").decode().split("\n")
            if line > len(lines) or anchor not in lines[line - 1] or source["status"] != "observed":
                raise ValueError("learning source anchor or observation status does not match")
            print(f"Observed exact README source for {name} at {commit[:7]} line {source['line']}.")


def recommendations(pilot, target, selected_sources):
    # This historical pilot uses only the curated pinned profiles and evidence.
    baseline = json.loads((ROOT / "learning/pilot.json").read_bytes())
    if target not in baseline["targets"].values():
        return []
    evidence = target.get("evidence")
    if evidence not in baseline["sources"] or pilot["sources"].get(evidence) != baseline["sources"][evidence]:
        return []
    active = {
        record["id"] for record in json.loads((ROOT / "techniques/registry.json").read_bytes())["techniques"]
        if record["status"] == "active"
    }
    return [
        {"technique": t["id"], "status": t["status"], "source": t["source"],
         "recommendation": t["recommendation"]}
        for t in pilot["techniques"]
        if t["profile"] == target["profile"] and t["source"] in selected_sources
        and (t["status"] == "candidate" or t["id"] in active)
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local-sources", type=Path, help="Use existing clones for the pinned public sources")
    args = parser.parse_args()
    audit_baseline()
    pilot = json.loads((ROOT / "learning/pilot.json").read_bytes())
    verify_sources(pilot["sources"], args.local_sources)
    game, template = pilot["targets"]["AlderVale"], pilot["targets"]["Lydite"]
    all_sources = set(pilot["sources"])
    game_result = recommendations(pilot, game, all_sources)
    template_result = recommendations(pilot, template, all_sources)
    assert [x["technique"] for x in game_result] == ["state-scope-documentation"]
    assert [x["technique"] for x in template_result] == ["clean-consumer-adoption"]
    assert recommendations(pilot, game, all_sources - {"aldervale-state"}) == []
    assert recommendations(pilot, template, all_sources - {"brand-adoption"}) == []
    print(json.dumps({"AlderVale": game_result, "Lydite": template_result}, indent=2))
    print("Pilot verified target-specific results and source selection sensitivity.")


if __name__ == "__main__":
    main()
