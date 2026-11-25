import importlib.util,json,os,subprocess,sys
from pathlib import Path
root=Path.cwd()
def require(ok,msg):
    if not ok: raise RuntimeError(msg)
require(subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()=="79619d43bc04ccc49097e62058fd3dc0653dd672","candidate mismatch")
sys.path[:0]=[str(root/"tools"),str(root/"graphify-hq/template/v0.0.8")]
spec=importlib.util.spec_from_file_location("version_maps",root/"graphify-hq/version_maps.py")
maps=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=maps
spec.loader.exec_module(maps)
from markdown_it import MarkdownIt
cases=[]
for title,summary in [("Public | preview","Old | new"),("Literal [link] | *stars*","Backslash \\ | & <tag>"),("A || B","C | D | E")]:
    record={"title":title,"summary":summary}
    rendered=maps.render_outline("v0.0.6","example/project",{"source_commit":"a"*40,"nodes":1,"edges":1},[(record,[],({"path":"README.md"},1))])
    tokens=MarkdownIt("commonmark").enable("table").parse(rendered)
    rows=[]; row=None; cell=False
    for token in tokens:
        if token.type=="tr_open": row=[]
        elif token.type=="td_open": cell=True
        elif token.type=="td_close": cell=False
        elif token.type=="inline" and cell: row.append("".join(x.content for x in token.children if x.type=="text"))
        elif token.type=="tr_close" and row: rows.append(row)
    require(len(rows)==1 and len(rows[0])==3 and rows[0][:2]==[title,summary],repr(rows))
    cases.append({"title":title,"summary":summary,"cells":3,"exact_text":True})
report={"issue":10,"candidate":"79619d43bc04ccc49097e62058fd3dc0653dd672","claim":"84fdb65152de5a52841b15dc0d0893ba586f8e04","run":os.environ["GITHUB_RUN_ID"],"attempt":os.environ["GITHUB_RUN_ATTEMPT"],"cases":cases}
print(json.dumps(report,indent=2));Path(sys.argv[1]).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
