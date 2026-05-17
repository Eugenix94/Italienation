from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MUR = ROOT / "local_data" / "MUR"
OUT = ROOT / "local_data" / "processed"

DSU_DIR = MUR / "2025-diritto-allo-studio-universitario-dsu-regionale"
ATENEI_DIR = MUR / "2024-contribuzione-e-interventi-atenei"


def read_semicolon_csv(path: Path) -> pd.DataFrame:
    try:
        df = pd.read_csv(path, sep=";", dtype=str, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, sep=";", dtype=str, encoding="cp1252")
    df.columns = [c.strip() for c in df.columns]
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].astype(str).str.strip()
    return df


def to_num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(
        s.astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.replace(" ", "", regex=False)
        .replace({"-": None, "": None, "nan": None}),
        errors="coerce",
    )


def key_entity(df: pd.DataFrame, reg_col: str = "NOME_REGIONE", ente_col: str = "NOME_ENTE") -> pd.Series:
    return (
        df[reg_col].astype(str).str.upper().str.strip()
        + "||"
        + df[ente_col].astype(str).str.upper().str.strip()
    )


def build_dsu_ersu_panel() -> pd.DataFrame:
    interventi = read_semicolon_csv(DSU_DIR / "2025_dsu_interventi_rett06032026.csv")
    spesa = read_semicolon_csv(DSU_DIR / "2025_dsu_spesa.csv")
    alloggi_mense = read_semicolon_csv(DSU_DIR / "2025_dsu_alloggi_mense.csv")
    pasti = read_semicolon_csv(DSU_DIR / "2025_dsu_pasti_erogati.csv")

    int_cols = [
        "INTERVENTI_LAUREA",
        "INTERVENTI_LAUREA_EXTRA_UE",
        "INTERVENTI_DOTTORATO",
        "INTERVENTI_SPECIALIZZAZIONE",
    ]
    for c in int_cols:
        interventi[c] = to_num(interventi[c]).fillna(0)
    interventi["interventi_tot"] = interventi[int_cols].sum(axis=1)
    interventi["k"] = key_entity(interventi)

    is_borsa_domande = interventi["DESCRIZIONE_INTERVENTO"].str.contains("borse di studio", case=False, na=False) & interventi["DESCRIZIONE_INTERVENTO"].str.contains("domande", case=False, na=False)
    is_idonei = interventi["DESCRIZIONE_INTERVENTO"].str.contains("borse di studio", case=False, na=False) & interventi["DESCRIZIONE_INTERVENTO"].str.contains("idonei", case=False, na=False)
    is_borse = interventi["DESCRIZIONE_INTERVENTO"].str.contains("borse di studio", case=False, na=False) & interventi["DESCRIZIONE_INTERVENTO"].str.contains("borse concesse", case=False, na=False)
    is_prestiti = interventi["DESCRIZIONE_INTERVENTO"].str.contains("prestiti concessi", case=False, na=False)
    is_disab = interventi["DESCRIZIONE_INTERVENTO"].str.contains("disabilit", case=False, na=False) & interventi["DESCRIZIONE_INTERVENTO"].str.contains("interventi concessi", case=False, na=False)

    int_agg = pd.DataFrame({
        "k": interventi["k"].drop_duplicates().values,
    }).set_index("k")

    int_agg["applications_total"] = interventi[is_borsa_domande].groupby("k")["interventi_tot"].sum()
    int_agg["eligible_students_total"] = interventi[is_idonei].groupby("k")["interventi_tot"].sum()
    int_agg["beneficiaries_borse_total"] = interventi[is_borse].groupby("k")["interventi_tot"].sum()
    int_agg["beneficiaries_prestiti_total"] = interventi[is_prestiti].groupby("k")["interventi_tot"].sum()
    int_agg["beneficiaries_disability_support_total"] = interventi[is_disab].groupby("k")["interventi_tot"].sum()

    int_agg = int_agg.fillna(0).reset_index()

    spend_cols = ["SPESA_LAUREA", "SPESA_DOTTORATO", "SPESA_SPECIALIZZAZIONE"]
    for c in spend_cols:
        spesa[c] = to_num(spesa[c]).fillna(0)
    spesa["spesa_tot"] = spesa[spend_cols].sum(axis=1)
    spesa["k"] = key_entity(spesa)

    cat_map = {
        "spesa_borse_total": "borse",
        "spesa_prestiti_total": "prestiti",
        "spesa_mobilita_total": "mobilit",
        "spesa_disability_support_total": "disabilit",
        "spesa_alloggi_total": "allogg",
        "spesa_ristorazione_total": "ristor",
    }

    spend_agg = pd.DataFrame({"k": spesa["k"].drop_duplicates().values}).set_index("k")
    for out_col, kw in cat_map.items():
        m = spesa["DESCRIZIONE_SPESA"].str.contains(kw, case=False, na=False)
        spend_agg[out_col] = spesa[m].groupby("k")["spesa_tot"].sum()
    spend_agg["spesa_dsu_total"] = spesa.groupby("k")["spesa_tot"].sum()
    spend_agg = spend_agg.fillna(0).reset_index()

    alloggi_mense["k"] = key_entity(alloggi_mense)
    alloggi_mense["NUMERO_N"] = to_num(alloggi_mense["NUMERO"]).fillna(0)

    serv_agg = pd.DataFrame({"k": alloggi_mense["k"].drop_duplicates().values}).set_index("k")

    m_alloggi = alloggi_mense["DESCRIZIONE_SERVIZIO"].str.contains("Posti alloggio in residenze - anno corrente$", case=False, na=False)
    m_alloggi_idonei = alloggi_mense["DESCRIZIONE_SERVIZIO"].str.contains("assegnati a studenti idonei", case=False, na=False)
    m_alloggi_nonid = alloggi_mense["DESCRIZIONE_SERVIZIO"].str.contains("assegnati a studenti non idonei", case=False, na=False)
    m_posti_mensa = alloggi_mense["DESCRIZIONE_SERVIZIO"].str.contains("numero posti mensa", case=False, na=False)

    serv_agg["posti_alloggio_total"] = alloggi_mense[m_alloggi].groupby("k")["NUMERO_N"].sum()
    serv_agg["posti_alloggio_idonei"] = alloggi_mense[m_alloggi_idonei].groupby("k")["NUMERO_N"].sum()
    serv_agg["posti_alloggio_non_idonei"] = alloggi_mense[m_alloggi_nonid].groupby("k")["NUMERO_N"].sum()
    serv_agg["posti_mensa_total"] = alloggi_mense[m_posti_mensa].groupby("k")["NUMERO_N"].sum()

    pasti["k"] = key_entity(pasti)
    pasti["NUMERO_N"] = to_num(pasti["NUMERO"]).fillna(0)

    m_pasti = pasti["DESCRIZIONE_TIPOLOGIA"].str.contains("Pasti erogati", case=False, na=False)
    m_studenti_mensa = pasti["DESCRIZIONE_TIPOLOGIA"].str.contains("Studenti che usufruiscono delle mense", case=False, na=False)

    serv_agg["pasti_erogati_total"] = pasti[m_pasti].groupby("k")["NUMERO_N"].sum()
    serv_agg["studenti_mensa_total"] = pasti[m_studenti_mensa].groupby("k")["NUMERO_N"].sum()

    serv_agg = serv_agg.fillna(0).reset_index()

    base_cols = ["NOME_REGIONE", "NOME_ENTE", "ANNO_ACCADEMICO"]
    base = interventi[base_cols].drop_duplicates().copy()
    base["k"] = key_entity(base)
    base["entity_is_ersu_like"] = base["NOME_ENTE"].str.contains("ERSU|EDISU|ADISU|ADSU|ARDSU|ARDIS|ER\\.GO|DIRITTO ALLO STUDIO|A\\.R\\.DI\\.S", case=False, regex=True, na=False)

    out = base.merge(int_agg, on="k", how="left").merge(spend_agg, on="k", how="left").merge(serv_agg, on="k", how="left")

    numeric_cols = [
        c
        for c in out.columns
        if c.endswith("_total") or c.startswith("spesa_") or c.startswith("posti_") or c.startswith("pasti_")
    ]
    out[numeric_cols] = out[numeric_cols].fillna(0)
    out[numeric_cols] = out[numeric_cols].clip(lower=0)

    out["grant_coverage_rate"] = out["beneficiaries_borse_total"].div(out["applications_total"].replace(0, pd.NA)).fillna(0)
    out["grant_coverage_rate_capped"] = out["grant_coverage_rate"].clip(upper=1)
    out["avg_borsa_support_eur"] = out["spesa_borse_total"].div(out["beneficiaries_borse_total"].replace(0, pd.NA)).fillna(0)
    out["avg_mensa_spend_per_student_eur"] = out["spesa_ristorazione_total"].div(out["studenti_mensa_total"].replace(0, pd.NA)).fillna(0)

    out = out.rename(columns={
        "NOME_REGIONE": "region",
        "NOME_ENTE": "dsu_ente",
        "ANNO_ACCADEMICO": "academic_year",
    })

    out = out.sort_values(["region", "dsu_ente"]).reset_index(drop=True)
    return out


def build_atenei_payment_support_panel() -> pd.DataFrame:
    contrib = read_semicolon_csv(ATENEI_DIR / "2024_atenei_contribuzione_media.csv")
    interventi = read_semicolon_csv(ATENEI_DIR / "2024_atenei_numero_interventi.csv")
    classi = read_semicolon_csv(ATENEI_DIR / "2024_atenei_classi_contribuzione.csv")

    contrib["tassa_media_paganti_laur_eur"] = to_num(contrib["TASSA_MEDIA_PAGANTI_LAUREA"])
    contrib["tassa_media_tot_iscr_laur_eur"] = to_num(contrib["TASSA_MEDIA_TOTALE_ISCRITTI_LAUREA"])

    contrib = contrib.rename(columns={
        "ANNO_ACCADEMICO": "academic_year",
        "COD_Ateneo": "ateneo_code",
        "NOME_ATENEO": "ateneo_name",
    })

    interventi["interventi_tot"] = (
        to_num(interventi["INTERVENTI_LAUREA"]).fillna(0)
        + to_num(interventi["INTERVENTI_LAUREA_EXTRA_UE"]).fillna(0)
        + to_num(interventi["INTERVENTI_DOTTORATO"]).fillna(0)
        + to_num(interventi["INTERVENTI_SPECIALIZZAZIONE"]).fillna(0)
        + to_num(interventi["INTERVENTI_MASTER"]).fillna(0)
    )

    m_borse = interventi["DESCRIZIONE_INTERVENTO"].str.contains("Borse di studio", case=False, na=False)
    m_mob_out = interventi["DESCRIZIONE_INTERVENTO"].str.contains("uscita", case=False, na=False)

    int_agg = pd.DataFrame({
        "ateneo_code": interventi["COD_ATENEO"].astype(str),
        "ateneo_name": interventi["NOME_ATENEO"].astype(str),
        "interventi_tot": interventi["interventi_tot"],
        "is_borse": m_borse,
        "is_mob_out": m_mob_out,
    })

    bors = int_agg[int_agg["is_borse"]].groupby(["ateneo_code", "ateneo_name"], as_index=False)["interventi_tot"].sum().rename(columns={"interventi_tot": "beneficiaries_borse_ateneo_total"})
    mob = int_agg[int_agg["is_mob_out"]].groupby(["ateneo_code", "ateneo_name"], as_index=False)["interventi_tot"].sum().rename(columns={"interventi_tot": "beneficiaries_mobility_out_total"})

    classi["count_laur"] = to_num(classi["CONTRIBUZIONE_LAUREA"]).fillna(0)
    classi["code"] = classi["CODICE_CLASSE"].astype(str).str.strip()

    dist = classi.groupby(["COD_Ateneo", "NOME_ATENEO"], as_index=False)["count_laur"].sum().rename(columns={"count_laur": "students_in_contrib_classes_total", "COD_Ateneo": "ateneo_code", "NOME_ATENEO": "ateneo_name"})
    no_contrib = classi[classi["code"].str.startswith("00", na=False)].groupby(["COD_Ateneo", "NOME_ATENEO"], as_index=False)["count_laur"].sum().rename(columns={"count_laur": "students_no_contrib_class", "COD_Ateneo": "ateneo_code", "NOME_ATENEO": "ateneo_name"})
    low_contrib = classi[classi["code"].isin(["01", "02", "03", "04", "05"])].groupby(["COD_Ateneo", "NOME_ATENEO"], as_index=False)["count_laur"].sum().rename(columns={"count_laur": "students_contrib_up_to_500", "COD_Ateneo": "ateneo_code", "NOME_ATENEO": "ateneo_name"})

    out = contrib.merge(bors, on=["ateneo_code", "ateneo_name"], how="left").merge(mob, on=["ateneo_code", "ateneo_name"], how="left").merge(dist, on=["ateneo_code", "ateneo_name"], how="left").merge(no_contrib, on=["ateneo_code", "ateneo_name"], how="left").merge(low_contrib, on=["ateneo_code", "ateneo_name"], how="left")

    num_cols = [
        "beneficiaries_borse_ateneo_total",
        "beneficiaries_mobility_out_total",
        "students_in_contrib_classes_total",
        "students_no_contrib_class",
        "students_contrib_up_to_500",
        "tassa_media_paganti_laur_eur",
        "tassa_media_tot_iscr_laur_eur",
    ]
    out[num_cols] = out[num_cols].fillna(0)

    out["avg_support_gap_eur"] = (out["tassa_media_paganti_laur_eur"] - out["tassa_media_tot_iscr_laur_eur"]).clip(lower=0)
    out["share_no_contrib_class"] = out["students_no_contrib_class"].div(out["students_in_contrib_classes_total"]).replace([pd.NA, pd.NaT, float("inf")], 0)
    out["share_contrib_up_to_500"] = out["students_contrib_up_to_500"].div(out["students_in_contrib_classes_total"]).replace([pd.NA, pd.NaT, float("inf")], 0)

    out = out[~out["ateneo_code"].isin(["TTTTT", "SSSSS", "LLLLL"])].copy()
    out = out.sort_values("ateneo_name").reset_index(drop=True)
    return out


def write_manifest() -> None:
    manifest = {
        "generated_at": pd.Timestamp.now("UTC").isoformat(),
        "outputs": [
            "dsu_ersu_support_panel_2024_2025.csv",
            "atenei_payment_support_panel_2023_2024.csv",
        ],
        "sources": [
            {
                "id": "mur_dsu_interventi",
                "path": "local_data/MUR/2025-diritto-allo-studio-universitario-dsu-regionale/2025_dsu_interventi_rett06032026.csv",
            },
            {
                "id": "mur_dsu_spesa",
                "path": "local_data/MUR/2025-diritto-allo-studio-universitario-dsu-regionale/2025_dsu_spesa.csv",
            },
            {
                "id": "mur_dsu_alloggi_mense",
                "path": "local_data/MUR/2025-diritto-allo-studio-universitario-dsu-regionale/2025_dsu_alloggi_mense.csv",
            },
            {
                "id": "mur_dsu_pasti",
                "path": "local_data/MUR/2025-diritto-allo-studio-universitario-dsu-regionale/2025_dsu_pasti_erogati.csv",
            },
            {
                "id": "mur_atenei_contribuzione_media",
                "path": "local_data/MUR/2024-contribuzione-e-interventi-atenei/2024_atenei_contribuzione_media.csv",
            },
            {
                "id": "mur_atenei_numero_interventi",
                "path": "local_data/MUR/2024-contribuzione-e-interventi-atenei/2024_atenei_numero_interventi.csv",
            },
            {
                "id": "mur_atenei_classi_contribuzione",
                "path": "local_data/MUR/2024-contribuzione-e-interventi-atenei/2024_atenei_classi_contribuzione.csv",
            },
        ],
        "notes": [
            "DSU/ERSU support metrics are aggregated at regional ente level.",
            "Atenei payment panel combines average fees with support and contribution-class distributions.",
            "ERSU-like entities are identified via name pattern (ERSU/EDISU/ADISU/ADSU/ARDSU/ARDIS/ER.GO/DSU).",
        ],
    }

    (OUT / "dsu_ersu_sources_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    md = ["# DSU/ERSU Sources Manifest", "", "## Outputs"]
    md.extend([f"- {o}" for o in manifest["outputs"]])
    md.extend(["", "## Sources"])
    md.extend([f"- {s['id']}: {s['path']}" for s in manifest["sources"]])
    md.extend(["", "## Notes"])
    md.extend([f"- {n}" for n in manifest["notes"]])
    (OUT / "dsu_ersu_sources.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    dsu = build_dsu_ersu_panel()
    atenei = build_atenei_payment_support_panel()

    dsu.to_csv(OUT / "dsu_ersu_support_panel_2024_2025.csv", index=False)
    atenei.to_csv(OUT / "atenei_payment_support_panel_2023_2024.csv", index=False)
    write_manifest()

    print("Wrote:", OUT / "dsu_ersu_support_panel_2024_2025.csv", "rows", len(dsu))
    print("Wrote:", OUT / "atenei_payment_support_panel_2023_2024.csv", "rows", len(atenei))


if __name__ == "__main__":
    main()
