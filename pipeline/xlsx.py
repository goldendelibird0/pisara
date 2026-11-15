"""Minimal .xlsx reader using only the standard library.

Yields rows as lists of strings for one sheet. Enough for flat government
workbooks; avoids a third-party dependency so the pipeline runs anywhere.
"""
import re
import zipfile
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "p": "http://schemas.openxmlformats.org/package/2006/relationships"}


def _col_index(ref):
    letters = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def sheet_names(path):
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        return [s.get("name") for s in wb.find("m:sheets", NS)]


def read_sheet(path, name):
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        targets = {r.get("Id"): r.get("Target") for r in rels.findall("p:Relationship", NS)}
        rid = next(s.get(f"{{{NS['r']}}}id") for s in wb.find("m:sheets", NS) if s.get("name") == name)
        target = targets[rid].lstrip("/")
        if not target.startswith("xl/"):
            target = "xl/" + target
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.iter(f"{{{NS['m']}}}t")))
        with z.open(target) as f:
            for _, el in ET.iterparse(f):
                if el.tag != f"{{{NS['m']}}}row":
                    continue
                row = []
                for c in el.findall("m:c", NS):
                    i = _col_index(c.get("r"))
                    while len(row) <= i:
                        row.append("")
                    t = c.get("t")
                    v = c.find("m:v", NS)
                    if t == "s" and v is not None:
                        row[i] = shared[int(v.text)]
                    elif t == "inlineStr":
                        row[i] = "".join(x.text or "" for x in c.iter(f"{{{NS['m']}}}t"))
                    elif v is not None:
                        row[i] = v.text or ""
                yield row
                el.clear()
