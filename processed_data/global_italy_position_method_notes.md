# Global Italy Position Notes

Data sources combined:
- World Bank-derived global panel: local_data/processed/global_he_cost_access_panel.csv
- OECD funding sources: local_data/oecd/oecd_education_funding_sources.csv
- OECD per-student finance: local_data/oecd/oecd_education_fin_perstud.csv

Ranking methodology:
- For each metric, Italy is ranked among countries with non-missing data for that metric.
- Rank direction is metric-specific (e.g., lower learning poverty is better; higher tertiary enrollment is better).
- italy_pct_better is converted to 0-100 scale where 100 indicates top rank for that metric.

Caveats:
- OECD and World Bank years can differ by metric; this table is a latest-available cross-sectional benchmark.
- Some variables are proxies, not direct causal policy measures.