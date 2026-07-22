import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Configure matplotlib for the Academic Observatory
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
    plt.figtext(0.99, 0.01, f"Data Provenance: {source_text} | Open Data", 
                ha='right', va='bottom', fontsize=9, color='#64748b', fontname='Inter', fontweight='bold')

def generate_demographic_winter():
    df = pd.read_csv('local_data/processed/demographic_winter_school_closures_projection.csv')
    df = df.sort_values('Variazione_Percentuale_2024_2035')
    
    fig, ax = plt.subplots(figsize=(12, 7))
    colors = ['#fb7185' if x < -15 else '#f43f5e' for x in df['Variazione_Percentuale_2024_2035']]
    bars = ax.barh(df['Regione'], df['Variazione_Percentuale_2024_2035'], color=colors, edgecolor='#e11d48')
    
    ax.set_title("Projected Collapse of Student Population (2020-2035)", fontsize=18, fontweight='black', fontname='Outfit', color='#ffffff', pad=20)
    ax.set_xlabel("Population Change (%)", fontsize=12, fontweight='bold')
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    
    # Add values
    for bar in bars:
        width = bar.get_width()
        ax.text(width - 1, bar.get_y() + bar.get_height()/2, f"{width}%", 
                ha='right', va='center', color='white', fontweight='bold', fontsize=10)

    add_provenance(ax, "ISTAT (Istituto Nazionale di Statistica)")
    plt.tight_layout()
    plt.savefig('web/assets/charts/macro_demographic_winter.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_seismic_risk():
    df = pd.read_csv('local_data/processed/school_infrastructure_seismic_safety_panel.csv')
    df['Percentuale_Edifici_Non_A_Norma_Sismica'] = 100 - df['Perc_Verifica_Antisismica']
    df = df.sort_values('Percentuale_Edifici_Non_A_Norma_Sismica', ascending=False).head(15)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(data=df, x='Percentuale_Edifici_Non_A_Norma_Sismica', y='Regione', color='#f59e0b', ax=ax)
    
    ax.set_title("Schools Non-Compliant with Seismic Safety Standards", fontsize=18, fontweight='black', fontname='Outfit', color='#ffffff', pad=20)
    ax.set_xlabel("Non-Compliant Buildings (%)", fontsize=12, fontweight='bold')
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    
    add_provenance(ax, "Ministero dell'Istruzione e del Merito (MIM)")
    plt.tight_layout()
    plt.savefig('web/assets/charts/decay_seismic_risk_by_region.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_commute_time():
    df = pd.read_csv('local_data/processed/demographic_winter_school_closures_projection.csv')
    df = df.sort_values('Pendolarismo_Medio_Minuti', ascending=False)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(data=df, x='Regione', y='Pendolarismo_Medio_Minuti', color='#8b5cf6', ax=ax)
    
    ax.set_title("Average Student Commute Time (Geographic Penalty)", fontsize=18, fontweight='black', fontname='Outfit', color='#ffffff', pad=20)
    ax.set_ylabel("Commute Time (Minutes)", fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    add_provenance(ax, "ISTAT | Trasporti e Mobilità")
    plt.tight_layout()
    plt.savefig('web/assets/charts/geography_commute_times.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_track_distribution():
    df = pd.read_csv('local_data/processed/italy_national_schools_geospatial_sample.csv')
    track_counts = df['TRACK_TRIPARTITO'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = ['#3b82f6', '#10b981', '#f97316', '#8b5cf6']
    
    # We'll just group them
    liceo = track_counts[track_counts.index.str.contains('Liceo')].sum()
    tech = track_counts[track_counts.index.str.contains('Tecnico')].sum()
    prof = track_counts[track_counts.index.str.contains('Professionale')].sum()
    
    wedges, texts, autotexts = ax.pie([liceo, tech, prof], labels=['Liceo (Academic)', 'Tecnico (Technical)', 'Professionale (Vocational)'], 
           autopct='%1.1f%%', startangle=90, colors=['#3b82f6', '#10b981', '#f97316'],
           textprops=dict(color="w", fontweight='bold'), wedgeprops=dict(width=0.4, edgecolor='#0b1121', linewidth=2))
    
    ax.set_title("National Distribution of Secondary School Tracks", fontsize=18, fontweight='black', fontname='Outfit', color='#ffffff', pad=20)
    
    add_provenance(ax, "Ministero dell'Istruzione e del Merito (MIM) | Open Data")
    plt.tight_layout()
    plt.savefig('web/assets/charts/tripartite_national_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_broadband_gap():
    try:
        df = pd.read_csv('local_data/processed/digital_divide_broadband_schools_nuts3.csv')
        df = df.groupby('Regione')['Copertura_Banda_Larga_Perc'].mean().reset_index().sort_values('Copertura_Banda_Larga_Perc')
        
        fig, ax = plt.subplots(figsize=(12, 7))
        sns.barplot(data=df, x='Regione', y='Copertura_Banda_Larga_Perc', color='#0ea5e9', ax=ax)
        
        ax.set_title("Digital Divide: Broadband Coverage in Schools", fontsize=18, fontweight='black', fontname='Outfit', color='#ffffff', pad=20)
        ax.set_ylabel("Coverage (%)", fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        
        add_provenance(ax, "Infratel Italia | Piano Scuola Connessa")
        plt.tight_layout()
        plt.savefig('web/assets/charts/infrastructure_broadband_divide.png', dpi=300, bbox_inches='tight')
        plt.close()
    except:
        pass

if __name__ == '__main__':
    Path('web/assets/charts').mkdir(parents=True, exist_ok=True)
    generate_demographic_winter()
    generate_seismic_risk()
    generate_commute_time()
    generate_track_distribution()
    generate_broadband_gap()
    print("Precision charts generated successfully.")
