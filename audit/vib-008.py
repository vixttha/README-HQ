import json, os, subprocess, sys, hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
root=Path.cwd()
def git(*args):
    return subprocess.check_output(["git",*args], text=True).strip()
def need(ok,msg):
    if not ok: raise RuntimeError(msg)
need(git("rev-parse","HEAD")=="79619d43bc04ccc49097e62058fd3dc0653dd672","candidate mismatch")
registry=root/"techniques/registry.json"
original=registry.read_bytes()
data=json.loads(original)
cases=[]
with TemporaryDirectory() as td:
    for label, mutate, message in [
      ("boolean schema",lambda d:d.update(schema=True),"integer schema"),
      ("string aliases",lambda d:d["techniques"][0].update(aliases="xy"),"aliases"),
      ("nonstring alias",lambda d:d["techniques"][0].update(aliases=[42]),"aliases")]:
        changed=json.loads(original);mutate(changed)
        try:
            registry.write_text(json.dumps(changed),encoding="utf-8")
            receipt=Path(td)/"receipt.json"
            p=subprocess.run([sys.executable,"tools/check_readme_hq.py","--draft","--list","--receipt",str(receipt)],capture_output=True,text=True,encoding="utf-8")
            need(p.returncode==1 and message in p.stderr and "Traceback" not in p.stderr,(label,p.returncode,p.stderr))
            need(json.loads(receipt.read_bytes())["result"]=="failed",label)
            cases.append({"case":label,"result":"passed","exit":p.returncode,"diagnostic":message})
        finally:
            registry.write_bytes(original)
    p=subprocess.run([sys.executable,"tools/check_readme_hq.py","--list","--receipt",str(Path(td)/"valid.json")],capture_output=True,text=True,encoding="utf-8")
    need(p.returncode==0,p.stderr)
    need(all(row["id"] in p.stdout for row in data["techniques"]), "catalog listing missing ID")
    need(json.loads((Path(td)/"valid.json").read_bytes())["result"]=="passed","valid receipt")
    cases.append({"case":"valid public list","result":"passed","records":len(data["techniques"])})
need(registry.read_bytes()==original and not git("status","--porcelain","--","techniques/registry.json"),"registry modified")
result={"issue":8,"version":"v0.0.6.8","candidate":"79619d43bc04ccc49097e62058fd3dc0653dd672","vib_claim":"8dcdf679b346dc109eb06869fd2f5d7baab4f8fd","run":os.environ["GITHUB_RUN_ID"],"attempt":os.environ["GITHUB_RUN_ATTEMPT"],"os":os.environ["RUNNER_OS"],"registry_sha256":hashlib.sha256(original).hexdigest(),"cases":cases}
print(json.dumps(result,indent=2))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
