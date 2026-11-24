"""Measure reproducible document navigation and immutable evidence retrieval.
No adopter programs are executed. Draft commits remain disposable."""
import hashlib,json,os,re,subprocess,sys,tempfile,time
from pathlib import Path
from urllib.parse import unquote,urlsplit
ROOT=Path(sys.argv[1]).resolve()
CONTROL=Path(__file__).resolve().parent
OUT=Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True,exist_ok=True)
plan=json.loads((CONTROL/"adoption-benchmark.json").read_bytes())
sys.path.insert(0,str(ROOT/"tools"))
from hq_data import GitTree,physical_lines
from hq_navigation import parse_markdown,readme_path,target_for
def git(path,*args):
    return subprocess.check_output(["git","--no-replace-objects","-C",str(path),*args],stderr=subprocess.PIPE)
def digest(b):return hashlib.sha256(b).hexdigest()
def links(text):
    # Inspect actual parsed link nodes, not code examples or prose lookalikes.
    tokens=parse_markdown(text)[2]
    return [child.attrGet("href") for tok in tokens for child in (tok.children or [])
            if child.type=="link_open" and child.attrGet("href")]
def route(tree,entry,href,path):
    try:
        u=urlsplit(href)
        if u.netloc:
            parts=unquote(u.path).strip("/").split("/")
            if u.hostname!="github.com" or "/".join(parts[:2]).casefold()!=tree.repository.casefold() or len(parts)<5 or parts[2] not in ("blob","tree"):
                return None
            # Only exact source SHA is accepted as immutable; a main link is
            # counted as visible but not immutable, and other refs need readback.
            target="/".join(parts[4:])
            if target==path:
                if parts[3] in (tree.commit,"main"):return ("pinned" if parts[3]==tree.commit else "moving")
                try:
                    if tree.resolve(parts[3])==tree.commit:return "pinned"
                except ValueError:pass
            return None
        if not u.path:return None
        import posixpath
        target=posixpath.normpath(unquote(u.path).lstrip("/") if u.path.startswith("/") else posixpath.join(posixpath.dirname(entry),unquote(u.path)))
        if target==path:return "selected-tree"
    except (ValueError,AttributeError):return None
def audit(path,ref,profile,name):
    receipt=OUT/(name+".json")
    result=subprocess.run([sys.executable,str(ROOT/"tools/check_readme_hq.py"),"--repo",str(path),"--ref",ref,"--profile",profile,"--receipt",str(receipt)],capture_output=True)
    if not receipt.exists():raise ValueError("missing reader receipt: "+name)
    data=json.loads(receipt.read_bytes())
    return {"exit":result.returncode,"result":data["result"],"entrypoint":data["cases"].get("entrypoint"),"local_links":data["cases"].get("local_links"),"errors":data["errors"],"unchecked":data["unchecked"],"receipt":receipt.name}
def measure(tree,entry,tasks,body):
    found=[]
    hrefs=links(body)
    for task in tasks:
        path=task["path"]
        modes=[m for h in hrefs if (m:=route(tree,entry,h,path))]
        row={**task,"direct_route":bool(modes),"route_modes":sorted(set(modes))}
        if path in tree.entries():
            raw=tree.read(path)
            lines=physical_lines(raw.decode("utf-8"))
            i=next((i for i,line in enumerate(lines,1) if line.strip()),None)
            row["source"]={"commit":tree.commit,"path":path,"blob":tree.entries()[path][1],"sha256":digest(raw),"line":i,"citation":f"https://github.com/{tree.repository}/blob/{tree.commit}/{path}?plain=1#L{i}"}
            row["recoverable"]=i is not None
        else:row["recoverable"]=False
        found.append(row)
    return {"direct_routes":sum(x["direct_route"] for x in found),"recoverable_sources":sum(x["recoverable"] for x in found),"tasks":found}
def checkout(path,repo,ref):
    path.mkdir()
    git(path,"init","-q")
    git(path,"remote","add","origin","https://github.com/"+repo+".git")
    git(path,"fetch","--quiet","--depth=1","--no-tags","origin",ref)
    git(path,"checkout","--quiet","--detach",ref)
    if git(path,"rev-parse","HEAD").decode().strip()!=ref:raise ValueError("source pin")
def compare(task,folder):
    repo,ref=task["repo"],task["commit"]
    path=folder/repo.split("/")[-1]
    checkout(path,repo,ref)
    tree=GitTree(path,ref)
    entry=readme_path(tree.entries(),"",homepage=True)
    if not entry:raise ValueError("no selected README")
    original=tree.read(entry).decode("utf-8")
    before=audit(path,ref,task["profile"],path.name+"-before")
    metrics_before=measure(tree,entry,task["tasks"],original)
    import posixpath
    additions="\n\n## Reader and agent entry points\n\n"
    for item in task["tasks"]:
        target=item["path"]
        if target not in tree.entries():raise ValueError("missing task source "+target)
        additions+=f"- **{item['kind'].replace('_',' ').capitalize()}:** [{item['label']}]({posixpath.relpath(target,posixpath.dirname(entry) or '.')})\n"
    additions+="\nThis review draft adds navigation only. The linked workflow describes checks; it does not certify a passing run.\n"
    draft=original.rstrip()+additions
    (path/entry).write_bytes(draft.encode())
    git(path,"add","--",entry)
    git(path,"-c","user.name=README HQ benchmark","-c","user.email=benchmark@example.invalid","commit","-qm","Disposable navigation draft")
    draft_sha=git(path,"rev-parse","HEAD").decode().strip()
    draft_tree=GitTree(path,draft_sha)
    after=audit(path,draft_sha,task["profile"],path.name+"-after")
    metrics_after=measure(draft_tree,entry,task["tasks"],draft)
    changed=git(path,"diff","--name-only",ref,draft_sha).decode().splitlines()
    unchanged=all(tree.entries()[x["path"]]==draft_tree.entries()[x["path"]] for x in task["tasks"])
    # Source links in the receipt are pinned to the ORIGINAL public SHA, not the local draft.
    for row in metrics_after["tasks"]:
        row["source"]=next(x["source"] for x in metrics_before["tasks"] if x["path"]==row["path"])
    if changed!=[entry] or not unchanged:raise ValueError("draft changed product source")
    (OUT/(path.name+"-draft.md")).write_bytes(draft.encode())
    return {"repo":repo,"base":ref,"draft_local_commit":draft_sha,"only_readme_changed":True,"task_sources_unchanged":True,"before":before,"after":after,"before_metrics":metrics_before,"after_metrics":metrics_after}
rows=[]
with tempfile.TemporaryDirectory(prefix="readme-hq-adoption-") as tmp:
    for target in plan["targets"]:
        started=time.monotonic()
        try:
            row=compare(target,Path(tmp))
            row["status"]="observed"
        except Exception as error:
            row={"repo":target["repo"],"base":target["commit"],"status":"failed","detail":str(error)}
        row["elapsed_seconds"]=round(time.monotonic()-started,3)
        rows.append(row)
        print(json.dumps({k:v for k,v in row.items() if k not in ("before","after","before_metrics","after_metrics")}),flush=True)
# Dogfooding: same candidate checkout used by the validator; compare real main homepage to actual proposed self-use branch.
baseline=git(ROOT,"show",plan["homepage_baseline"]+":README.md").decode()
candidate=git(ROOT,"show","HEAD:README.md").decode()
dog=(CONTROL/"dogfood-homepage.md").read_text(encoding="utf-8")
self_paths=["README-GUIDE.md","AGENTS.md","graphify-hq/README.md","versions/README.md",".github/workflows/readme-hq.yml","learning/README.md"]
self_tree=GitTree(ROOT)
tasks=[{"path":p,"kind":"self-use","label":p} for p in self_paths]
self_use={"main":measure(self_tree,"README.md",tasks,baseline),"candidate":measure(self_tree,"README.md",tasks,candidate),"draft":measure(self_tree,"README.md",tasks,dog),"scope":"Navigation against candidate tree; main is not modified, draft is not published."}
report={"candidate":plan["candidate"],"scope":plan["scope"],"rows":rows,"self_use":self_use,"status":"observed" if all(r["status"]=="observed" for r in rows) else "partial"}
(OUT/"benchmark.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
for row in rows:
    if row["status"]=="observed":
        print(f"{row['repo']}: direct routes {row['before_metrics']['direct_routes']} -> {row['after_metrics']['direct_routes']}; sources {row['after_metrics']['recoverable_sources']}; reader {row['before']['result']} -> {row['after']['result']}")
print("self-use direct routes",self_use["main"]["direct_routes"],self_use["candidate"]["direct_routes"],self_use["draft"]["direct_routes"])
raise SystemExit(0 if report["status"]=="observed" else 1)
