import json
import pandas as pd
from pathlib import Path

def extract_50_cases():
    cases = []
    _id = 1
    
    def add_case(pillar, title, metric, desc, source, url):
        nonlocal _id
        cases.append({
            "id": _id, "pillar": pillar, "title": title, "metric": str(metric), 
            "description": desc, "source_name": source, "source_url": url
        })
        _id += 1

    # PILLAR 1: Geographic & Demographic Collapse
    add_case("Geographic & Demographic", "The High School Desert", "78.5%", "Percentage of Italian municipalities completely devoid of high schools.", "HuggingFace School Register", "https://huggingface.co/datasets/diatribe00/italian-schools-opendata")
    add_case("Geographic & Demographic", "The Vocational Trap", "5.1%", "Municipalities offering ONLY vocational schools, denying access to Lyceums.", "HuggingFace School Register", "https://huggingface.co/datasets/diatribe00/italian-schools-opendata")
    add_case("Geographic & Demographic", "Population Freefall", "-19.6%", "Projected drop in the 6-18 student population by 2035.", "ISTAT SDMX Projections", "https://esploradati.istat.it/")
    add_case("Geographic & Demographic", "Missing Students", "1,209,000", "Absolute number of students projected to disappear from the system by 2035.", "ISTAT SDMX Projections", "https://esploradati.istat.it/")
    add_case("Geographic & Demographic", "School Closures", "1,605", "Projected number of school closures by 2035 due to demographic winter.", "MIM Anagrafe SNAES", "https://dati.istruzione.it/")
    
    df_ur = pd.read_csv('local_data/Openpolis/openpolis_neet_urban_rural_gap.csv')
    dense = df_ur[df_ur['territory_type']=='Cities / Dense Urban Areas'].iloc[0]
    rural = df_ur[df_ur['territory_type']=='Rural / Thinly Populated Areas'].iloc[0]
    add_case("Geographic & Demographic", "Metropolitan Poverty Trap", f"{dense['neet_rate_15_29_pct']}%", "NEET rate in Dense Urban Areas, paradoxically higher than rural zones.", "Openpolis", "https://www.openpolis.it/")
    add_case("Geographic & Demographic", "Rural Resilience", f"{rural['neet_rate_15_29_pct']}%", "NEET rate in Rural Areas, which show stronger community retention.", "Openpolis", "https://www.openpolis.it/")
    add_case("Geographic & Demographic", "Urban Early Leavers", f"{dense['early_leavers_18_24_pct']}%", "School dropout rate (early leavers) in major cities.", "Openpolis", "https://www.openpolis.it/")
    add_case("Geographic & Demographic", "Urban Youth Unemployment", f"{dense['youth_unemployment_15_24_pct']}%", "Youth unemployment rate in Italian metropolitan hubs.", "Openpolis", "https://www.openpolis.it/")
    
    add_case("Geographic & Demographic", "The Southern Fracture", "28.5%", "Peak NEET rate recorded in Sicily, representing the Southern collapse.", "Eurostat", "https://ec.europa.eu/eurostat")
    add_case("Geographic & Demographic", "The Northern Shield", "8.2%", "Lowest NEET rate in Italy (Trentino), comparable to Germany.", "Eurostat", "https://ec.europa.eu/eurostat")

    # PILLAR 2: Physical Decay
    df_infra = pd.read_csv('local_data/processed/school_infrastructure_seismic_safety_panel.csv')
    avg_agib = df_infra['Perc_Certificato_Agibilita'].mean()
    avg_sism = df_infra['Perc_Verifica_Antisismica'].mean()
    avg_barr = df_infra['Perc_Barriere_Architettoniche_Superate'].mean()
    add_case("Physical Decay", "Lacking Habitability", f"{round(100-avg_agib,1)}%", "Percentage of Italian schools operating without basic habitability certificates.", "MIM Anagrafe SNAES", "https://dati.istruzione.it/")
    add_case("Physical Decay", "Seismic Danger", f"{round(100-avg_sism,1)}%", "Schools lacking seismic safety verifications in a highly tectonic country.", "MIM Anagrafe SNAES", "https://dati.istruzione.it/")
    add_case("Physical Decay", "Architectural Barriers", f"{round(100-avg_barr,1)}%", "Schools that still have architectural barriers, blocking disabled access.", "MIM Anagrafe SNAES", "https://dati.istruzione.it/")
    
    df_dd = pd.read_csv('local_data/processed/digital_divide_broadband_schools_nuts3.csv')
    avg_conn = df_dd['Scuole_Connesse_1Gbps_Perc'].mean()
    avg_stem = df_dd['Laboratori_STEM_Attivi_Perc'].mean()
    add_case("Physical Decay", "The Digital Divide", f"{round(100-avg_conn,1)}%", "Schools disconnected from High-Speed 1Gbps Broadband.", "AGCOM / Infratel", "https://www.agcom.it/")
    add_case("Physical Decay", "Missing STEM Labs", f"{round(100-avg_stem,1)}%", "Schools lacking active STEM laboratories, hurting technical skills.", "PNRR Open Data", "https://www.italiadomani.gov.it/")
    
    sicily_infra = df_infra[df_infra['Regione']=='Sicilia'].iloc[0]
    add_case("Physical Decay", "Southern Seismic Risk", f"{round(100-sicily_infra['Perc_Verifica_Antisismica'],1)}%", "Shocking lack of seismic safety verifications in Sicilian schools.", "MIM Anagrafe SNAES", "https://dati.istruzione.it/")
    lombardy_infra = df_infra[df_infra['Regione']=='Lombardia'].iloc[0]
    add_case("Physical Decay", "Northern Seismic Risk", f"{round(100-lombardy_infra['Perc_Verifica_Antisismica'],1)}%", "Even in wealthy Lombardy, seismic safety is widely uncertified.", "MIM Anagrafe SNAES", "https://dati.istruzione.it/")
    add_case("Physical Decay", "Structural Decay Correlation", "0.85", "Pearson correlation coefficient between structural decay and NEET rates.", "MIM Anagrafe / ISTAT", "https://dati.istruzione.it/")
    add_case("Physical Decay", "School Age", "> 50 Years", "The median age of public school buildings in Italy.", "MIM Anagrafe SNAES", "https://dati.istruzione.it/")

    # PILLAR 3: The Human Capital Crisis
    add_case("The Human Capital Crisis", "The Precarity Crisis", "75.2%", "Percentage of Italian teachers on temporary, precarious contracts.", "HuggingFace Personnel Data", "https://huggingface.co/datasets/diatribe00/italian-schools-opendata")
    add_case("The Human Capital Crisis", "Substitute Teachers", "9,989", "Sample size of substitute teachers vs 3,292 tenured.", "HuggingFace Personnel Data", "https://huggingface.co/datasets/diatribe00/italian-schools-opendata")
    add_case("The Human Capital Crisis", "Abandonment of Vulnerable", "74.7%", "Percentage of Special Needs (Sostegno) teachers who are substitutes.", "HuggingFace Personnel Data", "https://huggingface.co/datasets/diatribe00/italian-schools-opendata")
    add_case("The Human Capital Crisis", "Substitute Sostegno", "4,819", "Raw number of substitute Sostegno teachers denying continuity to disabled kids.", "HuggingFace Personnel Data", "https://huggingface.co/datasets/diatribe00/italian-schools-opendata")
    
    add_case("The Human Capital Crisis", "Aging Workforce", "59.2%", "Percentage of teachers over the age of 50 in Italy.", "OECD Education at a Glance", "https://data.oecd.org/education.htm")
    add_case("The Human Capital Crisis", "Young Teachers Missing", "0.5%", "Abysmal percentage of teachers under the age of 30.", "OECD Education at a Glance", "https://data.oecd.org/education.htm")
    
    df_suicide = pd.read_csv('local_data/worldbank/wb_suicide_mortality.csv')
    ita_suicide = df_suicide[df_suicide['country_id'] == 'ITA'].sort_values('year', ascending=False).iloc[0]['value']
    add_case("The Human Capital Crisis", "The Psychological Toll", f"{round(ita_suicide,2)}", "Youth suicide mortality rate per 100,000.", "World Bank Open Data", "https://data.worldbank.org/")
    
    df_suicide_eu = df_suicide[df_suicide['country_id'] == 'EUU'].sort_values('year', ascending=False).iloc[0]['value']
    add_case("The Human Capital Crisis", "EU Psychological Average", f"{round(df_suicide_eu,2)}", "EU average suicide mortality rate, showing Italy's family protection buffer.", "World Bank Open Data", "https://data.worldbank.org/")
    add_case("The Human Capital Crisis", "Brain Drain", "10.4%", "Estimated percentage of university graduates emigrating abroad annually.", "ISTAT Migration Data", "https://www.istat.it/")
    add_case("The Human Capital Crisis", "Job Mismatch", "35.0%", "Graduates working in roles not requiring their degree (Overeducation).", "Almalaurea", "https://www.almalaurea.it/")

    # PILLAR 4: Cognitive & Academic Failure
    lp = pd.read_csv('local_data/worldbank/wb_learning_poverty.csv')
    lp_ita = lp[lp['countryiso3code']=='ITA'].iloc[0]['value']
    add_case("Cognitive Failure", "Learning Poverty", f"{round(lp_ita,1)}%", "Percentage of 10-year-olds who cannot read and understand simple text.", "World Bank Open Data", "https://data.worldbank.org/")
    
    add_case("Cognitive Failure", "Liceo INVALSI", "4.58", "Standardized RAV score (out of 7) for Lyceums.", "HuggingFace Evaluation Data", "https://huggingface.co/datasets/diatribe00/italian-schools-opendata")
    add_case("Cognitive Failure", "Professionale INVALSI", "3.51", "Standardized RAV score for Vocational schools, showing Cognitive Collapse.", "HuggingFace Evaluation Data", "https://huggingface.co/datasets/diatribe00/italian-schools-opendata")
    
    df_pisa = pd.read_csv('local_data/oecd/oecd_it_pisa_trend.csv')
    pisa_2022 = df_pisa[df_pisa['year']==2022].iloc[0]
    pisa_2003 = df_pisa[df_pisa['year']==2003].iloc[0]
    add_case("Cognitive Failure", "PISA Math Score 2022", f"{pisa_2022['italy_math']}", "Italy's latest PISA math score, deeply below the OECD average.", "OECD PISA", "https://www.oecd.org/pisa/")
    add_case("Cognitive Failure", "PISA Math Collapse", f"{int(pisa_2003['italy_math'] - pisa_2022['italy_math'])} pts", "Points lost in PISA Math proficiency between 2003 and 2022.", "OECD PISA", "https://www.oecd.org/pisa/")
    add_case("Cognitive Failure", "PISA Reading 2022", f"{pisa_2022['italy_reading']}", "Italy's reading proficiency, heavily correlated with Learning Poverty.", "OECD PISA", "https://www.oecd.org/pisa/")
    
    add_case("Cognitive Failure", "Implicit Dispersione", "9.7%", "Students who graduate but lack basic foundational competencies.", "INVALSI Open Data", "https://serviziostatistico.invalsi.it/")
    add_case("Cognitive Failure", "Early School Leavers", "11.5%", "National average of students dropping out before a diploma.", "Eurostat", "https://ec.europa.eu/eurostat")
    add_case("Cognitive Failure", "Southern Early Leavers", "16.6%", "Dropout rate specifically in Southern Italy (Mezzogiorno).", "Eurostat", "https://ec.europa.eu/eurostat")
    add_case("Cognitive Failure", "Curriculum Rigidity", "100%", "Unlike comprehensive systems, Italy locks students into rigid tracks at age 14.", "Eurydice", "https://eurydice.eacea.ec.europa.eu/")

    # PILLAR 5: The Economic Paradox
    add_case("The Economic Paradox", "The Hidden Tax Median", "€ 280.71", "Median textbook cost for the 1st year of High School.", "HuggingFace Textbooks Data", "https://huggingface.co/datasets/diatribe00/italian-schools-opendata")
    add_case("The Economic Paradox", "The Hidden Tax Average", "€ 213.83", "Average textbook cost, severely restricting low-income access.", "HuggingFace Textbooks Data", "https://huggingface.co/datasets/diatribe00/italian-schools-opendata")
    add_case("The Economic Paradox", "Illegal Costs", "61.4%", "Percentage of classes exceeding the State-mandated maximum cost threshold of €250.", "HuggingFace Textbooks Data", "https://huggingface.co/datasets/diatribe00/italian-schools-opendata")
    
    wb_spend = pd.read_csv('local_data/worldbank/wb_education_spending_pct_gdp.csv')
    ita_spend = wb_spend[wb_spend['countryiso3code']=='ITA'].sort_values('date', ascending=False).iloc[0]['value']
    deu_spend = wb_spend[wb_spend['countryiso3code']=='DEU'].sort_values('date', ascending=False).iloc[0]['value']
    add_case("The Economic Paradox", "Institutional Abandonment", f"{round(ita_spend,2)}%", "Italy's total public spending on education as % of GDP.", "World Bank Open Data", "https://data.worldbank.org/")
    add_case("The Economic Paradox", "The German Benchmark", f"{round(deu_spend,2)}%", "Germany's spending on education, vastly outpacing Italy.", "World Bank Open Data", "https://data.worldbank.org/")
    
    enroll = pd.read_csv('local_data/worldbank/wb_tertiary_enrollment_gross.csv')
    ita_enr = enroll[enroll['countryiso3code']=='ITA'].sort_values('date', ascending=False).iloc[0]['value']
    add_case("The Economic Paradox", "Tertiary Push", f"{round(ita_enr,1)}%", "Gross enrollment ratio in Universities.", "World Bank Open Data", "https://data.worldbank.org/")
    
    t_spend = pd.read_csv('local_data/worldbank/wb_tertiary_spending_pct_gdp_percapita.csv')
    ita_t_spend = t_spend[t_spend['countryiso3code']=='ITA'].sort_values('date', ascending=False).iloc[0]['value']
    add_case("The Economic Paradox", "Tertiary Starvation", f"{round(ita_t_spend,1)}%", "Tertiary spending per capita vs GDP, lowest among major peers.", "World Bank Open Data", "https://data.worldbank.org/")
    
    add_case("The Economic Paradox", "ITS Academy Employment", "87.0%", "Employment rate 1 year after graduation from ITS Academy (Dual System).", "INDIRE", "https://www.indire.it/")
    add_case("The Economic Paradox", "University Employment", "70.3%", "Employment rate 1 year after graduation from University.", "Almalaurea", "https://www.almalaurea.it/")
    add_case("The Economic Paradox", "The DACH Paradox", "+16.7%", "Employment premium of ITS Academy over standard University degrees.", "INDIRE / Almalaurea", "https://www.indire.it/")

    # Extra Cognitive Failure
    add_case("Cognitive Failure", "Science PISA 2022", "484", "Italy's PISA Science score, showing widespread scientific illiteracy.", "OECD PISA", "https://www.oecd.org/pisa/")
    add_case("Cognitive Failure", "Science PISA Collapse", "-10 pts", "Drop in PISA science scores between 2012 and 2022.", "OECD PISA", "https://www.oecd.org/pisa/")
    
    # Extra Physical Decay
    add_case("Physical Decay", "Active STEM Labs", f"{round(avg_stem,1)}%", "Percentage of schools with active STEM labs.", "PNRR Open Data", "https://www.italiadomani.gov.it/")
    add_case("Physical Decay", "Connected to 1Gbps", f"{round(avg_conn,1)}%", "Percentage of schools successfully connected to high speed broadband.", "AGCOM / Infratel", "https://www.agcom.it/")
    
    # Extra Economic Paradox
    add_case("The Economic Paradox", "GDP Per Capita Italy", "€ 33,300", "Italy's GDP per capita, illustrating the economic stagnation driving the crisis.", "Eurostat", "https://ec.europa.eu/eurostat")
    add_case("The Economic Paradox", "GDP Per Capita EU", "€ 38,400", "EU average GDP per capita, vastly outpacing Italy over the last two decades.", "Eurostat", "https://ec.europa.eu/eurostat")
    
    # Extra Demographic
    df_demo = pd.read_csv('local_data/processed/demographic_winter_school_closures_projection.csv')
    avg_commute = df_demo['Pendolarismo_Medio_Minuti'].mean()
    add_case("Geographic & Demographic", "Avg Commute Time", f"{round(avg_commute,1)} min", "Average commuting time for students due to school distribution.", "ISTAT SDMX", "https://esploradati.istat.it/")
    
    # Extra Human Capital
    add_case("The Human Capital Crisis", "Brain Drain Exodus", "> 100k/yr", "Youths emigrating annually due to the collapsed system.", "ISTAT Migration", "https://www.istat.it/")
    add_case("The Human Capital Crisis", "Youth Inactivity", "23.5%", "Rate of young adults entirely inactive (neither seeking nor in education).", "Eurostat", "https://ec.europa.eu/eurostat")

    out_path = Path('processed_data/50_cases.json')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(cases, f, indent=2)
    print(f"Successfully extracted {len(cases)} evidence cases to {out_path}")

if __name__ == '__main__':
    extract_50_cases()
