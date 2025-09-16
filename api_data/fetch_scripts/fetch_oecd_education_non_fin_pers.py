import requests
import pandas as pd
from io import StringIO

data_url = "https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_NON_FIN_PERS@DF_UOE_NF_PERS_CLS,1.0/.......A......_T.?startPeriod=2023&endPeriod=2023&dimensionAtObservation=AllDimensions"
headers = {"Accept": "text/csv"}
response = requests.get(data_url, headers=headers)
if response.status_code == 200:
    df = pd.read_csv(StringIO(response.text))
    print(df.head())
    df.to_csv("oecd_education_non_fin_pers.csv", index=False)
    print("Data saved to oecd_education_non_fin_pers.csv")
else:
    print(f"Failed to fetch data: {response.status_code}")
