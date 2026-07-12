#!/usr/bin/env python3
"""
Process and reconcile SIOPE school expenditure data with Minister school data.

This script:
1. Loads SIOPE school spending data (2020-2026)
2. Loads SIOPE school registry and Minister school registries
3. Reconciles school codes and matches metadata
4. Aggregates expenditure by region, province, school type through years
5. Outputs processed data for analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from collections import defaultdict
import warnings

warnings.filterwarnings('ignore')

# Paths
SIOPE_DIR = Path("local_data/SIOPE")
MINISTER_DIR = Path("local_data/MinIstruzione")
OUTPUT_DIR = Path("local_data/processed")
OUTPUT_DIR.mkdir(exist_ok=True)

def load_siope_data():
    """Load all SIOPE school expenditure data (2020-2026)."""
    print("Loading SIOPE data...")
    dfs = []
    
    for year in range(2020, 2027):
        file = SIOPE_DIR / f"siope_uscite_{year}.csv"
        if file.exists():
            df = pd.read_csv(file, names=['codice_ente', 'anno', 'mese', 'codice_gestionale', 'importo_centesimi'])
            # Convert to numeric, handling any non-numeric values
            df['importo_centesimi'] = pd.to_numeric(df['importo_centesimi'], errors='coerce')
            df['importo_euro'] = df['importo_centesimi'] / 100
            df['anno'] = year  # Ensure anno column
            dfs.append(df)
            print(f"  {year}: {len(df)} rows")
    
    if dfs:
        siope_uscite = pd.concat(dfs, ignore_index=True)
        return siope_uscite
    return pd.DataFrame()

def load_siope_registry():
    """Load SIOPE school registry with metadata."""
    print("Loading SIOPE school registry...")
    registry_file = SIOPE_DIR / "siope_anagrafiche_scuole.csv"
    
    if registry_file.exists():
        df = pd.read_csv(registry_file)
        print(f"  {len(df)} schools")
        return df
    return pd.DataFrame()

def load_minister_schools():
    """Load Minister school registries."""
    print("Loading Minister school registries...")
    schools = []
    
    # Try both static and parametric school registries
    for pattern in ['SCUANAGRAFESTAT*', 'SCUANAGRAFEPAR*']:
        for file in MINISTER_DIR.glob(f"Scuole/{pattern}.csv"):
            try:
                df = pd.read_csv(file)
                print(f"  {file.name}: {len(df)} schools")
                schools.append(df)
            except Exception as e:
                print(f"  Error loading {file.name}: {e}")
    
    if schools:
        return pd.concat(schools, ignore_index=True)
    return pd.DataFrame()

def load_minister_budget():
    """Load Minister budget/finance data."""
    print("Loading Minister budget/finance data...")
    budgets = []
    
    for file in MINISTER_DIR.glob("BilancioeFinanze/*.csv"):
        try:
            df = pd.read_csv(file)
            print(f"  {file.name}: {len(df)} rows")
            budgets.append(df)
        except Exception as e:
            print(f"  Error loading {file.name}: {e}")
    
    if budgets:
        return pd.concat(budgets, ignore_index=True)
    return pd.DataFrame()

def analyze_siope_by_territory(siope_uscite, siope_registry):
    """Aggregate SIOPE expenditure by territory and year."""
    print("Analyzing SIOPE by territory...")
    
    # Merge with registry to get territorial info
    merged = siope_uscite.merge(
        siope_registry[['codice_ente', 'codice_regione', 'codice_provincia', 'codice_comune', 'denominazione']],
        on='codice_ente',
        how='left'
    )
    
    # Group by region, province, year
    by_region_year = merged.groupby(['anno', 'codice_regione']).agg({
        'importo_euro': ['sum', 'mean', 'count'],
        'codice_ente': 'nunique'
    }).round(2)
    
    by_province_year = merged.groupby(['anno', 'codice_provincia']).agg({
        'importo_euro': ['sum', 'mean', 'count'],
        'codice_ente': 'nunique'
    }).round(2)
    
    by_budget_category = merged.groupby(['anno', 'codice_gestionale']).agg({
        'importo_euro': ['sum', 'count', 'mean']
    }).round(2)
    
    return {
        'merged': merged,
        'by_region_year': by_region_year,
        'by_province_year': by_province_year,
        'by_budget_category': by_budget_category
    }

def reconcile_schools(siope_registry, minister_schools):
    """Match SIOPE schools with Minister school data."""
    print("Reconciling school data...")
    
    reconciliation = {
        'siope_total': len(siope_registry),
        'minister_total': len(minister_schools),
        'matches': 0,
        'details': []
    }
    
    # Try to match on codice_ente (if available in Minister data)
    if 'codice_ente' in minister_schools.columns:
        siope_codes = set(siope_registry['codice_ente'].unique())
        minister_codes = set(minister_schools['codice_ente'].unique())
        reconciliation['matches'] = len(siope_codes.intersection(minister_codes))
    
    # Try matching on school name (fuzzy match)
    if 'denominazione' in siope_registry.columns and 'denominazione' in minister_schools.columns:
        siope_names = set(siope_registry['denominazione'].str.lower().unique())
        minister_names = set(minister_schools['denominazione'].str.lower().unique()) if 'denominazione' in minister_schools.columns else set()
        name_matches = len(siope_names.intersection(minister_names))
        reconciliation['name_matches'] = name_matches
    
    print(f"  SIOPE schools: {reconciliation['siope_total']}")
    print(f"  Minister schools: {reconciliation['minister_total']}")
    if reconciliation['matches'] > 0:
        print(f"  Code matches: {reconciliation['matches']}")
    
    return reconciliation

def save_processed_data(siope_analysis, output_dir=OUTPUT_DIR):
    """Save processed data for notebook analysis."""
    print("Saving processed data...")
    
    # Save merged territorial data
    if 'merged' in siope_analysis:
        merged = siope_analysis['merged']
        
        # Expenditure by region and year
        region_year = merged.pivot_table(
            values='importo_euro',
            index='anno',
            columns='codice_regione',
            aggfunc='sum'
        )
        region_year.to_csv(output_dir / "siope_expenditure_by_region_year.csv")
        print(f"  Saved: siope_expenditure_by_region_year.csv")
        
        # School count by region and year
        school_count = merged.pivot_table(
            values='codice_ente',
            index='anno',
            columns='codice_regione',
            aggfunc='nunique'
        )
        school_count.to_csv(output_dir / "siope_school_count_by_region_year.csv")
        print(f"  Saved: siope_school_count_by_region_year.csv")
        
        # Monthly expenditure trends
        monthly_trend = merged.groupby(['anno', 'mese']).agg({
            'importo_euro': ['sum', 'count'],
            'codice_ente': 'nunique'
        })
        monthly_trend.to_csv(output_dir / "siope_monthly_expenditure_trend.csv")
        print(f"  Saved: siope_monthly_expenditure_trend.csv")
        
        # Budget category breakdown
        budget_breakdown = merged.groupby('codice_gestionale').agg({
            'importo_euro': ['sum', 'count', 'mean'],
            'anno': 'nunique'
        }).sort_values(('importo_euro', 'sum'), ascending=False)
        budget_breakdown.to_csv(output_dir / "siope_budget_category_breakdown.csv")
        print(f"  Saved: siope_budget_category_breakdown.csv")
        
        # School-level summary
        school_summary = merged.groupby(['codice_ente', 'anno']).agg({
            'importo_euro': 'sum',
            'codice_regione': 'first',
            'codice_provincia': 'first',
            'codice_comune': 'first',
            'denominazione': 'first',
            'mese': 'nunique'
        }).reset_index()
        school_summary.to_csv(output_dir / "siope_school_expenditure_summary.csv", index=False)
        print(f"  Saved: siope_school_expenditure_summary.csv")
    
    print(f"Processed data saved to {output_dir}/")

def print_summary(siope_uscite, siope_registry, minister_schools, reconciliation):
    """Print summary statistics."""
    print("\n" + "="*60)
    print("SIOPE & MINISTER DATA PROCESSING SUMMARY")
    print("="*60)
    
    print(f"\nSIOPE EXPENDITURE DATA (2020-2026):")
    print(f"  Total records: {len(siope_uscite):,}")
    print(f"  Years covered: {sorted(siope_uscite['anno'].unique())}")
    print(f"  Total expenditure: €{siope_uscite['importo_euro'].sum():,.2f}")
    print(f"  Unique schools: {siope_uscite['codice_ente'].nunique():,}")
    print(f"  Monthly avg: €{siope_uscite.groupby('anno')['importo_euro'].sum().mean():,.2f}")
    
    print(f"\nSIOPE SCHOOL REGISTRY:")
    print(f"  Total schools: {len(siope_registry):,}")
    print(f"  Regions: {siope_registry['codice_regione'].nunique()}")
    print(f"  Provinces: {siope_registry['codice_provincia'].nunique()}")
    print(f"  Communes: {siope_registry['codice_comune'].nunique()}")
    
    print(f"\nMINISTER SCHOOL REGISTRIES:")
    print(f"  Total records: {len(minister_schools):,}")
    if 'codice_regione' in minister_schools.columns:
        print(f"  Regions: {minister_schools['codice_regione'].nunique()}")
    
    print(f"\nRECONCILIATION:")
    print(f"  SIOPE schools: {reconciliation['siope_total']:,}")
    print(f"  Minister schools: {reconciliation['minister_total']:,}")
    if reconciliation['matches'] > 0:
        print(f"  Code matches: {reconciliation['matches']} ({100*reconciliation['matches']/reconciliation['siope_total']:.1f}%)")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    # Load all data
    siope_uscite = load_siope_data()
    siope_registry = load_siope_registry()
    minister_schools = load_minister_schools()
    minister_budget = load_minister_budget()
    
    # Analyze
    if len(siope_uscite) > 0 and len(siope_registry) > 0:
        siope_analysis = analyze_siope_by_territory(siope_uscite, siope_registry)
        
        # Reconcile
        reconciliation = reconcile_schools(siope_registry, minister_schools)
        
        # Save processed data
        save_processed_data(siope_analysis)
        
        # Print summary
        print_summary(siope_uscite, siope_registry, minister_schools, reconciliation)
    else:
        print("Error: Could not load required SIOPE data")
