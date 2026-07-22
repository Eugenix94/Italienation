import pandas as pd
import os

def build_macro_infrastructure_data():
    print("Building Macro-Infrastructure & Demographics Proxy Dataset...")
    
    # Simulating MIM/ISTAT data for the final three systemic blind spots:
    # 1. Tempo Pieno (Full-time school with cafeterias, crucial for female employment & combating educational poverty)
    # 2. Denatalità / Dimensionamento (Demographic collapse leading to school mergers and closures)
    # 3. Supplentite (Precarious teachers, destroying pedagogical continuity)
    
    data = [
        # Northern Regions (Strong Infrastructure, Demographic Stability, High Teacher Turnover due to Cost of Living)
        ("Lombardia", "Nord", 2023, 58.5, -2.1, 28.5, "High Teacher Turnover (Cost of Living)"),
        ("Emilia-Romagna", "Nord", 2023, 62.0, -1.8, 25.0, "High Infrastructure, Moderate Precarity"),
        ("Veneto", "Nord", 2023, 55.0, -2.5, 26.5, "Strong Infrastructure"),
        
        # Central Regions
        ("Lazio", "Centro", 2023, 45.0, -4.0, 22.0, "Average Infrastructure, Moderate Mergers"),
        ("Toscana", "Centro", 2023, 52.0, -3.5, 20.0, "Good Infrastructure"),
        
        # Southern Regions (Severe Infrastructural Deficit, Demographic Collapse, Lower Turnover but High Precarity)
        ("Campania", "Sud", 2023, 18.5, -7.5, 32.0, "Severe Tempo Pieno Deficit, High Demographic Closures"),
        ("Sicilia", "Sud", 2023, 14.0, -8.2, 35.0, "Extreme Tempo Pieno Deficit, Extreme Demographic Closures"),
        ("Calabria", "Sud", 2023, 16.5, -9.0, 30.0, "Severe Demographic Collapse (Internal Migration)"),
        ("Puglia", "Sud", 2023, 22.0, -6.8, 28.0, "High Demographic Closures"),
    ]
    
    df = pd.DataFrame(data, columns=[
        "Region", "Macro_Area", "Year", 
        "Tempo_Pieno_Coverage_Percent", 
        "Demographic_Change_Percent_5Yr", 
        "Precarious_Teachers_Percent",
        "Systemic_Friction_Profile"
    ])
    
    # Calculate a composite "Structural Vulnerability Index" (0-100, higher is worse)
    # Low Tempo Pieno increases vulnerability. High demographic collapse (negative change) increases vulnerability. High precarity increases vulnerability.
    df["Structural_Vulnerability_Index"] = (
        (100 - df["Tempo_Pieno_Coverage_Percent"]) * 0.4 + 
        (df["Demographic_Change_Percent_5Yr"].abs() * 2) * 0.3 + 
        (df["Precarious_Teachers_Percent"]) * 0.3
    ).round(1)
    
    out_dir = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\processed"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "macro_infrastructure_demographics_panel.csv")
    
    df.to_csv(out_file, index=False)
    print(f"Macro-Infrastructure & Demographics Dataset saved to: {out_file}")

if __name__ == "__main__":
    build_macro_infrastructure_data()
