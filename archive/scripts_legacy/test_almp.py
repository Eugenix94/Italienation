import requests

# Let's test all ALMP datasets for Italy
BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"
codes = ['lmp_ind_exp', 'lmp_ind_actp', 'lmp_expend', 'lmp_expsumm', 'lmp_partme', 'lmp_partsumm']

for code in codes:
    url = f"{BASE_URL}/{code}?format=SDMX-CSV&geo=IT&startPeriod=2010"
    r = requests.get(url, timeout=30)
    print(f"{code}: {r.status_code}")
    if r.status_code == 200:
        print(f"  Rows: {len(r.text.splitlines())}")
