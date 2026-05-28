# Global Policy-Response Benchmark Schema

Purpose
- Add policy-instrument variables that explain how countries reduce social immobility and weak GDP-linked transitions from school to work.
- Designed to merge with `global_he_cost_access_panel.csv` and country-year outcome tables.

Primary keys
- `iso3` (ISO-3166 alpha-3)
- `year` (integer)

Recommended merge keys
- Exact merge on (`iso3`, `year`).
- If source is sparse (survey waves): use `merge_year` plus `year_imputed_from` and cap carry-forward/backward to 2 years.

Variable groups

1) Transition systems
- `apprenticeship_participation_pct_youth`
- `dual_vet_share_upper_secondary_pct`
- `apprenticeship_completion_rate_pct`
- `graduate_employment_rate_1y_pct`
- `neet_15_29_pct`

2) Equity financing
- `public_education_spending_pct_gdp`
- `state_funding_share_pct_total_edu`
- `household_private_share_pct_total_edu`
- `tuition_fee_public_usd_ppp`
- `grant_aid_coverage_pct_students`
- `grant_aid_avg_usd_ppp`
- `loan_aid_coverage_pct_students`

3) Early failure prevention
- `grade_repetition_rate_lower_secondary_pct`
- `grade_repetition_rate_upper_secondary_pct`
- `remedial_instruction_coverage_pct`
- `class_size_lower_secondary`
- `special_needs_support_staff_per_1000_students`
- `teacher_shortage_index`

4) Active labor market transition
- `youth_almp_spending_pct_gdp`
- `youth_almp_spending_per_unemployed_usd_ppp`
- `youth_guarantee_coverage_pct`
- `median_months_school_to_first_job`
- `share_temporary_contracts_youth_pct`

5) Institutional permeability
- `track_switching_possible_binary`
- `recognition_prior_learning_binary`
- `second_chance_program_coverage_pct`
- `adult_learning_participation_pct`
- `tertiary_access_rate_from_vet_pct`

Target outcomes for evaluation
- `gdp_per_capita_ppp`
- `intergenerational_income_elasticity`
- `social_mobility_index`
- `learning_poverty_pct`
- `neet_15_29_pct`

Quality and provenance fields (mandatory)
- `source_org`
- `source_dataset`
- `source_series_code`
- `source_url`
- `source_file`
- `value_raw`
- `value_standardized`
- `unit_raw`
- `unit_standardized`
- `method_note`
- `confidence_tier` (A=official exact, B=official transformed, C=proxy)
- `missing_reason`
- `last_verified_utc`

Normalization rules
- Percentages on 0-100 scale.
- Money standardized to `USD_PPP` at annual level where possible.
- Binary variables in {0,1} only.
- Keep raw and standardized values side-by-side for auditability.

Initial country focus for policy-learning comparisons
- Italy, Germany, Austria, Denmark, Netherlands, Finland, France, Spain, Portugal, UK, Korea, Australia, Canada.

Minimum viable panel target
- 2015-2025
- >= 12 countries
- >= 15 core policy variables
- <= 20% missingness on core variables
