"""
Patch education_spending_outcomes.ipynb to replace hardcoded placeholder cells
with code that loads real data from CSVs in the local_data/ directory.

Cells replaced (by original index):
  3  - spending_data    (OECD per-student, USD PPP)
  4  - spending chart   (adapts to total-only data)
  6  - neet_data        (Eurostat NEET by migration, wstatus=NEMP, 15-29)
  8  - hci_data         (World Bank HCI 2020)
  10 - gini_data        (World Bank Gini, latest available year)
"""

import json
from pathlib import Path

NB_PATH = Path(__file__).resolve().parents[1] / "Notebooks" / "education_spending_outcomes.ipynb"

# ---------------------------------------------------------------------------
# New cell sources (as lists of lines matching .ipynb convention)
# ---------------------------------------------------------------------------

SPENDING_SOURCE = [
    "import pandas as pd\n",
    "from pathlib import Path\n",
    "\n",
    "ROOT = Path('..').resolve()  # Notebooks/ -> workspace root\n",
    "ORDER = ['Italy', 'UK', 'Germany', 'Spain', 'Greece']\n",
    "COUNTRIES = {'ITA': 'Italy', 'GBR': 'UK', 'DEU': 'Germany', 'ESP': 'Spain', 'GRC': 'Greece'}\n",
    "\n",
    "perstud = pd.read_csv(ROOT / 'local_data/oecd/oecd_education_fin_perstud.csv', low_memory=False)\n",
    "spending_data = (\n",
    "    perstud[\n",
    "        perstud['REF_AREA'].isin(COUNTRIES.keys()) &\n",
    "        (perstud['EDUCATION_LEV'] == 'ISCED11_1T8') &\n",
    "        (perstud['UNIT_MEASURE'] == 'USD_PPP_ST')\n",
    "    ][['REF_AREA', 'OBS_VALUE', 'TIME_PERIOD']]\n",
    "    .assign(Country=lambda d: d['REF_AREA'].map(COUNTRIES))\n",
    "    .rename(columns={'OBS_VALUE': 'Total_per_student_USD_PPP'})\n",
    "    [['Country', 'Total_per_student_USD_PPP', 'TIME_PERIOD']]\n",
    "    .set_index('Country')\n",
    "    .loc[ORDER]\n",
    "    .reset_index()\n",
    ")\n",
    "print(f\"Source: OECD EAG, oecd_education_fin_perstud.csv, year \"\n",
    "      f\"{spending_data['TIME_PERIOD'].iloc[0]}\")\n",
    "print(\"Note: Govt/household expenditure breakdown not available in this dataset; \"\n",
    "      \"total direct expenditure per student (ISCED 1-8, all levels) shown.\")\n",
    "spending_data",
]

SPENDING_CHART_SOURCE = [
    "# Bar chart: Total per-student spending by country\n",
    "spending_data.set_index('Country')[['Total_per_student_USD_PPP']].plot(\n",
    "    kind='bar', figsize=(8, 5), color='steelblue', legend=False)\n",
    "import matplotlib.pyplot as plt\n",
    "plt.title('Total Per-Student Education Spending (2022, USD PPP)\\nSource: OECD EAG')\n",
    "plt.ylabel('USD PPP')\n",
    "plt.xlabel('')\n",
    "plt.xticks(rotation=30, ha='right')\n",
    "plt.tight_layout()\n",
    "plt.show()",
]

NEET_SOURCE = [
    "neet_raw = pd.read_csv(\n",
    "    ROOT / 'local_data/eurostat/eurostat_neet_by_migration.csv', low_memory=False)\n",
    "GEO_MAP = {'IT': 'Italy', 'UK': 'UK', 'DE': 'Germany', 'ES': 'Spain', 'EL': 'Greece'}\n",
    "\n",
    "neet_data = (\n",
    "    neet_raw[\n",
    "        neet_raw['geo'].isin(GEO_MAP.keys()) &\n",
    "        (neet_raw['sex'] == 'T') &\n",
    "        (neet_raw['age'] == 'Y15-29') &\n",
    "        (neet_raw['wstatus'] == 'NEMP')  # not employed + not in education/training\n",
    "    ][['geo', 'TIME_PERIOD', 'OBS_VALUE']]\n",
    "    .dropna()\n",
    "    .sort_values('TIME_PERIOD')\n",
    "    .groupby('geo').last().reset_index()\n",
    "    .assign(Country=lambda d: d['geo'].map(GEO_MAP))\n",
    "    .rename(columns={'OBS_VALUE': 'NEET_Rate', 'TIME_PERIOD': 'Year'})\n",
    "    [['Country', 'NEET_Rate', 'Year']]\n",
    "    .set_index('Country')\n",
    "    .loc[[c for c in ORDER if c in GEO_MAP.values()]]\n",
    "    .reset_index()\n",
    ")\n",
    "print('Source: Eurostat eurostat_neet_by_migration.csv')\n",
    "print('Metric: % of 15-29 not employed and not in education/training (wstatus=NEMP)')\n",
    "print('Note: UK data available to 2019 only (post-Brexit Eurostat coverage).')\n",
    "\n",
    "import plotly.express as px\n",
    "fig = px.bar(\n",
    "    neet_data, x='Country', y='NEET_Rate',\n",
    "    title='NEET Rate — % of youth 15-29 not employed and not in education/training<br>'\n",
    "          '<sup>Source: Eurostat; latest available year per country</sup>',\n",
    "    labels={'NEET_Rate': '% NEET'},\n",
    "    text='Year'\n",
    ")\n",
    "fig.show()",
]

HCI_SOURCE = [
    "hci_raw = pd.read_csv(\n",
    "    ROOT / 'local_data/API_HD.HCI.OVRL_DS63_en_csv_v2_756596.csv',\n",
    "    skiprows=4, low_memory=False)\n",
    "WB_CODES = {'ITA': 'Italy', 'GBR': 'UK', 'DEU': 'Germany', 'ESP': 'Spain', 'GRC': 'Greece'}\n",
    "\n",
    "hci_data = (\n",
    "    hci_raw[hci_raw['Country Code'].isin(WB_CODES.keys())]\n",
    "    [['Country Code', '2020']]\n",
    "    .dropna()\n",
    "    .assign(Country=lambda d: d['Country Code'].map(WB_CODES))\n",
    "    .rename(columns={'2020': 'HCI'})\n",
    "    [['Country', 'HCI']]\n",
    "    .set_index('Country')\n",
    "    .loc[ORDER]\n",
    "    .reset_index()\n",
    ")\n",
    "print('Source: World Bank Human Capital Index 2020 (scale 0-1)')\n",
    "\n",
    "px.bar(\n",
    "    hci_data, x='Country', y='HCI',\n",
    "    title='Human Capital Index (2020, scale 0-1)<br><sup>Source: World Bank</sup>',\n",
    "    labels={'HCI': 'HCI (0-1)'})",
]

GINI_SOURCE = [
    "gini_raw = pd.read_csv(\n",
    "    ROOT / 'local_data/WB_WDI_SI_POV_GINI.csv', low_memory=False)\n",
    "\n",
    "gini_data = (\n",
    "    gini_raw[gini_raw['REF_AREA'].isin(WB_CODES.keys())]\n",
    "    [['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE']]\n",
    "    .dropna()\n",
    "    .sort_values('TIME_PERIOD')\n",
    "    .groupby('REF_AREA').last().reset_index()\n",
    "    .assign(Country=lambda d: d['REF_AREA'].map(WB_CODES))\n",
    "    .rename(columns={'OBS_VALUE': 'Gini', 'TIME_PERIOD': 'Year'})\n",
    "    [['Country', 'Gini', 'Year']]\n",
    "    .set_index('Country')\n",
    "    .loc[ORDER]\n",
    "    .reset_index()\n",
    ")\n",
    "print('Source: World Bank WDI Gini index (latest available year per country)')\n",
    "\n",
    "px.bar(\n",
    "    gini_data, x='Country', y='Gini',\n",
    "    title='Gini Index — Income Inequality<br>'\n",
    "          '<sup>Source: World Bank WDI; latest available year per country</sup>',\n",
    "    labels={'Gini': 'Gini (0-100)'},\n",
    "    text='Year')",
]

# ---------------------------------------------------------------------------
# Apply patches
# ---------------------------------------------------------------------------

CELL_PATCHES = {
    3: SPENDING_SOURCE,
    4: SPENDING_CHART_SOURCE,
    6: NEET_SOURCE,
    8: HCI_SOURCE,
    10: GINI_SOURCE,
}


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding="utf-8"))

    patched = 0
    for idx, new_source in CELL_PATCHES.items():
        cell = nb["cells"][idx]
        assert cell["cell_type"] == "code", f"Cell {idx} is not a code cell"
        cell["source"] = new_source
        cell["outputs"] = []
        cell["execution_count"] = None
        patched += 1
        print(f"  Patched cell {idx}")

    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved: {NB_PATH}")
    print(f"Total cells patched: {patched}")


if __name__ == "__main__":
    main()
