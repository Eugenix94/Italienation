"""Quick data structure survey for notebook planning."""
import pandas as pd, warnings, pathlib, sys
warnings.filterwarnings('ignore')

ROOT = pathlib.Path('local_data')

def peek(p, n=2):
    p = str(p)
    for enc in ['utf-8','utf-8-sig','cp1252','latin-1']:
        for sep in [';',',','\t']:
            try:
                df = pd.read_csv(p, sep=sep, encoding=enc, nrows=n, low_memory=False)
                if df.shape[1] > 1:
                    print(f"  {pathlib.Path(p).name}: shape={df.shape} cols={list(df.columns[:8])}")
                    return df
            except:
                pass
    print(f"  FAILED: {p}")
    return None

print("=== Schools (Scuole) ===")
peek(ROOT/'MinIstruzione/Scuole/SCUANAGRAFESTAT20242520250831.csv')
peek(ROOT/'MinIstruzione/Scuole/SCUANAGRAFEPAR20242520250831.csv')

print("\n=== Alunni (Secondary) ===")
peek(ROOT/'MinIstruzione/Alunni/ALUSECGRADOINDPAR20242520250831.csv')
peek(ROOT/'MinIstruzione/Alunni/ALUCORSOINDCLAPAR20242520250831.csv')
peek(ROOT/'MinIstruzione/Alunni/ALUCORSOETAPAR20242520250831.csv')

print("\n=== MUR Immatricolati ===")
peek(ROOT/'MUR/immatricolati/10_immatricolatixdiplomascuolasecondariaxclasse.csv')
peek(ROOT/'MUR/immatricolati/01_immatricolatixanno.csv')
peek(ROOT/'MUR/immatricolati/05_immatricolatixresidenza.csv')
peek(ROOT/'MUR/immatricolati/11_immatricolatixdiplomascuolaxresidenza.csv')
peek(ROOT/'MUR/immatricolati/16_immatricolatixvotodiplomascuolasec.csv')

print("\n=== MUR Iscritti ===")
peek(ROOT/'MUR/MUR_iscritti/iscritti_per_regione.csv')
peek(ROOT/'MUR/MUR_iscritti/iscritti_per_provincia.csv')
peek(ROOT/'MUR/MUR_iscritti/iscritti_in_sede_fuori_sede.csv')

print("\n=== NEET files ===")
for f in ROOT.glob('NEET*.csv'):
    peek(f)
for f in ROOT.glob('Incidenza*.csv'):
    peek(f)

print("\n=== OECD ===")
peek(ROOT/'oecd/eurostat_gdp_per_capita.csv')
peek(ROOT/'oecd/oecd_eag_transition.csv')
peek(ROOT/'oecd/oecd_education_costs.csv')
peek(ROOT/'oecd/oecd_education_fin_gdp.csv')
peek(ROOT/'oecd/oecd_education_attainment_migration.csv')

print("\n=== OurWorldData ===")
peek(ROOT/'ourWorldData/completion-rate-of-upper-secondary-education-sdg/completion-rate-of-upper-secondary-education-sdg.csv')
peek(ROOT/'ourWorldData/productivity-vs-educational-attainment/productivity-vs-educational-attainment.csv')
peek(ROOT/'ourWorldData/total-number-of-emigrants.csv')

print("\n=== UK SDG Stats (Goal 4 Education) ===")
for sdg in ['4-1-1','4-1-2','4-2-1','4-3-1','4-4-1']:
    peek(ROOT/f'UKSDGstats/{sdg}.csv')

print("\n=== Gini / WB Human Capital ===")
peek(ROOT/'WB_WDI_SI_POV_GINI.csv')
peek(ROOT/'API_HD.HCI.OVRL_DS63_en_csv_v2_756596.csv')

print("\nDone.")
