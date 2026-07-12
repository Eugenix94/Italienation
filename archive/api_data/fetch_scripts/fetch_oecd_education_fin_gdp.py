import requests
import pandas as pd
from io import StringIO

data_url = "https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_INDIC_FIN_GDP,1.0/..ISCED11_1T8._T+S13+S1D_NON_EDU+S2.INST_EDU...?startPeriod=2015&endPeriod=2020&dimensionAtObservation=AllDimensions"
headers = {"Accept": "text/csv"}
response = requests.get(data_url, headers=headers)
if response.status_code == 200:
    df = pd.read_csv(StringIO(response.text))
    print(df.head())
    df.to_csv("oecd_education_fin_gdp.csv", index=False)
    print("Data saved to oecd_education_fin_gdp.csv")
else:
    print(f"Failed to fetch data: {response.status_code}")
