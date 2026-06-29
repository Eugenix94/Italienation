import requests

BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"
url = f"{BASE_URL}/demo_pjan?format=SDMX-CSV&geo=IT&startPeriod=2010"
r = requests.get(url, timeout=30)
print(f"demo_pjan: {r.status_code}")
