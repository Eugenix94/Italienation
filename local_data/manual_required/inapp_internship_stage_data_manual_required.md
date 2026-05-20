# INAPP/Isfol Internship (Tirocinio) Prevalence Data

**Priority:** low

## Why this is needed
Italy has a well-documented problem of unpaid or low-paid internships ('stage') as a barrier to youth labour market entry. Structured data on internship prevalence, duration, and compensation by sector and region would contextualise the post-secondary employment gap in AlmaLaurea and ANPAL data.

## API/automation status
no known machine-readable endpoint — INAPP (formerly Isfol) publishes annual reports as PDF; no open data SDMX or CSV feed found.

## Manual steps to obtain data
- 1. Go to https://www.inapp.gov.it/ → Publications → Tirocini
- 2. Download annual tirocini monitoring report tables.
- 3. Relevant report: 'Quarto rapporto di monitoraggio dei tirocini' (latest year).

## Target output file
`local_data/manual_required/inapp_tirocini_summary.csv`

## Expected columns
`year`, `region`, `sector`, `internship_count`, `avg_duration_months`, `avg_compensation_eur`