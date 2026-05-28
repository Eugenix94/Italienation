# Sources Verified (2026-05-23)

This file records live source checks for blind spots requested in the NEET/education pipeline.

## 1) INPS Open Data (apprenticeship pathway)

Status: reachable, with working catalog and API docs.

Verified pages:
- Open Data landing: https://www.inps.it/it/it/dati-e-bilanci/open-data.html
- Download catalog page: https://www.inps.it/it/it/dati-e-bilanci/open-data/scarica-gli-open-data.html
- API documentation: https://www.inps.it/it/it/dati-e-bilanci/open-data/api-inps.html

Verified API endpoints from INPS docs:
- https://serviziweb2.inps.it/odapi/package_list
- https://serviziweb2.inps.it/odapi/package_show?id={id-dataset}
- https://serviziweb2.inps.it/odapi/current_package_list_with_resources?limit=50
- https://serviziweb2.inps.it/odapi/bulk?limit=50
- https://serviziweb2.inps.it/odapi/bulk_download?limit=50
- https://serviziweb2.inps.it/odapi/status

Notes:
- `package_search` style queries (for example `.../package_search?q=apprendistato`) did not return CKAN JSON search results in this run and resolved to HTML Open Data content.
- Apprenticeship-specific datasets are likely present under catalog metadata labels/titles rather than obvious ID strings. Reliable extraction path is:
  1. Use `current_package_list_with_resources` in pages,
  2. filter titles/notes for `apprendistato`, `apprendista`, `contratti`,
  3. then pull detail metadata via `package_show?id=...`.

## 2) OECD TALIS (Italy pathways)

Status: reachable with direct Italy-specific endpoints.

Verified pages:
- TALIS 2024 report: https://www.oecd.org/en/publications/results-from-talis-2024_90df6235-en.html
- Support materials: https://www.oecd.org/en/publications/results-from-talis-2024_90df6235-en/support-materials.html
- TALIS participants index: https://www.oecd.org/en/about/programmes/talis/talis-participants.html
- TALIS Italy participant page: https://www.oecd.org/en/about/programmes/talis/italy.html

Verified direct downloads/data paths:
- TALIS 2024 PDF: https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/10/results-from-talis-2024_28fbde1d/90df6235-en.pdf
- TALIS participation summary XLSX: https://www.oecd.org/content/dam/oecd/en/about/programmes/edu/talis/directories-index/TALIS_cycles_participation.xlsx/_jcr_content/renditions/original.media_file.download_attachment.file/TALIS_cycles_participation.xlsx
- TALIS 2024 database landing: https://www.oecd.org/en/data/datasets/talis-2024-database.html
- TALIS Italy interactive dashboard entry: https://gpseducation.oecd.org/CountryProfile?plotter=h5&primaryCountry=ITA&treshold=5&topic=TA

## 3) ISTAT parental/family education flow discovery

Status: reached and parsed via SDMX dataflow endpoint.

Verified endpoint:
- https://esploradati.istat.it/SDMXWS/rest/dataflow/IT1/all/latest

Generated artifact:
- `local_data/processed/istat_parental_keyword_flows.csv` (351 rows)

Purpose of artifact:
- Maps `flow_id` + Italian flow title candidates related to:
  - NEET by role in family / education,
  - parental labor condition,
  - family-role structures,
  - parental background proxies.

High-priority flow candidates captured:
- `172_931_DF_DCCV_NEET1_2` (NEET by European professional condition and education)
- `172_931_DF_DCCV_NEET1_4` (NEET by role in family)
- `172_931_DF_DCCV_NEET1_8` (NEET incidence by education)
- `172_931_DF_DCCV_NEET1_10` (NEET incidence by role in family)
- `723_1040_DF_DCCV_RUOLOFAMCOND_4` (parents employed/unemployed/inactive by number of children)
- `723_1040_DF_DCCV_RUOLOFAMCOND_5` (parents employed/unemployed/inactive by age of youngest child)

## 4) Remaining blind-spot actions

- INPS apprenticeship: run full paginated metadata pull and filter on titles/notes/resource names, then pin exact dataset IDs and resource URLs.
- TALIS: extract machine-readable tables from `talis-2024-database` endpoint into a local staged CSV/manifest.
- ISTAT parental education: rank the 351 candidate flows into:
  - direct parent-education indicators,
  - indirect proxies,
  - out-of-scope family context series.

## 5) INPS ID Pinning Update (2026-05-24)

Artifacts generated:
- `local_data/processed/inps_odapi_candidate_packages_2026-05-24.json`
- `local_data/processed/inps_odapi_candidate_packages_2026-05-24.csv`
- `local_data/processed/inps_apprenticeship_informal_hits_2026-05-24.json`
- `local_data/processed/inps_apprenticeship_informal_hits_2026-05-24.csv`

Scan summary:
- 2,300 packages scanned before timeout on later pagination.
- 9 direct hits for apprenticeship/informal/irregular keywords.

Pinned examples (package_id -> resource URLs):
- `numero-dipendenti-apprendistato-e-con-contratto-a-termine,-numero-giornate-lavorate-e-variazioni-percentuali-nel-settore-extra-agricolo-e-nel-settore-pubblico-divisi-per-anno-e-tipologia-di-contratto.-anni-2016-2017.-tav.-1.13`
  - `http://www.inps.it/docallegati/Mig/OpenData/CSV/ID-5515.csv`
- `numero-dipendenti-apprendistato-e-con-contratto-a-termine,-numero-giornate-lavorate-e-variazioni-percentuali-nel-settore-extra-agricolo-e-nel-settore-pubblico-divisi-per-anno-e-tipologia-di-orario-di-lavoro.-anni-2016-2017.-tav.-1.13`
  - `http://www.inps.it/docallegati/Mig/OpenData/CSV/ID-5516.csv`
- `numero-rapporti-di-lavoro-operai-non-agricoli-ed-apprendisti-nelle-aziende-agricole-divisi-per-anno-e-regione.-serie-storica,-anni-2010-2016`
  - `http://www.inps.it/docallegati/Mig/OpenData/CSV/ID-5139.csv`
- `lavoratori-in-nero-e-irregolari-distribuzione-per-area-geografica--attivit&#224;-2013`
  - `http://www.inps.it/docallegati/Mig/OpenData/ID-2326.csv`
- `lavoratori-in-nero-e-irregolari-distribuzione-per-gestione--attivit&#224;-2013`
  - `http://www.inps.it/docallegati/Mig/OpenData/ID-2324.csv`

Operational note:
- INPS `odapi/current_package_list_with_resources` is the reliable discovery route.
- `package_search?q=...` did not provide usable CKAN JSON in this environment.

Implementation files added for repeatability:
- scripts/fetch_inps_destination_data.py
- scripts/build_oed_destination_panel.py
