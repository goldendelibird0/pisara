# Data dictionary

Derived from DepEd Project Bukas machine-ready files and the DBM COMPASS public export.
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
| public_elementary_schools, schools_with_reading, coverage | Reading-data coverage | Derived |
| has_brief | Whether a brief was generated | Derived |

## api/localities/<locality_id>.json

The full content of one brief: locality values, regional, division and all-published benchmarks,
reading-level shares, money fields (empty where a source is not yet connected), and one entry per school.
