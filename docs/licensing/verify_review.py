"""Read-only mechanical review; does not decide rights or publish a grant."""
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE="5adfd75f7a3a5864626bdbebff5d2249c381a975"
EXPECTED={
 "docs/licensing/README.md", "docs/licensing/README-HQ-NOTICE-REVIEW.md",
 "docs/licensing/rights-inventory.json", "docs/licensing/verify_review.py",
 "docs/licensing/reference/PolyForm-Strict-1.0.0.md",
 "docs/licensing/reference/PolyForm-text-permission.md",
 ".github/workflows/licensing-review.yml",
}
def git(*args):
 return subprocess.check_output(["git","--no-replace-objects","-C",str(ROOT),*args])
def check(ok,msg):
 if not ok: raise ValueError(msg)
def entries(ref):
 rows={}
 for record in git("ls-tree","-r","-z",ref).split(b"\0"):
  if record:
   meta,path=record.split(b"\t",1)
   mode,kind,sha=meta.decode().split()
   rows[path.decode("utf-8")]=(mode,sha)
 return rows
before=entries(BASE); after=entries("HEAD")
data=json.loads((ROOT/"docs/licensing/rights-inventory.json").read_bytes())
check(data["candidate"]==BASE and data["status"]=="REVIEW_ONLY_NOT_A_GRANT","inventory identity")
check(data["tree"]==git("rev-parse",BASE+"^{tree}").decode().strip(),"tree identity")
check(len(data["paths"])==len(before) and {p["path"]:(p["mode"],p["object"]) for p in data["paths"]}==before,"inventory coverage")
check(all(after.get(p)==v for p,v in before.items()),"prior source changed")
check(set(after)-set(before)==EXPECTED,"unexpected additions")
check(after["docs/licensing/reference/PolyForm-Strict-1.0.0.md"][1]=="90abd0e6c64a135f42451762337a397bf27f4862","reference text changed")
check(after["docs/licensing/reference/PolyForm-text-permission.md"][1]=="c801ad3329f26ed923accd6b3724ce5aa94ebb50","reference permission changed")
check(all("REVIEW_ONLY_NOT_A_GRANT" in (ROOT/p).read_text(encoding="utf-8") for p in ["docs/licensing/README.md","docs/licensing/README-HQ-NOTICE-REVIEW.md"]),"missing review-only label")
check(not any(p.split("/")[0].lower().split(".")[0] in ("license","licence","notice","copying") for p in after),"operative root notice")
notices=[p for p,v in before.items() if p.startswith("history/") and p.endswith("/LICENSE")]
check(len(notices)==4 and all(before[p][1]=="3a31b6b1dcedea9bb0ca27243d3d7b0cb504a4f5" for p in notices),"historical notices")
receipt={"result":"passed","scope":"mechanical review only, ownership unverified, no grant","base":BASE,"tested":git("rev-parse","HEAD").decode().strip(),"prior_leaf_objects_preserved":len(before),"review_only_additions":sorted(EXPECTED),"historical_license_notices_preserved":len(notices),"exact_reference_blobs":2}
print(json.dumps(receipt,indent=2))
if len(sys.argv)>1: Path(sys.argv[1]).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
