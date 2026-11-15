"""Step 2. Line up: one record per school (by School ID), one per locality (by name match to COMPASS and BLGF)."""
import glob
import os
from collections import defaultdict

import xlsx
from common import RAW, BUILD, LEVELS, load_csv, num, norm_place, slug, title_place, write_json

ES_GRADES = ("kinder", "g1", "g2", "g3", "g4", "g5", "g6")


def _compass_places():
    """(province, place) -> COMPASS row, from the Cities and Municipalities sheets."""
    path = glob.glob(os.path.join(RAW, "compass_nta", "*.xlsx"))[0]
    places = {}
    for sheet, kind in (("Cities", "city"), ("Municipalities", "municipality")):
        rows = xlsx.read_sheet(path, sheet)
        header = next(rows)
        years = [h for h in header if h.startswith("FY ") and "-" not in h]
        for r in rows:
            rec = dict(zip(header, r))
            name = rec.get("City") or rec.get("Municipality")
            if not name:
                continue
            key = (norm_place(rec["Province"]), norm_place(name))
            entry = {"compass_name": name, "compass_province": rec["Province"], "compass_region": rec["Region"],
                     "type": kind, "nta": {y: num(rec[y]) for y in years if rec.get(y)}}
            places.setdefault(key, []).append(entry)
    return places


def _sef_places():
    """(province, place) -> list of BLGF SEF records (FY2025): property-tax income and spending by office."""
    path = glob.glob(os.path.join(RAW, "blgf_sef", "*.xlsx"))[0]

    def table(sheet):
        rows = list(xlsx.read_sheet(path, sheet))
        h = next(i for i, r in enumerate(rows) if "LGU Name" in r)
        return rows, h, rows[h].index("Region")

    places = {}
    rows, h, c = table("Income")
    for r in rows[h + 1:]:
        r = r[c:] + [""] * 5
        if r[2] and r[3] in ("City", "Municipality"):
            places.setdefault((norm_place(r[1]), norm_place(r[2])), []).append(
                {"blgf_name": r[2], "type": r[3].lower(), "collected": round(num(r[4]), 2), "spent": None, "by_office": {}})
    rows, h, c = table("Expenditures")
    cats = [x for x in rows[h + 1][c:] if x]  # second header row: one column per office, then the total
    for r in rows[h + 2:]:
        r = r[c:] + [""] * (4 + len(cats))
        for rec in places.get((norm_place(r[1]), norm_place(r[2])), []):
            if rec["type"] == r[3].lower():
                vals = dict(zip(cats, (round(num(x), 2) for x in r[4:4 + len(cats)])))  # pesos and centavos
                rec["spent"] = vals.pop("Total Expenditures", round(sum(vals.values()), 2))
                rec["by_office"] = vals
    return places


def _pick(hits, municipality):
    """A city and a municipality can share a name: use DepEd's own wording to choose."""
    if len(hits) > 1:
        want = "city" if "CITY" in municipality.upper() else "municipality"
        hits = [h for h in hits if h["type"] == want] or hits
    return hits[0] if hits else None


def run():
    enr = load_csv("enrollment_2025_2026")
    crla = {r["school_id"]: r for r in load_csv("crla")}
    per = {r["school_id"]: r for r in load_csv("personnel_2023_2024")}
    fac = {r["school_id"]: r for r in load_csv("facilities_2023_2024")}
    teacher_cols = [c for c in next(iter(per.values())) if c.startswith("es_") and "teacher" in c]

    schools, by_loc = [], defaultdict(list)
    for e in enr:
        if e["sector"] != "Public" or e["offers_es"] != "Yes":
            continue
        sid = e["school_id"]
        loc_id = slug(e["province"], e["municipality"])
        rec = {"school_id": sid, "school_name": e["school_name"], "region": e["region"], "division": e["division"],
               "province": e["province"], "municipality": e["municipality"], "locality_id": loc_id,
               "k6_enrollment": sum(num(e[f"{g}_{s}"]) for g in ES_GRADES for s in ("male", "female")),
               "g1_3_enrollment": sum(num(e[f"g{g}_{s}"]) for g in (1, 2, 3) for s in ("male", "female")),
               "es_teachers": sum(num(per[sid][c]) for c in teacher_cols) if sid in per else None,
               "es_classrooms": num(fac[sid]["es_classrooms_instructional"]) if sid in fac else None,
               "has_reading": sid in crla}
        if sid in crla:
            c = crla[sid]
            rec["crla_assessed"] = num(c["n_test_takers"])
            for lv in LEVELS:
                rec[f"crla_{lv}"] = num(c[f"school_{lv}_total"])
        schools.append(rec)
        by_loc[loc_id].append(rec)

    places, sef_places = _compass_places(), _sef_places()
    localities, matched, sef_matched = [], 0, 0
    for loc_id, rows in by_loc.items():
        first = rows[0]
        key = (norm_place(first["province"]), norm_place(first["municipality"]))
        hit = _pick(places.get(key, []), first["municipality"])
        sef = _pick(sef_places.get(key, []), first["municipality"])
        matched += bool(hit)
        sef_matched += bool(sef)
        n_read = sum(1 for r in rows if r["has_reading"])
        localities.append({
            "locality_id": loc_id,
            "name": hit["compass_name"] if hit else title_place(first["municipality"]),
            "province": hit["compass_province"] if hit else title_place(first["province"]),
            "region": first["region"],
            "type": hit["type"] if hit else None,
            "psgc": None,
            "compass_matched": bool(hit),
            "nta": hit["nta"] if hit else None,
            "sef": {k: sef[k] for k in ("collected", "spent", "by_office")} if sef else None,
            "public_elementary_schools": len(rows),
            "schools_with_reading": n_read,
            "coverage": n_read / len(rows),
        })

    quality = {
        "public_elementary_schools": len(schools),
        "reading_file_schools": len(crla),
        "reading_schools_matched": sum(1 for s in schools if s["has_reading"]),
        "reading_schools_unmatched": len(crla) - sum(1 for s in schools if s["has_reading"]),
        "schools_with_personnel": sum(1 for s in schools if s["es_teachers"] is not None),
        "schools_with_facilities": sum(1 for s in schools if s["es_classrooms"] is not None),
        "localities": len(localities),
        "localities_matched_to_compass": matched,
        "localities_unmatched": sorted(f"{l['name']}, {l['province']}" for l in localities if not l["compass_matched"]),
        "localities_matched_to_sef": sef_matched,
        "sef_unmatched": sorted(f"{l['name']}, {l['province']}" for l in localities if not l["sef"]),
    }
    write_json(os.path.join(BUILD, "2_schools.json"), schools)
    write_json(os.path.join(BUILD, "2_localities.json"), localities)
    write_json(os.path.join(BUILD, "2_quality.json"), quality)
    print(f"2 line up   {len(schools):,} schools; reading matched {quality['reading_schools_matched']:,}/{len(crla):,}; "
          f"localities matched to COMPASS {matched:,}/{len(localities):,}, to BLGF SEF {sef_matched:,}/{len(localities):,}")


if __name__ == "__main__":
    run()
