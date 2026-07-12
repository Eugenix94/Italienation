import requests
import pandas as pd
from io import StringIO

data_url = "https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_LSO_EA@DF_LSO_NEAC_DISTR_EA_MIGR,1.0/AUS+AUT+BEL+CAN+CHL+COL+CRI+CZE+EST+FRA+DEU+GRC+HUN+IRL+ISR+ITA+LVA+LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+GBR+USA+OECD+BGR+ROU._T.Y25T64.ISCED11A_0T2+ISCED11A_3_4+ISCED11A_5T8....FB+NB._Z+_T.....OBS...A3?startPeriod=2020&endPeriod=2023&lastNObservations=1&dimensionAtObservation=AllDimensions"
headers = {"Accept": "text/csv"}
response = requests.get(data_url, headers=headers)
if response.status_code == 200:
    df = pd.read_csv(StringIO(response.text))
    print(df.head())
    df.to_csv("oecd_education_attainment_migration.csv", index=False)
    print("Data saved to oecd_education_attainment_migration.csv")
else:
    print(f"Failed to fetch data: {response.status_code}")
