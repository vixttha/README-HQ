"""Verify actual merge trees and adoption on isolated public runner checkouts."""
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT=Path(sys.argv[1]).resolve()
OUT=Path(sys.argv[2]).resolve()
OUT.mkdir()
FINAL="95a54600184d7b95235fc401eb26797cf4ab5b57"
BASE="a7a989ffb6b664df86aae0ea01053ea2fc0a4405"
STAGES=[
(68,"8d50caec2bc6fcb998994a1fd302294a029325f9","40db6461815c1c6b0b40378f5f9de1722e68afee"),
(141,"774bf783850162f731f3e38aff0f52b99a5202fc","acdd088c2919b8577acc93356eb2104cfeccefc7"),
(142,"941f6b49aac6ab78076f088ad6b58a00e9f03477","fa37682ee7f9b236bc92ed6f579efbbd2a453f2d"),
(144,"dc8ef21763240168227d67445f02fc4a05ea071c","6721377b9048ed58afb535b87da15a2fa614a029"),
(145,"921609e7a037d0ca37c66d8ef6438642cbeb17ea","c2bc1583be55ce8bc1123c2aec1525a66de4ecbc"),
(151,"d12d5c6bd82fe448f64adb3ae48024296b8e6db4","ada5ebf8f93b94bedd6236b510f2ff8afb789c44"),
]
report={"candidate":FINAL,"control_sha":os.environ.get("GITHUB_SHA"),"run_id":os.environ.get("GITHUB_RUN_ID"),"attempt":os.environ.get("GITHUB_RUN_ATTEMPT"),"platform":platform.platform(),"checks":{}}
def require(condition,msg):
    if not condition:
        raise ValueError(msg)
def run(args,cwd=ROOT,expected=0,env=None):
    result=subprocess.run(args,cwd=cwd,env=env,text=True,encoding="utf-8",errors="replace",capture_output=True)
    print(result.stdout,end="")
    print(result.stderr,end="",file=sys.stderr)
    if expected is not None:
        require(result.returncode==expected,f"{args[0]} exited {result.returncode}, expected {expected}")
    return result
def git(*args,cwd=ROOT):
    return subprocess.check_output(["git","--no-replace-objects",*args],cwd=cwd).decode("utf-8").strip()
def check(name,fn):
    try:
        report["checks"][name]={"status":"passed",**fn()}
    except Exception as error:
        report["checks"][name]={"status":"failed","detail":str(error)}
    (OUT/"summary.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
def merge_proof():
    require(git("rev-parse","HEAD")==FINAL,"unexpected candidate")
    rows=[]
    previous=BASE
    for n,source,merge in STAGES:
        parents=git("show","-s","--format=%P",merge).split()
        require(parents==[previous,source],f"PR {n} parents")
        tree=git("rev-parse",source+"^{tree}")
        require(tree==git("rev-parse",merge+"^{tree}"),f"PR {n} tree")
        computed=git("merge-tree","--write-tree",previous,source)
        require(computed==tree,f"PR {n} independently calculated merge tree differs")
        rows.append({"pr":n,"source":source,"merge":merge,"tree":tree})
        previous=merge
    require(git("show","-s","--format=%P",FINAL)==previous,"route correction parent")
    require(set(git("diff","--name-only",previous,FINAL).splitlines())=={"README.md","AGENTS.md"},"unexpected product diff")
    return {"stages":rows,"final_change":"README.md and AGENTS.md only"}
def reader():
    path=OUT/"reader.json"
    run([sys.executable,"tools/check_readme_hq.py","--receipt",str(path)])
    data=json.loads(path.read_bytes())
    require(data["commit"]==FINAL and data["result"]=="passed","reader receipt mismatch")
    tests=run([sys.executable,"-m","unittest","discover","-s","tests","-p","test_readme*.py","-v"])
    (OUT/"reader-tests.txt").write_text(tests.stdout+tests.stderr,encoding="utf-8")
    return {"cases":data["cases"],"unchecked":len(data.get("unchecked",[]))}
def graphify():
    if os.name=="nt":
        return {"coverage":"not applicable: Linux-only pinned Graphify environment"}
    env=os.environ.copy()
    # The report names the exact checked-out tree, not the separate harness commit.
    env["GITHUB_SHA"]=FINAL
    run([sys.executable,"tools/verify_graphify_ci.py",str(OUT/"graphify")],env=env)
    receipt=json.loads((OUT/"graphify/attempt.json").read_bytes())
    require(receipt["commit"]==FINAL and receipt["result"]=="passed","Graphify receipt mismatch")
    return {"steps":[x["name"] for x in receipt["steps"]],"maps":sum(len(x["verified_receipts"]) for x in receipt["steps"])}
def adopt():
    with TemporaryDirectory(prefix="readme-hq-adoption-") as folder:
        temp=Path(folder)
        # Actual published trial instructions: resolve the branch, detach at the approved trial SHA.
        trial=temp/"trial"
        run(["git","clone","--branch","repair/v0.0.6-batch-5","https://github.com/vixttha/README-HQ.git",str(trial)])
        run(["git","checkout","--detach",STAGES[-1][1]],cwd=trial)
        run([sys.executable,"tools/check_readme_hq.py","--receipt",str(OUT/"documented-trial.json")],cwd=trial)
        trial_receipt=json.loads((OUT/"documented-trial.json").read_bytes())
        require(trial_receipt["commit"]==STAGES[-1][1] and trial_receipt["result"]=="passed","trial pin mismatch")
        demo=temp/"demo"
        run([sys.executable,"examples/first_action_demo.py",str(demo)])
        for name,expected in (("passing","passed"),("failing","failed"),("url-unchecked","unchecked")):
            data=json.loads((demo/(name+".json")).read_bytes())
            require(data["cases"]["first_action"]["result"]==expected,"example outcome mismatch")
            (OUT/("demo-"+name+".json")).write_bytes((demo/(name+".json")).read_bytes())
        plain=temp/"plain"
        plain.mkdir()
        run(["git","init","--quiet"],cwd=plain)
        (plain/"README.md").write_text("# Sample app\n\nA small synthetic app with a reproducible first command.\n\n## Quickstart\n\n"+chr(96)*3+"sh\npython run.py\n"+chr(96)*3+"\n",encoding="utf-8")
        (plain/"run.py").write_text("print('adoption ready')\n",encoding="utf-8")
        run(["git","add","."],cwd=plain)
        run(["git","-c","user.name=Fixture","-c","user.email=fixture@example.invalid","commit","-qm","adoption fixture"],cwd=plain)
        sha=git("rev-parse","HEAD",cwd=plain)
        spec=temp/"smoke.json"
        spec.write_text(json.dumps({"commit":sha,"argv":[sys.executable,"run.py"],"expected":{"exit":0,"contains":"adoption ready"}}),encoding="utf-8")
        run([sys.executable,"tools/check_readme_hq.py","--repo",str(plain),"--ref",sha,"--smoke",str(spec),"--require-smoke","--receipt",str(OUT/"plain-adoption.json")])
        data=json.loads((OUT/"plain-adoption.json").read_bytes())
        require(data["commit"]==sha and data["cases"]["first_action"]["result"]=="passed","plain adoption mismatch")
    return {"documented_trial":STAGES[-1][1],"plain_required_smoke":"passed","monorepo_example":"pass/fail/unchecked distinguished"}
def external():
    observations=[]
    with TemporaryDirectory(prefix="readme-hq-public-targets-") as folder:
        for label,repo,sha in (
            ("aldervale","vixttha/AlderVale-Pact-of-Ten","5a7d0438e46582e625fc101efb6aa0f9e637c55e"),
            ("bart","vixttha/Blender-Agent-Refinement-Toolkit","3e7f9e02e61739825b56bcafecebbd0221cc9657"),
        ):
            target=Path(folder)/label
            target.mkdir()
            run(["git","init","--quiet"],cwd=target)
            run(["git","remote","add","origin","https://github.com/"+repo+".git"],cwd=target)
            run(["git","fetch","--quiet","--depth=1","origin",sha],cwd=target)
            run(["git","checkout","--detach",sha],cwd=target)
            path=OUT/(label+"-readonly.json")
            result=run([sys.executable,"tools/check_readme_hq.py","--repo",str(target),"--ref",sha,"--receipt",str(path)],expected=None)
            require(result.returncode in (0,1,2) and path.is_file(),"target audit did not return a classified receipt")
            data=json.loads(path.read_bytes())
            require(data["commit"]==sha and data["cases"]["entrypoint"],"target receipt mismatch")
            observations.append({"repository":repo,"commit":sha,"exit":result.returncode,"result":data["result"],"entrypoint":data["cases"]["entrypoint"],"errors":data.get("errors",[]),"scope":"read-only documentation audit; no target code executed"})
    return {"observations":observations,"scope":"successful audit execution does not imply a target README passed"}
def publication():
    result=run([sys.executable,"tools/check_publication_rules.py","vixttha/README-HQ","main","--require-check","README HQ on ubuntu-latest","--require-check","README HQ on windows-latest","--require-check","Recoverable Graphify evidence and plan"],expected=None)
    data=json.loads(result.stdout)
    (OUT/"publication-observation.json").write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    require(result.returncode in (0,2),"publication observer execution error")
    return {"observation":data,"scope":"read-only; no settings changed"}
for name,fn in (("merge",merge_proof),("reader",reader),("graphify",graphify),("adoption",adopt),("external",external),("publication",publication)):
    check(name,fn)
report["result"]="passed" if all(x["status"]=="passed" for x in report["checks"].values()) else "failed"
(OUT/"summary.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,indent=2))
raise SystemExit(0 if report["result"]=="passed" else 1)
