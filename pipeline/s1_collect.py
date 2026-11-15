"""Step 1. Collect: fetch each connected source and record where it came from.

Files already on disk are not fetched again. DepEd files are only downloaded
when --accept-deped-terms is passed, because DepEd requires users to agree to
its Terms of Use before downloading (see sources.json: deped_terms).
"""
import datetime
import hashlib
import os
import sys
import urllib.request
import zipfile

from common import PIPE, RAW, BUILD, read_json, write_json


def _safe_extract(zpath, out):
    with zipfile.ZipFile(zpath) as z:
        for info in z.infolist():
            target = os.path.realpath(os.path.join(out, info.filename))
            if target.startswith(os.path.realpath(out) + os.sep):
                z.extract(info, out)


def run(accept_deped_terms=False):
    cfg = read_json(os.path.join(PIPE, "sources.json"))
    manifest = []
    for s in cfg["sources"]:
        entry = {k: s.get(k) for k in ("id", "title", "publisher", "period", "key", "licence", "url", "status", "needs")}
        if s["status"] != "connected":
            manifest.append(entry)
            continue
        folder = os.path.join(RAW, s["id"])
        os.makedirs(folder, exist_ok=True)
        fname = s.get("filename") or s["url"].rsplit("/", 1)[-1]
        path = os.path.join(folder, fname)
        if not os.path.exists(path):
            if s.get("manual"):  # the publisher lists files on a page; there is no stable direct link
                raise SystemExit(f"{fname} is missing. {s['manual']}")
            if "deped.gov.ph" in s["url"] and not accept_deped_terms:
                raise SystemExit(f"{fname} is missing. Read DepEd's terms at {cfg['deped_terms']} "
                                 "and re-run with --accept-deped-terms to download it.")
            req = urllib.request.Request(s["url"], headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as f:
                f.write(r.read())
        if path.endswith(".zip") and not os.path.isdir(os.path.join(folder, "unzipped")):
            _safe_extract(path, os.path.join(folder, "unzipped"))
        with open(path, "rb") as f:
            data = f.read()
        entry.update(file=fname, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                     retrieved=datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat())
        manifest.append(entry)
    write_json(os.path.join(BUILD, "1_manifest.json"), manifest)
    done = sum(1 for m in manifest if m["status"] == "connected")
    print(f"1 collect   {done} sources connected, {len(manifest) - done} planned")
    return manifest


if __name__ == "__main__":
    run("--accept-deped-terms" in sys.argv)
