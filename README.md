# PISARA

**Public Information for School Allocation and Resource Accountability.** A prototype for the BetterGovPH
Fellowship, Basic Education challenge (DepEd).

PISARA gives every Local School Board a one-page brief for its own city or town. The brief shows which public
elementary schools need help most and what kind of help to look into, so the board can decide how to share the
Special Education Fund (SEF). It is built entirely from data the government already publishes.

- **Live site:** see the link in the repository description
- **Example briefs:** `site/briefs/pampanga-mabalacat.html`, `site/briefs/leyte-ormoc.html`
- **Full technical write-up:** `site/about.html` (sources, joins, formulas, grouping rule, limits, roadmap)

## The problem

Boards decide on the SEF every year, but the evidence sits in separate files: reading results, enrolment,
teachers and classrooms from DepEd, money from DBM. No one joins them school by school, so a board rarely sees
which schools need what.

## What a brief contains

1. **Bottom line.** How many early-grade learners are at the lowest reading level, and where to start.
2. **Where to act.** Each school is compared with the average for its region on two things: reading (share of
   Grades 1 to 3 learners at the lowest level) and space (learners per classroom). That sorts schools into four
   groups: needs reading help and more room, reading help only, more room only, or neither. Each group comes with
   what the board could look into.
3. **Questions for the meeting.**
4. **Planned:** where the SEF goes now, and follow-up after the meeting (needs SEF utilisation data).
5. **Supporting detail:** the reading distribution, every school's figures, and how to read them.

## Coverage of the current run

- 256 cities and municipalities get a brief, covering 6,041 schools and 641,031 assessed learners
- 6,113 of 6,121 schools in the reading file joined to the other files by DepEd School ID (99.9%)
- 1,564 of 1,644 localities matched by name to DBM COMPASS (95.1%)
- A locality gets a brief only if at least 90% of its public elementary schools are in the reading data, and at
  least 5 schools

## How it works

A five-step pipeline in plain Python (standard library only, Python 3.10+). It writes a static site, so it can be
hosted anywhere.

| Step | File | What it does |
| --- | --- | --- |
| 1 Collect | `pipeline/s1_collect.py` | Downloads each source in `sources.json`; records origin, period, licence and checksum |
| 2 Line up | `pipeline/s2_lineup.py` | Joins school files by School ID; matches each locality to COMPASS by province and name |
| 3 Measure | `pipeline/s3_measure.py` | Computes each indicator in `indicators.json` for every school, division and region |
| 4 Group | `pipeline/s4_group.py` | Rolls schools up to their locality and compares each school with its region |
| 5 Publish | `pipeline/s5_publish.py`, `s5_pages.py` | Writes the brief pages, a JSON file per locality, bulk CSVs and a data quality report |

Adding an indicator is a config change (a ratio of two school fields in `indicators.json`), not new code.

### Run it

```bash
python pipeline/run.py --accept-deped-terms
```

The flag is needed on the first run, which downloads DepEd's files; by passing it you agree to DepEd's Terms of
Use (https://www.deped.gov.ph/machine-ready-files/). Raw downloads are not stored in this repository. To rebuild
pages only, run `python pipeline/s5_publish.py`. To view the site, run
`python -m http.server 8765 --directory site`.

### Outputs in `site/`

- `index.html`: search for any locality
- `briefs/<locality>.html`: the brief
- `api/index.json`, `api/localities/<locality>.json`: the same content as open data
- `data/schools.csv`, `data/localities.csv`, `data/DATA_DICTIONARY.md`
- `quality.html`: join rates, unmatched places, source checksums

## Sources

| Data | Publisher | Period |
| --- | --- | --- |
| Comprehensive Rapid Literacy Assessment (CRLA) | DepEd, Project Bukas machine-ready files | SY 2025-26 |
| Enrolment | DepEd | SY 2025-26 |
| School personnel, school facilities | DepEd | SY 2023-24 |
| National Tax Allotment | DBM COMPASS public export | FY 2022-2027 |

## Limits

- DepEd's public reading file covers five regions (I, III, VIII, IX, CAR), so only localities there get a brief.
- SEF figures are not yet connected. The Planned sections stay empty until a local government's quarterly SEF
  utilisation report is added. The tax allotment shown "for scale" is not specific to education.
- Teacher and classroom counts are from SY 2023-24; reading and enrolment are from SY 2025-26.
- Localities are matched to COMPASS by name, because DepEd's files carry no location code (PSGC).
- The groups suggest a kind of help to look into. They do not claim that crowding causes low reading, or that
  spending will fix it.

## Roadmap for the fellowship

1. Connect SEF utilisation reports for pilot localities, so each brief shows where the money goes now.
2. Connect the COMPASS API for location codes and DepEd regional spending.
3. Test the brief with one Local School Board and revise it from their meeting.
4. Add a follow-up view, so a board can check next year what changed in the schools it chose.

## Rules this project follows

- Schools are never ranked. They are listed alphabetically and compared with a regional benchmark.
- Test results are not compared across school years.
- DepEd is credited as the source; the DepEd logo is not used; no endorsement is implied.
- Data derived from DepEd's files (`site/data`, `site/api`) is shared under the same terms as the source files.

## Credits

School data: Department of Education, Project Bukas machine-ready files. Tax allotment data: Department of Budget
and Management, COMPASS. This is an independent prototype, not produced, reviewed or endorsed by DepEd or DBM.
