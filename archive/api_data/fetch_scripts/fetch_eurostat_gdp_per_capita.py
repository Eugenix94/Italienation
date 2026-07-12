import requests
import pandas as pd
from io import StringIO

# Eurostat SDMX API endpoint for regional GDP per capita and related indices
data_url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/tec00114?format=SDMX-CSV"

# Fetch the CSV file from Eurostat
response = requests.get(data_url)
if response.status_code != 200:
    raise Exception(f"Failed to fetch data: {response.status_code}")

# Read the CSV directly from the response
try:
    df = pd.read_csv(StringIO(response.text))
except Exception as e:
    print("Error reading CSV from response. Saving raw response for inspection.")
    with open("api_data/eurostat_gdp_per_capita_raw.txt", "w", encoding="utf-8") as f:
        f.write(response.text)
    raise e

# Save the DataFrame to a new CSV file in api_data
df.to_csv("api_data/eurostat_gdp_per_capita.csv", index=False)
print("Eurostat regional GDP per capita data imported as api_data/eurostat_gdp_per_capita.csv")
