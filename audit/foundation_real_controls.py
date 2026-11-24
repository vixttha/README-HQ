"""Replay original foundation cases against the final combined candidate.
All non-README-HQ code is read as pinned Git data, never executed."""
import asyncio,contextlib,hashlib,importlib.util,json,os,re,subprocess,sys,tempfile
from pathlib import Path
from unittest.mock import patch
from urllib.request import Request,urlopen
from html.parser import HTMLParser

ROOT=Path(sys.argv[1]).resolve()
OUT=Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True,exist_ok=True)
CANDIDATE="5adfd75f7a3a5864626bdbebff5d2249c381a975"
os.chdir(ROOT)
sys.path[:0]=[str(ROOT/"tools"),str(ROOT/"graphify-hq/template/v0.0.8")]
from hq_data import GitTree,physical_lines
from hq_navigation import check_document,parse_markdown
import evidence_map as compiler
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module
maps=load("version_maps","graphify-hq/version_maps.py")
intake=load("intake","learning/intake.py")
def require(ok,msg):
    if not ok:raise ValueError(msg)
def git(path,*args):
    return subprocess.check_output(["git","--no-replace-objects","-C",str(path),*args],stderr=subprocess.PIPE)
require(git(ROOT,"rev-parse","HEAD").decode().strip()==CANDIDATE,"wrong candidate")
def commit(path):
    git(path,"add",".")
    git(path,"-c","user.name=Fixture","-c","user.email=fixture@example.invalid","commit","-qm","fixture")
    return git(path,"rev-parse","HEAD").decode().strip()
def clone(path,repo,ref):
    path.mkdir()
    git(path,"init","-q")
    git(path,"remote","add","origin","https://github.com/"+repo+".git")
    git(path,"fetch","--depth=1","--quiet","--no-tags","origin",ref)
    git(path,"checkout","--quiet","--detach",ref)
    require(git(path,"rev-parse","HEAD").decode().strip()==ref,"clone pin")
def get(url):
    req=Request(url,headers={"User-Agent":"README-HQ-public-qualification"})
    with urlopen(req,timeout=35) as response:
        return response.read()
def bart():
    tree=GitTree(ROOT)
    old="f50e3749dab90ddfe35894284d1660097a1fb1a8"
    routes=tree.read("versions/bart-homepages.md").decode()
    index=tree.read("versions/README.md").decode()
    require(index.count("(bart-homepages.md)")==2,"index lost reading routes")
    details=[]
    for snap in json.loads(tree.read("history/sources.json"))["snapshots"]:
        if snap["directory"] not in ("history/bart/published-v0.0.3","history/bart/main-rebrand-v0.0.4"):continue
        repo,ref=snap["repository"],snap["commit"]
        require("https://github.com/"+repo+"/tree/"+ref in routes,"wrong pinned route")
        archived=tree.read(snap["directory"]+"/README.md")
        require(archived==tree.read(snap["directory"]+"/README.md",old),"frozen README changed")
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"source"
            clone(path,repo,ref)
            upstream=GitTree(path)
            require(upstream.read("README.md")==archived,"upstream bytes differ")
            for file in ("CHANGELOG.md","docs/ARCHITECTURE.md","docs/HARNESS.md","SECURITY.md","CONTRIBUTING.md"):
                require(file in upstream.entries(),"relative documentation missing "+file)
            errors,gaps=[],[]
            count=check_document(upstream,"README.md",errors,gaps)
            require(not errors,repr(errors))
            details.append({"commit":ref,"readme_sha256":hashlib.sha256(archived).hexdigest(),"five_reported_targets":True,"checked_local_links":count,"unchecked":len(gaps)})
    require(len(details)==2,"missing archive")
    return {"snapshots":details}
def atomic_batch():
    with tempfile.TemporaryDirectory() as folder:
        out=Path(folder)/"maps"
        out.mkdir()
        call=0
        original=maps.subprocess.run
        def fault(*args,**kwargs):
            nonlocal call
            call+=1
            if call==2:
                raise subprocess.CalledProcessError(1,args[0])
            return original(*args,**kwargs)
        args=[str(ROOT/"graphify-hq/version_maps.py"),"--output",str(out)]
        with patch.object(sys,"argv",args),patch.object(maps.subprocess,"run",side_effect=fault),contextlib.redirect_stderr(open(os.devnull,"w")):
            try:maps.main()
            except SystemExit as error:require(error.code!=0,"unexpected success")
            else:raise ValueError("second map failure was not propagated")
        require(call==2 and not list(out.iterdir()),"partial batch published")
        with patch.object(sys,"argv",args):maps.main()
        expected=set(json.loads((ROOT/"graphify-hq/catalog.json").read_bytes())["versions"])
        require({p.name for p in out.iterdir()}==expected,"retry missing version")
        for directory in out.iterdir():
            receipt=json.loads((directory/"receipt.json").read_bytes())
            require(receipt["mcp_verified"] and hashlib.sha256((directory/"graph.json").read_bytes()).hexdigest()==receipt["graph_sha256"],"retry receipt")
        return {"second_map_fault":True,"retry_maps":len(expected)}
def private_marker():
    marker="SYNTHETIC-PRIVATE-PROBE-DO-NOT-PUBLISH"
    with tempfile.TemporaryDirectory() as folder:
        root=Path(folder);dest=root/"out"
        spec=root/"request.json"
        spec.write_text(json.dumps({"visibility":"private","repository":"fixture/"+marker,"anchor":marker,"target":{"id":marker}}),encoding="utf-8")
        for opts in ([],["--json-errors"]):
            result=subprocess.run([sys.executable,str(ROOT/"learning/intake.py"),str(spec),str(dest),*opts],capture_output=True)
            require(result.returncode!=0 and marker.encode() not in result.stdout+result.stderr and not dest.exists(),"private request leaked or wrote")
    return {"synthetic_private_request_default_and_json_logs_clean":True,"scope":"declared private request, not a proof of every mixed-visibility error path"}
def mcp_limits():
    with tempfile.TemporaryDirectory() as folder:
        tmp=Path(folder);project=tmp/"fixture";project.mkdir()
        git(project,"init","-q");git(project,"config","core.autocrlf","false")
        paths=["audit-fixture/%02d-%s.md"%(i,"x"*216) for i in range(48)]
        paths[0]="audit-fixture/guide [tested_by].md"
        for path in paths:
            p=project/path;p.parent.mkdir(exist_ok=True);p.write_bytes(b"# Fixture\n")
        unicode_path=project/"unicode.md"
        unicode_path.write_bytes("# Introduction\r\nOrdinary text\u2028still one physical line\r\n## 👩‍💻 Setup\r\n## Plain heading\r\n".encode("utf-8"))
        ref=commit(project)
        data={"repository":"example/fixture","source_commit":ref,"title":"Capacity and typed edge control","features":[{"id":"reader","label":"Reader",**{rel:[{"path":p,"anchor":"# Fixture","line":1} for p in paths[i*12:(i+1)*12]] for i,rel in enumerate(("documented_in","changed_in","tested_by","implemented_in"))}},{"id":"physical-lines","label":"Physical lines","documented_in":[{"path":"unicode.md","anchor":"## 👩‍💻 Setup","line":3}],"changed_in":[{"path":"unicode.md","anchor":"## Plain heading","line":4}],"tested_by":[{"path":"unicode.md","anchor":"# Introduction","line":1}]}],"source_files":paths+["unicode.md"]}
        previous=Path.cwd()
        try:
            os.chdir(project)
            manifest=compiler.validate_manifest(data)
            graph,receipt=compiler.build(manifest,tmp/"graph")
            asyncio.run(compiler.verify_mcp(graph,receipt))
            require(sum(receipt["feature_links"]["feature:reader"].values())==48,"capacity mismatch")
            require(all(n==12 for n in receipt["feature_links"]["feature:reader"].values()),"relation count")
            require(any(row[2]==paths[0] and row[0]=="documented_in" for row in receipt["feature_destinations"]["feature:reader"]),"bracketed path lost")
            lines,digest=compiler.source_lines(ref,"unicode.md")
            require(compiler.locate(lines,"## 👩‍💻 Setup","unicode.md")==3 and compiler.locate(lines,"## Plain heading","unicode.md")==4,"physical line mismatch")
            require(digest==hashlib.sha256(unicode_path.read_bytes()).hexdigest(),"raw digest mismatch")
            with patch.object(maps,"ROOT",project):
                checked,line=maps.reference(ref,{"path":"unicode.md","anchor":"## 👩‍💻 Setup","line":3})
                require(line==3 and checked["anchor"]=="## 👩‍💻 Setup","version map line mismatch")
        finally:os.chdir(previous)
        return {"mcp_feature_refs":48,"relations":4,"bracketed_filename":True,"crlf_and_unicode_physical_line":3,"emoji_and_plain_anchors":True}
def real_markup():
    samples=[("psf/requests","3c7baaa05ab4aa49cc819ce3a819d260de19c157","README.md"),("sphinx-doc/sphinx","035a07c32c3241fd3356f4d827800c1f88525272","README.rst"),("asciidoctor/asciidoctor","743f47d5e4d12049744e6d5236ad16cdfb6dca3d","README.adoc")]
    rows=[]
    for repo,ref,path in samples:
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/"source";clone(root,repo,ref)
            tree=GitTree(root)
            with patch.object(maps,"ROOT",root):
                record,line=maps.reference(ref,path)
            raw=tree.read(path)
            require(record["path"]==path and physical_lines(raw.decode())[line-1].strip()==record["anchor"],"selected wrong file/line")
            rows.append({"repo":repo,"commit":ref,"path":path,"line":line,"anchor":record["anchor"],"sha256":hashlib.sha256(raw).hexdigest()})
    return {"sources":rows,"scope":"actual auto-selected source anchors; external application tests not executed"}
class Anchors(HTMLParser):
    def __init__(self):super().__init__();self.ids=set()
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ("id","name"):self.ids.add(v)
def rendered():
    audit="030c72b099f06b83a8f64122ec9bf6ef7f4481ba"
    base="https://github.com/vixttha/README-HQ"
    fixtures={"audit/fixtures/alternate.markdown":"available-section","audit/fixtures/named-anchor.md":"owner-reviewed-quick-start"}
    with tempfile.TemporaryDirectory() as folder:
        root=Path(folder)/"source";clone(root,"vixttha/README-HQ",audit)
        tree=GitTree(root)
        for path,name in fixtures.items():
            body=tree.read(path).decode()
            anchors,_,_=parse_markdown(body)
            require(name in anchors and "audit-fixture-heading-absent" not in anchors,"offline anchor mismatch")
            html=Anchors();html.feed(get(base+"/blob/"+audit+"/"+path).decode())
            require("user-content-"+name in html.ids,"GitHub rendered anchor mismatch")
        # Pinned fixture bytes also exercise the candidate's actual link checker.
        local=Path(folder)/"local";local.mkdir();git(local,"init","-q")
        for path in fixtures:
            p=local/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(tree.read(path))
        (local/"README.md").write_text("# Fixture\n\n[Valid](audit/fixtures/named-anchor.md#owner-reviewed-quick-start)\n[Alternate](audit/fixtures/alternate.markdown#available-section)\n[Missing](audit/fixtures/named-anchor.md#absent)\n",encoding="utf-8")
        commit(local);errors,gaps=[],[]
        count=check_document(GitTree(local),"README.md",errors,gaps)
        require(count==2 and len(errors)==1 and "absent" in errors[0],"link control mismatch: "+repr(errors))
    return {"github_rendered_named_and_alternate":True,"valid_links":2,"missing_link_rejected":True}
checks={}
for key,fn in (("2",bart),("9",atomic_batch),("23",private_marker),("41,48,54,64",mcp_limits),("63",real_markup),("66,67",rendered)):
    try:checks[key]={"status":"passed",**fn()}
    except Exception as error:checks[key]={"status":"failed","detail":str(error)}
    print(json.dumps({key:checks[key]},ensure_ascii=False),flush=True)
report={"candidate":CANDIDATE,"checks":checks,"result":"passed" if all(c["status"]=="passed" for c in checks.values()) else "failed"}
(OUT/"real-controls.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
raise SystemExit(0 if report["result"]=="passed" else 1)
