import pandas as pd
import json

def build_matrix():
    data = [
        {
            "System_Type": "Underfunded Tripartite",
            "Region": "Italy",
            "NEET_Rate_Pct": 23.1,
            "Education_Spend_GDP_Pct": 4.1,
            "PISA_Math_Score": 471,
            "Teachers_Over_50_Pct": 59.0,
            "VET_Dropout_Rate_Pct": 14.8,
            "Pedagogical_Approach": "Early Tracking (Age 14) + Repetition"
        },
        {
            "System_Type": "Dual System Tripartite",
            "Region": "DACH (DE/CH/AT)",
            "NEET_Rate_Pct": 8.5,
            "Education_Spend_GDP_Pct": 5.2,
            "PISA_Math_Score": 495,
            "Teachers_Over_50_Pct": 38.0,
            "VET_Dropout_Rate_Pct": 3.2,
            "Pedagogical_Approach": "Early Tracking (Age 10-12) + Apprenticeship"
        },
        {
            "System_Type": "Comprehensive",
            "Region": "United Kingdom",
            "NEET_Rate_Pct": 12.6,
            "Education_Spend_GDP_Pct": 5.4,
            "PISA_Math_Score": 489,
            "Teachers_Over_50_Pct": 22.0,
            "VET_Dropout_Rate_Pct": 0.5,
            "Pedagogical_Approach": "Unified Curriculum to 16 + Social Promotion"
        },
        {
            "System_Type": "OECD Benchmark",
            "Region": "OECD Average",
            "NEET_Rate_Pct": 13.0,
            "Education_Spend_GDP_Pct": 4.9,
            "PISA_Math_Score": 472,
            "Teachers_Over_50_Pct": 36.0,
            "VET_Dropout_Rate_Pct": 5.0,
            "Pedagogical_Approach": "Mixed Average"
        }
    ]
    
    df = pd.DataFrame(data)
    
    # Save CSV
    out_path = 'processed_data/interconnected_global_reality.csv'
    df.to_csv(out_path, index=False)
    print(f"Interconnected matrix saved to {out_path}")
    
    # Also save as JSON for easy web integration
    json_path = 'rendered_outputs/data_interconnected_matrix.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"JSON matrix saved to {json_path}")

if __name__ == '__main__':
    build_matrix()
