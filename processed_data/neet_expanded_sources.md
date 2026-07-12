# Expanded NEET Sources

## Inputs
- local_data/ISTAT/istat_neet_new.csv
- local_data/NEET  (giovani non occupati e non in istruzione e formazione) - Dati regionali (IT1,172_931_DF_DCCV_NEET1_6,1.0).csv
- local_data/processed/transition_bridge_model_panel.csv

## Outputs
- neet_gender_year_panel.csv: National NEET panel by year, age group, and sex
- neet_gender_gap_by_year.csv: Female-minus-male NEET gap and female/male ratio by year and age group
- neet_gender_total_yearly.csv: Total-sex national NEET trend
- neet_covid_period_summary.csv: Pre-COVID, shock, and recovery summary by sex and age group
- neet_regional_target_panel.csv: Regional NEET target proxy using within-year normalized counts for ages 15-29
- neet_regional_model_panel.csv: Regional feature panel merged with the NEET target proxy
- neet_regional_risk_model_predictions.csv: Holdout-year predictions from the baseline region-level model
- neet_regional_risk_model_coefficients.csv: Standardized coefficients from the baseline model
- neet_regional_risk_model_metrics.json: Evaluation metrics for the baseline model

## Notes
- Gender analysis comes directly from the existing ISTAT national NEET micro-aggregation.
- COVID impact is summarized as a pre-COVID vs shock vs recovery comparison.
- The predictive model uses a within-year risk index because the regional source exposes counts rather than population shares.
- The baseline model is intentionally simple and reproducible; it is a starting point rather than a final forecasting system.
