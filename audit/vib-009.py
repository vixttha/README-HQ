import contextlib,hashlib,importlib.util,json,os,subprocess,sys,tempfile
from pathlib import Path
from unittest.mock import patch
root=Path.cwd()
def need(ok,msg):
    if not ok: raise RuntimeError(msg)
need(subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()=="79619d43bc04ccc49097e62058fd3dc0653dd672","candidate mismatch")
sys.path[:0]=[str(root/"tools"),str(root/"graphify-hq/template/v0.0.8")]
spec=importlib.util.spec_from_file_location("version_maps",root/"graphify-hq/version_maps.py")
maps=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=maps
spec.loader.exec_module(maps)
with tempfile.TemporaryDirectory() as folder:
    out=Path(folder)/"maps"
    out.mkdir()
    call=0
    original=maps.subprocess.run
    def fault(*args,**kwargs):
        global call
        call+=1
        if call==2:
            raise subprocess.CalledProcessError(1,args[0])
        return original(*args,**kwargs)
    args=[str(root/"graphify-hq/version_maps.py"),"--output",str(out)]
    with patch.object(sys,"argv",args),patch.object(maps.subprocess,"run",side_effect=fault),open(os.devnull,"w") as sink,contextlib.redirect_stderr(sink):
        try: maps.main()
        except SystemExit as error: need(error.code!=0,"unexpected success")
        else: raise RuntimeError("second map failure not propagated")
    need(call==2 and not list(out.iterdir()),"partial batch published")
    with patch.object(sys,"argv",args): maps.main()
    expected=set(json.loads((root/"graphify-hq/catalog.json").read_bytes())["versions"])
    need({p.name for p in out.iterdir()}==expected,"retry missing version")
    result=[]
    for directory in sorted(out.iterdir()):
        receipt=json.loads((directory/"receipt.json").read_bytes())
        need(receipt["mcp_verified"] and hashlib.sha256((directory/"graph.json").read_bytes()).hexdigest()==receipt["graph_sha256"],"retry receipt")
        result.append({"version":directory.name,"graph_sha256":receipt["graph_sha256"],"mcp_verified":True})
    # A completed destination must be rejected without changes.
    old={str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob("*") if p.is_file()}
    with patch.object(sys,"argv",args),open(os.devnull,"w") as sink,contextlib.redirect_stderr(sink):
        try: maps.main()
        except SystemExit as error: need(error.code!=0,"occupied output accepted")
        else: raise RuntimeError("occupied output accepted")
    need(old=={str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob("*") if p.is_file()},"completed destination modified")
receipt={"issue":9,"version":"v0.0.6.9","candidate":"79619d43bc04ccc49097e62058fd3dc0653dd672","vib_claim":"a6731914adb1c7a4680e4c281ae5de09fc025ea3","run":os.environ["GITHUB_RUN_ID"],"attempt":os.environ["GITHUB_RUN_ATTEMPT"],"second_map_failure_propagated":True,"no_partial_output":True,"retry_maps":result,"occupied_destination_preserved":True}
print(json.dumps(receipt,indent=2))
Path(sys.argv[1]).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
