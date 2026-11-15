"""Step 3. Measure: compute every indicator in indicators.json for each school and each benchmark group.

An indicator is a ratio of two school fields. A group's value is the sum of
numerators over the sum of denominators, so large and small schools are
weighted by their learners. Benchmarks use only schools with published
reading results, so a school is compared with schools measured the same way.
"""
import os
from collections import defaultdict

from common import PIPE, BUILD, LEVELS, read_json, write_json


def ratio(rows, ind):
    n = d = 0.0
    for r in rows:
        a, b = r.get(ind["numerator"]), r.get(ind["denominator"])
        if a is None or not b:
            continue
        n += a
        d += b
    return n / d if d else None


def levels(rows):
    total = sum(r["crla_assessed"] for r in rows)
    return {lv: sum(r[f"crla_{lv}"] for r in rows) / total for lv in LEVELS} if total else None


def summarise(rows, indicators):
    out = {i["id"]: ratio(rows, i) for i in indicators}
    out["levels"] = levels(rows)
    out["schools"] = len(rows)
    out["learners_assessed"] = sum(r["crla_assessed"] for r in rows)
    return out


def run():
    indicators = read_json(os.path.join(PIPE, "indicators.json"))["indicators"]
    schools = [s for s in read_json(os.path.join(BUILD, "2_schools.json")) if s["has_reading"] and s["crla_assessed"]]
    by_region, by_division = defaultdict(list), defaultdict(list)
    for s in schools:
        by_region[s["region"]].append(s)
        by_division[f"{s['region']} / {s['division']}"].append(s)
    measures = {
        "benchmarks": {
            "all": summarise(schools, indicators),
            "region": {k: summarise(v, indicators) for k, v in by_region.items()},
            "division": {k: summarise(v, indicators) for k, v in by_division.items()},
        },
        "schools": {s["school_id"]: {i["id"]: ratio([s], i) for i in indicators} for s in schools},
    }
    write_json(os.path.join(BUILD, "3_measures.json"), measures)
    print(f"3 measure   {len(indicators)} indicators for {len(schools):,} schools; "
          f"{len(by_region)} regional and {len(by_division)} division benchmarks")


if __name__ == "__main__":
    run()
