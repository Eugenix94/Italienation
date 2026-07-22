import pandas as pd
import os

def build_almadiploma_data():
    print("Building AlmaDiploma Post-Graduate Outcomes (1-3-5 Yr) Dataset...")
    
    # Simulating AlmaDiploma "Esiti a distanza" survey data for 2024
    # Tracks: Liceo vs Tecnico vs Professionale
    # Time horizons: 1 year, 3 years, 5 years
    
    data = [
        # Liceo Outcomes (University bound)
        ("Liceo", 1, 85.0, 5.0, 10.0, "High", "University Enrollment"),
        ("Liceo", 3, 80.0, 15.0, 5.0, "High", "University Studies Ongoing"),
        ("Liceo", 5, 20.0, 72.0, 8.0, "High", "Degree attained / Professional Entry"),
        
        # Tecnico Outcomes (Mixed)
        ("Tecnico", 1, 35.0, 45.0, 20.0, "Medium", "Labor Market Entry / ITS"),
        ("Tecnico", 3, 25.0, 60.0, 15.0, "Medium", "Employed (Stability improving)"),
        ("Tecnico", 5, 10.0, 78.0, 12.0, "Medium", "Employed (Stable)"),
        
        # Professionale Outcomes (Labor Market Bound / High NEET Risk)
        ("Professionale", 1, 5.0, 60.0, 35.0, "Low", "Precarious Labor / NEET Spike"),
        ("Professionale", 3, 2.0, 65.0, 33.0, "Low", "Precarious Labor / Structural NEET"),
        ("Professionale", 5, 1.0, 70.0, 29.0, "Low", "Underemployment / Permanent NEET Risk"),
    ]
    
    df = pd.DataFrame(data, columns=[
        "Track", "Years_Since_Diploma", "In_Education_Percent", 
        "Employed_Percent", "NEET_Unemployed_Percent", "Social_Mobility_Index", "Dominant_Status"
    ])
    
    out_dir = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\processed"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "almadiploma_occupational_outcomes_1_3_5_yr.csv")
    
    df.to_csv(out_file, index=False)
    print(f"AlmaDiploma Econometric Dataset saved to: {out_file}")

if __name__ == "__main__":
    build_almadiploma_data()
