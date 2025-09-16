import requests
import pandas as pd
from io import StringIO

# OECD SDMX API URL for education capital and costs
data_url = "https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_FIN_NATURE_STAFF,3.1/..ISCED11_1T8..INST_EDU_PUB+INST_EDU_PRIV_GOV.CUR_LC+CUR_RET+CUR_NLC.Q.USD_PPP.?startPeriod=2015&endPeriod=2023&dimensionAtObservation=AllDimensions"

headers = {"Accept": "text/csv"}
response = requests.get(data_url, headers=headers)

if response.status_code == 200:
    df = pd.read_csv(StringIO(response.text))
    print(df.head())
    df.to_csv("oecd_education_costs.csv", index=False)
    print("Data saved to oecd_education_costs.csv")
else:
    print(f"Failed to fetch data: {response.status_code}")
