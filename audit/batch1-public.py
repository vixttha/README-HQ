"""Bind public Batch 1 verification to the actual repaired Git trees."""
from hashlib import sha1, sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import quote
from urllib.request import Request, urlopen


POINTS = [
    (68, "f8be66616e362202705814fc977c615bd128eca2", None),
    (69, "732861b547b4fc725505ae7b3ce3cc7fb85ac51e", "cannot_vouch"),
    (70, "b094f18500fc4ca8b91e30889fd03a8709b17c97", "smoke_file_checks"),
    (71, "372ec50185b29077071d43320204d8c64405f6d0", "partition"),
    (72, "457a2301ba5b453e9e0251b6bab91db8ca68d95b", "fetched_repository"),
    (73, "f8784358ad4cb9a5d459e7f9386ac233af98f997", "responsive_image"),
    (74, "80c2acb21f91d08727227a099836cc2ed2a7de98", "deleted_draft"),
    (75, "7db8db996cb0dc3dfb44a9589d67c27f86691fcf", "learning_receipt"),
    (76, "f1b074945300a8a28b296a850c7bcd107d26f4e8", "graphify_reader"),
    (77, "a19af307781f0ff223141f790257247bcd3b6d07", "version_rows"),
    (78, "9505ce3bbbbbe38799cfad27d037e012d9b9d9c2", "executing_validator"),
    (79, "f575045d36593dfc32300f79452d5ffb7792a5b6", "registry_snapshot"),
    (80, "f64c6ba4e718b501a4f3e75725bdec1e79a649d4", "root_fragments"),
    (81, "31f49b5e723e791dea81003bc1581d23829b07c8", "wrong_registry"),
    (82, "cf7871eb2af31c6f3da9af3acf92715b388f2868", "broken_inline_links"),
]
BASE = "8d50caec2bc6fcb998994a1fd302294a029325f9"
BRANCH = "repair/v0.0.6-batch-1"
KIT = Path("graphify-hq/template/v0.0.8")


def run(directory, *argv):
    completed = subprocess.run(argv, cwd=directory, check=True, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    print(completed.stdout, end="", flush=True)
    return completed.stdout


def verify_public_sources(checkout):
    rows = json.loads((checkout / "techniques/public-source-inventory.json").read_bytes())
    for repo, commit, path, blob, digest, lines in rows:
        url = f"https://raw.githubusercontent.com/{repo}/{commit}/{quote(path)}"
        with urlopen(Request(url, headers={"User-Agent": "README HQ Batch 1"}), timeout=25) as response:
            content = response.read(1024 * 1024)
        header = f"blob {len(content)}\0".encode()
        actual = (sha1(header + content).hexdigest(), sha256(content).hexdigest(),
                  len(content.removesuffix(b"\n").split(b"\n")) if content else 0)
        if actual != (blob, digest, lines):
            raise ValueError(f"independent source bytes differ at {repo}/{commit}/{path}: {actual}")
    print(f"Independently verified {len(rows)} anonymously accessible pinned public documents", flush=True)
    return len(rows)


def verify_graphify_partition(checkout):
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        fixture = root / "source"
        fixture.mkdir()
        run(fixture, "git", "init", "-q")
        features = []
        for n in range(25):
            refs = []
            for suffix in ("doc", "change", "test"):
                path = f"checkpoint-{n}-{suffix}.md"
                anchor = f"# Checkpoint {n} {suffix}"
                (fixture / path).write_text(anchor + "\n", encoding="utf-8")
                refs.append({"path": path, "anchor": anchor})
            features.append({"id": f"checkpoint-{n}", "label": f"Checkpoint {n}",
                             "documented_in": refs[:1], "changed_in": refs[1:2], "tested_by": refs[2:]})
        run(fixture, "git", "add", ".")
        run(fixture, "git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
            "commit", "-qm", "Graphify partition fixture")
        commit = run(fixture, "git", "rev-parse", "HEAD").strip()
        sys.path.insert(0, str(checkout / "tools"))
        from verify_plan import stage_partitions
        paths = stage_partitions(features, root / "parts", commit, "example/fixture")
        manifests = [json.loads(path.read_bytes()) for path in paths]
        if [feature for manifest in manifests for feature in manifest["features"]] != features:
            raise ValueError("Partitioning changed checkpoint coverage")
        if [len(m["source_files"]) for m in manifests] != [63, 12]:
            raise ValueError("Unexpected source coverage at the partition boundary")
        for path in paths:
            run(fixture, sys.executable, str(checkout / KIT / "evidence_map.py"), str(path), str(path.parent / "graph"))
        return len(paths)


def main():
    checkout, output = map(lambda value: Path(value).resolve(), sys.argv[1:])
    output.mkdir(exist_ok=True)
    receipt = {"run_id": os.environ["GITHUB_RUN_ID"], "attempt": os.environ["GITHUB_RUN_ATTEMPT"],
               "job": os.environ["GITHUB_JOB"], "platform": os.environ["RUNNER_OS"],
               "observer_commit": os.environ["GITHUB_SHA"], "checkpoints": [], "combined": []}

    def capture():
        (output / "results.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    previous = BASE
    for number, sha, case in POINTS:
        print(f"::group::v0.0.6.{number} {sha}", flush=True)
        row = {"checkpoint": f"v0.0.6.{number}", "commit": sha, "parent": previous, "result": "started"}
        receipt["checkpoints"].append(row)
        capture()
        try:
            run(checkout, "git", "checkout", "--detach", sha)
            if run(checkout, "git", "rev-parse", "HEAD", "HEAD^").split() != [sha, previous]:
                raise ValueError("Exact checkpoint or parent differs")
            if number == 68:
                for path in ("README.md", "AGENTS.md"):
                    if BRANCH not in (checkout / path).read_text(encoding="utf-8"):
                        raise ValueError(f"Missing expected trial ref in {path}")
                advertised = run(checkout, "git", "ls-remote", "origin", "refs/heads/" + BRANCH)
                if advertised.split()[0] != POINTS[-1][1]:
                    raise ValueError("Hosted onboarding ref does not identify the reviewed Batch 1 head")
                if "--repo" not in run(checkout, sys.executable, "tools/check_readme_hq.py", "--help"):
                    raise ValueError("Adopter CLI is unavailable")
                run(checkout, sys.executable, "learning/intake.py", "--help")
            elif number == 76 and os.environ["RUNNER_OS"] != "Linux":
                row.update(result="not_applicable", detail="Graphify compiler lock is Linux-only")
                continue
            else:
                pattern = "test_graphify_repairs.py" if number == 76 else "test_readme_repairs.py"
                output_text = run(checkout, sys.executable, "-m", "unittest", "discover",
                                  "-s", "tests", "-p", pattern, "-k", case, "-v")
                if "Ran 0 tests" in output_text:
                    raise ValueError(f"No focused tests matched {case}")
            if number == 69 and os.environ["RUNNER_OS"] == "Linux":
                row["independent_public_sources"] = verify_public_sources(checkout)
            if number == 71 and os.environ["RUNNER_OS"] == "Linux":
                row["graphify_mcp_partitions"] = verify_graphify_partition(checkout)
            row["result"] = "passed"
        except Exception as error:
            row.update(result="failed", detail=str(error))
            if isinstance(error, subprocess.CalledProcessError):
                print(error.stdout or "", end="", flush=True)
            raise
        finally:
            previous = sha
            capture()
            print("::endgroup::", flush=True)

    tasks = [
        ("reader CLI", ("tools/check_readme_hq.py", "--receipt", str(output / "reader.json"))),
        ("reader regressions", ("-m", "unittest", "discover", "-s", "tests", "-p", "test_readme*.py", "-v")),
    ]
    if os.environ["RUNNER_OS"] == "Linux":
        tasks += [("Graphify regressions", ("-m", "unittest", "discover", "-s", "tests", "-p", "test_graphify*.py", "-v")),
                  ("version maps and MCP", ("graphify-hq/version_maps.py", "--check")),
                  ("repair-plan MCP", ("tools/verify_plan.py", "--mcp"))]
    for name, argv in tasks:
        row = {"name": name, "commit": previous, "result": "started"}
        receipt["combined"].append(row)
        try:
            run(checkout, sys.executable, *argv)
            row["result"] = "passed"
        except subprocess.CalledProcessError as error:
            print(error.stdout or "", end="", flush=True)
            row["result"] = "failed"
            raise
        finally:
            capture()


if __name__ == "__main__":
    main()
