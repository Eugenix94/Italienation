import pandas as pd
import os

def build_diplomifici_data():
    print("Building MIM Diplomifici (Diploma Mills) Anomaly Proxy Dataset...")
    
    # Simulating MIM (Ministero Istruzione) anomaly data for "Scuole Paritarie" (Private Schools)
    # The signature anomaly of a "diplomificio" is a massive spike in 5th-year (Maturità) enrollments 
    # compared to 4th-year enrollments, as failed public school students transfer in to buy the diploma.
    
    data = [
        # Normal Public School Profile
        ("Liceo Statale X", "Lombardia", "Statale", 150, 145, 1.03),
        ("Istituto Tecnico Statale Y", "Veneto", "Statale", 120, 115, 1.04),
        ("Istituto Professionale Statale Z", "Campania", "Statale", 80, 60, 0.75), # High dropout
        
        # Normal Private School Profile
        ("Liceo Paritario d'Elite", "Lombardia", "Paritaria", 50, 48, 0.96),
        
        # "Diplomifici" Anomalies (Based on Tuttoscuola / MIM investigations)
        ("Istituto Paritario A", "Campania", "Paritaria (Anomaly)", 15, 250, 16.6), 
        ("Istituto Paritario B", "Campania", "Paritaria (Anomaly)", 12, 180, 15.0),
        ("Istituto Paritario C", "Sicilia", "Paritaria (Anomaly)", 20, 190, 9.5),
        ("Istituto Paritario D", "Lazio", "Paritaria (Anomaly)", 18, 150, 8.3),
        ("Istituto Paritario E", "Campania", "Paritaria (Anomaly)", 5, 300, 60.0) # Extreme anomaly
    ]
    
    df = pd.DataFrame(data, columns=[
        "School_Name", "Region", "School_Type", 
        "Enrollment_Year_4", "Enrollment_Year_5", "Year_5_to_4_Ratio"
    ])
    
    # Flag cybernetic bypass (Ratio > 3.0 indicates almost certain diploma mill bypass)
    df["Is_Bypass_Valve"] = df["Year_5_to_4_Ratio"] > 3.0
    
    out_dir = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\processed"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "mim_diplomifici_anomaly_proxy.csv")
    
    df.to_csv(out_file, index=False)
    print(f"Diplomifici Anomaly Dataset saved to: {out_file}")
    
    bypass_count = df[df["Is_Bypass_Valve"]]["Enrollment_Year_5"].sum()
    print(f"Cybernetic Bypass Detected: {bypass_count} students bypassing the Bocciatura filter via private capital.")

if __name__ == "__main__":
    build_diplomifici_data()
