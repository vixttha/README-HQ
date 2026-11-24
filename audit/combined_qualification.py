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
FINAL="5adfd75f7a3a5864626bdbebff5d2249c381a975"
COMBINED="0d1fbf4c2d89bad7513f89e618829152a13d53cc"
REHEARSAL="95a54600184d7b95235fc401eb26797cf4ab5b57"
CATALOG_FIX="90c2944f9c293313af42042fa9a782a69f4e431b"
CATALOG="88feb6971d2f49c530535f09d0defb1e9e1808bf"
POLICY="b1bbc9a72a5193afcaeaf823f097753070bfa43f"
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
    require(git("show","-s","--format=%P",REHEARSAL)==previous,"route correction parent")
    require(git("show","-s","--format=%P",COMBINED).split()==[REHEARSAL,CATALOG_FIX],"combined parents")
    run(["git","merge-base","--is-ancestor",COMBINED,FINAL])
    require(set(git("diff","--name-only",COMBINED,FINAL).splitlines())=={"README.md","AGENTS.md","techniques/README.md","learning/audit_learning.py","tests/test_readme_repairs.py"},"unexpected follow-up paths")
    require(git("merge-tree","--write-tree",FINAL,CATALOG_FIX)==git("rev-parse",FINAL+"^{tree}"),"catalog still conflicts")
    require(not git("diff","--name-only",STAGES[-1][1],FINAL,"--","history/","versions/","evidence/"),"frozen material changed")
    return {"stages":rows,"catalog_parent":CATALOG_FIX,"combined_tree":git("rev-parse",FINAL+"^{tree}"),"frozen_material_unchanged":True}
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
        run(["git","clone","--branch","repair/v0.0.6-integration-candidate","https://github.com/vixttha/README-HQ.git",str(trial)])
        run(["git","checkout","--detach",FINAL],cwd=trial)
        run([sys.executable,"tools/check_readme_hq.py","--receipt",str(OUT/"documented-trial.json")],cwd=trial)
        trial_receipt=json.loads((OUT/"documented-trial.json").read_bytes())
        require(trial_receipt["commit"]==FINAL and trial_receipt["result"]=="passed","trial pin mismatch")
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
    return {"documented_trial":FINAL,"plain_required_smoke":"passed","monorepo_example":"pass/fail/unchecked distinguished"}
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
def live_catalog_and_policy():
    import importlib.util
    from hashlib import sha256
    import re
    from urllib.error import HTTPError
    def blob(ref,path):
        return subprocess.check_output(["git","--no-replace-objects","show",ref+":"+path],cwd=ROOT)
    require(blob(FINAL,"ENGINEERING-LAWS.md")==blob(POLICY,"ENGINEERING-LAWS.md"),"law source drift")
    for name in ("README.md","AGENTS.md"):
        actual=blob(FINAL,name).decode()
        original=blob(POLICY,name).decode()
        marker=r"<!-- agent-capability:v1\n(.*?)\n-->"
        observed=re.findall(marker,actual,re.S)
        expected=re.findall(marker,original,re.S)
        require(observed==expected and len(observed)==1,"discovery marker drift: "+name)
        metadata=json.loads(observed[0])
        require(metadata["required_ecosystem_tools"]==[] and metadata["authority"]=="owner" and metadata["discovery"]=="read-only","capability authority drift")
    law=r"<!-- engineering-laws:start -->.*?<!-- engineering-laws:end -->"
    require(re.findall(law,blob(FINAL,"AGENTS.md").decode(),re.S)==re.findall(law,blob(POLICY,"AGENTS.md").decode(),re.S),"law block drift")
    loader=importlib.util.spec_from_file_location("intake",ROOT/"learning/intake.py")
    intake=importlib.util.module_from_spec(loader)
    loader.loader.exec_module(intake)
    with TemporaryDirectory(prefix="readme-hq-live-catalog-") as folder:
        catalog=Path(folder)/"catalog"
        run(["git","clone","--quiet","--branch","README-Technique-Library","https://github.com/vixttha/README-HQ.git",str(catalog)])
        run(["git","checkout","--detach",CATALOG],cwd=catalog)
        source={"id":"sample","checkout":str(ROOT),"ref":FINAL,"repository":"vixttha/README-HQ","path":"README.md","line":1,"anchor":"# README HQ","visibility":"public"}
        finding={"source":"sample","decision":"adapt","rationale":"Synthetic qualification of catalog integration; not an adopter decision."}
        request={"visibility":"public","catalog":{"checkout":str(catalog),"commit":CATALOG},"sources":[source],"selected":["sample"],"target":{**source,"audience":"reader","capability":"test"},"findings":[{**finding,"technique":"relative-navigation"},{**finding,"combination":"pinned-walkthrough-with-evidence"}]}
        def fetch(route):
            # Authenticated read-only GET on the public repository, no token output.
            result=subprocess.run(["gh","api","--method","GET","repos/"+route],cwd=ROOT,capture_output=True)
            if result.returncode != 0:
                if b"HTTP 404" in result.stderr:
                    raise HTTPError("https://api.github.com/repos/"+route,404,"Not Found",{},None)
                raise RuntimeError("unexpected GitHub API failure in qualification")
            return json.loads(result.stdout)
        path=intake.record_intake(request,OUT/"catalog",fetch=fetch)
        data=json.loads(path.read_bytes())
        require(data["schema"]==2 and data["catalog"]["commit"]==CATALOG,"catalog receipt pin")
        require(data["target"]["commit"]==FINAL and data["target"]["anchor"]=="# README HQ","target anchor pin")
        rows=data["recommendations"]
        technique=next(row for row in rows if row.get("technique")=="relative-navigation")
        combo=next(row for row in rows if row.get("combination")=="pinned-walkthrough-with-evidence")
        require(len(combo["catalog_record"]["steps"])==5,"ordered combination")
        require(technique["catalog_record"]["sha256"]==sha256(subprocess.check_output(["git","--no-replace-objects","show",CATALOG+":techniques/relative-navigation.md"],cwd=catalog)).hexdigest(),"record digest")
        (catalog/"techniques/relative-navigation.md").write_text("changed working tree",encoding="utf-8")
        require(intake.record_intake(request,OUT/"catalog",fetch=fetch)==path,"catalog working tree changed receipt")
        for bad in ({k:v for k,v in request.items() if k!="catalog"},
                    {**request,"catalog":{"checkout":str(ROOT),"commit":FINAL}}):
            try:
                intake.record_intake(bad,OUT/"catalog",fetch=fetch)
            except ValueError:
                pass
            except HTTPError as error:
                require(error.code==404 and "catalog" in bad,"unexpected API failure on negative control")
            else:
                raise ValueError("missing or off-branch catalog accepted")
        require(len(list((OUT/"catalog").iterdir()))==1,"invalid intake wrote a receipt")
    return {"catalog":CATALOG,"schema":2,"ordered_steps":combo["catalog_record"]["steps"],"policy_source":POLICY,"law_and_discovery_parity":True,"scope":"live public catalog and pinned Git reads; not autonomous agent certification"}

def approved_pin():
    import re
    if os.name=="nt":
        return {"coverage":"POSIX documentation guard, tested on Ubuntu; Windows reader validated separately"}
    readme=(ROOT/"README.md").read_text(encoding="utf-8")
    command=re.search(r"```sh\n(git clone --branch repair/v0\.0\.6-integration-candidate[^\n]*\n[\s\S]*?)\n```",readme)
    require(command is not None,"documented trial missing")
    command=command.group(1)
    require("git checkout --detach \"$approved_sha\"" in command and "git checkout --detach HEAD" not in command,"unpinned checkout")
    with TemporaryDirectory(prefix="pin-check-") as folder:
        temp=Path(folder)
        env=os.environ.copy()
        env["PATH"]=str(temp)+os.pathsep+env["PATH"]
        env["PIN_EXPECTED"]=FINAL
        env["PIN_LOG"]=str(temp/"calls")
        fake=temp/"git"
        fake.write_text("#!/bin/sh\ncase \"$1\" in\nclone) mkdir -p README-HQ;;\ncheckout) [ \"$3\" = \"$PIN_EXPECTED\" ];;\nrev-parse) printf '%s\\n' \"${PIN_ACTUAL:-$PIN_EXPECTED}\";;\n*) exit 1;;\nesac\n",encoding="utf-8")
        fake.chmod(0o755)
        python=temp/"python3"
        python.write_text("#!/bin/sh\nprintf '%s\\n' \"$*\" >> \"$PIN_LOG\"\n",encoding="utf-8")
        python.chmod(0o755)
        for label,approved,actual,expected in (("placeholder","REPLACE_WITH_APPROVED_40_CHARACTER_SHA",FINAL,1),("wrong","a"*40,FINAL,1),("moved",FINAL,"b"*40,1),("correct",FINAL,FINAL,0)):
            work=temp/label;work.mkdir()
            env["PIN_ACTUAL"]=actual
            log=temp/"calls"
            if log.exists():log.unlink()
            result=subprocess.run(["sh","-c",command.replace("REPLACE_WITH_APPROVED_40_CHARACTER_SHA",approved)],cwd=work,env=env,capture_output=True)
            require(result.returncode==expected,"unexpected pin control "+label)
            require(log.exists()==(expected==0),"installation ran for rejected SHA "+label)
        return {"guard_cases":4,"rejected_before_install":3}

for name,fn in (("approved_pin",approved_pin),("catalog_policy",live_catalog_and_policy),("merge",merge_proof),("reader",reader),("graphify",graphify),("adoption",adopt),("external",external),("publication",publication)):
    check(name,fn)
report["result"]="passed" if all(x["status"]=="passed" for x in report["checks"].values()) else "failed"
(OUT/"summary.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,indent=2))
raise SystemExit(0 if report["result"]=="passed" else 1)
