import urllib.request
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import nbformat as nbf

# Configure Matplotlib
plt.style.use('dark_background')
plt.rcParams['font.sans-serif'] = ['Inter', 'Outfit', 'Arial', 'Helvetica']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.color'] = '#f8fafc'
plt.rcParams['axes.labelcolor'] = '#94a3b8'
plt.rcParams['axes.edgecolor'] = '#334155'
plt.rcParams['xtick.color'] = '#94a3b8'
plt.rcParams['ytick.color'] = '#94a3b8'
plt.rcParams['figure.facecolor'] = '#0b1121'
plt.rcParams['axes.facecolor'] = '#0b1121'
plt.rcParams['grid.color'] = '#1e293b'

def add_provenance(ax, source_text):
    plt.figtext(0.99, 0.01, f"Data Provenance: {source_text} | Open Data API", 
                ha='right', va='bottom', fontsize=9, color='#64748b', fontname='Inter', fontweight='bold')

def fetch_worldbank_data():
    print("Fetching WorldBank API Data...")
    # GDP per capita (current US$)
    url_gdp = 'https://api.worldbank.org/v2/country/ITA;FRA;DEU;EUU/indicator/NY.GDP.PCAP.CD?format=json&per_page=500&date=1995:2023'
    # Net migration
    url_mig = 'https://api.worldbank.org/v2/country/ITA;FRA;DEU/indicator/SM.POP.NETM?format=json&per_page=500&date=1995:2023'
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Fetch GDP
    req_gdp = urllib.request.Request(url_gdp, headers=headers)
    with urllib.request.urlopen(req_gdp) as res:
        gdp_data = json.loads(res.read().decode())[1]
    
    df_gdp = pd.DataFrame(gdp_data)
    df_gdp['country_id'] = df_gdp['country'].apply(lambda x: x['id'])
    df_gdp = df_gdp[['country_id', 'date', 'value']].rename(columns={'value': 'GDP_Per_Capita'})
    
    # Fetch Migration
    req_mig = urllib.request.Request(url_mig, headers=headers)
    with urllib.request.urlopen(req_mig) as res:
        mig_data = json.loads(res.read().decode())[1]
    
    df_mig = pd.DataFrame(mig_data)
    df_mig['country_id'] = df_mig['country'].apply(lambda x: x['id'])
    df_mig = df_mig[['country_id', 'date', 'value']].rename(columns={'value': 'Net_Migration'})
    
    # Merge
    df = pd.merge(df_gdp, df_mig, on=['country_id', 'date'], how='outer')
    df['date'] = df['date'].astype(int)
    df = df.sort_values(['country_id', 'date'])
    
    Path('local_data/processed').mkdir(parents=True, exist_ok=True)
    df.to_csv('local_data/processed/api_worldbank_gdp_migration.csv', index=False)
    return df

def generate_gdp_chart(df):
    fig, ax = plt.subplots(figsize=(12, 7))
    colors = {'IT': '#ef4444', 'FR': '#3b82f6', 'DE': '#10b981', 'EU': '#8b5cf6'}
    
    for c in ['IT', 'FR', 'DE', 'EU']:
        d = df[df['country_id'] == c].dropna(subset=['GDP_Per_Capita'])
        label = {'IT': 'Italy', 'FR': 'France', 'DE': 'Germany', 'EU': 'EU Average'}[c]
        linewidth = 4 if c == 'IT' else 2
        alpha = 1.0 if c == 'IT' else 0.7
        ax.plot(d['date'], d['GDP_Per_Capita'], label=label, color=colors[c], linewidth=linewidth, alpha=alpha, marker='o', markersize=4)
        
    ax.set_title("Historical GDP Per Capita vs EU Core (1995-2023)", fontsize=18, fontweight='black', fontname='Outfit', color='#ffffff', pad=20)
    ax.set_ylabel("GDP Per Capita (USD)", fontsize=12, fontweight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.legend(loc='upper left', frameon=True, facecolor='#1e293b', edgecolor='#334155')
    
    add_provenance(ax, "WorldBank API (NY.GDP.PCAP.CD)")
    plt.tight_layout()
    Path('web/assets/charts').mkdir(parents=True, exist_ok=True)
    plt.savefig('web/assets/charts/macro_gdp_comparative_worldbank.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_migration_chart(df):
    d = df[df['country_id'] == 'IT'].dropna(subset=['Net_Migration'])
    fig, ax = plt.subplots(figsize=(12, 7))
    
    colors = ['#10b981' if x > 0 else '#ef4444' for x in d['Net_Migration']]
    ax.bar(d['date'], d['Net_Migration'], color=colors, edgecolor='#0b1121')
    
    ax.set_title("Italy Net Migration Timeline (Brain Drain vs Influx)", fontsize=18, fontweight='black', fontname='Outfit', color='#ffffff', pad=20)
    ax.set_ylabel("Net Migration (Persons)", fontsize=12, fontweight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.axhline(0, color='#94a3b8', linewidth=1)
    
    add_provenance(ax, "WorldBank API (SM.POP.NETM)")
    plt.tight_layout()
    plt.savefig('web/assets/charts/macro_migration_brain_drain_worldbank.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_jupyter_notebook():
    nb = nbf.v4.new_notebook()
    
    nb.cells = [
        nbf.v4.new_markdown_cell("# 19. Global Historical Context (API Expansion)\n\nThis notebook dynamically fetches historical data from the WorldBank API to contextualize the Italian educational and labor crisis within a global macroeconomic framework."),
        nbf.v4.new_code_cell("import pandas as pd\nimport urllib.request\nimport json\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\n# The data has been fetched via the build_global_historical_notebook.py script\ndf = pd.read_csv('../../local_data/processed/api_worldbank_gdp_migration.csv')\ndf.head()"),
        nbf.v4.new_markdown_cell("## 1. The Stagnation Point\nIf we track GDP per capita, we can pinpoint exactly when Italy's trajectory decoupled from the European core (France, Germany) and began its structural decline. This corresponds directly with wage stagnation and the lack of a minimum wage framework."),
        nbf.v4.new_code_cell("df_gdp = df.pivot(index='date', columns='country_id', values='GDP_Per_Capita')\ndf_gdp.plot(figsize=(12, 6), linewidth=2, title='GDP Per Capita (Italy vs EU Core)')\nplt.ylabel('Current USD')\nplt.grid(True)\nplt.show()"),
        nbf.v4.new_markdown_cell("## 2. The Brain Drain Correlation\nAs wages stagnate and the educational system rigidly tracks students into unprotected labor markets, we observe severe shifts in Net Migration (The Brain Drain)."),
        nbf.v4.new_code_cell("df_mig = df[df['country_id'] == 'IT'][['date', 'Net_Migration']].set_index('date')\ndf_mig.plot(kind='bar', figsize=(12, 6), color=['red' if x < 0 else 'green' for x in df_mig['Net_Migration']], title='Italy Net Migration')\nplt.show()")
    ]
    
    Path('archive/notebooks_legacy').mkdir(parents=True, exist_ok=True)
    with open('archive/notebooks_legacy/19_global_historical_context.ipynb', 'w') as f:
        nbf.write(nb, f)

if __name__ == '__main__':
    df = fetch_worldbank_data()
    generate_gdp_chart(df)
    generate_migration_chart(df)
    generate_jupyter_notebook()
    print("Global Historical Pipeline Executed Successfully.")
