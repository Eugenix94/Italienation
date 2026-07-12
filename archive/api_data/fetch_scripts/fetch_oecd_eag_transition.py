import requests
import pandas as pd
from io import StringIO

# OECD SDMX API endpoint for Education at a Glance transition data
url = "https://sdmx.oecd.org/archive/rest/data/OECD,DF_EAG_TRANS,/all?startPeriod=2995&dimensionAtObservation=AllDimensions"

# Fetch the CSV file directly
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to fetch data: {response.status_code}")

# Try to decode as text and read as CSV
try:
    df = pd.read_csv(StringIO(response.text))
except Exception as e:
    print("Error reading CSV from response. Saving raw response for inspection.")
    with open("api_data/oecd/oecd_eag_transition_raw.txt", "w", encoding="utf-8") as f:
        f.write(response.text)
    raise e

# Save the DataFrame to a new CSV file in api_data
df.to_csv("api_data/oecd/oecd_eag_transition.csv", index=False)
print("OECD Education at a Glance transition data imported as api_data/oecd/oecd_eag_transition.csv")
