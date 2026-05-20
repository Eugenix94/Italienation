# INPS Apprenticeship Contracts by Region/Sector/Year

**Priority:** high

## Why this is needed
Apprenticeship (contratto di apprendistato) is the main institutionalised school-to-work bridge in Italy. Data on contracts activated/terminated by region, sector, and school type directly measures the VET pathway's employment-creation capacity.

## API/automation status
blocked — INPS open data portal (inps.it/opendata) returns 404; odapi/wrapper.php endpoint not found; no SDMX feed identified.

## Manual steps to obtain data
- 1. Go to https://www.inps.it/it/it/dati-e-bilanci/opendata.html
- 2. Search for 'apprendistato' in the dataset catalogue.
- 3. Download annual CSV files for apprenticeship activations by region.
- Alternative: https://www.cliclavoro.gov.it/Barometro-Del-Lavoro/ → Apprendistato section → export tables.
- Alternative 2: https://www.lavoro.gov.it/temi-e-priorita/lavoro/focus-on/contratti-di-lavoro/Pagine/apprendistato.aspx → Dati statistici PDF/Excel.

## Target output file
`local_data/ISTAT/apprenticeship_contracts.csv`

## Expected columns
`year`, `region`, `sector_nace2`, `contracts_activated`, `contracts_terminated`