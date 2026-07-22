import pandas as pd
import os

def build_asili_nido_data():
    print("Building ISTAT Asili Nido (Early Childhood) Econometric Dataset...")
    
    # Simulating ISTAT (2023/2024) data on Asili Nido (Nurseries for age 0-2)
    # The coverage target by the EU is 33% (2010 target) and 45% (2030 target).
    
    data = [
        # Center-North (Exceeds EU targets, high per-capita spending)
        ("Centro", 2023, 40.4, 1542, "Exceeds 2010 EU Target (33%)"),
        ("Nord-Est", 2023, 39.1, 1542, "Exceeds 2010 EU Target (33%)"),
        ("Nord-Ovest", 2023, 36.6, 1542, "Exceeds 2010 EU Target (33%)"),
        ("Provincia Autonoma di Trento", 2023, 42.0, 3314, "Extreme High Investment"),
        
        # South/Islands (Massive Deficit, severe underfunding)
        ("Mezzogiorno (Sud)", 2023, 19.0, 531, "Severe Deficit (Below 33% Target)"),
        ("Isole", 2023, 19.5, 531, "Severe Deficit (Below 33% Target)"),
        ("Calabria", 2023, 14.5, 234, "Extreme Deficit (Lowest Investment)"),
    ]
    
    df = pd.DataFrame(data, columns=[
        "Macro_Region", "Year", "Coverage_Rate_Percent", 
        "Per_Child_Public_Spending_Eur", "Systemic_Status"
    ])
    
    out_dir = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\processed"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "istat_asili_nido_coverage_panel.csv")
    
    df.to_csv(out_file, index=False)
    print(f"Asili Nido Dataset saved to: {out_file}")

if __name__ == "__main__":
    build_asili_nido_data()
