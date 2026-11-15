"""Shared paths and helpers for the five pipeline steps."""
import csv
import glob
import json
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPE = os.path.join(ROOT, "pipeline")
RAW = os.path.join(ROOT, "data", "raw")
BUILD = os.path.join(ROOT, "build")
SITE = os.path.join(ROOT, "site")

LEVELS = ["low_emerging", "high_emerging", "developing", "transitioning", "at_grade_level"]
LEVEL_LABELS = ["Low Emerging", "High Emerging", "Developing", "Transitioning", "At Grade Level"]


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def load_csv(source_id):
    """Read the single CSV inside a source's folder, whatever its encoding."""
    paths = glob.glob(os.path.join(RAW, source_id, "**", "*.csv"), recursive=True)
    if len(paths) != 1:
        raise SystemExit(f"expected one CSV for {source_id}, found {len(paths)}")
    for enc in ("utf-8-sig", "cp1252"):
        try:
            with open(paths[0], newline="", encoding=enc) as f:
                return list(csv.DictReader(f))
        except UnicodeDecodeError:
            continue
    raise SystemExit(f"cannot decode {paths[0]}")


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


PROVINCE_ALIASES = {"WESTERN SAMAR": "SAMAR", "NORTH COTABATO": "COTABATO", "COMPOSTELA VALLEY": "DAVAO DE ORO",
                    "BARAUEN": "BURAUEN"}  # DepEd spells Burauen, Leyte as "Barauen"


def norm_place(name):
    """Reduce a place name to a comparable form: 'CITY OF TARLAC (Capital)' -> 'TARLAC'."""
    s = unicodedata.normalize("NFKD", name or "").encode("ascii", "ignore").decode().upper()
    s = re.sub(r"\(.*?\)", " ", s)
    s = s.replace("STA.", "SANTA ").replace("STO.", "SANTO ")
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    s = re.sub(r"\b(ISLAND GARDEN )?CITY OF\b", " ", s)
    s = re.sub(r"\bCITY\b", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return PROVINCE_ALIASES.get(s, s)


def slug(*parts):
    s = "-".join(norm_place(p) for p in parts).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def title_place(name):
    s = re.sub(r"\(.*?\)", "", name or "").strip().title()
    return re.sub(r"\b(Of|Del|De|La|Las|Los)\b", lambda m: m.group(0).lower(), s).replace("city of", "City of")
