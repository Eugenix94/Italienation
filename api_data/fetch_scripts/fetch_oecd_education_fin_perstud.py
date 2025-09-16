import requests
import pandas as pd
from io import StringIO

data_url = "https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_INDIC_FIN_PERSTUD,3.1/..ISCED11_1+ISCED11_2+ISCED11_3+ISCED11_34+ISCED11_35+ISCED11_4+ISCED11_5+ISCED11_5T8+ISCED11_6T8+ISCED11_1T8._T.INST_EDU.DIR_EXP.V+_Z.USD_PPP_ST+PT_B1GQ_POP.?startPeriod=2022&endPeriod=2022&dimensionAtObservation=AllDimensions"
headers = {"Accept": "text/csv"}
response = requests.get(data_url, headers=headers)
if response.status_code == 200:
    df = pd.read_csv(StringIO(response.text))
    print(df.head())
    df.to_csv("oecd_education_fin_perstud.csv", index=False)
    print("Data saved to oecd_education_fin_perstud.csv")
else:
    print(f"Failed to fetch data: {response.status_code}")
