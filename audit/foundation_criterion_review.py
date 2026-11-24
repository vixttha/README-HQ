"""Focused post-hoc criterion controls; no history rewriting."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
candidate = "0d1fbf4c2d89bad7513f89e618829152a13d53cc"
if subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"]).decode().strip()!=candidate:
    raise ValueError("wrong candidate")
sys.path.insert(0,str(root/"tools"))
from hq_data import GitTree
from check_readme_hq import check_history, check_versions, check_registry
from hq_navigation import PARSER
tree = GitTree(root)
def require(condition, message):
    if not condition:
        raise ValueError(message)
def changed_read(path, body, check, expected):
    original = tree.read
    def read(name, commit=None):
        return body if name == path and commit is None else original(name, commit)
    problems=[]
    with patch.object(tree,"read",side_effect=read):
        check(problems,tree)
    require(any(expected in problem for problem in problems),repr(problems))
def history():
    errors=[]
    require(check_history(errors,tree)==159 and not errors,"unchanged inventory")
    entries=tree.entries()
    path=next(p for p in entries if p.startswith("history/") and p not in {"history/README.md","history/sources.json","history/source-inventory.json"})
    original=tree.entries
    def mode(commit=None):
        result=dict(original(commit))
        if commit is None:
            result[path]=("100755" if result[path][0]=="100644" else "100644",result[path][1])
        return result
    with patch.object(tree,"entries",side_effect=mode):
        errors=[]
        check_history(errors,tree)
    require(any(path in e and "mode" in e for e in errors),"mode-only drift not rejected")
    manifest=json.loads(tree.read("history/sources.json"))
    manifest["snapshots"][0]["commit"]="0"*40
    changed_read("history/sources.json",json.dumps(manifest).encode(),check_history,"independently pinned")
    return {"source_mode_and_manifest_drift_rejected":True}
def versions():
    errors=[]
    check_versions(errors,tree)
    require(not errors,repr(errors))
    entries=tree.entries
    path=next(p for p in entries() if p.startswith("versions/v") and p.endswith("/CHANGELOG.md"))
    def changed(commit=None):
        result=dict(entries(commit))
        if commit is None:
            result[path]=(result[path][0],"0"*40)
        return result
    with patch.object(tree,"entries",side_effect=changed):
        errors=[]
        check_versions(errors,tree)
    require(any(path in e and "frozen" in e for e in errors),"changelog digest drift accepted")
    body=tree.read("versions/README.md").decode()
    row=next(l for l in body.splitlines() if l.startswith("| v0.0.6 |"))
    changed_read("versions/README.md",body.replace(row,row+"\n"+row).encode(),check_versions,"expected one release row")
    return {"frozen_changelog_entry_and_duplicate_row_rejected":True}
def registry():
    path="techniques/registry.json"
    data=json.loads(tree.read(path))
    errors=[]
    check_registry(errors,tree)
    require(not errors,repr(errors))
    case=copy.deepcopy(data);case["schema"]=True
    changed_read(path,json.dumps(case).encode(),check_registry,"integer schema")
    case=copy.deepcopy(data);case["techniques"][0]["aliases"]="invalid"
    changed_read(path,json.dumps(case).encode(),check_registry,"invalid technique fields")
    for status in ("active","retired"):
        case=copy.deepcopy(data);record=copy.deepcopy(case["techniques"][0])
        record.update(id="fixture-duplicate-mechanism",title="Fixture unique title",outcome_key="fixture-unique-outcome",outcome="Fixture unique outcome",aliases=[],status=status)
        case["techniques"].append(record)
        changed_read(path,json.dumps(case).encode(),check_registry,"mechanism duplicates")
    for field in ("id","outcome_key","aliases"):
        case=copy.deepcopy(data);first,second=case["techniques"][:2]
        if field=="id":
            second["aliases"]=[first["id"]]
        elif field=="outcome_key":
            second["outcome_key"]=first["id"]
        else:
            first["aliases"]=["fixture-collision"]
            second["aliases"]=["fixture-collision"]
        changed_read(path,json.dumps(case).encode(),check_registry,"lookup key collision")
    return {"boolean_schema_alias_type_active_retired_duplicates_and_lookup_keys_rejected":True}
def coordinates():
    path="README.md"
    spec=importlib.util.spec_from_file_location("intake",root/"learning/intake.py")
    intake=importlib.util.module_from_spec(spec);spec.loader.exec_module(intake)
    from hq_data import physical_lines
    lines=physical_lines(tree.read(path).decode())
    last=max(i for i,line in enumerate(lines,1) if line.strip())
    for line,anchor in ((1,lines[0]),(last,lines[last-1])):
        result=intake.verify_anchor(tree,path,line,anchor)
        require(result["line"]==line and result["anchor"]==anchor,"valid coordinates not preserved")
    for line,anchor in ((0,"#"),(-1,"#"),(True,"#"),(1,""),(len(lines)+1,"#")):
        try:
            intake.verify_anchor(tree,path,line,anchor)
        except ValueError:
            pass
        else:
            raise ValueError("invalid coordinate accepted")
    return {"first_last_and_five_invalid_cases":True}
def listing():
    import os
    for encoding in ("ascii","utf-8"):
        result=subprocess.run([sys.executable,"tools/check_readme_hq.py","--list"],cwd=root,env={**os.environ,"PYTHONIOENCODING":encoding},capture_output=True)
        require(result.returncode==0 and b"exact-revision-walkthrough [active]" in result.stdout,"listing failed")
    return {"ascii_and_utf8":True}
def outline():
    spec=importlib.util.spec_from_file_location("version_maps",root/"graphify-hq/version_maps.py")
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    record={"title":"A | B","summary":"C | D"}
    text=module.render_outline("v0.0.6","vixttha/README-HQ",{"source_commit":candidate,"nodes":1,"edges":1},[(record,[({"path":"README.md"},1)],({"path":"README.md"},1))])
    rows=PARSER.parse(text)
    inline=[t for t in rows if t.type=="inline"]
    require(any(t.content=="A &#124; B" or t.content=="A | B" for t in inline),"title not escaped/rendered")
    require(sum(t.type=="td_open" for t in rows)==3,"rendered row does not contain three cells")
    return {"rendered_cells":3}
cases={}
for ids,fn in (("3",history),("4,57",versions),("8,20,61",registry),("46",coordinates),("60",listing),("10",outline)):
    try:
        cases[ids]={"status":"passed",**fn()}
    except Exception as error:
        cases[ids]={"status":"failed","detail":str(error)}
report={"candidate":candidate,"cases":cases,"result":"passed" if all(c["status"]=="passed" for c in cases.values()) else "failed"}
out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,indent=2))
raise SystemExit(0 if report["result"]=="passed" else 1)
