# Italienation: Open Science Data Release

Welcome to the definitive Open Science data repository for **Italienation**. 
This release contains the complete, reproducible dataset and codebase used to empirically demonstrate the "Structural Double Penalty" within the Italian educational system.

## Overview
The research provides a mathematical and structural audit of the Italian educational system using the sociological Origin-Education-Destination (OED) framework. We demonstrate how early tracking (at age 14) serves as a mechanism of class segregation, exacerbated by regressive state resource allocation (infrastructural decay and teacher precarity concentrated in vocational institutes).

## Archive Structure
This repository contains the following key components necessary to replicate our findings:

*   **`processed_data/`**: Cleaned and normalized CSV/JSON files synthesizing nearly 900 raw datasets from ISTAT, MIM, MUR, Eurostat, OpenCoesione, and others.
    *   `master_oed_destination_matrix.json`: The core probabilities for dropout/NEET status across different tracks and systems.
*   **`local_data/`**: Contains the intermediate processed JSON and CSV datasets.
*   **`notebooks/`**: 60+ Jupyter notebooks detailing the econometric methodology, causal inference, and machine learning models (XGBoost/SHAP) used to validate the thesis. 
    *   `notebooks/regional_profiles/`: 21 automated, region-specific econometric profiles.
*   **`scripts/`**: The Python extraction, formatting, and scraping tools used to compile the raw data (ensuring strict provenance).
*   **`frontend/`**: The complete React (Vite) source code for the interactive OED Dashboard and Data Catalog.
*   **`docs/`**: The full suite of methodological audits, metadata tracing, AI methodology, and the definitive URL provenance registry.

## Methodology & Reproducibility
The core hypothesis was tested by linking MEF (Ministry of Economy) sub-municipal IRPEF tax data with MIM (Ministry of Education) school registries (`Scuole_in_chiaro`). Predictive modeling and correlation matrices confirmed that the probability of attending a Lyceum vs. a Vocational institute scales almost perfectly with neighborhood taxable income. 

1. Ensure you have a standard Python 3.10+ data science environment (`pandas`, `numpy`, `scikit-learn`, `shap`, etc.).
2. Execute any of the `.ipynb` files sequentially to reproduce the visualizations and statistical models.

## Web Dashboard
The mathematical profiles contained in this data release power an interactive React dashboard, available here:
[https://eugenix94.github.io/Italienation/](https://eugenix94.github.io/Italienation/)

## License & Citation
*   **Data**: All data derived from public ministries is subject to Open Data policies (IODL 2.0 / CC BY 4.0).
*   **Code**: The codebase (React frontend, Python scripts, Jupyter notebooks) is released under the MIT License.
*   **Citation**: Please use the Zenodo/OSF DOI generated for this release when referencing the data or the econometric methodology in academic publications.
