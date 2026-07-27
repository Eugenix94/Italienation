# Italienation: OSF Data Release

Welcome to the Open Science Framework repository for **Italienation**.

This project provides a definitive mathematical and structural audit of the Italian educational system using the sociological Origin-Education-Destination (OED) framework.

## Archive Structure

This release (`Italienation_Data_Release_v1.zip`) contains the following key components necessary to replicate our findings:

*   **`local_data/processed/`**: Contains the final, synthesized JSON and CSV datasets. These files are the result of fusing hundreds of raw administrative files from the Ministry of Education (MIM), Ministry of Economy (MEF), ISTAT, and OpenCoesione. Key files include:
    *   `master_oed_destination_matrix.json`: The core probabilities for dropout/NEET status across different tracks and systems.
    *   `italy_systemic_ontology.json` / `blind_spots_ontology.json`: Structural and qualitative mapping of the data reality.
    *   `catania_structural_diagnostic.csv`: The granular case-study demonstrating severe urban inequality.
*   **`notebooks/regional_profiles/`**: 21 Jupyter notebooks containing automated, region-specific econometric profiles mapping educational supply against socioeconomic conditions.
*   **`notebooks/archive/`**: The macro-level synthesis notebooks (e.g., `48_grand_unified_capstone.ipynb`, `57_causal_inference_econometrics.ipynb`) that generate the high-level insights.
*   **`scripts/`**: The Python extraction, formatting, and scraping tools used to compile the raw data (ensuring strict provenance).

## Reproducibility

1.  Extract the archive to your local environment.
2.  Ensure you have a standard Python 3.10+ data science environment (`pandas`, `numpy`, `scikit-learn`, `shap`, etc.).
3.  Execute any of the `.ipynb` files sequentially to reproduce the visualizations and statistical models.

## License

All code and processed datasets are released under the **CC-BY-4.0** license. You are free to share and adapt the material for any purpose, even commercially, provided you give appropriate credit.

## Web Dashboard

The mathematical profiles contained in this data release power an interactive React dashboard, available here:
[https://eugenix94.github.io/Italienation/](https://eugenix94.github.io/Italienation/)
