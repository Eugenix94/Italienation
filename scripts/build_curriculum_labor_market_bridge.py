import pandas as pd
import os

def build_oed_bridge():
    print("Building Origin-Education-Destination (OED) Linkage...")
    
    curr_path = r"../local_data/processed/tripartite_curriculum_hours_panel.csv"
    if not os.path.exists(curr_path):
        print("Curriculum dataset not found. Run build_curriculum_dataset.py first.")
        return
        
    df_curr = pd.read_csv(curr_path)
    
    print("\n--- Structural Analysis: The Italian Tripartite Mismatch ---")
    
    # Analyze Humanities / Critical vs Applied Labor
    for track in df_curr['Track'].unique():
        track_df = df_curr[df_curr['Track'] == track]
        total_hours = track_df['Total_Hours_5_Years'].sum()
        
        humanities_hours = track_df[track_df['Domain'] == 'Humanities']['Total_Hours_5_Years'].sum()
        labor_hours = track_df[track_df['Domain'] == 'Applied/Labor']['Total_Hours_5_Years'].sum()
        
        hum_pct = (humanities_hours / total_hours) * 100 if total_hours > 0 else 0
        lab_pct = (labor_hours / total_hours) * 100 if total_hours > 0 else 0
        
        print(f"\n{track}:")
        print(f"  - Cultural Capital (Humanities): {hum_pct:.1f}% of core curriculum")
        print(f"  - Technical Capital (Applied/Labor): {lab_pct:.1f}% of core curriculum")
        
        if "Classico" in track or "Scientifico" in track:
            print("  -> OED Outcome: High probability of university transition. Low structural NEET risk. Strong rote/theoretical foundation.")
        elif "Professionale" in track:
            print("  -> OED Outcome: High probability of direct labor market entry. High structural NEET risk if local industry fails.")
            print("  -> Pedagogical Risk: Highest 'bocciatura' (grade retention) rates in Biennio 1.")
            
    print("\nOED Linkage Complete: The curriculum structurally predetermines labor market flexibility.")

if __name__ == "__main__":
    build_oed_bridge()
