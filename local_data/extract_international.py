import pandas as pd
import os

equity_file = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\openEURYDICE\Equity_system_level_indicators_2023_2025_open_data_2.xlsx"
oecd_file = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\oecd\oecd_teacher_experience.csv"
out_dir = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\processed"

# 1. Student Services (Sheet: 2023_2024_5_Student_services)
try:
    df_services = pd.read_excel(equity_file, sheet_name='2023_2024_5_Student_services')
    df_services.to_csv(os.path.join(out_dir, "eurydice_student_services_equity.csv"), index=False)
    print("Created eurydice_student_services_equity.csv")
except Exception as e:
    print(f"Error extracting services: {e}")

# 2. Grade Repetition (Sheet: 2024_2025_1_Grade repetition)
try:
    df_rep = pd.read_excel(equity_file, sheet_name='2024_2025_1_Grade repetition')
    df_rep.to_csv(os.path.join(out_dir, "eurydice_grade_repetition.csv"), index=False)
    print("Created eurydice_grade_repetition.csv")
except Exception as e:
    print(f"Error extracting repetition: {e}")

# 3. OECD Teacher Experience
try:
    chunks = []
    for chunk in pd.read_csv(oecd_file, chunksize=50000, low_memory=False):
        # We look for columns that might indicate country. Usually 'LOCATION' or 'COUNTRY' or 'COU'
        country_col = [c for c in chunk.columns if c.upper() in ['LOCATION', 'COUNTRY', 'COU']]
        if country_col:
            cc = country_col[0]
            # Keep ITA and OECD average
            filtered = chunk[chunk[cc].isin(['ITA', 'OAVG', 'OECD', 'EU27'])]
            chunks.append(filtered)
        else:
            chunks.append(chunk.head(100))
            break
    
    if chunks:
        df_teachers = pd.concat(chunks)
        df_teachers.to_csv(os.path.join(out_dir, "oecd_teacher_demographics.csv"), index=False)
        print("Created oecd_teacher_demographics.csv")
except Exception as e:
    print(f"Error extracting OECD teachers: {e}")
