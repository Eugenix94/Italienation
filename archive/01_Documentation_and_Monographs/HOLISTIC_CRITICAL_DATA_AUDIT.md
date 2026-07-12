# ITALIENATION HOLISTIC CRITICAL DATA AUDIT & EMPIRICAL EVALUATION

## Executive Synthesis & Empirical Diagnosis

This document provides a rigorous empirical evaluation across all datasets in the repository, analyzing their temporal granularity, spatial dimensions, statistical integrity, and core research findings.

## 1. Canonical Data Panels (`holistic_analysis/data_panels/`)

### Dataset: `01_macro_fiscal_expenditure_1913_2026.csv`
- **Dimensions**: 50 rows × 14 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `year, public_pct_gdp_owid, public_pct_govexp_owid, state_pct_gdp, parents_private_pct_gdp, total_pct_gdp, state_share_of_total_pct, parents_private_share_of_total_pct, state_usd_ppp, parents_private_usd_ppp, total_usd_ppp, siope_school_expenditure_eur...`
- **Key Numeric Indicators**: `year` (Mean: 1997.24), `public_pct_gdp_owid` (Mean: 4.08), `public_pct_govexp_owid` (Mean: 8.45), `state_pct_gdp` (Mean: 3.34), `parents_private_pct_gdp` (Mean: 0.48)

### Dataset: `01b_global_italy_oecd_wb_benchmark.csv`
- **Dimensions**: 252 rows × 54 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `iso3, education_spending_pct_gdp_year, education_spending_pct_gdp, tertiary_enrollment_gross_pct_year, tertiary_enrollment_gross_pct, learning_poverty_pct_year, learning_poverty_pct, access_minus_learning_gap_year, access_minus_learning_gap, cost_intensity_x_access_year, cost_intensity_x_access, country...`
- **Key Numeric Indicators**: `education_spending_pct_gdp_year` (Mean: 2021.72), `education_spending_pct_gdp` (Mean: 4.23), `tertiary_enrollment_gross_pct_year` (Mean: 2020.56), `tertiary_enrollment_gross_pct` (Mean: 43.61), `learning_poverty_pct_year` (Mean: 2018.17)

### Dataset: `02_eurostat_social_scoreboard_eu27.csv`
- **Dimensions**: 20 rows × 8 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `iso3, year, indicator_code, value_standardized, unit_standardized, source_org, source_dataset, last_verified_utc`
- **Key Numeric Indicators**: `year` (Mean: 2024.0), `value_standardized` (Mean: 14.59)

### Dataset: `03_covid19_age_selective_scarring.csv`
- **Dimensions**: 54 rows × 7 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `covid_period, classe_eta, sex_label, mean_neet_obs_value, pre_covid_mean_neet_obs_value, delta_vs_pre_covid_pp, pct_change_vs_pre_covid`
- **Key Numeric Indicators**: `mean_neet_obs_value` (Mean: 326.27), `pre_covid_mean_neet_obs_value` (Mean: 331.23), `delta_vs_pre_covid_pp` (Mean: -4.96), `pct_change_vs_pre_covid` (Mean: -1.48)

### Dataset: `03b_neet_gender_disparity_2018_2024.csv`
- **Dimensions**: 297 rows × 4 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `year, classe_eta, sex_label, obs_value`
- **Key Numeric Indicators**: `year` (Mean: 2015.0), `obs_value` (Mean: 330.33)

### Dataset: `04_transition_jump_trap_bocciature_panel.csv`
- **Dimensions**: 198 rows × 19 columns
- **Temporal Coverage**: 2016 - 2024 (9 periods)
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `REF_AREA, REF_AREA_LABEL, TIME_PERIOD, lower_disability_per_1000_t_minus_1, lower_class_size_t_minus_1, lower_exam_success_t_minus_1, lower_foreign_share_t_minus_1, lower_median_grade_t_minus_1, lower_public_share_t_minus_1, lower_exam_failure_t_minus_1, upper_repeaters_all_t, upper_repeaters_fir_t...`
- **Key Numeric Indicators**: `lower_disability_per_1000_t_minus_1` (Mean: 40.86), `lower_class_size_t_minus_1` (Mean: 20.22), `lower_exam_success_t_minus_1` (Mean: 99.84), `lower_foreign_share_t_minus_1` (Mean: 9.8), `lower_median_grade_t_minus_1` (Mean: 7.68)

### Dataset: `05_tripartite_upper_secondary_tracking.csv`
- **Dimensions**: 18 rows × 10 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `REGIONE, LICEO, PROFESSIONALE, PROFESSIONALE IeFP, TECNICO, TOTAL, LICEO_share_pct, PROFESSIONALE_share_pct, PROFESSIONALE IeFP_share_pct, TECNICO_share_pct`
- **Key Numeric Indicators**: `LICEO` (Mean: 71302.67), `PROFESSIONALE` (Mean: 22178.78), `PROFESSIONALE IeFP` (Mean: 647.17), `TECNICO` (Mean: 42987.17), `TOTAL` (Mean: 137115.78)

### Dataset: `06_teacher_workforce_precariato_815k_posts.csv`
- **Dimensions**: 8 rows × 6 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `ORDINESCUOLA, TIPOPOSTO, total_titular, total_suppl, total_teachers, suppl_share_pct`
- **Key Numeric Indicators**: `total_titular` (Mean: 92447.62), `total_suppl` (Mean: 29597.75), `total_teachers` (Mean: 122045.38), `suppl_share_pct` (Mean: 34.43)

### Dataset: `07_university_mur_academic_staff_ford_gender.csv`
- **Dimensions**: 111313 rows × 12 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `ANNO, CODICE_ATENEO, NOME_ATENEO, REGIONE, AREA_GEO, COD_QUALIFICA, DESC_QUALIFICA, GRADE, AREA_SD, FoRD, GENERE, N_AcStaff`
- **Key Numeric Indicators**: `ANNO` (Mean: 2018.4), `N_AcStaff` (Mean: 17.09)

### Dataset: `08_openpolis_metropolitan_urban_penalty.csv`
- **Dimensions**: 10 rows × 7 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `comune, macro_area, neet_rate_15_29_pct, early_school_leavers_pct, nursery_coverage_pct, escs_context_index, poverty_risk_pct`
- **Key Numeric Indicators**: `neet_rate_15_29_pct` (Mean: 16.61), `early_school_leavers_pct` (Mean: 12.23), `nursery_coverage_pct` (Mean: 28.85), `escs_context_index` (Mean: -0.01), `poverty_risk_pct` (Mean: 24.35)

### Dataset: `09_invalsi_foundational_competency_gaps.csv`
- **Dimensions**: 20029 rows × 12 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `school_type, academic_year, codice_istituto, rows, avg_score, min_score, low_score_rows, weak_score_rows, proxy_rows, keyword_hits, proxy_rate, school_proxy_flag`
- **Key Numeric Indicators**: `rows` (Mean: 3.99), `avg_score` (Mean: 4.79), `min_score` (Mean: 3.88), `low_score_rows` (Mean: 0.14), `weak_score_rows` (Mean: 0.51)

### Dataset: `10_household_financial_burden_textbook_tax.csv`
- **Dimensions**: 12 rows × 7 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `level, indicator, school_year, min_eur, max_eur, note, source_file`
- **Key Numeric Indicators**: `min_eur` (Mean: 1031.48), `max_eur` (Mean: 1185.64)

### Dataset: `10b_public_university_tuition_benchmark.csv`
- **Dimensions**: 2 rows × 6 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `academic_year, aggregation_code, aggregation_name, avg_tuition_payers_eur, avg_tuition_all_students_eur, source`
- **Key Numeric Indicators**: `avg_tuition_payers_eur` (Mean: 1826.46), `avg_tuition_all_students_eur` (Mean: 1218.88)

### Dataset: `11_istat_demographic_winter_projections_2024_2070.csv`
- **Dimensions**: 20 rows × 7 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `region, macro_area, pop_6_18_2024, pop_6_18_2040, pop_6_18_2070, projected_change_2040_pct, projected_change_2070_pct`
- **Key Numeric Indicators**: `pop_6_18_2024` (Mean: 374330.0), `pop_6_18_2040` (Mean: 311280.0), `pop_6_18_2070` (Mean: 242520.0), `projected_change_2040_pct` (Mean: -18.06), `projected_change_2070_pct` (Mean: -37.39)

### Dataset: `12_eurostat_nuts2_regional_neet_panel.csv`
- **Dimensions**: 14 rows × 6 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `region, country, nuts2_code, neet_rate_15_29_pct, early_school_leaving_pct, youth_unemployment_pct`
- **Key Numeric Indicators**: `neet_rate_15_29_pct` (Mean: 16.61), `early_school_leaving_pct` (Mean: 11.54), `youth_unemployment_pct` (Mean: 21.33)

### Dataset: `13_invalsi_implicit_dropout_regional.csv`
- **Dimensions**: 20 rows × 5 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `region, explicit_dropout_esl_pct, implicit_dropout_grade13_pct, total_dispersion_index_pct, invalsi_math_score_dev`
- **Key Numeric Indicators**: `explicit_dropout_esl_pct` (Mean: 10.83), `implicit_dropout_grade13_pct` (Mean: 9.58), `total_dispersion_index_pct` (Mean: 20.41), `invalsi_math_score_dev` (Mean: -1.44)

### Dataset: `14_almalaurea_brain_drain_wages_by_discipline.csv`
- **Dimensions**: 10 rows × 6 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `degree_discipline, ford_area, emp_rate_5yr_pct, net_monthly_wage_eur, working_abroad_brain_drain_pct, precarious_contract_pct`
- **Key Numeric Indicators**: `emp_rate_5yr_pct` (Mean: 86.15), `net_monthly_wage_eur` (Mean: 1646.0), `working_abroad_brain_drain_pct` (Mean: 12.29), `precarious_contract_pct` (Mean: 23.44)

### Dataset: `15_tripartite_neet_area_orientation_matrix.csv`
- **Dimensions**: 20 rows × 10 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `region, macro_area, licei_share_pct, tecnici_share_pct, professionali_share_pct, neet_rate_15_29_pct, bocciature_grade9_pct, implicit_dropout_pct, industrial_absorption_index, orientation_profile`
- **Key Numeric Indicators**: `licei_share_pct` (Mean: 53.74), `tecnici_share_pct` (Mean: 31.93), `professionali_share_pct` (Mean: 14.32), `neet_rate_15_29_pct` (Mean: 16.18), `bocciature_grade9_pct` (Mean: 9.21)

### Dataset: `16_intergenerational_social_mobility_escs_tracking.csv`
- **Dimensions**: 6 rows × 9 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `parental_occupational_class_goldthorpe, mean_escs_index, prob_liceo_classico_scientifico_pct, prob_istituto_tecnico_pct, prob_istituto_professionale_pct, tertiary_attainment_prob_pct, intergenerational_income_elasticity_beta, generations_to_mean_income_oecd, sociological_tracking_mechanism`
- **Key Numeric Indicators**: `mean_escs_index` (Mean: 0.03), `prob_liceo_classico_scientifico_pct` (Mean: 45.25), `prob_istituto_tecnico_pct` (Mean: 36.43), `prob_istituto_professionale_pct` (Mean: 18.32), `tertiary_attainment_prob_pct` (Mean: 43.62)

### Dataset: `17_special_needs_sostegno_inclusion_precariato.csv`
- **Dimensions**: 20 rows × 9 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `region, macro_area, students_with_disability_l104, total_sostegno_teaching_posts, precarious_substitute_sostegno_posts, precariato_sostegno_share_pct, non_specialized_sostegno_share_pct, student_to_sostegno_teacher_ratio, pedagogical_continuity_status`
- **Key Numeric Indicators**: `students_with_disability_l104` (Mean: 20848.5), `total_sostegno_teaching_posts` (Mean: 11467.5), `precarious_substitute_sostegno_posts` (Mean: 7404.0), `precariato_sostegno_share_pct` (Mean: 62.76), `non_specialized_sostegno_share_pct` (Mean: 44.88)

### Dataset: `18_school_infrastructure_seismic_safety_energetic_panel.csv`
- **Dimensions**: 20 rows × 9 columns
- **Temporal Coverage**: Cross-sectional / Snapshot
- **Spatial Granularity**: National (Aggregate)
- **Data Integrity / Missingness**: 0.0% total missing values across matrix
- **Schema Columns**: `region, macro_area, total_active_school_buildings, built_before_1976_anti_seismic_law_pct, located_in_high_seismic_risk_zone_1_2_pct, buildings_with_gym_palestra_pct, buildings_with_canteen_mensa_pct, fire_safety_certification_cpi_pct, infrastructure_safety_diagnostic`
- **Key Numeric Indicators**: `total_active_school_buildings` (Mean: 2393.0), `built_before_1976_anti_seismic_law_pct` (Mean: 59.34), `located_in_high_seismic_risk_zone_1_2_pct` (Mean: 50.55), `buildings_with_gym_palestra_pct` (Mean: 68.36), `buildings_with_canteen_mensa_pct` (Mean: 47.7)

## 2. Local Processed Panels (`local_data/processed/`)

### Dataset: `anpal_replacement_early_school_leavers.csv`
- **Dimensions**: 136213 rows × 13 columns | **Temporal**: 2005 - 2025 | **Spatial**: National / Mixed | **Missing**: 13.71%
- **Columns**: `DATAFLOW, LAST UPDATE, freq, sex, age, training, wstatus, unit...`

### Dataset: `anpal_replacement_neet_annual.csv`
- **Dimensions**: 35 rows × 2 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `anno, neet_rate_pct`

### Dataset: `anpal_replacement_neet_by_migration.csv`
- **Dimensions**: 98818 rows × 13 columns | **Temporal**: 2010 - 2024 | **Spatial**: National / Mixed | **Missing**: 13.9%
- **Columns**: `DATAFLOW, LAST UPDATE, freq, sex, age, training, wstatus, unit...`

### Dataset: `anpal_replacement_youth_unemployment.csv`
- **Dimensions**: 948 rows × 11 columns | **Temporal**: 2005 - 2025 | **Spatial**: National / Mixed | **Missing**: 17.69%
- **Columns**: `DATAFLOW, LAST UPDATE, freq, age, sex, unit, geo, TIME_PERIOD...`

### Dataset: `atenei_payment_support_panel_2023_2024.csv`
- **Dimensions**: 92 rows × 15 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `academic_year, ateneo_code, ateneo_name, TASSA_MEDIA_PAGANTI_LAUREA, TASSA_MEDIA_TOTALE_ISCRITTI_LAUREA, tassa_media_paganti_laur_eur, tassa_media_tot_iscr_laur_eur, beneficiaries_borse_ateneo_total...`

### Dataset: `dsu_ersu_support_panel_2024_2025.csv`
- **Dimensions**: 76 rows × 27 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `region, dsu_ente, academic_year, k, entity_is_ersu_like, applications_total, eligible_students_total, beneficiaries_borse_total...`

### Dataset: `education_expenditure_state_parents_gdp.csv`
- **Dimensions**: 39 rows × 15 columns | **Temporal**: 2015 - 2022 | **Spatial**: National / Mixed | **Missing**: 1.37%
- **Columns**: `REF_AREA, Country, TIME_PERIOD, state_pct_gdp, parents_private_pct_gdp, rest_world_pct_gdp, total_pct_gdp, state_usd_ppp...`

### Dataset: `education_expenditure_state_parents_gdp_latest.csv`
- **Dimensions**: 5 rows × 15 columns | **Temporal**: 2022 - 2022 | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `REF_AREA, Country, TIME_PERIOD, state_pct_gdp, parents_private_pct_gdp, rest_world_pct_gdp, total_pct_gdp, state_usd_ppp...`

### Dataset: `education_fiscal_inventory.csv`
- **Dimensions**: 39 rows × 9 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `source_group, source_file, direction, coverage, latest_year, metric, value, unit...`

### Dataset: `estimated_bes_students_by_region_order_2024_25_using_istat_rates.csv`
- **Dimensions**: 54 rows × 8 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 4.17%
- **Columns**: `school_year_code, school_year, region, order, students_total, source_school_year, bes_rate_per_100, estimated_bes_students`

### Dataset: `estimated_disabled_students_by_region_order_2024_25_using_national_rates.csv`
- **Dimensions**: 54 rows × 8 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `school_year_code, school_year, region, order, students_total, disability_rate_per_100_national, estimated_disabled_students, source_school_year`

### Dataset: `eurostat_social_scoreboard_panel.csv`
- **Dimensions**: 20 rows × 8 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `iso3, year, indicator_code, value_standardized, unit_standardized, source_org, source_dataset, last_verified_utc`

### Dataset: `global_he_cost_access_latest_year.csv`
- **Dimensions**: 252 rows × 10 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 48.37%
- **Columns**: `iso3, year, learning_poverty_pct, education_spending_pct_gdp, tertiary_spending_pct_gdp_percap, tertiary_enrollment_gross_pct, country, access_minus_learning_gap...`

### Dataset: `global_he_cost_access_panel.csv`
- **Dimensions**: 58476 rows × 9 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 70.95%
- **Columns**: `iso3, year, learning_poverty_pct, education_spending_pct_gdp, tertiary_spending_pct_gdp_percap, tertiary_enrollment_gross_pct, country, access_minus_learning_gap...`

### Dataset: `global_italy_position_oecd_wb_latest.csv`
- **Dimensions**: 252 rows × 54 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 52.13%
- **Columns**: `iso3, education_spending_pct_gdp_year, education_spending_pct_gdp, tertiary_enrollment_gross_pct_year, tertiary_enrollment_gross_pct, learning_poverty_pct_year, learning_poverty_pct, access_minus_learning_gap_year...`

### Dataset: `hf_evaluation_scores_by_area.csv`
- **Dimensions**: 20 rows × 5 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `AREAGEOGRAFICA, CODICECRITERIO, count, mean, std`

### Dataset: `hf_teachers_by_school_order_panel.csv`
- **Dimensions**: 8 rows × 6 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `ORDINESCUOLA, TIPOPOSTO, total_titular, total_suppl, total_teachers, suppl_share_pct`

### Dataset: `hf_upper_sec_track_enrollment_panel.csv`
- **Dimensions**: 18 rows × 10 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `REGIONE, LICEO, PROFESSIONALE, PROFESSIONALE IeFP, TECNICO, TOTAL, LICEO_share_pct, PROFESSIONALE_share_pct...`

### Dataset: `inps_apprenticeship_informal_hits_2026-05-24.csv`
- **Dimensions**: 9 rows × 5 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `package_id, title, metadata_modified, resource_count, resource_urls`

### Dataset: `inps_destination_dataset_inventory_2026-05-24.csv`
- **Dimensions**: 9 rows × 9 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 14.81%
- **Columns**: `package_id, title, local_file, status, rows, cols, year_min, year_max...`

### Dataset: `inps_destination_shortlist_2026-05-24.csv`
- **Dimensions**: 216 rows × 6 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `package_id, title, tags, metadata_modified, resource_count, resource_urls`

### Dataset: `inps_odapi_candidate_packages_2026-05-24.csv`
- **Dimensions**: 272 rows × 5 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `package_id, title, metadata_modified, resource_count, resource_urls`

### Dataset: `istat_bes_rate_by_region_order_2022_2023.csv`
- **Dimensions**: 26 rows × 7 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 2.75%
- **Columns**: `region, bes_rate_per_100_infanzia, bes_rate_per_100_primaria, bes_rate_per_100_secondaria_i, bes_rate_per_100_secondaria_ii, bes_rate_per_100_all_orders, source_school_year`

### Dataset: `istat_disability_rate_timeseries_by_order.csv`
- **Dimensions**: 9 rows × 6 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `school_year, disability_rate_per_100_infanzia, disability_rate_per_100_primaria, disability_rate_per_100_secondaria_i, disability_rate_per_100_secondaria_ii, disability_rate_per_100_all_orders`

### Dataset: `istat_lower_secondary_exam_proxy_latest.csv`
- **Dimensions**: 131 rows × 14 columns | **Temporal**: 2024 - 2024 | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `REF_AREA, REF_AREA_LABEL, DATA_TYPE, DATA_TYPE_LABEL, TYPE_SCHOOL_MANAGEMENT, TYPE_SCHOOL_MANAGEMENT_LABEL, OBS_VALUE, failure_at_exam_proxy...`

### Dataset: `istat_lower_secondary_indicators_latest.csv`
- **Dimensions**: 2755 rows × 13 columns | **Temporal**: 2024 - 2024 | **Spatial**: National / Mixed | **Missing**: 6.65%
- **Columns**: `REF_AREA, REF_AREA_LABEL, DATA_TYPE, DATA_TYPE_LABEL, TYPE_SCHOOL_MANAGEMENT, TYPE_SCHOOL_MANAGEMENT_LABEL, OBS_VALUE, failure_at_exam_proxy...`

### Dataset: `istat_lower_secondary_sources_manifest.csv`
- **Dimensions**: 1 rows × 14 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `source, flow_id, flow_title_it, endpoint, min_time_period, max_time_period, max_school_year_proxy, has_direct_repeaters_flow...`

### Dataset: `istat_parental_keyword_flows.csv`
- **Dimensions**: 351 rows × 2 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `flow_id, name_it`

### Dataset: `istat_repeaters_upper_secondary_latest.csv`
- **Dimensions**: 528 rows × 10 columns | **Temporal**: 2024 - 2024 | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `REF_AREA, REF_AREA_LABEL, TYPE_SCHOOL, TYPE_SCHOOL_LABEL, repeaters, TIME_PERIOD, SCHOOL_YEAR_PROXY, SOURCE...`

### Dataset: `istat_repeaters_upper_secondary_ranking.csv`
- **Dimensions**: 131 rows × 11 columns | **Temporal**: 2024 - 2024 | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `REF_AREA, REF_AREA_LABEL, TYPE_SCHOOL, TYPE_SCHOOL_LABEL, repeaters, TIME_PERIOD, SCHOOL_YEAR_PROXY, SOURCE...`

### Dataset: `istat_school_outcomes_sources_manifest.csv`
- **Dimensions**: 1 rows × 14 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `source, flow_id, flow_title_it, endpoint, min_time_period, max_time_period, max_school_year_proxy, has_time_period_2025...`

### Dataset: `italy_education_expenditure_history_panel.csv`
- **Dimensions**: 50 rows × 14 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 70.43%
- **Columns**: `year, public_pct_gdp_owid, public_pct_govexp_owid, state_pct_gdp, parents_private_pct_gdp, total_pct_gdp, state_share_of_total_pct, parents_private_share_of_total_pct...`

### Dataset: `italy_education_expenditure_state_parents_trend.csv`
- **Dimensions**: 8 rows × 15 columns | **Temporal**: 2015 - 2022 | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `REF_AREA, Country, TIME_PERIOD, state_pct_gdp, parents_private_pct_gdp, rest_world_pct_gdp, total_pct_gdp, state_usd_ppp...`

### Dataset: `italy_education_finance_levels_real.csv`
- **Dimensions**: 39 rows × 19 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 28.61%
- **Columns**: `year, sector, sector_label, isced11, level_label, nominal_million_eur, nominal_eur, series_group...`

### Dataset: `italy_education_territorial_proxy_panel.csv`
- **Dimensions**: 18 rows × 27 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `region_name, school_students_total, students_primary, students_lower_secondary, students_upper_secondary, estimated_disabled_students_total, estimated_bes_students_total, neet_region_code...`

### Dataset: `italy_household_burden_module.csv`
- **Dimensions**: 19 rows × 10 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 13.68%
- **Columns**: `domain, reference_period, segment, indicator, value, unit, min_eur, max_eur...`

### Dataset: `italy_mur_tuition_benchmark_2024.csv`
- **Dimensions**: 2 rows × 6 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `academic_year, aggregation_code, aggregation_name, avg_tuition_payers_eur, avg_tuition_all_students_eur, source`

### Dataset: `italy_position_summary_oecd_wb.csv`
- **Dimensions**: 10 rows × 6 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `metric, better_direction, italy_value, italy_rank, countries_with_metric, italy_pct_better`

### Dataset: `italy_school_household_cost_snapshot.csv`
- **Dimensions**: 12 rows × 7 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `level, indicator, school_year, min_eur, max_eur, note, source_file`

### Dataset: `ministry_students_by_region_order_2024_25.csv`
- **Dimensions**: 54 rows × 5 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `school_year_code, school_year, region, order, students_total`

### Dataset: `neet_covid_period_summary.csv`
- **Dimensions**: 54 rows × 7 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `covid_period, classe_eta, sex_label, mean_neet_obs_value, pre_covid_mean_neet_obs_value, delta_vs_pre_covid_pp, pct_change_vs_pre_covid`

### Dataset: `neet_gender_gap_by_year.csv`
- **Dimensions**: 99 rows × 7 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `year, classe_eta, female, male, total, female_minus_male_pp, female_to_male_ratio`

### Dataset: `neet_gender_total_yearly.csv`
- **Dimensions**: 11 rows × 2 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `year, neet_total_obs_value`

### Dataset: `neet_gender_year_panel.csv`
- **Dimensions**: 297 rows × 4 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `year, classe_eta, sex_label, obs_value`

### Dataset: `neet_regional_model_panel.csv`
- **Dimensions**: 198 rows × 23 columns | **Temporal**: 2016 - 2024 | **Spatial**: National / Mixed | **Missing**: 23.47%
- **Columns**: `REF_AREA, REF_AREA_LABEL, TIME_PERIOD, lower_disability_per_1000_t_minus_1, lower_class_size_t_minus_1, lower_exam_success_t_minus_1, lower_foreign_share_t_minus_1, lower_median_grade_t_minus_1...`

### Dataset: `neet_regional_risk_model_coefficients.csv`
- **Dimensions**: 17 rows × 3 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `feature, coefficient, absolute_coefficient`

### Dataset: `neet_regional_risk_model_predictions.csv`
- **Dimensions**: 22 rows × 7 columns | **Temporal**: 2024 - 2024 | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `REF_AREA, REF_AREA_LABEL, TIME_PERIOD, neet_count_15_29, neet_risk_index, predicted_neet_risk_index, prediction_error`

### Dataset: `neet_regional_target_panel.csv`
- **Dimensions**: 48 rows × 7 columns | **Temporal**: 2023 - 2024 | **Spatial**: `Territorio` (24 units) | **Missing**: 0.0%
- **Columns**: `REF_AREA, Territorio, TIME_PERIOD, neet_count_15_29, neet_risk_index, neet_percentile, covid_period`

### Dataset: `oed_destination_risk_panel.csv`
- **Dimensions**: 9 rows × 3 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `year, metric, value`

### Dataset: `sample_education.csv`
- **Dimensions**: 300 rows × 6 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `year, region, school, students, expenditure_euro, graduation_rate`

### Dataset: `save_the_children_italy_school_stats.csv`
- **Dimensions**: 5 rows × 6 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `indicator, value, unit, reference_year, source_url, note`

### Dataset: `save_the_children_validation_panel.csv`
- **Dimensions**: 5 rows × 7 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 17.14%
- **Columns**: `indicator, pdf_value, local_validated_value, local_reference_year, validation_status, validation_note, gap_pdf_minus_local`

### Dataset: `siope_budget_category_breakdown.csv`
- **Dimensions**: 205 rows × 5 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.59%
- **Columns**: `Unnamed: 0, importo_euro, importo_euro.1, importo_euro.2, anno`

### Dataset: `siope_expenditure_by_region_year.csv`
- **Dimensions**: 2 rows × 215 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 3.72%
- **Columns**: `anno, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0...`

### Dataset: `siope_monthly_expenditure_trend.csv`
- **Dimensions**: 103 rows × 5 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.97%
- **Columns**: `Unnamed: 0, Unnamed: 1, importo_euro, importo_euro.1, codice_ente`

### Dataset: `siope_school_count_by_region_year.csv`
- **Dimensions**: 2 rows × 215 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 3.72%
- **Columns**: `anno, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0...`

### Dataset: `siope_school_expenditure_summary.csv`
- **Dimensions**: 7959 rows × 8 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 33.04%
- **Columns**: `codice_ente, anno, importo_euro, codice_regione, codice_provincia, codice_comune, denominazione, mese`

### Dataset: `siope_school_expenditure_summary.sample.csv`
- **Dimensions**: 20 rows × 8 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `codice_ente, anno, importo_euro, codice_regione, codice_provincia, codice_comune, denominazione, mese`

### Dataset: `snv_esiti_manifest.csv`
- **Dimensions**: 4 rows × 7 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 14.29%
- **Columns**: `school_type, source_page, download_url, local_path, status, rows, error`

### Dataset: `snv_esiti_school_year_proxy.csv`
- **Dimensions**: 20029 rows × 12 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `school_type, academic_year, codice_istituto, rows, avg_score, min_score, low_score_rows, weak_score_rows...`

### Dataset: `transition_bridge_latest_top_jump.csv`
- **Dimensions**: 15 rows × 19 columns | **Temporal**: 2024 - 2024 | **Spatial**: National / Mixed | **Missing**: 0.35%
- **Columns**: `REF_AREA, REF_AREA_LABEL, TIME_PERIOD, lower_disability_per_1000_t_minus_1, lower_class_size_t_minus_1, lower_exam_success_t_minus_1, lower_foreign_share_t_minus_1, lower_median_grade_t_minus_1...`

### Dataset: `transition_bridge_model_panel.csv`
- **Dimensions**: 198 rows × 19 columns | **Temporal**: 2016 - 2024 | **Spatial**: National / Mixed | **Missing**: 12.04%
- **Columns**: `REF_AREA, REF_AREA_LABEL, TIME_PERIOD, lower_disability_per_1000_t_minus_1, lower_class_size_t_minus_1, lower_exam_success_t_minus_1, lower_foreign_share_t_minus_1, lower_median_grade_t_minus_1...`

### Dataset: `worldbank_italy_cpi_index.csv`
- **Dimensions**: 65 rows × 2 columns | **Temporal**: Cross-sectional | **Spatial**: National / Mixed | **Missing**: 0.0%
- **Columns**: `year, cpi_index`
