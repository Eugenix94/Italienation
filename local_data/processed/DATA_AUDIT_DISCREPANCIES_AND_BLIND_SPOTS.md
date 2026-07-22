# Holistic Data Audit: Discrepancies and Blind Spots

I have analyzed the 20 core processed datasets in our `local_data/processed/` directory. Looking at them holistically, rather than individually, reveals profound structural discrepancies in how the Italian state operates, as well as distinct methodological blind spots in our data.

## 1. Structural Discrepancies (The Data Contradictions)

When we cross-reference the datasets against each other, the state's policies explicitly contradict the reality of the crisis:

### A. The CapEx vs OpEx Disconnect (PNRR vs INVALSI)
- **The Reality (`invalsi_overall_performance.csv`)**: Campania has a 19.8% Implicit Dropout rate and disastrous math scores. This is a pedagogical and socioeconomic failure (lack of full-time schooling, cultural poverty).
- **The State Response (`macro_pnrr_allocation_vs_spending.csv`)**: The PNRR Mission 4 is almost entirely **CapEx** (Capital Expenditure—building infrastructure). It allocates €3.9B to *Edilizia* (buildings). 
- **The Discrepancy**: You cannot fix a pedagogical crisis (OpEx: teacher salaries, full-time hours, tutors) by building a slightly newer school building (CapEx). The PNRR is treating a software problem with hardware.

### B. The Execution Gap (Universities vs Nurseries)
- **The Data (`macro_pnrr_allocation_vs_spending.csv`)**: The state has successfully spent 64.9% of the €11.44 Billion allocated to *Universities and Research* (which disproportionately serve high-SES Liceo graduates). 
- **The Discrepancy**: Conversely, for *Asili Nido* (Nurseries—the absolute foundation of early intervention for low-SES families), the state has only managed to spend 27.1% of its funds. The system is structurally optimized to funnel money to the top of the OED pathway, while failing to execute at the origin.

---

## 2. Methodological Blind Spots (What we are missing)

While we have the most comprehensive macro-dataset possible, there are statistical blind spots because the Italian State does not collect (or publish) true longitudinal micro-data.

### A. The "Rimandati" Black Box
- **The Data (`istat_bocciati_rimandati_rates.csv`)**: 13.6% of Liceo Scientifico students are suspended in June (*Rimandati*), but only 1.2% ultimately fail in September (*Bocciati*). 
- **The Blind Spot**: We know macro-economically that this gap is bridged by parents buying private tutoring (`shiw_private_tutoring_shadow_economy.csv`). However, we **lack the micro-data** to track individual students from June to September. We cannot mathematically prove *which specific* student passed because they spent €2000, we can only prove the systemic correlation.

### B. Exact ISEE to Track Mapping
- **The Data**: We know the median household income of the South is €24,800 (`istat_household_income_by_region.csv`). We know Southern students are heavily pushed into Vocational tracks.
- **The Blind Spot**: We lack the exact **ISEE (Indicatore della Situazione Economica Equivalente)** of individual students at the moment they choose their high school at age 14. We are forced to use regional averages and national quintiles as proxies because the Ministry (MIM) does not publish open micro-data linking track choice to individual family tax brackets.

---

## Conclusion
The data is not just comprehensive; the *discrepancies between the datasets* tell the real story. The government is spending billions on university infrastructure while failing to build nurseries, and building new high schools while ignoring the fact that students are failing because they can't afford private tutors. 

The blind spots exist because the state actively avoids publishing the granular micro-data (ISEE vs Track) that would explicitly prove this inequality at an individual level.
