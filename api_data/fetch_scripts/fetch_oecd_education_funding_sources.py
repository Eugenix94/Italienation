import requests
import pandas as pd
from io import StringIO

# OECD SDMX API URL for education funding sources and flows
data_url = "https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_FIN_SOURCE_GV_PR_NDOM,3.1/..ISCED11_1T8._T+S13+S1D_NON_EDU+S2.INST_EDU..Q+_Z.USD_PPP+PT_EXP+PT_B1GQ.?startPeriod=2015&endPeriod=2023&dimensionAtObservation=AllDimensions"

headers = {"Accept": "text/csv"}
response = requests.get(data_url, headers=headers)

if response.status_code == 200:
    df = pd.read_csv(StringIO(response.text))
    print(df.head())
    df.to_csv("oecd_education_funding_sources.csv", index=False)
    print("Data saved to oecd_education_funding_sources.csv")
else:
    print(f"Failed to fetch data: {response.status_code}")
