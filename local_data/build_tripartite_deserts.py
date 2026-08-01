import pandas as pd
import json
import os

path = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\MinIstruzione\Scuole\SCUANAGRAFESTAT20252620250901.csv"
out_csv = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\processed\tripartite_territorial_deserts.csv"
out_json = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\processed\tripartite_territorial_summary.json"

df = pd.read_csv(path, sep=',', dtype=str, on_bad_lines='skip')

# Extract full list of municipalities in Italy (using all schools)
municipalities = df[['CODICECOMUNESCUOLA', 'DESCRIZIONECOMUNE', 'PROVINCIA', 'REGIONE', 'AREAGEOGRAFICA']].drop_duplicates()

# Map school types to macro-tracks
def get_macro_track(desc):
    desc = str(desc).upper()
    if 'LICEO' in desc or 'MAGISTRALE' in desc or 'EDUCANDATO' in desc:
        return 'Liceo'
    if 'TECNICO' in desc or 'TEC ' in desc or 'GEOMETRI' in desc or 'NAUTICO' in desc or 'AERONAUTICO' in desc:
        return 'Tecnico'
    if 'PROF' in desc or "D'ARTE" in desc:
        return 'Professionale'
    if 'SUPERIORE' in desc or 'CONVITTO' in desc:
        return 'IIS_or_Mixed'
    return 'Other'

df['Macro_Track'] = df['DESCRIZIONETIPOLOGIAGRADOISTRUZIONESCUOLA'].apply(get_macro_track)

# Filter out non-upper-secondary based on our manual inspection
exclude = ['SCUOLA INFANZIA', 'SCUOLA PRIMARIA', 'SCUOLA PRIMO GRADO', 'ISTITUTO COMPRENSIVO', 'CENTRO TERRITORIALE', 'DIREZ. DIDATTICA', 'Other']
upper = df[~df['DESCRIZIONETIPOLOGIAGRADOISTRUZIONESCUOLA'].isin(exclude)]

# Group by Municipality and Track
grouped = upper.groupby(['CODICECOMUNESCUOLA', 'Macro_Track']).size().unstack(fill_value=0).reset_index()

# Ensure all columns exist
for col in ['Liceo', 'Tecnico', 'Professionale', 'IIS_or_Mixed']:
    if col not in grouped.columns:
        grouped[col] = 0

# Merge back to the full list of municipalities
result = pd.merge(municipalities, grouped, on='CODICECOMUNESCUOLA', how='left').fillna(0)

# Convert counts to int
for col in ['Liceo', 'Tecnico', 'Professionale', 'IIS_or_Mixed']:
    result[col] = result[col].astype(int)

# Calculate Flags
result['Has_Upper_Secondary'] = (result['Liceo'] + result['Tecnico'] + result['Professionale'] + result['IIS_or_Mixed']) > 0
result['Is_Total_Desert'] = ~result['Has_Upper_Secondary']

# A Track Monopoly is when a town has EXACTLY ONE track, and NO IIS (which mixes tracks)
# Examples: only Liceo, or only Professionale.
result['Liceo_Only_Monopoly'] = (result['Liceo'] > 0) & (result['Tecnico'] == 0) & (result['Professionale'] == 0) & (result['IIS_or_Mixed'] == 0)
result['Tecnico_Only_Monopoly'] = (result['Liceo'] == 0) & (result['Tecnico'] > 0) & (result['Professionale'] == 0) & (result['IIS_or_Mixed'] == 0)
result['Prof_Only_Monopoly'] = (result['Liceo'] == 0) & (result['Tecnico'] == 0) & (result['Professionale'] > 0) & (result['IIS_or_Mixed'] == 0)

# Save CSV
result.to_csv(out_csv, index=False)

# Build JSON Summary
total_muni = len(result)
total_desert = int(result['Is_Total_Desert'].sum())
liceo_monopoly = int(result['Liceo_Only_Monopoly'].sum())
tecnico_monopoly = int(result['Tecnico_Only_Monopoly'].sum())
prof_monopoly = int(result['Prof_Only_Monopoly'].sum())

summary = {
    "total_municipalities_analyzed": total_muni,
    "total_educational_deserts_no_upper_sec": total_desert,
    "percent_deserts": round((total_desert / total_muni) * 100, 2) if total_muni else 0,
    "track_monopolies": {
        "liceo_only_towns": liceo_monopoly,
        "tecnico_only_towns": tecnico_monopoly,
        "professionale_only_towns": prof_monopoly
    },
    "regional_deserts": result[result['Is_Total_Desert']].groupby('REGIONE').size().to_dict(),
    "regional_liceo_monopolies": result[result['Liceo_Only_Monopoly']].groupby('REGIONE').size().to_dict(),
    "regional_prof_monopolies": result[result['Prof_Only_Monopoly']].groupby('REGIONE').size().to_dict()
}

with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print(f"Analysis complete. Found {total_desert} towns with no upper secondary school.")
print(f"Found {liceo_monopoly} Liceo-only monopolies, and {prof_monopoly} Professionale-only monopolies.")
