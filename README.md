# 🇮🇹 Italienation: An Open Science Observatory & Data Laboratory on Italian Education & Youth Transitions

> **Open Science Philosophy & Invitation:** This repository is built on the conviction that structural challenges in education and youth labor markets cannot be resolved through top-down policy dogma. Instead of dictating closed conclusions, we provide an **open-ended empirical laboratory** across **11 open data domains**, **815,000+ teaching posts**, and **113 years of fiscal history**. We invite researchers, data scientists, educators, citizens, and policymakers to explore the data, test alternative hypotheses, and debate interpretations collaboratively.

---

## 📖 What is *Italienation* (*Italienazione*)? An Extensive 7-Dimension Manifesto

To analyze Italian educational and youth transition dynamics, we must move beyond synthetic definitions. **Italienation** (*Italienazione*) is a chronic, multi-generational, structural equilibrium that crosses seven interconnected sociological, economic, and institutional dimensions:

1. **Etymological & Conceptual Genesis (*Structural Anomie*):** A neologism fusing *Italy* and *Alienation*, describing a structural condition where public institutions, economic incentives, and educational bottlenecks systematically estrange youth (*NEETs*, early school leavers, precarious workers, young researchers) from active civic and economic life.
2. **Intergenerational Breakdown & Demographic Winter (*Inverno Demografico*):** Operating alongside a birth rate of `1.20 children per woman` and an aging population (`>48 yrs median`), public wealth is overwhelmingly allocated toward passive incumbent preservation (pensions, senior welfare, debt servicing) while forward-looking human capital investments (nursery care, schools, university labs) face four decades of structural retrenchment.
3. **Territorial Dualism & Municipal Urban Penalty (*Penalità Urbana*):** Where municipal nursery seat coverage (`0–2 years`) drops below `15%` across Southern metropolitan capitals (`Napoli, Catania, Palermo`), youth NEET rates systematically exceed `25% to 35%` (`r = -0.88`), pre-sorting educational inequality before age three.
4. **Pedagogical Segregation & Workforce Precariato (*Giungla del Precariato*):** Secondary schools suffer from rigid age-14 tracking (*Licei* vs *Tecnici* vs *Professionali*) coupled with massive teaching instability: `18.5%` of classroom chairs and **over 60% of special needs (*Sostegno*) chairs** are filled by temporary annual substitutes (`Supplenti`), destroying pedagogical continuity.
5. **Higher Education Bottleneck & Brain Drain (*Fuga dei Cervelli*):** Chronic university underfunding (`MUR`) and rigid academic recruitment structures drive over **40,000+ young graduates to emigrate abroad annually** because domestic micro-enterprises cannot offer competitive R&D wages or meritocratic ladders.
6. **Labor Market Trap & Real Wage Stagnation (*Lavoro Povero*):** Italy holds the highest youth NEET rate (`16.1%`) in the EU-27 and is the only OECD economy where real wages declined between 1990 and 2024, locking youth into precarious, low-wage dependency well into adulthood.
7. **The Open Science Imperative:** Because *Italienation* is a complex web of interlocking historical and economic feedback loops, no single dogma can resolve it. It demands an **Open Science Collaborative Observatory** where global researchers and citizens can freely interrogate raw data, test hypotheses, and debate structural solutions.

---

## 🌟 Quick Access: The Holistic Open Science Observatory (`holistic_analysis/`)

We have gathered our complete, highly analysed data panels (`data_panels/`) and a zero-setup interactive web observatory into a dedicated standalone folder for the public:

* **👉 Explore the Interactive HTML Observatory:** [`holistic_analysis/interactive_web_experience/index.html`](./holistic_analysis/interactive_web_experience/index.html) (Single-file open-ended web experience featuring our 7-dimension definition, interactive tabs, live tables, reflection prompts, and notebook diagnostics).
* **📊 Download the 13 Open Data Panels:** [`holistic_analysis/data_panels/`](./holistic_analysis/data_panels/) (Curated CSV tables covering public expenditure, Eurostat benchmarks, Openpolis municipal censuses, HuggingFace teacher registries, and INVALSI competency gaps).
* **💻 Fork the Master Python Pipeline:** [`holistic_analysis/jupyter_notebook/italienation_holistic_master_analysis.ipynb`](./holistic_analysis/jupyter_notebook/italienation_holistic_master_analysis.ipynb) (Fully reproducible, open-source synthesis notebook).

---
## 🌟 Quick Access: The Holistic Open Science Observatory (`holistic_analysis/`)

We have gathered our complete, highly analysed data panels (`data_panels/`) and a zero-setup interactive web observatory into a dedicated standalone folder for the public:

* **👉 Explore the Interactive HTML Observatory:** [`holistic_analysis/interactive_web_experience/index.html`](./holistic_analysis/interactive_web_experience/index.html) (Single-file open-ended web experience with tabs, live tables, reflection prompts, and notebook diagnostics).
* **📊 Download the 13 Open Data Panels:** [`holistic_analysis/data_panels/`](./holistic_analysis/data_panels/) (Curated CSV tables covering public expenditure, Eurostat benchmarks, Openpolis municipal censuses, HuggingFace teacher registries, and INVALSI competency gaps).
* **💻 Fork the Master Python Pipeline:** [`holistic_analysis/jupyter_notebook/italienation_holistic_master_analysis.ipynb`](./holistic_analysis/jupyter_notebook/italienation_holistic_master_analysis.ipynb) (Fully reproducible, open-source synthesis notebook).

---

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
