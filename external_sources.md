# External Data Sources

This file lists the original sources for all datasets used in this repository, including direct links, dataset identifiers, and license/access notes. Datasets cover Italian NEETs, education spending, outcomes, and related socio-economic indicators.

---

## 1. ISTAT — Italian National Institute of Statistics

**Website:** <https://esploradati.istat.it/databrowser/>  
**Legacy portal (I.Stat):** <http://dati.istat.it/>  
**License:** Open data — [ISTAT data licence](https://www.istat.it/en/legal-notes)

| File (local_data/) | Dataset / Dataflow | Description |
|---|---|---|
| `NEET … Dati regionali (IT1,172_931_DF_DCCV_NEET1_6,1.0).csv` | `DF_DCCV_NEET1_6` | Italian NEET counts by region and age group |
| `NEET … Condizione professionele europea, cittadinanza (IT1,172_931_DF_DCCV_NEET1_3,1.0).csv` | `DF_DCCV_NEET1_3` | Italian NEET by European employment status and citizenship |
| `NEET … Condizione professionale europea, titolo di studio (IT1,172_931_DF_DCCV_NEET1_2,1.0).csv` | `DF_DCCV_NEET1_2` | Italian NEET by European employment status and education level |
| `Incidenza dei giovani Neet - Titolo di studio (IT1,172_931_DF_DCCV_NEET1_8,1.0).csv` | `DF_DCCV_NEET1_8` | NEET incidence rate by education level |

All four files share the dataflow family `DCCV_NEET1` (dataflow series `172_931`) from the ISTAT SDMX dissemination service.  
Direct API base URL: `https://esploradati.istat.it/SDMXWS/rest/data/IT1,172_931_DF_DCCV_NEET1_<variant>,1.0/`

---

## 2. Eurostat — EU Statistical Office

**Website:** <https://ec.europa.eu/eurostat/web/main/data/database>  
**License:** [Eurostat copyright and free re-use policy](https://ec.europa.eu/eurostat/web/main/about/our-partners/reuse-of-eurostat-data)

| File (local_data/) | Dataset code | Description | Direct link |
|---|---|---|---|
| `ESTAT_EDAT_LFSE_22$DEFAULTVIEW_1.0.xml` | `edat_lfse_22` | Young people (15–29) not in employment, education or training | <https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_22/default/table> |
| `ESTAT_TPS00203_1.0.xml` | `tps00203` | Share of young people not in education, employment or training (NEET), Eurostat SDG indicator | <https://ec.europa.eu/eurostat/databrowser/view/tps00203/default/table> |
| `EurostatNeet/dataset1/` | `edat_lfse_22` (subset) | NEET — detailed breakdown, downloaded as TSV | <https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_22/default/table> |
| `EurostatNeet/dataset2/` | `edat_lfse_22` (subset) | NEET — additional breakdown | <https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_22/default/table> |
| `educ_uoe_fini01$defaultview_linear_2_0.csv` | `educ_uoe_fini01` | Expenditure of educational institutions by level, institution type and expenditure category | <https://ec.europa.eu/eurostat/databrowser/view/educ_uoe_fini01/default/table> |

SDMX REST API base URL: `https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/<dataset_code>`  
Example (GDP per capita, fetched by fetch script): `https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/tec00114?format=SDMX-CSV`

---

## 3. OECD — Organisation for Economic Co-operation and Development

**Website:** <https://data.oecd.org/>  
**SDMX API:** <https://sdmx.oecd.org/public/rest/>  
**License:** [OECD Terms and Conditions](https://www.oecd.org/termsandconditions/)

### 3a. Education at a Glance (EAG) — fetched via API (api_data/)

| Output file | SDMX dataflow | Description | OECD.Stat link |
|---|---|---|---|
| `oecd_education_fin_perstud.csv` | `OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_INDIC_FIN_PERSTUD,3.1` | Annual expenditure per student by education level (USD PPP) | <https://data.oecd.org/eduresource/education-spending.htm> |
| `oecd_education_fin_gdp.csv` | `OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_INDIC_FIN_GDP,1.0` | Education spending as % of GDP by source | <https://data.oecd.org/eduresource/education-spending.htm> |
| `oecd_education_fin_indic_source_nature.csv` | `OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_FIN_INDIC_SOURCE_NATURE,3.1` | Financial indicators by source and nature of expenditure | <https://data.oecd.org/eduresource/education-spending.htm> |
| `oecd_education_funding_sources.csv` | `OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_FIN_SOURCE_GV_PR_NDOM,3.1` | Education funding sources (public, private, international) | <https://data.oecd.org/eduresource/education-spending.htm> |
| `oecd_education_nature_cur_cap.csv` | `OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_FIN_NATURE_CUR_CAP,3.1` | Education expenditure by current vs capital nature | <https://data.oecd.org/eduresource/education-spending.htm> |
| `oecd_education_nature_staff.csv` | `OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_FIN_NATURE_STAFF,3.1` | Education expenditure by staff nature and institution type | <https://data.oecd.org/eduresource/education-spending.htm> |
| `oecd_education_costs.csv` | `OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_FIN_NATURE_STAFF,3.1` | Education capital and cost data | <https://data.oecd.org/eduresource/education-spending.htm> |
| `oecd_education_non_fin_pers.csv` | `OECD.EDU.IMEP,DSD_EAG_UOE_NON_FIN_PERS@DF_UOE_NF_PERS_CLS,1.0` | Non-financial education personnel (teachers/staff) | <https://data.oecd.org/teachers/education-staff.htm> |
| `oecd_education_attainment_migration.csv` | `OECD.EDU.IMEP,DSD_EAG_LSO_EA@DF_LSO_NEAC_DISTR_EA_MIGR,1.0` | Adults' educational attainment by country of birth and migration age | <https://data.oecd.org/eduatt/adult-education-level.htm> |
| `oecd_eag_transition.csv` | `OECD,DF_EAG_TRANS` | Education-to-work transition indicators (EAG) | <https://data.oecd.org/education.htm> |

### 3b. Downloaded OECD datasets (local_data/oecd/)

| File | SDMX dataflow | Description | OECD.Stat link |
|---|---|---|---|
| `OECD.EDU.IMEP,DSD_EAG_LSO_EA@DF_LSO_NEAC_DISTR_EA_MIGR,1.0+all.csv` | `DSD_EAG_LSO_EA@DF_LSO_NEAC_DISTR_EA_MIGR` | Adults' educational attainment distribution, by country of birth | <https://data.oecd.org/eduatt/adult-education-level.htm> |
| `OECD.ELS.JAI,DSD_TAXBEN_HOURSPOV@DF_HOURSPOV,1.0+all.csv` | `DSD_TAXBEN_HOURSPOV@DF_HOURSPOV` | Working hours needed to escape poverty (tax-benefit model) | <https://data.oecd.org/socialexp/social-spending.htm> |
| `OECD.ELS.SAE,DSD_EARNINGS@AGE_WAGE_GAP,1.0+all.csv` | `DSD_EARNINGS@AGE_WAGE_GAP` | Age wage gap | <https://data.oecd.org/earnwage/average-wages.htm> |
| `OECD.ELS.SAE,DSD_EARNINGS@PAY_INCIDENCE,1.0+all.csv` | `DSD_EARNINGS@PAY_INCIDENCE` | Low pay incidence | <https://data.oecd.org/earnwage/average-wages.htm> |
| `OECD.ELS.SAE,DSD_EARNINGS@RMW,1.0+all.csv` | `DSD_EARNINGS@RMW` | Real minimum wages | <https://data.oecd.org/earnwage/minimum-wages.htm> |
| `OECD.GOV.GIP,DSD_GOV@DF_GOV_INFPD_2025,1.0+all.csv` | `DSD_GOV@DF_GOV_INFPD_2025` | Infrastructure planning and delivery indexes (Government at a Glance 2025) | <https://data.oecd.org/government.htm> |
| `OECD.GOV.GIP,DSD_GOV@DF_GOV_PPROC_2025,1.0+all.csv` | `DSD_GOV@DF_GOV_PPROC_2025` | Public procurement indicators (Government at a Glance 2025) | <https://data.oecd.org/government/public-procurement.htm> |
| `OECD.GOV.GIP,DSD_QDD_GOV_PUBPRO_2024@DF_GOV_PUBPRO_2024,1.0+all.csv` | `DSD_QDD_GOV_PUBPRO_2024@DF_GOV_PUBPRO_2024` | Public sector productivity (Government at a Glance 2024) | <https://data.oecd.org/government.htm> |
| `OECD.SDD.TPS,DSD_EAR@DF_HOU_EAR,1.0+all.csv` | `DSD_EAR@DF_HOU_EAR` | Household earnings distribution | <https://data.oecd.org/earnwage/average-wages.htm> |

---

## 4. World Bank — Open Data

**Website:** <https://data.worldbank.org/>  
**License:** [Creative Commons Attribution 4.0 (CC BY 4.0)](https://datacatalog.worldbank.org/public-licenses#cc-by)

| File (local_data/) | Indicator code | Description | Direct link |
|---|---|---|---|
| `API_HD.HCI.OVRL_DS63_en_csv_v2_756596.csv` | `HD.HCI.OVRL` | Human Capital Index (HCI), scale 0–1, 2020 | <https://data.worldbank.org/indicator/HD.HCI.OVRL> |
| `WB_WDI_SI_POV_GINI.csv` | `SI.POV.GINI` | Gini index (World Development Indicators) | <https://data.worldbank.org/indicator/SI.POV.GINI> |

---

## 5. Our World in Data

**Website:** <https://ourworldindata.org/>  
**License:** Data files carry the licence of the underlying original source (see each dataset's `readme.md`). Our World in Data's own work is [CC BY 4.0](https://ourworldindata.org/faqs#can-i-use-or-reproduce-your-data-and-visualizations).

All files below are in `local_data/ourWorldData/`.

| Subfolder | Chart / Original source | Description | Direct link |
|---|---|---|---|
| `EdGovSpending/` | UNESCO UIS via World Bank (WDI) | Education spending as share of total government spending | <https://ourworldindata.org/grapher/share-of-education-in-government-expenditure> |
| `completion-rate-of-upper-secondary-education-sdg/` | UNESCO Institute for Statistics | Completion rate of upper secondary education | <https://ourworldindata.org/grapher/completion-rate-of-upper-secondary-education-sdg> |
| `duration-of-compulsory-education/` | UNESCO UIS | Duration of compulsory education (years) | <https://ourworldindata.org/grapher/duration-of-compulsory-education> |
| `gni-per-capita-vs-gdp-per-capita/` | World Bank | GNI per capita vs GDP per capita | <https://ourworldindata.org/grapher/gni-per-capita-vs-gdp-per-capita> |
| `inequality-adjusted-hdi-vs-human-development-index/` | UNDP (Human Development Reports) | Inequality-adjusted HDI vs HDI | <https://ourworldindata.org/grapher/inequality-adjusted-hdi-vs-human-development-index> |
| `literacy-rates-vs-average-years-of-schooling/` | UNESCO UIS / Barro & Lee | Literacy rates vs average years of schooling | <https://ourworldindata.org/grapher/literacy-rates-vs-average-years-of-schooling> |
| `mean-daily-per-capita-expenditure-vs-gdp-per-capita/` | World Bank PovcalNet | Mean daily per-capita expenditure vs GDP per capita | <https://ourworldindata.org/grapher/mean-daily-per-capita-expenditure-vs-gdp-per-capita> |
| `poverty-vs-mean-schooling/` | World Bank / Barro & Lee | Poverty rate vs mean years of schooling | <https://ourworldindata.org/grapher/poverty-vs-mean-schooling> |
| `primary-secondary-enrollment-completion-rates/` | UNESCO UIS | Primary and secondary enrollment and completion rates | <https://ourworldindata.org/grapher/primary-secondary-enrollment-completion-rates> |
| `productivity-vs-educational-attainment/` | Penn World Table / Barro & Lee | Labour productivity vs educational attainment | <https://ourworldindata.org/grapher/productivity-vs-educational-attainment> |
| `quality-vs-quantity-of-schooling/` | PISA / Barro & Lee | Quality vs quantity of schooling | <https://ourworldindata.org/grapher/quality-vs-quantity-of-schooling> |
| `share-employment-agriculture-industry-services/` | ILO (ILOSTAT) | Share of employment by sector | <https://ourworldindata.org/grapher/share-employment-agriculture-industry-services> |
| `tax-revenues-as-a-share-of-gdp-unu-wider/` | UNU-WIDER (Government Revenue Dataset) | Tax revenues as % of GDP | <https://ourworldindata.org/grapher/tax-revenues-as-a-share-of-gdp-unu-wider> |
| `total-government-expenditure-on-education-gdp/` | UNESCO UIS via World Bank (WDI) | Government education expenditure as % of GDP | <https://ourworldindata.org/grapher/total-government-expenditure-on-education-gdp> |
| `total-number-of-emigrants.csv` | UN DESA (International Migrant Stock) | Total number of emigrants by country | <https://ourworldindata.org/migration> |

---

## 6. UK ONS — Office for National Statistics

**Website:** <https://www.ons.gov.uk/>  
**License:** [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)

| File (local_data/) | Description | Direct link |
|---|---|---|
| `Figure_1__The_percentage_of_young_people_who_are_not_in_education,_employment_or_training_(NEET)_increased_over_the_quarter_(January_to_March_2025).csv` | UK NEET rate for 16–24 year olds (seasonally adjusted), January 2019–June 2025 | <https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/bulletins/youngpeoplenotineducationemploymentortrainingneet/latest> |

---

## 7. UK SDG Statistics — Office for National Statistics

**Website:** <https://sdgdata.gov.uk/>  
**License:** [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)

Files in `local_data/UKSDGstats/` contain UK data for UN Sustainable Development Goals indicators, covering education (SDG 4), reduced inequalities (SDG 10), peace and institutions (SDG 16), and poverty (SDG 1).  
Direct link to the data platform: <https://sdgdata.gov.uk/>

---

## 8. NEETs ET2025 — European Commission / Cedefop

**File:** `local_data/NEETs_ET2025.xlsx`  
**Likely source:** European Commission Education and Training Monitor and/or Cedefop NEET data series under the Education and Training 2025 framework.

- **European Commission — Education and Training Monitor:** <https://education.ec.europa.eu/et-monitor>  
- **Cedefop NEET data:** <https://www.cedefop.europa.eu/en/tools/neet-online-tool>  
- **Eurostat ET2025 indicators:** <https://ec.europa.eu/eurostat/web/europe-2020-indicators/europe-2020-strategy/headline-indicators-scoreboard>

---

## 9. Italian Ministry of Education (MIM) — Ministero dell'Istruzione e del Merito

**Website:** <https://www.istruzione.it/>  
**License:** Open data — [Italian Open Government Licence](https://www.dati.gov.it/content/italian-open-data-license-v20)

| File (local_data/) | Description | Source |
|---|---|---|
| `ItalyPrimarySchoolBookExpenses.csv` | Official cover prices of primary school textbooks for the 2025/2026 school year, as set by Ministerial Decree n. 73/2025 | [MIM — Testi scolastici](https://www.istruzione.it/area_studenti/testi_scolastici.shtml) |
| `ItalianMeanSecondarySchoolExpenses.csv` | Estimated mean annual spending per student in Italian secondary schools (textbooks + materials) | Derived from MIM ministerial ceiling tables for secondary school textbooks |
