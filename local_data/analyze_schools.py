import pandas as pd

path = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\MinIstruzione\Scuole\SCUANAGRAFESTAT20252620250901.csv"
df = pd.read_csv(path, sep=',', dtype=str, on_bad_lines='skip')

# Filter out elementary/middle schools
# Scuole dell'infanzia, primaria, primo grado, and ICs are not upper secondary.
exclude = ['SCUOLA INFANZIA', 'SCUOLA PRIMARIA', 'SCUOLA PRIMO GRADO', 'ISTITUTO COMPRENSIVO', 'CENTRO TERRITORIALE', 'DIREZ. DIDATTICA']

upper = df[~df['DESCRIZIONETIPOLOGIAGRADOISTRUZIONESCUOLA'].isin(exclude)]

print(upper['DESCRIZIONETIPOLOGIAGRADOISTRUZIONESCUOLA'].value_counts())
