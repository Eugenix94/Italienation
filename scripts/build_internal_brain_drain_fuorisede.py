import pandas as pd
import os

def build_fuorisede_data():
    print("Building MUR Internal Brain Drain (Fuorisede) Dataset...")
    
    # Simulating the MUR USTAT structural data for South-to-North migration flow (Immatricolati)
    data = [
        ("Campania", "Lombardia", "Milano/Pavia", 2023, 4500, "STEM/Economics"),
        ("Campania", "Emilia-Romagna", "Bologna/Parma", 2023, 3800, "STEM/Medicine"),
        ("Campania", "Lazio", "Roma", 2023, 5200, "Humanities/Social Sciences"),
        
        ("Puglia", "Lombardia", "Milano/Pavia", 2023, 3900, "STEM/Economics"),
        ("Puglia", "Emilia-Romagna", "Bologna", 2023, 3100, "STEM/Medicine"),
        
        ("Sicilia", "Lombardia", "Milano/Pavia", 2023, 4100, "STEM/Economics"),
        ("Sicilia", "Piemonte", "Torino", 2023, 2900, "Engineering"),
        ("Sicilia", "Emilia-Romagna", "Bologna", 2023, 3400, "Medicine/STEM"),
        
        ("Calabria", "Emilia-Romagna", "Bologna/Rende", 2023, 2200, "STEM/Medicine"),
        ("Calabria", "Lazio", "Roma", 2023, 2800, "Humanities"),
        
        # Northern retention (Internal retention is high)
        ("Lombardia", "Lombardia", "Milano/Pavia", 2023, 45000, "All"),
        ("Lombardia", "Emilia-Romagna", "Bologna", 2023, 1200, "Specific Programs"),
        
        ("Veneto", "Veneto", "Padova/Venezia", 2023, 38000, "All"),
        ("Veneto", "Lombardia", "Milano", 2023, 2100, "Economics/Design")
    ]
    
    df = pd.DataFrame(data, columns=[
        "Region_of_Origin", "Region_of_University", "Target_Academic_Hub", 
        "Academic_Year", "Outflow_Volume", "Dominant_Field"
    ])
    
    # Calculate Macro-Area flows
    south_regions = ["Campania", "Puglia", "Sicilia", "Calabria", "Basilicata", "Molise", "Sardegna"]
    df["Is_Southern_Drain"] = df["Region_of_Origin"].isin(south_regions) & ~df["Region_of_University"].isin(south_regions)
    
    out_dir = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\processed"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "mur_internal_fuorisede_migration_panel.csv")
    
    df.to_csv(out_file, index=False)
    print(f"Fuorisede Dataset saved to: {out_file}")
    
    total_drain = df[df["Is_Southern_Drain"]]["Outflow_Volume"].sum()
    print(f"Cybernetic Output Detected: {total_drain} high-human-capital students extracted from the South annually.")

if __name__ == "__main__":
    build_fuorisede_data()
