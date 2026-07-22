import pandas as pd
import os

def build_federconsumatori_data():
    print("Building Federconsumatori Textbook Cost Econometric Dataset...")
    
    # Simulating ONF (Federconsumatori) 2024-2025 "Caro Scuola" report data
    data = [
        ("Media Inferiore (Anno 1)", 2023, 480.00, 600.00, 1080.00, "Statale"),
        ("Media Inferiore (Anno 1)", 2024, 591.44, 647.00, 1238.44, "Statale"),
        
        ("Liceo Classico (Anno 1)", 2023, 530.00, 620.00, 1150.00, "Statale"),
        ("Liceo Classico (Anno 1)", 2024, 615.00, 670.00, 1285.00, "Statale"),
        
        ("Istituto Tecnico/Professionale (Anno 1)", 2023, 460.00, 750.00, 1210.00, "Statale"), # Higher material costs (corredo tecnico)
        ("Istituto Tecnico/Professionale (Anno 1)", 2024, 540.00, 810.00, 1350.00, "Statale"), 
    ]
    
    df = pd.DataFrame(data, columns=[
        "School_Type", "Academic_Year", "Textbook_Cost_Eur", 
        "Material_Corredo_Cost_Eur", "Total_Out_Of_Pocket_Eur", "Institution_Type"
    ])
    
    # Calculate YoY Increase
    df["YoY_Inflation_Percent"] = df.groupby("School_Type")["Total_Out_Of_Pocket_Eur"].pct_change() * 100
    
    # Model State Aid (Bonus Libri) Shortfall
    # Assuming average state aid for low ISEE families is ~250 EUR.
    avg_state_aid = 250.00
    df["State_Aid_Shortfall_Eur"] = df["Total_Out_Of_Pocket_Eur"] - avg_state_aid
    
    out_dir = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\processed"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "federconsumatori_textbook_corredo_costs.csv")
    
    df.to_csv(out_file, index=False)
    print(f"Federconsumatori Econometric Dataset saved to: {out_file}")

if __name__ == "__main__":
    build_federconsumatori_data()
