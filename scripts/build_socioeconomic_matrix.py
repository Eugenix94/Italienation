import pandas as pd
from pathlib import Path

LOCAL_DATA = Path('local_data')
PROCESSED_DATA = Path('processed_data')

# 1. Load Holistic Decay
df_decay = pd.read_csv(PROCESSED_DATA / 'holistic_educational_decay_index.csv')

# 2. Load Eurostat GDP
nuts2_to_regione = {
    'ITC1': 'PIEMONTE', 'ITC2': "VALLE D'AOSTA", 'ITC3': 'LIGURIA', 'ITC4': 'LOMBARDIA',
    'ITF1': 'ABRUZZO', 'ITF2': 'MOLISE', 'ITF3': 'CAMPANIA', 'ITF4': 'PUGLIA',
    'ITF5': 'BASILICATA', 'ITF6': 'CALABRIA', 'ITG1': 'SICILIA', 'ITG2': 'SARDEGNA',
    'ITH1': 'TRENTINO-ALTO ADIGE', 'ITH2': 'TRENTINO-ALTO ADIGE', 
    'ITH3': 'VENETO', 'ITH4': 'FRIULI-VENEZIA GIULIA', 'ITH5': 'EMILIA-ROMAGNA',
    'ITI1': 'TOSCANA', 'ITI2': 'UMBRIA', 'ITI3': 'MARCHE', 'ITI4': 'LAZIO'
}
df_gdp = pd.read_csv(LOCAL_DATA / 'eurostat' / 'eurostat_it_regional_gdp_nuts2.csv')
df_gdp = df_gdp[(df_gdp['TIME_PERIOD'] == 2022) & (df_gdp['unit'] == 'EUR_HAB')]
df_gdp = df_gdp[df_gdp['geo'].str.len() == 4]
df_gdp['Regione'] = df_gdp['geo'].map(nuts2_to_regione)
gdp_reg = df_gdp.groupby('Regione')['OBS_VALUE'].mean().reset_index()
gdp_reg.rename(columns={'OBS_VALUE': 'GDP_Per_Capita'}, inplace=True)

# 3. Load MEF IRPEF Data
mef_map = {
    'Piemonte': 'PIEMONTE', "Valle d'Aosta": "VALLE D'AOSTA", 'Lombardia': 'LOMBARDIA', 
    'Liguria': 'LIGURIA', 'Trentino Alto Adige(P.A.Trento)': 'TRENTINO-ALTO ADIGE', 
    'Trentino Alto Adige(P.A.Bolzano)': 'TRENTINO-ALTO ADIGE', 'Veneto': 'VENETO', 
    'Friuli Venezia Giulia': 'FRIULI-VENEZIA GIULIA', 'Emilia Romagna': 'EMILIA-ROMAGNA', 
    'Toscana': 'TOSCANA', 'Umbria': 'UMBRIA', 'Marche': 'MARCHE', 'Lazio': 'LAZIO', 
    'Abruzzo': 'ABRUZZO', 'Molise': 'MOLISE', 'Campania': 'CAMPANIA', 'Puglia': 'PUGLIA', 
    'Basilicata': 'BASILICATA', 'Calabria': 'CALABRIA', 'Sicilia': 'SICILIA', 'Sardegna': 'SARDEGNA'
}
df_mef = pd.read_csv(LOCAL_DATA / 'MEF' / 'irpef_open_data' / 'mef_reg_calcolo_irpef_2025.csv', sep=';')
df_mef = df_mef[df_mef['Regione'] != 'Mancante/errata']
df_mef['Regione_Standard'] = df_mef['Regione'].map(mef_map)

# Aggregate MEF by Region
cols_to_clean = ['Numero contribuenti', 'Reddito imponibile - Ammontare in euro']
for col in cols_to_clean:
    df_mef[col] = df_mef[col].astype(str).str.replace('.', '', regex=False).astype(float)

mef_agg = df_mef.groupby('Regione_Standard').agg({
    'Numero contribuenti': 'sum',
    'Reddito imponibile - Ammontare in euro': 'sum'
}).reset_index()

# Note: MEF values in 'Ammontare in euro' are expressed in euro
mef_agg['IRPEF_Taxable_Income_Per_Capita'] = mef_agg['Reddito imponibile - Ammontare in euro'] / mef_agg['Numero contribuenti']
mef_agg.rename(columns={'Regione_Standard': 'Regione'}, inplace=True)

# 4. Merge all together
df_matrix = pd.merge(df_decay, gdp_reg, on='Regione', how='inner')
df_matrix = pd.merge(df_matrix, mef_agg[['Regione', 'IRPEF_Taxable_Income_Per_Capita']], on='Regione', how='inner')

# Calculate Evasion Proxy
df_matrix['Evasion_Proxy_Index'] = df_matrix['GDP_Per_Capita'] - df_matrix['IRPEF_Taxable_Income_Per_Capita']

# 5. Load INPS Lavoro Nero data and map to Regions
# Macro Areas mapping:
region_to_macro = {
    'PIEMONTE': 'Nord ovest', "VALLE D'AOSTA": 'Nord ovest', 'LIGURIA': 'Nord ovest', 'LOMBARDIA': 'Nord ovest',
    'TRENTINO-ALTO ADIGE': 'Nord est', 'VENETO': 'Nord est', 'FRIULI-VENEZIA GIULIA': 'Nord est', 'EMILIA-ROMAGNA': 'Nord est',
    'TOSCANA': 'Centro', 'UMBRIA': 'Centro', 'MARCHE': 'Centro', 'LAZIO': 'Centro',
    'ABRUZZO': 'Sud e isole', 'MOLISE': 'Sud e isole', 'CAMPANIA': 'Sud e isole', 'PUGLIA': 'Sud e isole',
    'BASILICATA': 'Sud e isole', 'CALABRIA': 'Sud e isole', 'SICILIA': 'Sud e isole', 'SARDEGNA': 'Sud e isole'
}

df_inps = pd.read_csv(LOCAL_DATA / 'INPS' / 'destination' / 'lavoratori-in-nero-e-irregolari-distribuzione-per-area-geografica--attivit_-2013__1.csv', sep=';')
df_inps.rename(columns={'Percentuale lavoratori in nero e irregolari': 'Black_Labour_Rate', 'Area geografica': 'Macro_Area'}, inplace=True)

df_matrix['Macro_Area'] = df_matrix['Regione'].map(region_to_macro)
# Merge INPS
df_matrix = pd.merge(df_matrix, df_inps[['Macro_Area', 'Black_Labour_Rate']], on='Macro_Area', how='left')

# Convert Black_Labour_Rate string percentage to float
df_matrix['Black_Labour_Rate'] = df_matrix['Black_Labour_Rate'].astype(str).str.replace(',', '.').str.replace('%', '').astype(float)

df_matrix.to_csv(PROCESSED_DATA / 'socioeconomic_context_matrix.csv', index=False)
print("Saved matrix to processed_data/socioeconomic_context_matrix.csv")
print(df_matrix[['Regione', 'NEET_Rate', 'GDP_Per_Capita', 'IRPEF_Taxable_Income_Per_Capita', 'Black_Labour_Rate']].head())
