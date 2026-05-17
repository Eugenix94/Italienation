# Valid Data Shortlist (Verified 2026-05-17)

## Confirmed valid and accessible now

### ISTAT (Italy)
- Disability inclusion tables (download works):
  - https://www.istat.it/wp-content/uploads/2024/02/tavole-alunni-con-disabilit%C3%A0-as.2022-2023.xlsx
- Mental wellbeing tables (download works):
  - https://www.istat.it/wp-content/uploads/2018/07/Tavole-dati-_Salute-mentale.xlsx

### World Bank (global)
- Learning poverty (valid code): `SE.LPV.PRIM`
  - Example API: https://api.worldbank.org/v2/country/ITA/indicator/SE.LPV.PRIM?format=json&per_page=5000
- Public spending on education (% GDP): `SE.XPD.TOTL.GD.ZS`
- Tertiary spending per student (% GDP per capita): `SE.XPD.TERT.PC.ZS`
- Tertiary enrollment, gross: `SE.TER.ENRR`

Downloaded to local files:
- local_data/worldbank/wb_learning_poverty.csv
- local_data/worldbank/wb_education_spending_pct_gdp.csv
- local_data/worldbank/wb_tertiary_spending_pct_gdp_percapita.csv
- local_data/worldbank/wb_tertiary_enrollment_gross.csv

### UNESCO UIS (global)
- UIS Data Browser is reachable and supports direct CSV/Excel export:
  - https://databrowser.uis.unesco.org/

## Confirmed invalid / blocked in this environment

### Eurostat ALMP legacy codes
- `lmp_ind_exp`: not found in Eurostat SDMX 2.1 catalog / databrowser
- `lmp_ind_actp`: not found in Eurostat SDMX 2.1 catalog / databrowser

### OECD web indicators
- OECD tuition-fee and EAG pages are Cloudflare/403 blocked from this execution environment.
- Source remains valid for manual browser export outside this environment:
  - https://www.oecd.org/en/data/indicators/annual-tuition-fees-charged-by-educational-institutions.html

## Practical recommendation
- Use World Bank + UIS as the global machine-readable backbone.
- Use OECD tuition-fee indicator via manual browser export and then ingest as CSV into local_data/oecd.
- Keep ISTAT manual tables as authoritative Italy deep-dive inputs for disability and wellbeing dimensions.
