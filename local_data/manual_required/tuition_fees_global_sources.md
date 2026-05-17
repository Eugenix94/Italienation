# Global Tuition Fees and Tertiary Cost Sources

This file lists browser-verified sources to compare tuition fees and higher/tertiary costs across countries.

## 1) OECD (best source for tuition-fee comparability)

- OECD indicator page (tuition fees):
  - https://www.oecd.org/en/data/indicators/annual-tuition-fees-charged-by-educational-institutions.html
- OECD Data Explorer (interactive extraction):
  - https://data-explorer.oecd.org/
- OECD PIAAC portal (skills distribution and equity context):
  - https://www.oecd.org/skills/piaac/

Notes:
- OECD pages are JS-heavy and may fail automated fetch in this environment.
- Use browser export from OECD Data Explorer (CSV) for tuition-fee tables and country panels.

## 2) Eurostat (Europe-wide cost and aid, fully open API)

- Financial aid to students by education level:
  - https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/educ_uoe_fina01?format=TSV&compressed=true
- Annual expenditure per student (FTE):
  - https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/educ_uoe_fini04?format=TSV&compressed=true
- Expenditure by education level and institution type:
  - https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/educ_uoe_fini01?format=TSV&compressed=true

Notes:
- These are not direct tuition-fee prices, but are strong cost/support comparators.
- Pair with OECD tuition-fee indicators for full affordability analysis.

## 3) World Bank (global affordability and expenditure context)

- Learning poverty (now available and downloaded locally):
  - indicator code: SE.LPV.PRIM
  - API example (Italy): https://api.worldbank.org/v2/country/ITA/indicator/SE.LPV.PRIM?format=json&per_page=5000
- Public expenditure on education (% GDP):
  - indicator code: SE.XPD.TOTL.GD.ZS
  - API: https://api.worldbank.org/v2/country/all/indicator/SE.XPD.TOTL.GD.ZS?format=json&per_page=20000
- School enrollment, tertiary (gross):
  - indicator code: SE.TER.ENRR
  - API: https://api.worldbank.org/v2/country/all/indicator/SE.TER.ENRR?format=json&per_page=20000

Notes:
- WB does not directly provide tuition fees by country in WDI; use this for macro affordability context.

## 4) UNESCO UIS (global education finance and participation)

- UIS portal:
  - https://www.uis.unesco.org/en
- UIS data browser:
  - https://databrowser.uis.unesco.org/
- Education finance topic landing:
  - https://www.uis.unesco.org/en/topic/education-finance

Notes:
- UIS provides broad global comparability for education finance and participation metrics.

## 5) Italy-specific tuition/aid sources (for benchmark against global)

- USTAT MUR open data catalog:
  - https://dati-ustat.mur.gov.it/
- 2024 university contribution and interventions (fees/exemptions/interventions):
  - https://dati-ustat.mur.gov.it/dataset/2024-contribuzione-e-interventi-atenei
- DSU regional (right to study, aid and services):
  - https://dati-ustat.mur.gov.it/dataset/2025-diritto-allo-studio-universitario-dsu-regionale

## Recommended integration order

1. Italy tuition + aid: MUR (contribuzione, esoneri, DSU).
2. Europe tuition-support comparability: Eurostat aid + per-student expenditure.
3. OECD tuition-fee indicator export for direct international fee comparisons.
4. WB/UIS indicators for global affordability and participation context.
