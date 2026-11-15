"""Step 5. Publish: one brief page and one JSON file per locality, bulk CSVs, and a data quality report.

Page templates live in s5_pages.py.
"""
import csv
import os

from common import PIPE, BUILD, SITE, LEVELS, read_json, write_json
from s5_pages import ATTRIBUTION, about_html, brief_html, index_html, quality_html

DICTIONARY = """# Data dictionary

Derived from DepEd Project Bukas machine-ready files, DepEd's FY 2026 school MOOE allocation and the DBM COMPASS public export.
Shared under the same terms as the DepEd source files; credit the Department of Education.

## schools.csv (one row per public elementary school)

| Field | Meaning | Source |
| --- | --- | --- |
| school_id | 6-digit DepEd School ID; the join key | Enrolment SY 2025-26 |
| school_name, region, division, province, municipality | As published by DepEd | Enrolment SY 2025-26 |
| locality_id | Province and city or municipality, normalised; links to localities.csv | Derived |
| k6_enrollment | Kinder to Grade 6 learners | Enrolment SY 2025-26 |
| g1_3_enrollment | Grades 1 to 3 learners | Enrolment SY 2025-26 |
| es_teachers | Elementary teaching posts | Personnel SY 2023-24 |
| es_classrooms | Elementary instructional classrooms | Facilities SY 2023-24 |
| mooe_es_fy2026 | Elementary MOOE allocated to the school for FY 2026, in pesos (an allocation, not spending); empty if the school is not in the file | DepEd school MOOE allocation FY 2026 |
| has_reading | Whether the school is in the public reading file | CRLA SY 2025-26 |
| crla_assessed | Grades 1 to 3 learners assessed | CRLA SY 2025-26 |
| crla_low_emerging ... crla_at_grade_level | Learners at each of the five reading levels | CRLA SY 2025-26 |

## localities.csv (one row per city or municipality)

| Field | Meaning | Source |
| --- | --- | --- |
| locality_id | Join key to schools.csv | Derived |
| name, province, region | COMPASS spelling where matched, DepEd spelling otherwise | COMPASS / DepEd |
| type | city or municipality | COMPASS |
| psgc | 10-digit location code; empty until the COMPASS API is connected | Planned |
| compass_matched | Whether the name matched a COMPASS record | Derived |
| nta_fy2022 ... nta_fy2027 | National Tax Allotment in pesos | DBM COMPASS |
| mooe_es_fy2026 | Elementary MOOE allocated for FY 2026 to the locality's public elementary schools, in pesos | DepEd school MOOE allocation FY 2026 |
| mooe_schools_listed | How many of its public elementary schools are in the MOOE file | Derived |
| public_elementary_schools, schools_with_reading, coverage | Reading-data coverage | Derived |
| has_brief | Whether a brief was generated | Derived |

## api/localities/<locality_id>.json

The full content of one brief: locality values, regional, division and all-published benchmarks,
reading-level shares, money fields (empty where a source is not yet connected), and one entry per school.

`money.special_education_fund` holds the locality's FY2025 (preliminary) Special Education Fund figures from the
Bureau of Local Government Finance (BLGF): `collected` (property-tax income), `spent` (total expenditure) and
`by_office` (spending by the office it was charged to), in pesos. Credit BLGF when you use them. The full BLGF
workbook is not republished here; it is at https://blgf.gov.ph/lgu-fiscal-data/.

`money.deped_school_mooe` holds DepEd's FY 2026 school MOOE allocation for the locality: `elementary_allocation`
(pesos allocated to its public elementary schools), `schools_listed` and `public_elementary_schools`. Each school entry
carries `mooe_es_fy2026` and `k6_enrollment`. These are allocations set by formula, not spending.
"""


def run():
    cfg = read_json(os.path.join(PIPE, "indicators.json"))
    indicators, rules = cfg["indicators"], cfg["brief_rules"]
    briefs = read_json(os.path.join(BUILD, "4_briefs.json"))
    quality = read_json(os.path.join(BUILD, "2_quality.json"))
    manifest = read_json(os.path.join(BUILD, "1_manifest.json"))
    for sub in ("briefs", "api/localities", "data"):
        os.makedirs(os.path.join(SITE, sub), exist_ok=True)
    current = {b["locality_id"] for b in briefs}
    for sub, ext in (("briefs", ".html"), ("api/localities", ".json")):  # drop pages for renamed or dropped places
        for name in os.listdir(os.path.join(SITE, sub)):
            if name.endswith(ext) and name[:-len(ext)] not in current:
                os.remove(os.path.join(SITE, sub, name))

    for b in briefs:
        with open(os.path.join(SITE, "briefs", b["locality_id"] + ".html"), "w", encoding="utf-8") as f:
            f.write(brief_html(b, indicators, rules["headline"]))
        write_json(os.path.join(SITE, "api", "localities", b["locality_id"] + ".json"),
                   dict(b, indicators=indicators, attribution=ATTRIBUTION))
    write_json(os.path.join(SITE, "api", "index.json"), {
        "attribution": ATTRIBUTION, "indicators": indicators, "sources": manifest,
        "localities": [{"locality_id": b["locality_id"], "name": b["name"], "province": b["province"],
                        "region": b["region"], "reading_lowest": b["values"]["reading_lowest"],
                        "json": f"api/localities/{b['locality_id']}.json",
                        "brief": f"briefs/{b['locality_id']}.html"} for b in briefs]})

    schools = read_json(os.path.join(BUILD, "2_schools.json"))
    fields = ["school_id", "school_name", "region", "division", "province", "municipality", "locality_id",
              "k6_enrollment", "g1_3_enrollment", "es_teachers", "es_classrooms", "mooe_es_fy2026", "has_reading", "crla_assessed"] + \
             [f"crla_{lv}" for lv in LEVELS]
    with open(os.path.join(SITE, "data", "schools.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(schools)
    has = {b["locality_id"] for b in briefs}
    years = [f"FY {y}" for y in range(2022, 2028)]
    with open(os.path.join(SITE, "data", "localities.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["locality_id", "name", "province", "region", "type", "psgc", "compass_matched"] +
                   [y.lower().replace(" ", "_").replace("fy_", "nta_fy") for y in years] +
                   ["mooe_es_fy2026", "mooe_schools_listed", "public_elementary_schools", "schools_with_reading", "coverage", "has_brief"])
        for l in read_json(os.path.join(BUILD, "2_localities.json")):
            w.writerow([l["locality_id"], l["name"], l["province"], l["region"], l["type"] or "", l["psgc"] or "",
                        l["compass_matched"]] + [(l["nta"] or {}).get(y, "") for y in years] +
                       [round(l["mooe_es_fy2026"]), l["mooe_schools_listed"],
                        l["public_elementary_schools"], l["schools_with_reading"], round(l["coverage"], 4),
                        l["locality_id"] in has])
    with open(os.path.join(SITE, "data", "DATA_DICTIONARY.md"), "w", encoding="utf-8") as f:
        f.write(DICTIONARY)
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html(briefs, quality, manifest, rules["featured"]))
    with open(os.path.join(SITE, "about.html"), "w", encoding="utf-8") as f:
        f.write(about_html(quality, briefs, manifest, indicators, rules))
    with open(os.path.join(SITE, "quality.html"), "w", encoding="utf-8") as f:
        f.write(quality_html(quality, manifest, briefs))
    print(f"5 publish   {len(briefs)} briefs, {len(briefs)} JSON files, 2 CSVs, quality report -> site/")


if __name__ == "__main__":
    run()
