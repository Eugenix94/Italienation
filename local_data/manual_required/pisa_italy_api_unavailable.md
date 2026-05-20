# PISA Italy Data — API Unavailable

## Status
- `data-api.oecd.org` not DNS-resolvable from this environment.
- OECD SDMX via `sdmx.oecd.org` has no PISA dataflow in OECD.EDU.IMEP catalogue.
- PISA Excel files at oecd.org return 404/403.

## Current workaround
A static table `oecd/oecd_it_pisa_trend.csv` was generated from published OECD PISA reports.
All values carry `verification_required=True`. **Verify before use in published analysis.**

## Manual download options
1. https://www.oecd.org/pisa/data/ → 'PISA Data' → country-level mean scores CSV
2. OECD iLibrary PISA volumes → Annex B tables (Excel)
3. https://pisadataexplorer.oecd.org/ → export Italy trend data

## Target file
Place verified data at: `local_data/oecd/oecd_it_pisa_trend.csv`
Overwrite the static version (remove `data_type=static_curated` column when replacing).