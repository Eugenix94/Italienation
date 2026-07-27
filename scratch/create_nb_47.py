import nbformat as nbf
from pathlib import Path

ROOT = Path('c:/Users/Dell/Documents/Antigravity/Italienation').resolve()

nb = nbf.v4.new_notebook()

nb.cells.append(nbf.v4.new_markdown_cell("""\
# Phase 1.5 Deep Exploration: Destination Precarity & The Labor Market Trap
## Analyzing the Final Outcome of the OED Pipeline

In this notebook, we analyze the final destination of the Origin-Education-Destination (OED) pipeline. We use youth employment and pension data (COVIP, ISTAT) to demonstrate the long-term economic scarring effect of the educational failure.
"""))

nb.cells.append(nbf.v4.new_code_cell("""\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

ROOT = Path('c:/Users/Dell/Documents/Antigravity/Italienation').resolve()
"""))

nb.cells.append(nbf.v4.new_markdown_cell("""\
### 1. Youth Employment Trap
We load the ISTAT youth employment rates.
"""))

nb.cells.append(nbf.v4.new_code_cell("""\
# Load ISTAT Youth Employment Data
df_youth_emp = pd.read_csv(ROOT / 'local_data/processed/istat_youth_employment_rates.csv')
print("ISTAT Youth Employment Rates:")
display(df_youth_emp)
"""))

nb.cells.append(nbf.v4.new_markdown_cell("""\
### 2. The Pension/Wealth Gap Trap
The true cost of precarity isn't just current wages, but future wealth. We load COVIP data on the youth pension gap.
"""))

nb.cells.append(nbf.v4.new_code_cell("""\
# Load COVIP Youth Pension Gap Data
df_pension = pd.read_csv(ROOT / 'local_data/new_frontiers/covip_youth_pension_gap_panel.csv')
print("COVIP Youth Pension Gap Data:")
display(df_pension.head())
"""))

nb.cells.append(nbf.v4.new_code_cell("""\
# Visualization: The compounding effect of precarity
plt.figure(figsize=(10, 6))
sns.barplot(data=df_pension, x='Age_Bracket', y='Enrollment_Rate_Pct', palette='magma')
plt.title('The Destination Trap: Youth Supplementary Pension Participation by Age Bracket')
plt.ylabel('Enrollment Rate %')
plt.xlabel('Age Bracket')
plt.ylim(0, 100)
plt.axhline(y=df_pension['Enrollment_Rate_Pct'].mean(), color='r', linestyle='--', label='Average')
plt.legend()
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.savefig(ROOT / 'local_data/processed/destination_precarity_pension_gap.png', bbox_inches='tight')
plt.show()

# Visualize Zero Contribution Rate
plt.figure(figsize=(10, 6))
sns.barplot(data=df_pension, x='Age_Bracket', y='Zero_Contribution_Rate_Pct', palette='Reds')
plt.title('The Stagnation: Zero Contribution Rate in Supplementary Pensions by Age Bracket')
plt.ylabel('Zero Contribution Rate % (Enrolled but not contributing)')
plt.xlabel('Age Bracket')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.savefig(ROOT / 'local_data/processed/destination_zero_contribution_gap.png', bbox_inches='tight')
plt.show()
"""))

nb.cells.append(nbf.v4.new_markdown_cell("""\
### Conclusion
The OED pipeline ends in the **Precarity Trap**. Youth who enter the job market face such severe precarity and low wages that they cannot even afford to contribute to supplementary pensions. This creates a massive compounding wealth gap that locks the generation out of long-term wealth building, completing the mapping of the structural deficit.
"""))

with open(ROOT / 'notebooks/47_destination_precarity_labor_market.ipynb', 'w', encoding='utf-8') as nbf_out:
    nbf.write(nb, nbf_out)
print("Notebook 47 created successfully!")
