import pandas as pd

files = {
    "scuole": r"local_data\Scuola_in_chiaro\scuole\SCUANAGRAFESTAT.parquet",
    "edilizia": r"local_data\Scuola_in_chiaro\edilizia_scolastica\EDIANAGRAFESTA202120242520250806.parquet",
    "docsup": r"local_data\MinIstruzione\Personale\personale\DOCSUPXXV.parquet",
    "invalsi": r"local_data\INVALSI\hf_evaluation_outcomes_stat.parquet"
}

for name, path in files.items():
    try:
        print(f"--- {name} ---")
        df = pd.read_parquet(path)
        print("Columns:", df.columns.tolist()[:30])
        print("Shape:", df.shape)
    except Exception as e:
        print("Error:", e)
