# OED Destination - Missing Data Matrix (2026-05-24)

This matrix focuses on the destination side of the OED triangle: contract quality, informal work, underpayment, and contribution/tax compliance.

## A) What is still missing (high priority)

1. Individual-level linkage between education and informality
- Needed: probability of informal/no-contract work by education level, region, age, gender.
- Why missing: current sources are mostly aggregate and not linkable at micro level.
- Candidate sources: ISTAT labor microdata (RCFL), INPS-Uniemens administrative microdata access channels.

2. Wage underpayment relative to legal/sector minimum standards
- Needed: gap between observed wages and contractual minima by sector and contract type.
- Why missing: current INPS open data does not provide full wage distribution with contract-standard benchmarks.
- Candidate sources: INL inspection outcomes, CNEL collective agreement datasets, MLPS/INL sanction statistics.

3. Non-payment / partial payment of social contributions by firm-worker profile
- Needed: contribution evasion rates by sector, firm size, territory, worker type.
- Why missing: available open indicators are old or aggregate.
- Candidate sources: INPS enforcement/arrears datasets, Guardia di Finanza annual reports, Corte dei Conti compliance audits.

4. School-to-first-job destination quality panel
- Needed: transition time, first contract type, persistence to formal employment after 6/12/24 months.
- Why missing: transition data and contract-register data are not yet integrated in one panel.
- Candidate sources: INPS + Comunicazioni Obbligatorie + ISTAT/AlmaLaurea linkage.

5. Youth NEET to informal-work transitions
- Needed: transition matrix among NEET, formal employment, informal employment, inactivity.
- Why missing: current NEET panels do not separately identify informal destination states.
- Candidate sources: ISTAT labor force microdata and ad hoc youth surveys.

## B) Medium-priority gaps

1. Apprenticeship quality outcomes
- Needed: completion, conversion to open-ended contract, wage progression, contribution continuity.
- Current status: apprenticeship count proxies available; quality trajectory mostly missing.

2. Territorial enforcement intensity
- Needed: inspections per 1,000 workers and sanctions per inspection by province.
- Current status: INPS irregular-work datasets exist but are old and not yet normalized into current pipeline.

3. Sectoral vulnerability index (informality risk)
- Needed: synthetic risk index combining temporary contracts, undeclared work findings, wage non-compliance.
- Current status: no integrated composite yet.

## C) Data now pinned and usable immediately

From INPS ODAPI scan:
- Apprenticeship proxy datasets (historical):
  - ID-5515, ID-5516, ID-5139 CSV resources.
- Irregular/undeclared labor datasets:
  - ID-2324, ID-2326 CSV resources.

Now downloaded in workspace (9/9 CSV resources from current shortlist):
- local_data/INPS/destination/ID-2324.csv
- local_data/INPS/destination/ID-2326.csv
- local_data/INPS/destination/ID-2492.csv
- local_data/INPS/destination/ID-2520.csv
- local_data/INPS/destination/ID-2531.csv
- local_data/INPS/destination/ID-5139.csv
- local_data/INPS/destination/ID-5515.csv
- local_data/INPS/destination/ID-5516.csv
- local_data/INPS/destination/attivit_-ispettiva-di-vigilanza-per-ente-controllore_-aziende-ispezionate-e-lavoratori-non__1.csv

Artifacts:
- local_data/INPS/destination/manifest.json
- local_data/processed/inps_apprenticeship_informal_hits_2026-05-24.csv
- local_data/processed/inps_apprenticeship_informal_hits_2026-05-24.json
- local_data/processed/inps_destination_dataset_inventory_2026-05-24.csv
- local_data/processed/oed_destination_risk_panel.csv

## D) Suggested next implementation sequence

1. Completed: scripted fetch pipeline in scripts/fetch_inps_destination_data.py.
2. Completed: scripted panel/inventory build in scripts/build_oed_destination_panel.py.
3. Next: enrich the risk panel with fresh enforcement-compliance data (post-2017) from INL/MLPS/Guardia di Finanza where available.
4. Next: integrate destination metrics with NEET and education outcomes to estimate informality risk by education level and region.
