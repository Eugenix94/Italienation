import pandas as pd
import os

istat_dir = os.path.join(os.path.dirname(__file__), "..", "local_data", "ISTAT")
files = sorted(f for f in os.listdir(istat_dir) if f.endswith(".csv") and "manifest" not in f)

print(f"{'Dataset':<44} {'Year range':<15} {'Rows':>10}")
print("-" * 75)
for fname in files:
    df = pd.read_csv(os.path.join(istat_dir, fname))
    slug = fname.replace("istat_", "").replace(".csv", "")
    if "year" in df.columns:
        yr_min = int(df["year"].min())
        yr_max = int(df["year"].max())
        yr_str = f"{yr_min}-{yr_max}"
    else:
        yr_str = "no year col"
    print(f"{slug:<44} {yr_str:<15} {len(df):>10,}")
