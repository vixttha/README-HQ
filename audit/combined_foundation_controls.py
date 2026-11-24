"""Post-hoc acceptance controls. Never fabricate historical checkpoint evidence."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
CANDIDATE = "5adfd75f7a3a5864626bdbebff5d2249c381a975"
def require(condition, detail):
    if not condition:
        raise ValueError(detail)

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args]).decode().strip()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def new_repo(path):
    path.mkdir()
    git(path, "init", "--quiet")
    git(path, "config", "user.name", "Acceptance fixture")
    git(path, "config", "user.email", "fixture@example.invalid")
    git(path, "config", "core.autocrlf", "false")

def commit(path, message):
    git(path, "add", ".")
    git(path, "commit", "--quiet", "-m", message)
    return git(path, "rev-parse", "HEAD")

def publication_guard():
    # Verify the actual guard string and evaluate its documented input cases.
    # This does not emulate the GitHub Actions scheduler.
    source = (ROOT / ".github/workflows/readme-hq.yml").read_text(encoding="utf-8")
    guards = re.findall(r"    if: >-\n((?:      [^\n]+\n)+)", source)
    expected = "github.event.repository.private == false && github.event.repository.visibility == 'public' && (github.event_name != 'push' || github.ref_name == (vars.README_HQ_PUBLICATION_BRANCH || github.event.repository.default_branch) || github.ref_name == 'readme-hq' || github.ref_name == 'graphify-hq' || startsWith(github.ref_name, 'repair/'))"
    require(len(guards) == 2 and all(" ".join(x.split()) == expected for x in guards), "workflow predicate drift")
    def selected(visibility, private, event, ref, default, configured=""):
        return private is False and visibility == "public" and (event != "push" or ref in (configured or default, "readme-hq", "graphify-hq") or ref.startswith("repair/"))
    cases = []
    for default in ("main", "master", "trunk", "custom-publish"):
        for configured in ("", "owner-publish"):
            for ref in (default, "owner-publish", "unrelated", "readme-hq", "graphify-hq", "repair/test"):
                expected_result = ref in ((configured or default), "readme-hq", "graphify-hq", "repair/test")
                require(selected("public", False, "push", ref, default, configured) == expected_result, "public push case")
                require(selected("public", False, "pull_request", ref, default, configured), "public PR case")
                cases.append({"default":default,"configured":configured,"ref":ref,"push":expected_result,"pr":True})
    for visibility, private in (("private",True),("internal",True),(None,None),("public",True)):
        require(not selected(visibility, private, "push", "main", "main"), "nonpublic push unexpectedly enabled")
        require(not selected(visibility, private, "pull_request", "main", "main"), "nonpublic PR unexpectedly enabled")
    return {"cases":cases,"nonpublic_controls":8,"scope":"source guard and synthetic cases; no live custom-branch or fork PR scheduler events"}

def optimized_verification(base):
    project = base / "synthetic-repo"
    new_repo(project)
    (project / "README.md").write_bytes(b"# Evidence\n")
    sha = commit(project,"Valid evidence")
    blob = git(project,"rev-parse",sha+":README.md")
    loader = "import importlib.util; from pathlib import Path; s=importlib.util.spec_from_file_location('audit_learning', %r); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); m.verify_sources(%r,Path(%r))"
    cases = []
    valid={"repository":"synthetic-repo","commit":sha,"blob":blob,"anchor":"# Evidence","line":1,"status":"observed"}
    for mode in ([],["-O"]):
        for label, value, good in (
            ("valid",valid,True),
            ("wrong blob",dict(valid,blob="0"*40),False),
            ("wrong anchor",dict(valid,anchor="absent evidence"),False),
            ("zero line",dict(valid,line=0),False),
        ):
            code=loader % (str(ROOT/"learning/audit_learning.py"),{"fixture":value},str(base))
            result=subprocess.run([sys.executable,*mode,"-c",code],cwd=ROOT,capture_output=True,text=True)
            if mode:
                require(result.returncode != 0 and "The historical learning audit requires assertions enabled" in result.stderr and "Observed exact README source" not in result.stdout,
                        f"optimized historical verifier did not refuse explicitly: {label}: {result.stderr}")
                outcome="explicit unsupported-mode refusal"
            else:
                require((result.returncode==0)==good and ("Observed exact README source" in result.stdout)==good,
                        f"normal verification mismatch: {label}: {result.stderr}")
                if not good:
                    require("ValueError" in result.stderr,"expected explicit validation failure")
                outcome="verified" if good else "explicit invalid-evidence rejection"
            cases.append({"optimization":bool(mode),"case":label,"returncode":result.returncode,"outcome":outcome})
    return {"cases":cases,"scope":"original learning verify_sources acceptance boundary; not all historical audit assertions"}

def replacement_refs(base):
    project=base/"replacement"
    new_repo(project)
    body=b"# Evidence\nOriginal content.\n"
    replacement=b"Replacement content.\n# Evidence\n"
    (project/"guide.md").write_bytes(body)
    original=commit(project,"Original")
    (project/"guide.md").write_bytes(replacement)
    other=commit(project,"Replacement")
    git(project,"replace",original,other)
    require(git(project,"show",original+":guide.md").startswith("Replacement"),"negative control ineffective")
    sys.path.insert(0,str(ROOT/"tools"))
    sys.path.insert(0,str(ROOT/"graphify-hq/template/v0.0.8"))
    from hq_data import GitTree
    require(GitTree(project,original).read("guide.md")==body,"reader source read changed")
    result={"original_digest":hashlib.sha256(body).hexdigest(),"replacement_digest":hashlib.sha256(replacement).hexdigest(),"reader_original_bytes":True}
    try:
        if os.name == "nt":
            result.update(graphify_scope="not run: vendored dependency hashes are Linux-specific")
        else:
            compiler=load("evidence_map","graphify-hq/template/v0.0.8/evidence_map.py")
            versions=load("version_maps","graphify-hq/version_maps.py")
            prev=Path.cwd()
            try:
                os.chdir(project)
                lines,digest=compiler.source_lines(original,"guide.md")
                require(compiler.locate(lines,"# Evidence","guide.md")==1,"compiler accepted replacement coordinate")
                require(digest==hashlib.sha256(body).hexdigest(),"compiler accepted replacement digest")
                versions.ROOT=project
                require(versions.source_bytes(original,"guide.md")==body,"version map source read changed")
                result.update(compiler_anchor=1,version_builder_original_bytes=True,graphify_scope="real compiler and version-map read paths; no full MCP regeneration")
            finally:
                os.chdir(prev)
    finally:
        git(project,"replace","-d",original)
    return result

def review_pagination():
    module=load("acceptance_provenance","graphify-hq/template/v0.0.8/github_provenance.py")
    results=[]
    repo="vixttha/README-HQ"
    sha="a"*40
    def control(total):
        requests=[]
        def fetch(route):
            if route=="pulls/17":
                return {"number":17,"state":"open","merged":False,"draft":False,"user":{"id":0},"base":{"repo":{"full_name":repo},"ref":"main","sha":"b"*40},"head":{"repo":{"full_name":repo},"ref":"docs/readme","sha":sha}}
            if route.startswith("collaborators/"):
                name=route.split("/")[1]
                return {"user":{"id":int(name[1:])},"permission":"write"}
            require(route.startswith("pulls/17/reviews?per_page=100&page="),route)
            page=int(route.rsplit("=",1)[1])
            requests.append(page)
            end=min(page*100,total)
            items=[{"state":"APPROVED","user":{"id":n,"login":f"u{n}","type":"User"},"commit_id":sha} for n in range((page-1)*100+1,end+1)]
            return module.Page(items,end<total)
        return fetch,requests
    for total in (999,1000,1001):
        fetch,requests=control(total)
        result=module.verify_pull_request(repo,sha,{"number":17,"source_branch":"docs/readme"},fetch)
        require(result["exact_commit_approvals"]==total and result["qualifying_exact_commit_approvals"]==total,"review count mismatch")
        require(requests==list(range(1,(total+99)//100+1)),"incorrect final page handling")
        results.append({"total":total,"pages":len(requests),"exact":result["exact_commit_approvals"]})
    # More pages than the supported observation limit must fail closed.
    try:
        list(module.pages(lambda route: module.Page([{}],True),"reviews"))
    except ValueError as error:
        require("pagination incomplete" in str(error),"wrong cap failure")
    else:
        raise ValueError("unbounded pagination did not fail")
    return {"cases":results,"cap_negative_control":"passed","scope":"synthetic API responses with explicit pagination metadata and eligible reviewers"}

require(git(ROOT,"rev-parse","HEAD")==CANDIDATE,"unexpected candidate SHA")
receipt={"candidate":CANDIDATE,"platform":platform.platform(),"python":sys.version,"run_id":os.environ.get("GITHUB_RUN_ID"),"attempt":os.environ.get("GITHUB_RUN_ATTEMPT"),"cases":{}}
with TemporaryDirectory(prefix="readme-hq-foundation-") as tmp:
    for name,fn in (("17",publication_guard),("31",lambda:optimized_verification(Path(tmp))),("53",lambda:replacement_refs(Path(tmp))),("62",review_pagination)):
        try:
            receipt["cases"][name]={"status":"passed",**fn()}
        except Exception as error:
            receipt["cases"][name]={"status":"failed","detail":str(error)}
receipt["result"]="passed" if all(x["status"]=="passed" for x in receipt["cases"].values()) else "failed"
OUT.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:{x:y for x,y in v.items() if x!="cases"} for k,v in receipt["cases"].items()},indent=2))
raise SystemExit(0 if receipt["result"]=="passed" else 1)
