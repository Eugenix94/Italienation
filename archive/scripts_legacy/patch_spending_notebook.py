"""Rebuild the front section of education_spending_outcomes.ipynb.

The notebook had drifted into a half-patched state with duplicated placeholder
cells and misordered sections. This script rewrites the first analytical block
so it consistently uses real data for:
    - total/state/parent education expenditure
    - expenditure as % of GDP
    - Italy trend over time
    - NEET rates
    - Human Capital Index
    - Gini index
"""

import json
from pathlib import Path

NB_PATH = Path(__file__).resolve().parents[1] / "Notebooks" / "education_spending_outcomes.ipynb"

# ---------------------------------------------------------------------------
# Replacement cell sources
# ---------------------------------------------------------------------------

SECTION_1_MD = [
    "## 1. Education Spending: State, Parents, and GDP Burden\n",
    "Data: OECD funding-source accounts for all education levels (ISCED11_1T8), latest year and Italy trend."
]

SECTION_1B_MD = [
    "## 1b. Italy Trend: State vs Parents and GDP Burden\n",
    "Data: OECD funding sources, 2015-2022."
]

SECTION_2_MD = [
    "## 2. NEET Rates (latest available, % of youth 15-29)\n",
    "Data: Eurostat, wstatus=NEMP from the NEET by migration panel."
]

SECTION_3_MD = [
    "## 3. Human Capital Index (HCI, 2020)\n",
    "Data: World Bank. Scale 0-1."
]

SECTION_4_MD = [
    "## 4. Gini Index (latest available)\n",
    "Data: World Bank WDI. Scale 0-100."
]

IMPORT_SOURCE = [
    "# Import required libraries\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import numpy as np"
]

SPENDING_SOURCE = [
    "from pathlib import Path\n",
    "\n",
    "ROOT = Path.cwd()\n",
    "if not (ROOT / 'local_data').exists():\n",
    "    ROOT = (ROOT / '..').resolve()\n",
    "if not (ROOT / 'local_data').exists():\n",
    "    raise FileNotFoundError('Could not resolve repository root containing local_data/')\n",
    "ORDER = ['Italy', 'UK', 'Germany', 'Spain', 'Greece']\n",
    "\n",
    "exp_latest = pd.read_csv(ROOT / 'local_data/processed/education_expenditure_state_parents_gdp_latest.csv')\n",
    "spending_data = (\n",
    "    exp_latest[[\n",
    "        'Country',\n",
    "        'TIME_PERIOD',\n",
    "        'state_usd_ppp',\n",
    "        'parents_private_usd_ppp',\n",
    "        'total_usd_ppp',\n",
    "        'state_pct_gdp',\n",
    "        'parents_private_pct_gdp',\n",
    "        'total_pct_gdp',\n",
    "        'state_share_of_total_pct',\n",
    "        'parents_private_share_of_total_pct',\n",
    "    ]]\n",
    "    .set_index('Country')\n",
    "    .loc[ORDER]\n",
    "    .reset_index()\n",
    ")\n",
    "for col in ['state_usd_ppp', 'parents_private_usd_ppp', 'total_usd_ppp']:\n",
    "    spending_data[col] = spending_data[col] / 1000.0\n",
    "\n",
    "spending_data = spending_data.rename(columns={\n",
    "    'TIME_PERIOD': 'Year',\n",
    "    'state_usd_ppp': 'State_Funding_USD_PPP_Bn',\n",
    "    'parents_private_usd_ppp': 'Parents_Private_USD_PPP_Bn',\n",
    "    'total_usd_ppp': 'Total_USD_PPP_Bn',\n",
    "    'state_pct_gdp': 'State_pct_GDP',\n",
    "    'parents_private_pct_gdp': 'Parents_Private_pct_GDP',\n",
    "    'total_pct_gdp': 'Total_pct_GDP',\n",
    "    'state_share_of_total_pct': 'State_share_pct',\n",
    "    'parents_private_share_of_total_pct': 'Parents_Private_share_pct',\n",
    "})\n",
    "\n",
    "print('Source: OECD funding sources, ISCED11_1T8, destination=INST_EDU, direct expenditure')\n",
    "print('Interpretation: S13 = state/public, S1D_NON_EDU = parents/private, _T = total')\n",
    "spending_data",
]

SPENDING_CHART_SOURCE = [
    "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
    "\n",
    "spending_data.set_index('Country')[['State_Funding_USD_PPP_Bn', 'Parents_Private_USD_PPP_Bn']].plot(\n",
    "    kind='bar', stacked=True, ax=axes[0], color=['#4C78A8', '#F58518']\n",
    ")\n",
    "axes[0].set_title('Education Funding by Source (2022, USD PPP billions)')\n",
    "axes[0].set_ylabel('USD PPP billions')\n",
    "axes[0].set_xlabel('')\n",
    "axes[0].tick_params(axis='x', rotation=20)\n",
    "\n",
    "spending_data.set_index('Country')[['State_pct_GDP', 'Parents_Private_pct_GDP']].plot(\n",
    "    kind='bar', stacked=True, ax=axes[1], color=['#4C78A8', '#F58518']\n",
    ")\n",
    "axes[1].set_title('Education Expenditure as % of GDP (2022)')\n",
    "axes[1].set_ylabel('% of GDP')\n",
    "axes[1].set_xlabel('')\n",
    "axes[1].tick_params(axis='x', rotation=20)\n",
    "plt.tight_layout()\n",
    "plt.show()",
]

ITALY_TREND_SOURCE = [
    "trend_it = pd.read_csv(ROOT / 'local_data/processed/italy_education_expenditure_state_parents_trend.csv')\n",
    "trend_it = trend_it.sort_values('TIME_PERIOD')\n",
    "\n",
    "plt.figure(figsize=(9, 5))\n",
    "plt.plot(trend_it['TIME_PERIOD'], trend_it['state_pct_gdp'], marker='o', label='State (% GDP)')\n",
    "plt.plot(trend_it['TIME_PERIOD'], trend_it['parents_private_pct_gdp'], marker='o', label='Parents/Private (% GDP)')\n",
    "plt.plot(trend_it['TIME_PERIOD'], trend_it['total_pct_gdp'], marker='o', linewidth=2, label='Total (% GDP)')\n",
    "plt.title('Italy Education Expenditure Burden vs GDP (2015-2022)')\n",
    "plt.xlabel('Year')\n",
    "plt.ylabel('% of GDP')\n",
    "plt.grid(alpha=0.3)\n",
    "plt.legend()\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "trend_it[['TIME_PERIOD', 'state_pct_gdp', 'parents_private_pct_gdp', 'total_pct_gdp',\n",
    "          'state_share_of_total_pct', 'parents_private_share_of_total_pct']]",
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
    "    .loc[ORDER]\n",
    "    .reset_index()\n",
    ")\n",
    "print('Source: Eurostat eurostat_neet_by_migration.csv')\n",
    "print('Metric: % of 15-29 not employed and not in education/training (wstatus=NEMP)')\n",
    "print('Note: UK data available to 2019 only (post-Brexit Eurostat coverage).')\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(8, 5))\n",
    "ax.bar(neet_data['Country'], neet_data['NEET_Rate'], color='#E45756')\n",
    "ax.set_title('NEET Rate: latest available by country')\n",
    "ax.set_ylabel('% of youth 15-29')\n",
    "ax.set_xlabel('')\n",
    "for idx, row in neet_data.iterrows():\n",
    "    ax.text(idx, row['NEET_Rate'] + 0.3, str(int(row['Year'])), ha='center', fontsize=9)\n",
    "plt.xticks(rotation=20)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "neet_data",
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
    "fig, ax = plt.subplots(figsize=(8, 5))\n",
    "ax.bar(hci_data['Country'], hci_data['HCI'], color='#54A24B')\n",
    "ax.set_title('Human Capital Index (2020)')\n",
    "ax.set_ylabel('HCI (0-1)')\n",
    "ax.set_xlabel('')\n",
    "plt.xticks(rotation=20)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "hci_data",
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
    "fig, ax = plt.subplots(figsize=(8, 5))\n",
    "ax.bar(gini_data['Country'], gini_data['Gini'], color='#B279A2')\n",
    "ax.set_title('Gini Index: latest available year by country')\n",
    "ax.set_ylabel('Gini (0-100)')\n",
    "ax.set_xlabel('')\n",
    "for idx, row in gini_data.iterrows():\n",
    "    ax.text(idx, row['Gini'] + 0.15, str(int(row['Year'])), ha='center', fontsize=9)\n",
    "plt.xticks(rotation=20)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "gini_data",
]

def make_cell(cell_type: str, source: list[str], cell_id: str, language: str | None = None) -> dict:
    metadata = {}
    if language is not None:
        metadata["language"] = language
    cell = {
        "cell_type": cell_type,
        "id": cell_id,
        "metadata": metadata,
        "source": source,
    }
    if cell_type == "code":
        cell["outputs"] = []
        cell["execution_count"] = None
    return cell


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding="utf-8"))

    tail = nb["cells"][13:]
    rebuilt_front = [
        nb["cells"][0],
        make_cell("code", IMPORT_SOURCE, "#VSC-imports", "python"),
        make_cell("markdown", SECTION_1_MD, "#VSC-sec-1", "markdown"),
        make_cell("code", SPENDING_SOURCE, "#VSC-code-spend-table", "python"),
        make_cell("code", SPENDING_CHART_SOURCE, "#VSC-code-spend-charts", "python"),
        make_cell("markdown", SECTION_1B_MD, "#VSC-sec-1b", "markdown"),
        make_cell("code", ITALY_TREND_SOURCE, "#VSC-code-italy-trend", "python"),
        make_cell("markdown", SECTION_2_MD, "#VSC-sec-2", "markdown"),
        make_cell("code", NEET_SOURCE, "#VSC-code-neet", "python"),
        make_cell("markdown", SECTION_3_MD, "#VSC-sec-3", "markdown"),
        make_cell("code", HCI_SOURCE, "#VSC-code-hci", "python"),
        make_cell("markdown", SECTION_4_MD, "#VSC-sec-4", "markdown"),
        make_cell("code", GINI_SOURCE, "#VSC-code-gini", "python"),
    ]
    nb["cells"] = rebuilt_front + tail

    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved: {NB_PATH}")
    print(f"Rebuilt front section with {len(rebuilt_front)} cells; preserved tail with {len(tail)} cells.")


if __name__ == "__main__":
    main()
