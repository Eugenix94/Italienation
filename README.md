# Italienation

A compact, data-first repository supporting a comparative study of Italian NEETs (Not in Education, Employment, or Training). The Jupyter notebooks show how the author analysed the data in Python, but you do not need Python to use the data — the datasets are ready for exploration with spreadsheets or any analysis tool.

Why this repo
- Research goal: describe and compare the NEET phenomenon in Italy (demographics, trends, regional differences).
- Use the data directly for tables, charts, or your own analyses — the notebooks are optional examples.

Data 
- Location: primary project datasets are under local_data/ (raw-like source extracts and curated outputs).
- Processed indicators used by recent school-outcomes analyses are under local_data/processed/.
- Formats: CSV, parquet, or similar — can be opened in Excel/LibreOffice, R/Stata, Tableau, or any BI tool.
- NEET definition used: individuals in the chosen age range (e.g., 15–29) who are not in education, employment, or training. See data/codebooks for exact variable logic.
- Provenance & access: data/external_sources.md lists original sources (ISTAT, Eurostat, etc.), download dates and license notes. Do not expect restricted microdata to be bundled.
- Additional education source: the repository now includes a derived SNV Esiti bocciatura proxy built from the official Ministero dell'Istruzione opendata pages for school outcomes and class-admission language. See local_data/processed/snv_esiti_school_year_proxy.csv for the analysis-ready summary.

Quick start (no Python required)
1. Inspect data:
   - Open `data/processed/*.csv` in Excel, LibreOffice Calc, or your BI tool.
2. Load into R, Stata, or Tableau for analysis and visualization.
3. See `data/codebooks/` for variable descriptions and the exact NEET classification.

If you want to reproduce the author’s analyses
- Jupyter notebooks in `notebooks/` contain the Python workflow used to clean, analyse and plot the data (optional).
- To run them: install Jupyter and the listed packages, or view the notebooks directly on GitHub.

School Outcomes (2024/2025 proxy)
- Upper-secondary repeaters pipeline (ISTAT SDMX): local_data/processed/istat_repeaters_upper_secondary_latest.csv and local_data/processed/istat_repeaters_upper_secondary_ranking.csv.
- Lower-secondary indicators + exam-failure proxy: local_data/processed/istat_lower_secondary_indicators_latest.csv and local_data/processed/istat_lower_secondary_exam_proxy_latest.csv.
- Upper-secondary full notebook: Notebooks/italy_bocciatura_repeaters_full_analysis_v2.ipynb.
- Lower-secondary full notebook: Notebooks/italy_lower_secondary_middle_school_analysis.ipynb.
- Integrated transition notebook (middle -> upper): Notebooks/italy_middle_to_upper_transition_analysis.ipynb.
- Exported transition charts for reuse: Notebooks/transition_outputs/transition_01_national_contrast.png, Notebooks/transition_outputs/transition_02_regional_stress_index.png, Notebooks/transition_outputs/transition_03_scatter_lower_vs_upper.png, Notebooks/transition_outputs/transition_04_upper_track_by_region.png, Notebooks/transition_outputs/transition_05_upper_voc_minus_lic_gap.png.

Cite & contact
- Please cite the repo and the original data sources when using results.
- Issues or questions: open an issue or contact the repository owner: https://github.com/Eugenix94

License
- Add a LICENSE file to clarify reuse terms (recommended: MIT or another appropriate license).
