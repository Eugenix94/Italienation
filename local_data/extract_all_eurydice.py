import os
import pandas as pd
import warnings

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

eurydice_dir = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\openEURYDICE"
out_dir = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\processed"

for f in os.listdir(eurydice_dir):
    if f.endswith(".xlsx") and not f.startswith("~"):
        path = os.path.join(eurydice_dir, f)
        print(f"Processing {f}...")
        try:
            xl = pd.ExcelFile(path)
            for sheet in xl.sheet_names:
                df = xl.parse(sheet)
                
                # clean sheet name
                clean_sheet = sheet.replace(' ', '_').replace('/', '_').replace('\\', '_')
                
                # clean file name
                clean_file = f.replace('.xlsx', '').replace(' ', '_')
                
                # truncate names to avoid Windows path limit issues
                if len(clean_file) > 20:
                    clean_file = clean_file[:20]
                if len(clean_sheet) > 20:
                    clean_sheet = clean_sheet[:20]
                    
                out_name = f"eury_{clean_file}_{clean_sheet}.csv"
                out_name = out_name.replace('\'', '').replace('__', '_')
                
                # drop completely empty columns and rows
                df.dropna(how='all', axis=1, inplace=True)
                df.dropna(how='all', axis=0, inplace=True)
                
                if not df.empty:
                    df.to_csv(os.path.join(out_dir, out_name), index=False)
                    print(f"  -> Extracted {out_name}")
        except Exception as e:
            print(f"Error processing {f}: {e}")
