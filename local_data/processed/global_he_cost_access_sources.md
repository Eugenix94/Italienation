# Global HE Cost/Access Sources

Generated (UTC): 2026-05-16T23:10:13.563243+00:00

## Output files
- local_data/processed/global_he_cost_access_panel.csv
- local_data/processed/global_he_cost_access_latest_year.csv
- local_data/processed/italy_mur_tuition_benchmark_2024.csv

## World Bank indicators
- learning_poverty_pct
  - code: SE.LPV.PRIM
  - name: Learning poverty: share below minimum reading proficiency
  - source file: local_data/worldbank/wb_learning_poverty.csv
  - API: https://api.worldbank.org/v2/country/all/indicator/SE.LPV.PRIM?format=json&per_page=20000
- education_spending_pct_gdp
  - code: SE.XPD.TOTL.GD.ZS
  - name: Government expenditure on education, total (% of GDP)
  - source file: local_data/worldbank/wb_education_spending_pct_gdp.csv
  - API: https://api.worldbank.org/v2/country/all/indicator/SE.XPD.TOTL.GD.ZS?format=json&per_page=20000
- tertiary_spending_pct_gdp_percap
  - code: SE.XPD.TERT.PC.ZS
  - name: Expenditure per tertiary student (% of GDP per capita)
  - source file: local_data/worldbank/wb_tertiary_spending_pct_gdp_percapita.csv
  - API: https://api.worldbank.org/v2/country/all/indicator/SE.XPD.TERT.PC.ZS?format=json&per_page=20000
- tertiary_enrollment_gross_pct
  - code: SE.TER.ENRR
  - name: School enrollment, tertiary (% gross)
  - source file: local_data/worldbank/wb_tertiary_enrollment_gross.csv
  - API: https://api.worldbank.org/v2/country/all/indicator/SE.TER.ENRR?format=json&per_page=20000

## Italy tuition benchmark source (MUR)
- Dataset: 2024 Contribuzione e interventi atenei
- Catalog: https://dati-ustat.mur.gov.it/dataset/2024-contribuzione-e-interventi-atenei
- Source file: local_data/MUR/2024-contribuzione-e-interventi-atenei/2024_atenei_contribuzione_media.csv

## Caveats
- OECD tuition-fee pages were blocked in this execution environment and are not part of the automated pull.
- Eurostat legacy ALMP dataset codes lmp_ind_exp and lmp_ind_actp are invalid in current SDMX 2.1 catalog.
