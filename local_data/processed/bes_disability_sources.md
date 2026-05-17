# BES and Disability Sources Manifest

This manifest documents files used to build BES/disability indicators and student-count estimates.

## Outputs
- istat_disability_rate_timeseries_by_order.csv
- istat_bes_rate_by_region_order_2022_2023.csv
- ministry_students_by_region_order_2024_25.csv
- estimated_bes_students_by_region_order_2024_25_using_istat_rates.csv
- estimated_disabled_students_by_region_order_2024_25_using_national_rates.csv

## Sources
- istat_disability_bes_2022_2023: local_data/ISTAT/istat_disability_schools_2022_2023.xlsx
  - url: https://www.istat.it/wp-content/uploads/2024/02/tavole-alunni-con-disabilit%C3%A0-as.2022-2023.xlsx
  - notes: Tavola 1 (disability rates by order/year) and Tavola 11 (BES rates by region/order).
- mim_students_statali_2024_25: local_data/MinIstruzione/Alunni/ALUCORSOETASTA20242520250831.csv
  - notes: School-level students by age/course; used for regional enrollment totals.
- mim_students_paritarie_2024_25: local_data/MinIstruzione/Alunni/ALUCORSOETAPAR20242520250831.csv
  - notes: School-level students by age/course; used for regional enrollment totals.
- mim_school_registry_statali_2024_25: local_data/MinIstruzione/Scuole/SCUANAGRAFESTAT20242520250831.csv
  - notes: Contains school-region mapping for state schools.
- mim_school_registry_paritarie_2024_25: local_data/MinIstruzione/Scuole/SCUANAGRAFEPAR20242520250831.csv
  - notes: Contains school-region mapping for non-state schools.

## Caveats
- BES and disability student counts are estimated for 2024/25 by applying published ISTAT rates to Ministry enrollment totals.
- Estimated disability counts use national order-specific rates (from ISTAT Tavola 1), not region-specific disability rates.
- Estimated BES counts use region+order rates from ISTAT Tavola 11 (school year 2022/23).
- Current Ministry student extracts used in this pipeline do not include scuola infanzia rows, so estimates cover primary and secondary levels only.
