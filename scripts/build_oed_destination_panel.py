from __future__ import annotations

import json
import pathlib
import re

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "local_data" / "INPS" / "destination" / "manifest.json"
OUT_DIR = ROOT / "local_data" / "processed"


def _read_csv(path: pathlib.Path) -> tuple[pd.DataFrame, str]:
    for enc in ("utf-8", "latin1"):
        try:
            return pd.read_csv(path, low_memory=False, encoding=enc), enc
        except Exception:  # noqa: BLE001
            pass
    raise ValueError(f"Could not read file with utf-8/latin1: {path}")


def _year_from_title(title: str) -> int | None:
    years = re.findall(r"(20\d{2}|19\d{2})", title)
    if not years:
        return None
    return int(years[-1])


def build_inventory(manifest_rows: list[dict[str, object]]) -> pd.DataFrame:
    inv_rows: list[dict[str, object]] = []

    for item in manifest_rows:
        if item.get("status") != "ok":
            continue
        file_path = pathlib.Path(str(item["local_file"]))
        if not file_path.exists():
            continue

        try:
            df, enc = _read_csv(file_path)
        except ValueError:
            inv_rows.append(
                {
                    "package_id": item["package_id"],
                    "title": item["title"],
                    "local_file": str(file_path).replace("\\", "/"),
                    "status": "parse_error",
                    "rows": None,
                    "cols": None,
                    "year_min": None,
                    "year_max": None,
                    "encoding": None,
                }
            )
            continue

        year_min = year_max = None
        for col in ("Anno", "ANNO", "anno", "year", "YEAR", "TIME_PERIOD"):
            if col in df.columns:
                y = pd.to_numeric(df[col], errors="coerce")
                y = y[(y >= 1900) & (y <= 2035)]
                if len(y):
                    year_min, year_max = int(y.min()), int(y.max())
                break

        inv_rows.append(
            {
                "package_id": item["package_id"],
                "title": item["title"],
                "local_file": str(file_path).replace("\\", "/"),
                "status": "ok",
                "rows": int(len(df)),
                "cols": int(len(df.columns)),
                "year_min": year_min,
                "year_max": year_max,
                "encoding": enc,
            }
        )

    return pd.DataFrame(inv_rows).sort_values(["package_id", "local_file"])


def build_destination_panel(manifest_rows: list[dict[str, object]]) -> pd.DataFrame:
    panel_rows: list[dict[str, object]] = []

    for item in manifest_rows:
        if item.get("status") != "ok":
            continue

        package_id = str(item["package_id"]).lower()
        title = str(item["title"])
        file_path = pathlib.Path(str(item["local_file"]))

        if not file_path.exists():
            continue

        try:
            df, _ = _read_csv(file_path)
        except ValueError:
            continue

        # Apprenticeship employees by year from ID-5515 table (avoids double counting with ID-5516).
        if "id-5515.csv" in file_path.name.lower() and {"Anno", "Tipologia contratto", "Numero dipendenti"}.issubset(df.columns):
            w = df.copy()
            w["Anno"] = pd.to_numeric(w["Anno"], errors="coerce").astype(int)
            w = w[(w["Anno"] >= 2000) & (w["Anno"] <= 2035)]
            w = w[w["Tipologia contratto"].astype(str).str.contains("apprend", case=False, na=False)]
            if len(w):
                grouped = w.groupby("Anno", as_index=False)["Numero dipendenti"].sum()
                for _, r in grouped.iterrows():
                    panel_rows.append(
                        {
                            "year": int(r["Anno"]),
                            "metric": "apprenticeship_employees",
                            "value": float(r["Numero dipendenti"]),
                            "source_package_id": item["package_id"],
                            "source_file": str(file_path).replace("\\", "/"),
                        }
                    )

        # Agricultural apprenticeship-related labor relations by year (ID-5139).
        if {"Anno", "Numero rapporti"}.issubset(df.columns) and "apprend" in package_id:
            w = df.copy()
            w["Anno"] = pd.to_numeric(w["Anno"], errors="coerce").astype(int)
            w["Numero rapporti"] = pd.to_numeric(w["Numero rapporti"], errors="coerce")
            w = w[(w["Anno"] >= 2000) & (w["Anno"] <= 2035)]
            w = w[w["Numero rapporti"].notna()]
            if len(w):
                grouped = w.groupby("Anno", as_index=False)["Numero rapporti"].sum()
                for _, r in grouped.iterrows():
                    panel_rows.append(
                        {
                            "year": int(r["Anno"]),
                            "metric": "apprenticeship_related_relations",
                            "value": float(r["Numero rapporti"]),
                            "source_package_id": item["package_id"],
                            "source_file": str(file_path).replace("\\", "/"),
                        }
                    )

        # Irregular/no-contract workers (2013 snapshots).
        if "irregolari" in package_id and "Numero lavoratori in nero e irregolari" in df.columns:
            w = df.copy()
            w["Numero lavoratori in nero e irregolari"] = pd.to_numeric(
                w["Numero lavoratori in nero e irregolari"], errors="coerce"
            )
            total_row = w[w.astype(str).apply(lambda s: s.str.contains("Totale", case=False, na=False)).any(axis=1)]
            if len(total_row):
                val = float(total_row["Numero lavoratori in nero e irregolari"].iloc[0])
                yr = _year_from_title(title) or 2013
                panel_rows.append(
                    {
                        "year": int(yr),
                        "metric": "irregular_workers_total",
                        "value": val,
                        "source_package_id": item["package_id"],
                        "source_file": str(file_path).replace("\\", "/"),
                    }
                )

    panel = pd.DataFrame(panel_rows)
    if len(panel):
        panel = panel.groupby(["year", "metric"], as_index=False)["value"].sum()
    return panel


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    rows = manifest.get("files", [])

    inventory = build_inventory(rows)
    panel = build_destination_panel(rows)

    inv_out = OUT_DIR / "inps_destination_dataset_inventory_2026-05-24.csv"
    panel_out = OUT_DIR / "oed_destination_risk_panel.csv"

    inventory.to_csv(inv_out, index=False)
    panel.to_csv(panel_out, index=False)

    print(f"Inventory rows: {len(inventory)}")
    print(f"Panel rows: {len(panel)}")
    print(f"Inventory: {inv_out}")
    print(f"Panel: {panel_out}")


if __name__ == "__main__":
    main()
