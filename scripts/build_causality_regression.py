import pandas as pd
import numpy as np
import statsmodels.api as sm
from pathlib import Path
import json

PROCESSED_DATA = Path('processed_data')

print("--- 1. Loading Socio-Economic Matrix ---")
df = pd.read_csv(PROCESSED_DATA / 'socioeconomic_context_matrix.csv')

print("--- 2. OLS Regression: NEET vs Decay, Income Tax, Black Labour ---")
# Prepare variables for regression
# NEET_Rate = alpha + beta1 * Structural_Decay_Index + beta2 * IRPEF_Taxable_Income_Per_Capita + beta3 * Black_Labour_Rate
X = df[['Structural_Decay_Index', 'IRPEF_Taxable_Income_Per_Capita', 'Black_Labour_Rate']]
X = sm.add_constant(X)
y = df['NEET_Rate']

model = sm.OLS(y, X).fit()
print(model.summary())

# Extract coefficients
results = {
    'R_squared': round(model.rsquared, 3),
    'Adj_R_squared': round(model.rsquared_adj, 3),
    'P_values': {
        'Structural_Decay': round(model.pvalues['Structural_Decay_Index'], 4),
        'IRPEF_Taxable_Income': round(model.pvalues['IRPEF_Taxable_Income_Per_Capita'], 4),
        'Black_Labour_Rate': round(model.pvalues['Black_Labour_Rate'], 4)
    },
    'Coefficients': {
        'Structural_Decay': round(model.params['Structural_Decay_Index'], 4),
        'IRPEF_Taxable_Income': round(model.params['IRPEF_Taxable_Income_Per_Capita'], 4),
        'Black_Labour_Rate': round(model.params['Black_Labour_Rate'], 4)
    }
}

# Save regression results
with open(PROCESSED_DATA / 'causality_regression_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("Saved socioeconomic regression results to processed_data/causality_regression_results.json")
