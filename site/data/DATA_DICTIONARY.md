# Data dictionary

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
