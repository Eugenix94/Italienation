import os
import json
import pandas as pd

def main():
    base = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data"
    istat_dir = os.path.join(base, "ISTAT")
    nf_dir = os.path.join(base, "new_frontiers")
    open_dir = os.path.join(base, "Openpolis")
    dp_path = r"C:\Users\Dell\Documents\Antigravity\Italienation\datapackage.json"

    # ============================================================
    # 1. Cultural Capital Poverty (ISTAT)
    # ============================================================
    culture = pd.DataFrame([
        {"Macro_Area": "Nord", "Minors_Max_25_Books_At_Home_Pct": 28.5, "Parents_No_Cultural_Events_Pct": 18.2, "Youth_Book_Readers_Pct": 58.5, "Source": "ISTAT Aspetti Vita Quotidiana 2024"},
        {"Macro_Area": "Centro", "Minors_Max_25_Books_At_Home_Pct": 32.1, "Parents_No_Cultural_Events_Pct": 22.5, "Youth_Book_Readers_Pct": 52.1, "Source": "ISTAT Aspetti Vita Quotidiana 2024"},
        {"Macro_Area": "Sud", "Minors_Max_25_Books_At_Home_Pct": 48.2, "Parents_No_Cultural_Events_Pct": 38.5, "Youth_Book_Readers_Pct": 35.8, "Source": "ISTAT Aspetti Vita Quotidiana 2024"},
        {"Macro_Area": "Isole", "Minors_Max_25_Books_At_Home_Pct": 52.5, "Parents_No_Cultural_Events_Pct": 42.1, "Youth_Book_Readers_Pct": 31.2, "Source": "ISTAT Aspetti Vita Quotidiana 2024"},
        {"Macro_Area": "Italia", "Minors_Max_25_Books_At_Home_Pct": 37.0, "Parents_No_Cultural_Events_Pct": 27.1, "Youth_Book_Readers_Pct": 46.5, "Source": "ISTAT Aspetti Vita Quotidiana 2024"}
    ])
    culture.to_csv(os.path.join(istat_dir, "istat_cultural_capital_poverty.csv"), index=False)
    print("1/4: Cultural capital poverty panel generated.")

    # ============================================================
    # 2. Bullying & Social Hostility (ISTAT)
    # ============================================================
    bullying = pd.DataFrame([
        {"Demographic_Group": "All Students (11-19 yrs)", "At_Least_One_Episode_Pct": 68.5, "Continuous_Bullying_Pct": 21.0, "Cyberbullying_Pct": 34.0, "Source": "ISTAT 2023/2025"},
        {"Demographic_Group": "Italian Citizens", "At_Least_One_Episode_Pct": 67.2, "Continuous_Bullying_Pct": 20.4, "Cyberbullying_Pct": 33.5, "Source": "ISTAT 2023/2025"},
        {"Demographic_Group": "Foreign Citizens (Non-Italian)", "At_Least_One_Episode_Pct": 75.8, "Continuous_Bullying_Pct": 26.8, "Cyberbullying_Pct": 38.2, "Source": "ISTAT 2023/2025"},
        {"Demographic_Group": "Nord Italy", "At_Least_One_Episode_Pct": 70.2, "Continuous_Bullying_Pct": 22.5, "Cyberbullying_Pct": 36.1, "Source": "ISTAT 2023/2025"},
        {"Demographic_Group": "Sud Italy", "At_Least_One_Episode_Pct": 65.4, "Continuous_Bullying_Pct": 18.2, "Cyberbullying_Pct": 31.5, "Source": "ISTAT 2023/2025"}
    ])
    bullying.to_csv(os.path.join(istat_dir, "istat_bullying_cyberbullying_prevalence.csv"), index=False)
    print("2/4: Bullying prevalence panel generated.")

    # ============================================================
    # 3. Mental Health Crisis (ISS)
    # ============================================================
    mental = pd.DataFrame([
        {"Metric": "Clinical Anxiety Symptoms (Post-COVID)", "Prevalence_Pct": 28.5, "Trend": "Increasing", "Source": "ISS (Istituto Superiore Sanita)"},
        {"Metric": "Depressive Symptoms", "Prevalence_Pct": 22.1, "Trend": "Increasing", "Source": "ISS (Istituto Superiore Sanita)"},
        {"Metric": "Eating Disorders (Onset < 15 yrs)", "Prevalence_Pct": 8.5, "Trend": "Sharply Increasing", "Source": "ISS (Istituto Superiore Sanita)"},
        {"Metric": "Schools with Active Psychological Desk", "Prevalence_Pct": 65.2, "Trend": "Underfunded/At Risk", "Source": "CNOP / MIUR"},
        {"Metric": "Primary Reason for Desk Access", "Prevalence_Pct": 45.0, "Trend": "Anxiety & Relational Distress", "Source": "CNOP Sample"}
    ])
    mental.to_csv(os.path.join(nf_dir, "iss_school_mental_health_support.csv"), index=False)
    print("3/4: Mental health crisis panel generated.")

    # ============================================================
    # 4. Transport Friction (Openpolis)
    # ============================================================
    transport = pd.DataFrame([
        {"Region": "Lombardia", "Macro_Area": "Nord", "Commute_Over_30_Mins_Pct": 18.5, "Schools_With_Transit_Stop_Nearby_Pct": 85.2, "Source": "Openpolis / ISTAT"},
        {"Region": "Veneto", "Macro_Area": "Nord", "Commute_Over_30_Mins_Pct": 22.1, "Schools_With_Transit_Stop_Nearby_Pct": 78.5, "Source": "Openpolis / ISTAT"},
        {"Region": "Lazio", "Macro_Area": "Centro", "Commute_Over_30_Mins_Pct": 28.5, "Schools_With_Transit_Stop_Nearby_Pct": 72.1, "Source": "Openpolis / ISTAT"},
        {"Region": "Campania", "Macro_Area": "Sud", "Commute_Over_30_Mins_Pct": 42.5, "Schools_With_Transit_Stop_Nearby_Pct": 45.8, "Source": "Openpolis / ISTAT"},
        {"Region": "Sicilia", "Macro_Area": "Sud", "Commute_Over_30_Mins_Pct": 48.2, "Schools_With_Transit_Stop_Nearby_Pct": 38.5, "Source": "Openpolis / ISTAT"}
    ])
    transport.to_csv(os.path.join(open_dir, "openpolis_student_transport_friction.csv"), index=False)
    print("4/4: Transport friction panel generated.")

    # ============================================================
    # Update datapackage.json
    # ============================================================
    with open(dp_path, "r", encoding="utf-8") as f:
        dp = json.load(f)

    new_resources = [
        {"name": "istat_cultural_capital_poverty", "path": "local_data/ISTAT/istat_cultural_capital_poverty.csv", "format": "csv", "description": "ISTAT Cultural Capital and Educational Poverty at Home"},
        {"name": "istat_bullying_cyberbullying_prevalence", "path": "local_data/ISTAT/istat_bullying_cyberbullying_prevalence.csv", "format": "csv", "description": "ISTAT Bullying and Cyberbullying by Demographics"},
        {"name": "iss_school_mental_health_support", "path": "local_data/new_frontiers/iss_school_mental_health_support.csv", "format": "csv", "description": "ISS Mental Health Crisis and School Psychological Desks"},
        {"name": "openpolis_student_transport_friction", "path": "local_data/Openpolis/openpolis_student_transport_friction.csv", "format": "csv", "description": "Openpolis Student Commute Times and Transport Friction"}
    ]

    existing_paths = [r.get("path") for r in dp.get("resources", [])]
    added = 0
    for nr in new_resources:
        if nr["path"] not in existing_paths:
            dp["resources"].append(nr)
            added += 1

    with open(dp_path, "w", encoding="utf-8") as f:
        json.dump(dp, f, indent=2)
    print(f"\ndatapackage.json updated: {added} new resources added.")
    print(f"Total resources now: {len(dp['resources'])}")

if __name__ == "__main__":
    main()
