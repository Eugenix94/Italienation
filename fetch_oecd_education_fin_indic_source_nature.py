import requests
import pandas as pd
from io import StringIO

data_url = "https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_FIN_INDIC_SOURCE_NATURE,3.1/.EXP.ISCED11_1T8+ISCED11_1T4+ISCED11_5T8.S13.INST_EDU.DIR_EXP.V.XDC.SOURCE?startPeriod=2022&endPeriod=2022&dimensionAtObservation=AllDimensions"
headers = {"Accept": "text/csv"}
response = requests.get(data_url, headers=headers)
if response.status_code == 200:
    df = pd.read_csv(StringIO(response.text))
    print(df.head())
    df.to_csv("oecd_education_fin_indic_source_nature.csv", index=False)
    print("Data saved to oecd_education_fin_indic_source_nature.csv")
else:
    print(f"Failed to fetch data: {response.status_code}")
