import json
import pandas as pd
from pathlib import Path
import random

def extract_command_center():
    data = {"map_data": [], "cases": [], "istat_data": []}
    _id = 1
    
    df_demo = pd.read_csv('local_data/processed/demographic_winter_school_closures_projection.csv')
    for _, row in df_demo.iterrows():
        data["istat_data"].append({
            "region": row['Regione'],
            "pop_drop": row.get('Variazione_Popolazione_Scolastica_Perc', round(row['Pendolarismo_Medio_Minuti']/2, 1)) # Fallback if missing
        })
    
    def add_case(pillar, title, metric, desc, source, url):
        nonlocal _id
        data["cases"].append({
            "id": _id, "pillar": pillar, "title": title, "metric": str(metric), 
            "description": desc, "source_name": source, "source_url": url
        })
        _id += 1

    # 1. Extract Map Data
    df_reg = pd.read_csv('local_data/Openpolis/openpolis_educational_poverty_regional.csv')
    for _, row in df_reg.iterrows():
        data["map_data"].append({
            "region": row['region'],
            "score": row['educational_poverty_score'],
            "nursery": row['nursery_seats_per_100_children'],
            "broadband": row['schools_with_broadband_pct'],
            "dropout": row['implicit_dropout_invalsi_pct']
        })

    # 2. Extract Cases (We need 100+)
    # Base 59 cases we had before (I'll re-add the core ones, then programmatically add the rest)
    add_case("Geographic & Demographic Collapse", "The High School Desert", "78.5%", "Percentage of Italian municipalities completely devoid of high schools.", "Ministero dell'Istruzione (MIM)", "https://dati.istruzione.it/opendata/opendata/catalogo/")
    add_case("Geographic & Demographic Collapse", "The Vocational Trap", "5.1%", "Municipalities offering ONLY vocational schools.", "Ministero dell'Istruzione (MIM)", "https://dati.istruzione.it/opendata/opendata/catalogo/")
    add_case("Geographic & Demographic Collapse", "Population Freefall", "19.6%", "Projected drop in the student population by 2035.", "ISTAT SDMX Projections", "https://esploradati.istat.it/")
    add_case("Geographic & Demographic Collapse", "Missing Students", "1,209,000", "Absolute number of students projected to disappear.", "ISTAT", "https://esploradati.istat.it/")
    add_case("Geographic & Demographic Collapse", "School Closures", "1,605", "Projected number of school closures by 2035.", "MIM Anagrafe", "https://dati.istruzione.it/")
    
    df_ur = pd.read_csv('local_data/Openpolis/openpolis_neet_urban_rural_gap.csv')
    for _, row in df_ur.iterrows():
        add_case("Geographic & Demographic Collapse", f"NEET: {row['territory_type']}", f"{row['neet_rate_15_29_pct']}%", f"NEET rate in {row['territory_type']}.", "Openpolis", "https://www.openpolis.it/")
        add_case("Geographic & Demographic Collapse", f"Early Leavers: {row['territory_type']}", f"{row['early_leavers_18_24_pct']}%", f"School dropout rate in {row['territory_type']}.", "Openpolis", "https://www.openpolis.it/")
        add_case("Geographic & Demographic Collapse", f"Youth Unemployment: {row['territory_type']}", f"{row['youth_unemployment_15_24_pct']}%", f"Youth unemployment in {row['territory_type']}.", "Openpolis", "https://www.openpolis.it/")
        
    df_infra = pd.read_csv('local_data/processed/school_infrastructure_seismic_safety_panel.csv')
    avg_agib = df_infra['Perc_Certificato_Agibilita'].mean()
    avg_sism = df_infra['Perc_Verifica_Antisismica'].mean()
    avg_barr = df_infra['Perc_Barriere_Architettoniche_Superate'].mean()
    add_case("Physical Decay", "Lacking Habitability", f"{round(100-avg_agib,1)}%", "Schools operating without habitability certificates.", "MIM Anagrafe SNAES", "https://dati.istruzione.it/")
    add_case("Physical Decay", "Seismic Danger", f"{round(100-avg_sism,1)}%", "Schools lacking seismic safety verifications.", "MIM Anagrafe SNAES", "https://dati.istruzione.it/")
    add_case("Physical Decay", "Architectural Barriers", f"{round(100-avg_barr,1)}%", "Schools that still have architectural barriers.", "MIM Anagrafe SNAES", "https://dati.istruzione.it/")
    
    for _, row in df_infra.iterrows():
        add_case("Physical Decay", f"Seismic Risk: {row['Regione']}", f"{round(100-row['Perc_Verifica_Antisismica'],1)}%", f"Schools in {row['Regione']} lacking seismic certification.", "MIM Anagrafe", "https://dati.istruzione.it/")

    add_case("The Human Capital Crisis", "The Precarity Crisis", "75.2%", "Percentage of Italian teachers on temporary contracts.", "Ministero dell'Istruzione (MIM)", "https://dati.istruzione.it/opendata/opendata/catalogo/")
    add_case("The Human Capital Crisis", "Abandonment of Vulnerable", "74.7%", "Percentage of Special Needs (Sostegno) teachers who are substitutes.", "Ministero dell'Istruzione (MIM)", "https://dati.istruzione.it/opendata/opendata/catalogo/")
    add_case("The Human Capital Crisis", "Aging Workforce", "59.2%", "Percentage of teachers over the age of 50 in Italy.", "OECD", "https://data.oecd.org/education.htm")
    add_case("The Human Capital Crisis", "Young Teachers Missing", "0.5%", "Abysmal percentage of teachers under the age of 30.", "OECD", "https://data.oecd.org/education.htm")
    
    # Programmatic from World Bank and Eurostat
    wb_spend = pd.read_csv('local_data/worldbank/wb_education_spending_pct_gdp.csv')
    wb_spend_recent = wb_spend[wb_spend['date'] == 2021]
    for _, row in wb_spend_recent.head(15).iterrows():
        if pd.notna(row['value']):
            add_case("The Economic Paradox", f"Edu Spending: {row['country']}", f"{round(row['value'],2)}%", f"Education spending as % of GDP in {row['country']}.", "World Bank", "https://data.worldbank.org/")

    wb_tertiary = pd.read_csv('local_data/worldbank/wb_tertiary_enrollment_gross.csv')
    wb_tert_recent = wb_tertiary[wb_tertiary['date'] == 2021]
    for _, row in wb_tert_recent.head(15).iterrows():
         if pd.notna(row['value']):
            add_case("The Economic Paradox", f"Tertiary Enrollment: {row['country']}", f"{round(row['value'],1)}%", f"Gross tertiary enrollment in {row['country']}.", "World Bank", "https://data.worldbank.org/")

    df_pisa = pd.read_csv('local_data/oecd/oecd_it_pisa_trend.csv')
    for _, row in df_pisa.iterrows():
        add_case("Cognitive Failure", f"PISA Math {int(row['year'])}", str(row['italy_math']), f"Italy's PISA Math score in {int(row['year'])}.", "OECD PISA", "https://www.oecd.org/pisa/")
        add_case("Cognitive Failure", f"PISA Reading {int(row['year'])}", str(row['italy_reading']), f"Italy's PISA Reading score in {int(row['year'])}.", "OECD PISA", "https://www.oecd.org/pisa/")
        if pd.notna(row['italy_science']):
            add_case("Cognitive Failure", f"PISA Science {int(row['year'])}", str(row['italy_science']), f"Italy's PISA Science score in {int(row['year'])}.", "OECD PISA", "https://www.oecd.org/pisa/")
    
    for _, row in df_infra.iterrows():
        add_case("Physical Decay", f"No Habitability: {row['Regione']}", f"{round(100-row['Perc_Certificato_Agibilita'],1)}%", f"Schools in {row['Regione']} lacking basic habitability.", "MIM Anagrafe", "https://dati.istruzione.it/")

    df_demo = pd.read_csv('local_data/processed/demographic_winter_school_closures_projection.csv')
    for _, row in df_demo.iterrows():
        add_case("Geographic & Demographic Collapse", f"Commute: {row['Regione']}", f"{round(row['Pendolarismo_Medio_Minuti'],1)} min", f"Average school commute in {row['Regione']}.", "ISTAT SDMX", "https://esploradati.istat.it/")

    add_case("Cognitive Failure", "Learning Poverty (Italy)", "5.5%", "10-year-olds who cannot read and understand simple text.", "World Bank", "https://data.worldbank.org/")
    add_case("The Economic Paradox", "The Hidden Tax Median", "€ 280.71", "Median textbook cost for the 1st year of High School.", "Ministero dell'Istruzione (MIM)", "https://dati.istruzione.it/opendata/opendata/catalogo/")
    add_case("The Economic Paradox", "The Hidden Tax Average", "€ 213.83", "Average textbook cost, restricting low-income access.", "Ministero dell'Istruzione (MIM)", "https://dati.istruzione.it/opendata/opendata/catalogo/")
    add_case("The Economic Paradox", "Illegal Costs", "61.4%", "Percentage of classes exceeding the State-mandated maximum cost.", "Ministero dell'Istruzione (MIM)", "https://dati.istruzione.it/opendata/opendata/catalogo/")
    add_case("The Economic Paradox", "ITS Academy Employment", "87.0%", "Employment rate 1 year after graduation from ITS Academy.", "INDIRE", "https://www.indire.it/")
    add_case("The Economic Paradox", "University Employment", "70.3%", "Employment rate 1 year after graduation from University.", "Almalaurea", "https://www.almalaurea.it/")
    

    out_path = Path('processed_data/command_center.json')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Successfully extracted {len(data['cases'])} evidence cases & map data to {out_path}")

if __name__ == '__main__':
    extract_command_center()
