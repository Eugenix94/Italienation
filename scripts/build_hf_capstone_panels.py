import pandas as pd
import os
import json

output_dir = "local_data/processed"
os.makedirs(output_dir, exist_ok=True)

# 1. Teachers summary by school order and type of post (Titular vs Supplementary)
print("Processing teachers summary...")
df_tit = pd.read_parquet("local_data/HuggingFace/hf_teachers_titular.parquet")
for col in ["DOCENTITITOLARIMASCHI", "DOCENTITITOLARIFEMMINE"]:
    if col in df_tit.columns:
        df_tit[col] = pd.to_numeric(df_tit[col], errors="coerce").fillna(0)

df_tit["total_titular"] = df_tit["DOCENTITITOLARIMASCHI"] + df_tit["DOCENTITITOLARIFEMMINE"]
tit_summary = df_tit.groupby(["ORDINESCUOLA", "TIPOPOSTO"])["total_titular"].sum().reset_index()

df_sup = pd.read_parquet("local_data/HuggingFace/hf_teachers_suppl_2024_25.parquet")
for col in ["DOCENTISUPPLENTIMASCHI", "DOCENTISUPPLENTIFEMMINE"]:
    if col in df_sup.columns:
        df_sup[col] = pd.to_numeric(df_sup[col], errors="coerce").fillna(0)

df_sup["total_suppl"] = df_sup["DOCENTISUPPLENTIMASCHI"] + df_sup["DOCENTISUPPLENTIFEMMINE"]
sup_summary = df_sup.groupby(["ORDINESCUOLA", "TIPOPOSTO"])["total_suppl"].sum().reset_index()

teachers_panel = pd.merge(tit_summary, sup_summary, on=["ORDINESCUOLA", "TIPOPOSTO"], how="outer").fillna(0)
teachers_panel["total_titular"] = pd.to_numeric(teachers_panel["total_titular"], errors="coerce").fillna(0)
teachers_panel["total_suppl"] = pd.to_numeric(teachers_panel["total_suppl"], errors="coerce").fillna(0)
teachers_panel["total_teachers"] = teachers_panel["total_titular"] + teachers_panel["total_suppl"]
teachers_panel["suppl_share_pct"] = (teachers_panel["total_suppl"] / teachers_panel["total_teachers"].replace(0, 1) * 100).round(2)
teachers_panel.to_csv(os.path.join(output_dir, "hf_teachers_by_school_order_panel.csv"), index=False)
print("Saved hf_teachers_by_school_order_panel.csv")

# 2. Upper secondary enrollment by track (Liceo vs Tecnico vs Professionale)
print("Processing upper secondary enrollment by track...")
df_stu = pd.read_parquet("local_data/HuggingFace/hf_students_upper_sec_stat_2024_25.parquet")
for col in ["ALUNNIMASCHI", "ALUNNIFEMMINE"]:
    if col in df_stu.columns:
        df_stu[col] = pd.to_numeric(df_stu[col], errors="coerce").fillna(0)

df_stu["total_students"] = df_stu["ALUNNIMASCHI"] + df_stu["ALUNNIFEMMINE"]

# Merge with school registry to get Region/Provincia
df_sch = pd.read_parquet("local_data/HuggingFace/hf_schools_registry_stat.parquet")[["CODICESCUOLA", "REGIONE", "PROVINCIA", "AREAGEOGRAFICA"]].drop_duplicates("CODICESCUOLA")
df_stu_reg = pd.merge(df_stu, df_sch, on="CODICESCUOLA", how="left")

track_summary = df_stu_reg.groupby(["REGIONE", "TIPOPERCORSO"])["total_students"].sum().reset_index()
track_pivot = track_summary.pivot(index="REGIONE", columns="TIPOPERCORSO", values="total_students").fillna(0).reset_index()
track_pivot["TOTAL"] = track_pivot.sum(axis=1, numeric_only=True)
for col in track_pivot.columns:
    if col not in ["REGIONE", "TOTAL"]:
        track_pivot[col] = pd.to_numeric(track_pivot[col], errors="coerce").fillna(0)
        track_pivot[f"{col}_share_pct"] = (track_pivot[col] / track_pivot["TOTAL"].replace(0, 1) * 100).round(2)

track_pivot.to_csv(os.path.join(output_dir, "hf_upper_sec_track_enrollment_panel.csv"), index=False)
print("Saved hf_upper_sec_track_enrollment_panel.csv")

# 3. Evaluation criteria outcomes across schools
print("Processing school evaluation scores...")
df_val = pd.read_parquet("local_data/HuggingFace/hf_evaluation_outcomes_stat.parquet")
df_val["score_numeric"] = pd.to_numeric(df_val["PUNTEGGIOSCUOLA"], errors="coerce")
val_clean = df_val.dropna(subset=["score_numeric"])

# Merge with school registry for geographical grouping
df_val_reg = pd.merge(val_clean, df_sch, left_on="CODICEISTITUTO", right_on="CODICESCUOLA", how="left")
val_summary = df_val_reg.groupby(["AREAGEOGRAFICA", "CODICECRITERIO"])["score_numeric"].agg(["count", "mean", "std"]).reset_index()
val_summary["mean"] = val_summary["mean"].round(2)
val_summary.to_csv(os.path.join(output_dir, "hf_evaluation_scores_by_area.csv"), index=False)
print("Saved hf_evaluation_scores_by_area.csv")

print("All HuggingFace panels successfully generated under local_data/processed/!")
