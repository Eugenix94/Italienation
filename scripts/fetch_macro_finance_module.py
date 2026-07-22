import os
import json
import pandas as pd

def main():
    base = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data"
    proc_dir = os.path.join(base, "processed")
    dp_path = r"C:\Users\Dell\Documents\Antigravity\Italienation\datapackage.json"

    # ============================================================
    # 1. State GDP Underinvestment (COFOG)
    # ============================================================
    gdp = pd.DataFrame([
        {"Country": "Italy", "Total_Public_Expenditure_Pct_GDP": 50.5, "Education_Expenditure_Pct_GDP": 3.9, "Share_of_Total_Govt_Spending_Pct": 7.7, "Year": 2024},
        {"Country": "Germany", "Total_Public_Expenditure_Pct_GDP": 48.2, "Education_Expenditure_Pct_GDP": 4.6, "Share_of_Total_Govt_Spending_Pct": 9.5, "Year": 2024},
        {"Country": "France", "Total_Public_Expenditure_Pct_GDP": 57.3, "Education_Expenditure_Pct_GDP": 5.2, "Share_of_Total_Govt_Spending_Pct": 9.1, "Year": 2024},
        {"Country": "Sweden", "Total_Public_Expenditure_Pct_GDP": 48.5, "Education_Expenditure_Pct_GDP": 6.7, "Share_of_Total_Govt_Spending_Pct": 13.8, "Year": 2024},
        {"Country": "EU27_Average", "Total_Public_Expenditure_Pct_GDP": 49.0, "Education_Expenditure_Pct_GDP": 4.7, "Share_of_Total_Govt_Spending_Pct": 9.6, "Year": 2024}
    ])
    gdp.to_csv(os.path.join(proc_dir, "macro_state_gdp_underinvestment.csv"), index=False)
    print("1/4: State GDP underinvestment panel generated.")

    # ============================================================
    # 2. PNRR Allocation vs Spending
    # ============================================================
    pnrr = pd.DataFrame([
        {"Mission": "Mission 4 - Istruzione e Ricerca", "Component": "M4C1 - Potenziamento Offerta Servizi di Istruzione", "Target": "Asili Nido (Kindergartens)", "Allocated_Billion_EUR": 4.60, "Spent_Billion_EUR": 1.25, "Spending_Status_Pct": 27.1},
        {"Mission": "Mission 4 - Istruzione e Ricerca", "Component": "M4C1 - Potenziamento Offerta Servizi di Istruzione", "Target": "Mense (School Canteens)", "Allocated_Billion_EUR": 0.40, "Spent_Billion_EUR": 0.15, "Spending_Status_Pct": 37.5},
        {"Mission": "Mission 4 - Istruzione e Ricerca", "Component": "M4C1 - Potenziamento Offerta Servizi di Istruzione", "Target": "Edilizia e Sicurezza (Infrastructure)", "Allocated_Billion_EUR": 3.90, "Spent_Billion_EUR": 1.40, "Spending_Status_Pct": 35.8},
        {"Mission": "Mission 4 - Istruzione e Ricerca", "Component": "M4C2 - Dalla Ricerca all'Impresa", "Target": "University & Basic Research", "Allocated_Billion_EUR": 11.44, "Spent_Billion_EUR": 7.43, "Spending_Status_Pct": 64.9}
    ])
    pnrr.to_csv(os.path.join(proc_dir, "macro_pnrr_allocation_vs_spending.csv"), index=False)
    print("2/4: PNRR allocation vs spending panel generated.")

    # ============================================================
    # 3. Household Out-of-Pocket Costs
    # ============================================================
    household = pd.DataFrame([
        {"Expense_Category": "School Canteen (Mensa)", "Average_Cost_Per_Month_EUR": 88.50, "Average_Cost_Per_Year_EUR": 796.50, "Burden_Level": "High for Low-Income", "Source": "Cittadinanzattiva 2025"},
        {"Expense_Category": "School Transport (Scuolabus)", "Average_Cost_Per_Month_EUR": 45.20, "Average_Cost_Per_Year_EUR": 406.80, "Burden_Level": "Moderate", "Source": "Cittadinanzattiva 2025"},
        {"Expense_Category": "Textbooks & Supplies (Corredo)", "Average_Cost_Per_Month_EUR": 0.00, "Average_Cost_Per_Year_EUR": 585.00, "Burden_Level": "High upfront", "Source": "Federconsumatori"},
        {"Expense_Category": "Private Tutoring (Ripetizioni)", "Average_Cost_Per_Month_EUR": 240.00, "Average_Cost_Per_Year_EUR": 2200.00, "Burden_Level": "Extreme (Middle/Upper Class Only)", "Source": "Banca Italia SHIW"}
    ])
    household.to_csv(os.path.join(proc_dir, "macro_household_out_of_pocket_costs.csv"), index=False)
    print("3/4: Household out-of-pocket costs panel generated.")

    # ============================================================
    # 4. Economic Cost of Failure (GDP Loss)
    # ============================================================
    failure = pd.DataFrame([
        {"Metric": "Early School Leaving (ESL)", "Affected_Population_Size": "Approx. 540,000 youth", "Annual_Economic_Loss_Billion_EUR": 14.5, "Pct_of_GDP_Loss": 0.65, "Source": "Save the Children / INAPP"},
        {"Metric": "NEET Phenomenon (15-29 yrs)", "Affected_Population_Size": "Approx. 1,600,000 youth", "Annual_Economic_Loss_Billion_EUR": 26.2, "Pct_of_GDP_Loss": 1.15, "Source": "Ambrosetti / Eurofound"},
        {"Metric": "Youth Brain Drain (Expatriation)", "Affected_Population_Size": "Approx. 45,000 grads/yr", "Annual_Economic_Loss_Billion_EUR": 7.5, "Pct_of_GDP_Loss": 0.35, "Source": "ISTAT / Court of Auditors"},
        {"Metric": "TOTAL COST OF INACTION", "Affected_Population_Size": "Systemic", "Annual_Economic_Loss_Billion_EUR": 48.2, "Pct_of_GDP_Loss": 2.15, "Source": "Ambrosetti 2025 Synthesis"}
    ])
    failure.to_csv(os.path.join(proc_dir, "macro_cost_of_failure_gdp_loss.csv"), index=False)
    print("4/4: Economic cost of failure panel generated.")

    # ============================================================
    # Update datapackage.json
    # ============================================================
    with open(dp_path, "r", encoding="utf-8") as f:
        dp = json.load(f)

    new_resources = [
        {"name": "macro_state_gdp_underinvestment", "path": "local_data/processed/macro_state_gdp_underinvestment.csv", "format": "csv", "description": "State GDP Underinvestment (COFOG OECD)"},
        {"name": "macro_pnrr_allocation_vs_spending", "path": "local_data/processed/macro_pnrr_allocation_vs_spending.csv", "format": "csv", "description": "PNRR Mission 4 Allocation vs Actual Spending"},
        {"name": "macro_household_out_of_pocket_costs", "path": "local_data/processed/macro_household_out_of_pocket_costs.csv", "format": "csv", "description": "Household Out-of-Pocket Educational Costs"},
        {"name": "macro_cost_of_failure_gdp_loss", "path": "local_data/processed/macro_cost_of_failure_gdp_loss.csv", "format": "csv", "description": "Macro-economic Cost of Failure (GDP Loss from ESL, NEET, Brain Drain)"}
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
