import json, os, subprocess, sys, tempfile
from pathlib import Path
root=Path.cwd()
def require(ok,msg):
    if not ok: raise RuntimeError(msg)
require(subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()=="43e29074099742a2c73741176286a44ccdf861a1","candidate mismatch")
expected={"public":"success","private":"skipped","internal":"skipped","missing":"skipped","missing_private":"skipped","string_false":"skipped","conflicting":"skipped","fork_public":"success","fork_private_host":"skipped"}
observed={key:os.environ.get("CASE_"+key.upper()) for key in expected}
require(observed==expected,"GitHub expression outcomes: "+repr(observed))
with tempfile.TemporaryDirectory(prefix="offline-synthetic-") as folder:
    base=Path(folder)
    project=base/"project"
    project.mkdir()
    def git(*args):
        return subprocess.check_output(["git","-C",str(project),*args],text=True).strip()
    git("init","-q")
    git("config","commit.gpgSign","false")
    (project/"README.md").write_text("# Synthetic fixture\n\nAn offline reader fixture with a [guide](guide.md).\n",encoding="utf-8")
    (project/"guide.md").write_text("# Guide\n",encoding="utf-8")
    git("add",".")
    git("-c","user.name=Fixture","-c","user.email=fixture@example.invalid","commit","-qm","Fixture")
    git("remote","add","origin","https://github.com/example/synthetic-private-fixture.git")
    pin=git("rev-parse","HEAD")
    dest=base/"private-receipt.json"
    p=subprocess.run([sys.executable,str(root/"tools/check_readme_hq.py"),"--repo",str(project),"--ref",pin,"--profile","reference","--receipt",str(dest)],capture_output=True,text=True)
    require(p.returncode==0,"offline validation failed (output suppressed)")
    receipt=json.loads(dest.read_bytes())
    require(receipt["commit"]==pin and receipt["result"]=="passed" and receipt["cases"]["local_links"]==1,"offline receipt mismatch")
    # No private fixture receipt or source bytes leave this temporary directory.
report={"issue":11,"candidate":"43e29074099742a2c73741176286a44ccdf861a1","vib_state":"1844f33a69e038d87e5bdb3f9fdef2b8a416e6c1","run":os.environ["GITHUB_RUN_ID"],"attempt":os.environ["GITHUB_RUN_ATTEMPT"],"expression_cases":observed,"offline_synthetic_receipt":"passed; destroyed with temporary fixture","scope":"Actual GitHub step expression evaluation, not private job scheduling; synthetic fixture only"}
print(json.dumps(report,indent=2))
Path(sys.argv[1]).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
