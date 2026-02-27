# Italienation

A compact, data-first repository supporting a comparative study of Italian NEETs (Not in Education, Employment, or Training). The Jupyter notebooks show how the author analysed the data in Python, but you do not need Python to use the data — the datasets are ready for exploration with spreadsheets or any analysis tool.

Why this repo
- Research goal: describe and compare the NEET phenomenon in Italy (demographics, trends, regional differences).
- Use the data directly for tables, charts, or your own analyses — the notebooks are optional examples.

Data 
- Location: data/ (raw/ contains original files; processed/ contains analysis-ready files).
- Formats: CSV, parquet, or similar — can be opened in Excel/LibreOffice, R/Stata, Tableau, or any BI tool.
- NEET definition used: individuals in the chosen age range (e.g., 15–29) who are not in education, employment, or training. See data/codebooks for exact variable logic.
- Provenance & access: [external_sources.md](external_sources.md) lists original sources (ISTAT, Eurostat, OECD, World Bank, Our World in Data, UK ONS, etc.) with direct links, dataset identifiers, and license notes. Do not expect restricted microdata to be bundled.

Quick start (no Python required)
1. Inspect data:
   - Open `data/processed/*.csv` in Excel, LibreOffice Calc, or your BI tool.
2. Load into R, Stata, or Tableau for analysis and visualization.
3. See `data/codebooks/` for variable descriptions and the exact NEET classification.

If you want to reproduce the author’s analyses
- Jupyter notebooks in `notebooks/` contain the Python workflow used to clean, analyse and plot the data (optional).
- To run them: install Jupyter and the listed packages, or view the notebooks directly on GitHub.

Cite & contact
- Please cite the repo and the original data sources when using results.
- Issues or questions: open an issue or contact the repository owner: https://github.com/Eugenix94

License
- Add a LICENSE file to clarify reuse terms (recommended: MIT or another appropriate license).
