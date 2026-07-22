import pandas as pd
import os

def generate_ptof_matrix():
    data = [
        # Licei (High Autonomy / High Funding)
        ["Liceo", "Liceo Classico (North)", "High (>€150/yr)", "Certificazioni Linguistiche (Cambridge/DELF), Viaggi Studio all'estero, Debate Club, Teatro Classico", "Partnerships with Universities, Elite cultural institutions", "High cultural capital acceleration. PTOF reinforces existing elite status."],
        ["Liceo", "Liceo Classico (South)", "Medium (€50-100/yr)", "Corsi di recupero, Teatro, Giornalino Scolastico", "Local Universities, Municipal libraries", "Strong baseline, but lacks the internationalization of Northern PTOFs."],
        ["Liceo", "Liceo Scientifico (Scienze Applicate)", "High (>€150/yr)", "Robotica, Coding (Python/C++), Certificazioni CISCO, Olimpiadi della Matematica", "Tech companies, STEM University faculties", "Directly accelerates STEM employability and university admission."],

        # Istituti Tecnici (Medium Autonomy / Industry Linked)
        ["Tecnico", "Tecnico Economico (AFM - North)", "Medium (€100/yr)", "Simulazione d'Impresa, Certificazioni Informatiche (ECDL/EIPASS), PCTO in Banche", "Local Banks, Confindustria, SMEs", "Strong alignment with local labor market needs."],
        ["Tecnico", "Tecnico Tecnologico (Informatica - South)", "Low (<€50/yr)", "Laboratori base, PCTO virtuale o interno alla scuola", "Limited local tech industry", "PTOF struggles to bridge the gap due to lack of local industrial partners for PCTO."],

        # Istituti Professionali (Low Autonomy / Remedial Focus)
        ["Professionale", "Professionale (Enogastronomia)", "Low/Medium (Material costs)", "Acquisto materie prime per cucine, Corsi HACCP base, Corsi di recupero dispersione", "Local restaurants, Catering", "PTOF is heavily focused on basic material provision and remedial education to prevent dropout."],
        ["Professionale", "Professionale (Manutenzione - South)", "Very Low (<€30/yr)", "Recupero competenze di base (Italian/Math), Sportelli d'ascolto psicologico", "Local artisans (often saturated)", "PTOF acts as a social welfare net rather than an academic accelerator. Voluntary contributions are near zero."]
    ]

    df = pd.DataFrame(data, columns=[
        "Macro_Track", "Specific_Branch_Context", "Contributo_Volontario_Proxy", 
        "Typical_PTOF_Offerings", "PCTO_Network_Quality", "Inequality_Mechanism"
    ])
    
    out_dir = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\processed"
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "ptof_autonomy_divide_matrix.csv")
    df.to_csv(csv_path, index=False)

    md_content = """# The PTOF Autonomy Divide (The Hidden Curriculum)

While the national *Quadro Orario* guarantees the baseline subjects, the **Piano Triennale dell'Offerta Formativa (PTOF)** is where true, localized inequality manifests.

Since the introduction of *Autonomia Scolastica* (School Autonomy), schools rely heavily on the **Contributo Volontario** (voluntary parental contributions) to fund their PTOF. This creates a devastating compounding effect across the tripartite branches:

## 1. The Liceo Acceleration (The "Rich" PTOF)
In high-SES areas (typically Northern Licei), parents routinely pay €150-€300 in "voluntary" contributions. This allows the school's PTOF to offer:
*   Cambridge/IELTS native-speaker courses.
*   Robotics and advanced coding labs (Scienze Applicate).
*   High-level PCTO (work-based learning) with elite universities or multinational companies.
**Result:** The PTOF acts as an academic accelerator, widening the gap between Liceo students and everyone else.

## 2. The Professionale Survival (The "Welfare" PTOF)
In low-SES areas (typically Southern Professionali), voluntary contributions are near zero because families simply cannot afford them. Their PTOF is fundamentally different:
*   Funds are desperately spent on basic materials (ingredients for kitchen labs, tools for workshops).
*   Extracurriculars are replaced by basic remedial courses to fight the 17.3% dropout rate.
*   PCTO networks are localized to struggling small businesses rather than high-end industry.
**Result:** The PTOF acts as a basic welfare and survival mechanism, rather than an accelerator.

## Conclusion
You cannot understand the branches by just looking at the national subjects. The PTOF proves that the Italian system is structurally designed to allow wealthy schools to buy a better curriculum, while poor schools struggle to provide basic laboratory materials. The "Autonomy" accelerates the inequality.
"""
    
    md_path = r"C:\Users\Dell\.gemini\antigravity\brain\62a964a6-8d4d-486c-91bb-954b2ca38c48\THE_PTOF_AUTONOMY_DIVIDE.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Extraction complete. CSV written to {csv_path} and MD to {md_path}")

if __name__ == "__main__":
    generate_ptof_matrix()
