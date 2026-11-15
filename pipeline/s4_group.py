"""Step 4. Group: roll schools up to their city or municipality and attach the locality's money.

A locality gets a brief only if its public elementary schools are well covered
by the reading data (brief_rules in indicators.json). Schools are never ranked:
each is marked as above or not above the regional benchmark.
"""
import os
from collections import defaultdict

from common import PIPE, BUILD, read_json, write_json
from s3_measure import summarise


def run():
    cfg = read_json(os.path.join(PIPE, "indicators.json"))
    rules, indicators = cfg["brief_rules"], cfg["indicators"]
    head = rules["headline"]
    more_need = {i["id"]: i["higher_means"] == "more need" for i in indicators}
    measures = read_json(os.path.join(BUILD, "3_measures.json"))
    by_loc = defaultdict(list)
    for s in read_json(os.path.join(BUILD, "2_schools.json")):
        if s["has_reading"] and s["crla_assessed"]:
            by_loc[s["locality_id"]].append(s)

    briefs = []
    for loc in read_json(os.path.join(BUILD, "2_localities.json")):
        rows = by_loc.get(loc["locality_id"], [])
        if loc["coverage"] < rules["min_coverage"] or len(rows) < rules["min_schools"]:
            continue
        region = measures["benchmarks"]["region"][loc["region"]]
        div_keys = sorted({f"{s['region']} / {s['division']}" for s in rows})
        division = None
        if len(div_keys) == 1 and measures["benchmarks"]["division"][div_keys[0]]["schools"] > len(rows):
            division = dict(measures["benchmarks"]["division"][div_keys[0]], name=div_keys[0].split(" / ")[1])

        school_rows = []
        for s in sorted(rows, key=lambda s: s["school_name"]):
            vals = measures["schools"][s["school_id"]]
            above = {k: (vals[k] is not None and region[k] is not None and
                         ((vals[k] > region[k]) if more_need[k] else (vals[k] < region[k]))) for k in more_need}
            school_rows.append({
                "school_id": s["school_id"], "school_name": s["school_name"],
                "learners_assessed": s["crla_assessed"], "small_group": s["crla_assessed"] < rules["small_group"],
                "values": vals, "more_need_than_region": above,
                "headline_gap_points": (vals[head] - region[head]) * 100 if vals[head] is not None else None,
            })
        flagged = [r for r in school_rows if r["more_need_than_region"][head]]
        total = summarise(rows, indicators)
        briefs.append({
            **{k: loc[k] for k in ("locality_id", "name", "province", "region", "type", "psgc", "compass_matched",
                                   "public_elementary_schools", "schools_with_reading", "coverage")},
            "values": total,
            "benchmarks": {"region": region, "division": division, "all_published": measures["benchmarks"]["all"]},
            "g1_3_enrolled": sum(s["g1_3_enrollment"] for s in rows),
            "schools_above_region": len(flagged),
            "learners_in_schools_above_region": sum(r["learners_assessed"] for r in flagged),
            "schools_above_region_on_reading_and_classrooms": sum(
                1 for r in flagged if r["more_need_than_region"].get("learners_per_classroom")),
            "money": {
                "national_tax_allotment": loc["nta"],
                "special_education_fund": dict(loc["sef"], fiscal_year="FY 2025", status="preliminary",
                                               source="Bureau of Local Government Finance") if loc["sef"] else None,
                "deped_regional_spending": None,
            },
            "schools": school_rows,
        })
    write_json(os.path.join(BUILD, "4_briefs.json"), briefs)
    print(f"4 group     {len(briefs)} localities qualify for a brief "
          f"({sum(len(b['schools']) for b in briefs):,} schools, "
          f"{sum(b['values']['learners_assessed'] for b in briefs):,.0f} learners)")


if __name__ == "__main__":
    run()
