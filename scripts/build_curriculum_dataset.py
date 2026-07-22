import pandas as pd
import os

def build_curriculum_data():
    print("Building Tripartite Curriculum Framework Dataset...")
    
    # Data is based on standard D.P.R. 89/2010 (Licei), 88/2010 (Tecnici), 87/2010 (Professionali)
    # The hours are approximate averages across the years to highlight the structural bifurcation.
    
    data = [
        # Liceo Classico
        ("Liceo Classico", "Humanities", "Italiano", 4, 4, 4),
        ("Liceo Classico", "Humanities", "Latino", 5, 4, 4),
        ("Liceo Classico", "Humanities", "Greco", 4, 3, 3),
        ("Liceo Classico", "Humanities", "Filosofia", 0, 3, 3),
        ("Liceo Classico", "Humanities", "Storia e Geografia", 3, 3, 3),
        ("Liceo Classico", "STEM", "Matematica", 3, 2, 2),
        ("Liceo Classico", "STEM", "Fisica", 0, 2, 2),
        ("Liceo Classico", "STEM", "Scienze Naturali", 2, 2, 2),
        ("Liceo Classico", "Applied/Labor", "Laboratori Tecnici", 0, 0, 0),
        ("Liceo Classico", "Applied/Labor", "Economia/Diritto", 0, 0, 0),
        
        # Liceo Scientifico
        ("Liceo Scientifico", "Humanities", "Italiano", 4, 4, 4),
        ("Liceo Scientifico", "Humanities", "Latino", 3, 3, 3),
        ("Liceo Scientifico", "Humanities", "Filosofia", 0, 3, 3),
        ("Liceo Scientifico", "Humanities", "Storia e Geografia", 3, 2, 2),
        ("Liceo Scientifico", "STEM", "Matematica", 5, 4, 4),
        ("Liceo Scientifico", "STEM", "Fisica", 2, 3, 3),
        ("Liceo Scientifico", "STEM", "Scienze Naturali", 2, 3, 3),
        ("Liceo Scientifico", "Applied/Labor", "Laboratori Tecnici", 0, 0, 0),
        ("Liceo Scientifico", "Applied/Labor", "Economia/Diritto", 0, 0, 0),
        
        # Istituto Tecnico (Economico/AFM)
        ("Istituto Tecnico (Econ)", "Humanities", "Italiano", 4, 4, 4),
        ("Istituto Tecnico (Econ)", "Humanities", "Storia", 2, 2, 2),
        ("Istituto Tecnico (Econ)", "Humanities", "Filosofia / Latino", 0, 0, 0),
        ("Istituto Tecnico (Econ)", "STEM", "Matematica", 4, 3, 3),
        ("Istituto Tecnico (Econ)", "Applied/Labor", "Economia Aziendale", 2, 6, 7),
        ("Istituto Tecnico (Econ)", "Applied/Labor", "Diritto ed Economia Politica", 2, 5, 5),
        ("Istituto Tecnico (Econ)", "Applied/Labor", "Informatica", 2, 2, 0),
        ("Istituto Tecnico (Econ)", "Applied/Labor", "Laboratori Tecnici", 0, 0, 0),
        
        # Istituto Professionale (Manutenzione/Assistenza Tecnica)
        ("Istituto Professionale", "Humanities", "Italiano", 4, 4, 4),
        ("Istituto Professionale", "Humanities", "Storia", 2, 2, 2),
        ("Istituto Professionale", "Humanities", "Filosofia / Latino", 0, 0, 0),
        ("Istituto Professionale", "STEM", "Matematica", 3, 3, 3),
        ("Istituto Professionale", "Applied/Labor", "Laboratori Tecnologici ed Esercitazioni", 6, 8, 10),
        ("Istituto Professionale", "Applied/Labor", "Tecnologie Meccaniche/Elettriche", 3, 5, 5),
        ("Istituto Professionale", "Applied/Labor", "Economia/Diritto", 2, 0, 0)
    ]
    
    df = pd.DataFrame(data, columns=[
        "Track", "Domain", "Subject", 
        "Weekly_Hours_Biennio1", "Weekly_Hours_Biennio2", "Weekly_Hours_Year5"
    ])
    
    # Calculate total instruction hours over 5 years
    # Biennio 1 = 2 years, Biennio 2 = 2 years, Year 5 = 1 year
    # Assuming ~33 weeks per year
    WEEKS_PER_YEAR = 33
    df["Total_Hours_5_Years"] = (
        (df["Weekly_Hours_Biennio1"] * 2 * WEEKS_PER_YEAR) +
        (df["Weekly_Hours_Biennio2"] * 2 * WEEKS_PER_YEAR) +
        (df["Weekly_Hours_Year5"] * 1 * WEEKS_PER_YEAR)
    )
    
    out_dir = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\processed"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "tripartite_curriculum_hours_panel.csv")
    
    df.to_csv(out_file, index=False)
    print(f"Curriculum Dataset saved to: {out_file}")

if __name__ == "__main__":
    build_curriculum_data()
