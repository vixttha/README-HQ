"""Read-only review of unchecked observations; no claims of semantic validation."""
import collections
import json
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import time

root, receipt_path, out = map(pathlib.Path, sys.argv[1:])
receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
expected = "d12d5c6bd82fe448f64adb3ae48024296b8e6db4"
if receipt.get("commit") != expected or receipt.get("result") != "passed":
    raise SystemExit("expected a passing exact-candidate reader receipt")
snapshots = json.loads((root / "history/sources.json").read_text(encoding="utf-8"))["snapshots"]
class PublicGitHubOnly(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed(newurl):
            raise ValueError("redirect outside approved public GitHub origin")
        return super().redirect_request(req, fp, code, msg, headers, newurl)
def allowed(url):
    p = urllib.parse.urlsplit(url)
    return (p.scheme == "https" and p.netloc == "github.com"
            and not p.query and not p.fragment
            and bool(re.fullmatch(r"/vixttha/[A-Za-z0-9_.-]+(?:/[^?#]*)?", p.path, flags=re.I)))
opener = urllib.request.build_opener(PublicGitHubOnly())
cache = {}
def observe(url):
    if not allowed(url):
        return {"status": "outside-approved-probe-scope"}
    if url in cache:
        return cache[url]
    time.sleep(0.25)
    try:
        with opener.open(urllib.request.Request(url, headers={"User-Agent":"README-HQ-public-link-review/1"}), timeout=10) as response:
            status, final = response.status, response.geturl()
            result = {"http_status":status, "final_url":final,
                      "status":"route-responded" if 200 <= status < 300 else "unresolved"}
    except urllib.error.HTTPError as error:
        with error:
            status = error.code
        result = {"http_status": status,
                  "status":"not-found-or-not-public" if status in (404,410) else "unresolved"}
    except (OSError, ValueError) as error:
        result = {"status":"unresolved", "error_type":type(error).__name__}
    cache[url] = result
    return result
def classify(line):
    record = {"observation":line}
    m = re.match(r"^(.+?):(\d+): (external link not checked|original repository route outside import): (.+)$", line)
    if not m:
        return {**record,"status":"unclassified"}
    source, lineno, kind, destination = m.groups()
    record.update(source=source,line=int(lineno),kind=kind,destination=destination)
    if kind == "original repository route outside import":
        matches = [s for s in snapshots if source.startswith(s["directory"]+"/")]
        if not matches:
            return {**record,"status":"source-snapshot-unresolved"}
        snapshot = max(matches,key=lambda s:len(s["directory"]))
        relative_source = pathlib.PurePosixPath(source).relative_to(snapshot["directory"])
        target = pathlib.PurePosixPath(relative_source.parent,destination)
        if target.is_absolute() or ".." in target.parts:
            return {**record,"status":"source-route-unresolved"}
        dest = urllib.parse.quote(str(target),safe="/")
        url = f"https://github.com/{snapshot['repository']}/blob/{snapshot['commit']}/{dest}"
        record["pinned_source_url"] = url
    else:
        parsed = urllib.parse.urlsplit(destination)
        if parsed.hostname in ("localhost","127.0.0.1","::1"):
            return {**record,"status":"local-example-not-probed"}
        url = destination
    return {**record,**observe(url)}
rows = [classify(line) for line in receipt.get("unchecked",[])]
counts = dict(collections.Counter(row["status"] for row in rows))
data = {"candidate":expected,"reader_result":receipt["result"],"run_id":__import__("os").environ.get("GITHUB_RUN_ID"),"attempt":__import__("os").environ.get("GITHUB_RUN_ATTEMPT"),"count":len(rows),"counts":counts,"unique_public_requests":len(cache),"limitations":"HTTP route observations only; not rendered link, anchor, content, permission or semantic validation. No localhost or other hosts probed. No failures waived.", "observations":rows}
out.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:v for k,v in data.items() if k!="observations"},indent=2))
