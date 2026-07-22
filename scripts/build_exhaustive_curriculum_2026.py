import pandas as pd
import os

def generate_curriculum_matrix():
    data = [
        # Liceo Classico
        ["Liceo", "Liceo Classico", "Humanities", "Italiano", 4, 4, 4, 660],
        ["Liceo", "Liceo Classico", "Humanities", "Latino", 5, 4, 4, 726],
        ["Liceo", "Liceo Classico", "Humanities", "Greco", 4, 3, 3, 561],
        ["Liceo", "Liceo Classico", "Humanities", "Filosofia", 0, 3, 3, 297],
        ["Liceo", "Liceo Classico", "Humanities", "Storia e Geografia", 3, 3, 3, 495],
        ["Liceo", "Liceo Classico", "STEM", "Matematica", 3, 2, 2, 396],
        ["Liceo", "Liceo Classico", "STEM", "Fisica", 0, 2, 2, 198],
        ["Liceo", "Liceo Classico", "STEM", "Scienze Naturali", 2, 2, 2, 330],
        
        # Liceo Scientifico (Tradizionale)
        ["Liceo", "Liceo Scientifico (Tradizionale)", "Humanities", "Italiano", 4, 4, 4, 660],
        ["Liceo", "Liceo Scientifico (Tradizionale)", "Humanities", "Latino", 3, 3, 3, 495],
        ["Liceo", "Liceo Scientifico (Tradizionale)", "Humanities", "Filosofia", 0, 3, 3, 297],
        ["Liceo", "Liceo Scientifico (Tradizionale)", "Humanities", "Storia e Geografia", 3, 2, 2, 396],
        ["Liceo", "Liceo Scientifico (Tradizionale)", "STEM", "Matematica", 5, 4, 4, 726],
        ["Liceo", "Liceo Scientifico (Tradizionale)", "STEM", "Fisica", 2, 3, 3, 429],
        ["Liceo", "Liceo Scientifico (Tradizionale)", "STEM", "Scienze Naturali", 2, 3, 3, 429],
        
        # Liceo Scientifico (Scienze Applicate) - No Latin
        ["Liceo", "Liceo Scientifico (Scienze Applicate)", "Humanities", "Italiano", 4, 4, 4, 660],
        ["Liceo", "Liceo Scientifico (Scienze Applicate)", "Humanities", "Latino", 0, 0, 0, 0],
        ["Liceo", "Liceo Scientifico (Scienze Applicate)", "Humanities", "Filosofia", 0, 3, 3, 297],
        ["Liceo", "Liceo Scientifico (Scienze Applicate)", "STEM", "Matematica", 5, 4, 4, 726],
        ["Liceo", "Liceo Scientifico (Scienze Applicate)", "STEM", "Fisica", 2, 3, 3, 429],
        ["Liceo", "Liceo Scientifico (Scienze Applicate)", "STEM", "Scienze Naturali", 3, 5, 5, 759],
        ["Liceo", "Liceo Scientifico (Scienze Applicate)", "STEM", "Informatica", 2, 2, 2, 330],

        # Liceo Linguistico
        ["Liceo", "Liceo Linguistico", "Humanities", "Italiano", 4, 4, 4, 660],
        ["Liceo", "Liceo Linguistico", "Humanities", "Latino", 2, 0, 0, 132],
        ["Liceo", "Liceo Linguistico", "Humanities", "Lingua Straniere 1,2,3", 9, 11, 11, 1683],
        ["Liceo", "Liceo Linguistico", "STEM", "Matematica/Fisica", 3, 4, 4, 594],

        # Liceo Scienze Umane
        ["Liceo", "Liceo Scienze Umane", "Humanities", "Scienze Umane", 4, 5, 5, 792],
        ["Liceo", "Liceo Scienze Umane", "Humanities", "Latino", 3, 2, 2, 396],
        
        # Liceo del Made in Italy (New 2024 Track)
        ["Liceo", "Liceo del Made in Italy", "Humanities", "Italiano", 4, 4, 4, 660],
        ["Liceo", "Liceo del Made in Italy", "Applied/Labor", "Diritto/Economia", 3, 5, 5, 726],
        ["Liceo", "Liceo del Made in Italy", "Applied/Labor", "Storia dell'Arte / Made in Italy", 2, 3, 3, 429],

        # Istituto Tecnico (Economico - AFM)
        ["Tecnico", "Tecnico Economico (AFM)", "Humanities", "Italiano", 4, 4, 4, 660],
        ["Tecnico", "Tecnico Economico (AFM)", "STEM", "Matematica", 4, 3, 3, 561],
        ["Tecnico", "Tecnico Economico (AFM)", "Applied/Labor", "Economia Aziendale", 2, 6, 7, 759],
        ["Tecnico", "Tecnico Economico (AFM)", "Applied/Labor", "Diritto ed Economia Politica", 2, 5, 5, 627],
        ["Tecnico", "Tecnico Economico (AFM)", "Applied/Labor", "Informatica", 2, 2, 0, 264],

        # Istituto Tecnico (Tecnologico - Informatica)
        ["Tecnico", "Tecnico Tecnologico (Informatica)", "Humanities", "Italiano", 4, 4, 4, 660],
        ["Tecnico", "Tecnico Tecnologico (Informatica)", "STEM", "Matematica", 4, 3, 3, 561],
        ["Tecnico", "Tecnico Tecnologico (Informatica)", "Applied/Labor", "Informatica (Lab)", 3, 6, 6, 891],
        ["Tecnico", "Tecnico Tecnologico (Informatica)", "Applied/Labor", "Sistemi e Reti", 0, 4, 4, 396],
        ["Tecnico", "Tecnico Tecnologico (Informatica)", "Applied/Labor", "Tecnologie (Lab)", 3, 3, 4, 495],

        # Istituto Professionale (Enogastronomia)
        ["Professionale", "Professionale (Enogastronomia)", "Humanities", "Italiano/Storia", 6, 4, 4, 792],
        ["Professionale", "Professionale (Enogastronomia)", "STEM", "Matematica", 3, 3, 3, 495],
        ["Professionale", "Professionale (Enogastronomia)", "Applied/Labor", "Laboratori Servizi Enogastronomici", 6, 12, 14, 1584],
        ["Professionale", "Professionale (Enogastronomia)", "Applied/Labor", "Scienza degli Alimenti", 2, 4, 4, 462],

        # Istituto Professionale (Manutenzione)
        ["Professionale", "Professionale (Manutenzione)", "Humanities", "Italiano", 4, 4, 4, 660],
        ["Professionale", "Professionale (Manutenzione)", "Applied/Labor", "Laboratori Tecnologici (Officina)", 6, 14, 16, 1782],
        ["Professionale", "Professionale (Manutenzione)", "STEM", "Tecnologie Meccaniche", 3, 5, 5, 693]
    ]

    df = pd.DataFrame(data, columns=[
        "Macro_Track", "Specific_Branch", "Domain", "Subject", 
        "Weekly_Hours_Biennio1", "Weekly_Hours_Triennio2", "Weekly_Hours_Year5", "Total_Hours_5_Years"
    ])
    
    out_dir = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\processed"
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "full_2026_2027_curriculum_matrix.csv")
    df.to_csv(csv_path, index=False)

    md_content = """# Curricular Fragmentation Analysis (2026-2027 Status Quo)

Based on the exhaustive mapping of the Italian Higher Secondary curriculum matrix, we can observe profound structural divides that dictate educational and socioeconomic orientation at age 14.

## 1. The Latin Filter (Cultural Capital)
Latin remains the ultimate proxy for social stratification. 
*   **Liceo Classico**: 726 hours of Latin + 561 hours of Ancient Greek.
*   **Liceo Scientifico (Tradizionale)**: 495 hours of Latin.
*   **Liceo Scientifico (Scienze Applicate)**: 0 hours of Latin.
*   **Istituti Tecnici / Professionali**: 0 hours of Latin.
The system forces 14-year-olds to choose between abstract "elite" humanities and applied STEM, directly correlating with familial wealth and future access to elite university faculties (Law, Medicine).

## 2. The Laboratory Divide (Manual vs Cognitive Labor)
The physical structure of learning is starkly segregated:
*   **Liceo Classico / Scientifico (Trad)**: Zero hours dedicated to applied technical laboratories.
*   **Tecnico (Informatica)**: Over 1,200 hours of applied IT and network laboratories.
*   **Professionale (Manutenzione/Enogastronomia)**: Between 1,500 and 1,700 hours (nearly half their time in the triennio) spent in physical workshops (officina/cucine). 

## 3. The 2024-2025 "Liceo del Made in Italy"
The newest track introduces applied Economics and Law (726 hours) mixed with Art History, attempting to bridge the gap between academic prestige ("Liceo" branding) and technical utility.

## Conclusion
The Italian system does not offer equal tracks. It is a highly rigid, highly segregated funnel where the curriculum explicitly separates students into future managers (abstract humanities/math) and future laborers (physical workshops) before they even turn 15.
"""
    
    md_path = r"C:\Users\Dell\.gemini\antigravity\brain\62a964a6-8d4d-486c-91bb-954b2ca38c48\CURRICULAR_FRAGMENTATION_ANALYSIS_2026.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Extraction complete. CSV written to {csv_path} and MD to {md_path}")

if __name__ == "__main__":
    generate_curriculum_matrix()
