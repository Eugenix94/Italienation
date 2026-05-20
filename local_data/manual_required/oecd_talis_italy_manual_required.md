# OECD TALIS Italy — Teacher Working Conditions and Professional Development

**Priority:** medium

## Why this is needed
TALIS 2018 and 2024 provide teacher professional development participation, job satisfaction, classroom management practices, and share with permanent contracts. Relevant for hypothesis that teacher precariousness affects educational quality (bocciatura rates, INVALSI scores).

## API/automation status
blocked — OECD SDMX (sdmx.oecd.org) has no TALIS dataflow in OECD.EDU.IMEP catalogue; data-api.oecd.org DNS unresolvable from this environment; TALIS microdata requires registration.

## Manual steps to obtain data
- 1. Go to https://www.oecd.org/education/talis/talisproducts.htm
- 2. Download 'TALIS 2018 Country Notes — Italy' PDF for key indicators.
- 3. For structured data: https://stats.oecd.org/Index.aspx?DataSetCode=TALIS_2018 → export Italy data as CSV.
- 4. Alternatively use the TALIS 2018 Technical Report Annex tables.

## Target output file
`local_data/oecd/oecd_it_talis_teacher_conditions.csv`

## Expected columns
`year`, `indicator`, `italy_value`, `oecd_avg`