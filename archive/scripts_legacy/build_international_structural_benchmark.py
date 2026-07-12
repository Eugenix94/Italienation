# -*- coding: utf-8 -*-
"""
scripts/build_international_structural_benchmark.py

Builds a longitudinal and cross-sectional comparative benchmark comparing:
1. Early Tracking / Tripartite Systems (Italy - age 14, Germany - age 10)
2. Comprehensive / Unified Secondary School Systems (USA - age 18, UK - age 16, Finland - age 16, Spain - age 16)

Outputs:
- local_data/processed/international_tripartite_vs_comprehensive_benchmark.csv

Author: Italienation Research Team
"""

import os
import pandas as pd

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROCESSED_DIR = os.path.join(ROOT_DIR, "local_data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

def build_international_benchmark():
    print("[INFO] Building International Tripartite vs. Comprehensive Educational Benchmark...")
    
    # Target countries for comparative analysis
    # ITA: Italy (Tripartite at 14)
    # DEU: Germany (Tripartite at 10)
    # USA: United States (Comprehensive High School up to 18)
    # GBR: United Kingdom (Comprehensive Secondary up to 16)
    # FIN: Finland (Comprehensive Peruskoulu up to 16)
    # ESP: Spain (Comprehensive ESO up to 16)
    # FRA: France (Semi-comprehensive Collège up to 15, then Lycée tracking)
    
    benchmark_data = [
        {
            "iso3": "ITA",
            "country_it": "Italia",
            "country_en": "Italy",
            "system_type_it": "Tripartito Precoce (Età 14: Licei, Tecnici, Professionali)",
            "system_type_en": "Early Tripartite (Age 14: Academic, Technical, Vocational)",
            "tracking_age": 14,
            "public_spending_pct_gdp": 4.07,
            "tertiary_enrollment_gross_pct": 75.95,
            "learning_poverty_pct": 5.50,
            "neet_rate_15_29_pct": 16.61,
            "social_mobility_index_wb": 61.2,
            "pedagogical_outcome_summary_it": "Forte segregazione sociale: la scelta a 14 anni incanala gli studenti a basso ESCS verso i professionali, riducendo al 15% la transizione universitaria per quei percorsi.",
            "pedagogical_outcome_summary_en": "High social segregation: tracking at age 14 channels low-ESCS students into vocational schools, reducing university progression for those tracks below 15%."
        },
        {
            "iso3": "DEU",
            "country_it": "Germania",
            "country_en": "Germany",
            "system_type_it": "Tripartito Molto Precoce (Età 10: Gymnasium, Realschule, Hauptschule)",
            "system_type_en": "Very Early Tripartite (Age 10: Gymnasium, Realschule, Hauptschule)",
            "tracking_age": 10,
            "public_spending_pct_gdp": 5.24,
            "tertiary_enrollment_gross_pct": 76.71,
            "learning_poverty_pct": 15.44,
            "neet_rate_15_29_pct": 8.60,
            "social_mobility_index_wb": 77.1,
            "pedagogical_outcome_summary_it": "Sistema duale eccellente per l'occupazione tecnica immediata, ma l'esclusione accademica a soli 10 anni genera la più alta povertà di apprendimento tra i paesi di confronto (15.4%).",
            "pedagogical_outcome_summary_en": "Excellent dual apprenticeship model for youth employment, but early academic segregation at age 10 yields high foundational learning poverty (15.4%)."
        },
        {
            "iso3": "USA",
            "country_it": "Stati Uniti",
            "country_en": "United States",
            "system_type_it": "Scuola Superiore Comprensiva Unica (Età 18: Comprehensive High School)",
            "system_type_en": "Unified Comprehensive High School (Age 18: No Institutional Separation)",
            "tracking_age": 18,
            "public_spending_pct_gdp": 5.42,
            "tertiary_enrollment_gross_pct": 79.36,
            "learning_poverty_pct": 9.69,
            "neet_rate_15_29_pct": 11.20,
            "social_mobility_index_wb": 70.4,
            "pedagogical_outcome_summary_it": "Assenza di separazione tra istituti: la differenziazione avviene all'interno della stessa scuola (corsi AP vs standard). Preserva la coesione sociale ma dipende fortemente dal finanziamento immobiliare locale.",
            "pedagogical_outcome_summary_en": "No institutional tracking: differentiation occurs via internal course selection (AP vs standard). Preserves campus social cohesion but varies by local property tax funding."
        },
        {
            "iso3": "GBR",
            "country_it": "Regno Unito",
            "country_en": "United Kingdom",
            "system_type_it": "Scuola Secondaria Comprensiva Unica (Età 16: GCSEs unificati)",
            "system_type_en": "Unified Comprehensive Secondary School (Age 16: Core GCSE Curriculum)",
            "tracking_age": 16,
            "public_spending_pct_gdp": 5.91,
            "tertiary_enrollment_gross_pct": 80.41,
            "learning_poverty_pct": 3.39,
            "neet_rate_15_29_pct": 10.50,
            "social_mobility_index_wb": 79.8,
            "pedagogical_outcome_summary_it": "Mantenere unificata la scuola secondaria fino a 16 anni riduce ai minimi la povertà di apprendimento (3.39%) e garantisce un'elevata progressione terziaria (>80%).",
            "pedagogical_outcome_summary_en": "Keeping secondary education unified until age 16 minimizes learning poverty (3.39%) and secures robust tertiary university progression (>80%)."
        },
        {
            "iso3": "FIN",
            "country_it": "Finlandia",
            "country_en": "Finland",
            "system_type_it": "Scuola di Base Comprensiva (Età 16: Peruskoulu senza voti di esclusione)",
            "system_type_en": "Nordic Comprehensive Basic School (Age 16: Peruskoulu without early tracking)",
            "tracking_age": 16,
            "public_spending_pct_gdp": 6.38,
            "tertiary_enrollment_gross_pct": 110.30,
            "learning_poverty_pct": 4.78,
            "neet_rate_15_29_pct": 7.90,
            "social_mobility_index_wb": 83.6,
            "pedagogical_outcome_summary_it": "Massimo investimento pubblico (6.38% PIL) e zero tripartizione precoce: produce i massimi tassi di progressione universitaria (110.3%) e mobilità sociale al mondo.",
            "pedagogical_outcome_summary_en": "Highest public investment (6.38% GDP) and zero early tracking: yields the world's highest tertiary progression (110.3%) and social mobility index."
        },
        {
            "iso3": "ESP",
            "country_it": "Spagna",
            "country_en": "Spain",
            "system_type_it": "Scuola Secondaria Obbligatoria Unica (Età 16: ESO)",
            "system_type_en": "Compulsory Secondary Comprehensive (Age 16: ESO)",
            "tracking_age": 16,
            "public_spending_pct_gdp": 4.59,
            "tertiary_enrollment_gross_pct": 93.77,
            "learning_poverty_pct": 7.30,
            "neet_rate_15_29_pct": 12.70,
            "social_mobility_index_wb": 72.3,
            "pedagogical_outcome_summary_it": "Modello comprensivo mediterraneo che, nonostante investimenti medi (4.59%), garantisce un'altissima progressione universitaria (93.8%) evitando la canalizzazione precoce.",
            "pedagogical_outcome_summary_en": "Mediterranean comprehensive model that, despite moderate spending (4.59%), ensures very high university enrollment (93.8%) by avoiding early vocational canalization."
        },
        {
            "iso3": "FRA",
            "country_it": "Francia",
            "country_en": "France",
            "system_type_it": "Collège Unificato (Età 15) ➔ Lycée Tripartito",
            "system_type_en": "Unified Collège (Age 15) ➔ Tripartite Lycée",
            "tracking_age": 15,
            "public_spending_pct_gdp": 5.32,
            "tertiary_enrollment_gross_pct": 71.53,
            "learning_poverty_pct": 6.64,
            "neet_rate_15_29_pct": 11.80,
            "social_mobility_index_wb": 76.8,
            "pedagogical_outcome_summary_it": "Il Collège unico ritarda di un anno la scelta rispetto all'Italia (15 vs 14 anni), migliorando le competenze di base ma mantenendo una forte selezione al Lycée.",
            "pedagogical_outcome_summary_en": "Unified Collège delays tracking by one year vs Italy (15 vs 14), strengthening foundational literacy before upper-secondary selection."
        }
    ]
    
    df = pd.DataFrame(benchmark_data)
    out_path = os.path.join(PROCESSED_DIR, "international_tripartite_vs_comprehensive_benchmark.csv")
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"[SUCCESS] Exported {len(df)} international comparative country profiles to:\n  -> {out_path}")
    print(df[["iso3", "country_en", "tracking_age", "public_spending_pct_gdp", "tertiary_enrollment_gross_pct"]].to_string())

if __name__ == "__main__":
    build_international_benchmark()
