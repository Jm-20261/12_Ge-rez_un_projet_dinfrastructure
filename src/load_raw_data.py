from pathlib import Path
import re
import unicodedata

import pandas as pd
from sqlalchemy import text

from db import get_engine


def normalize_column_name(name: str) -> str:
    name = str(name).strip()
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name


def load_excel_files():
    project_root = Path(__file__).resolve().parents[1]
    raw_dir = project_root / "data" / "raw"

    rh_path = next(raw_dir.glob("*RH*.xlsx"))
    sport_path = next(raw_dir.glob("*Sportive*.xlsx"))

    print(f"Lecture RH : {rh_path.name}")
    print(f"Lecture Sport : {sport_path.name}")

    rh_df = pd.read_excel(rh_path)
    sport_df = pd.read_excel(sport_path)

    rh_df.columns = [normalize_column_name(col) for col in rh_df.columns]
    sport_df.columns = [normalize_column_name(col) for col in sport_df.columns]

    engine = get_engine()

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE rh_raw"))
        conn.execute(text("TRUNCATE TABLE sport_raw"))

    rh_df.to_sql("rh_raw", engine, if_exists="append", index=False)
    sport_df.to_sql("sport_raw", engine, if_exists="append", index=False)

    print("\nChargement terminé.")
    print(f"rh_raw : {len(rh_df)} lignes")
    print(f"sport_raw : {len(sport_df)} lignes")

    print("\nColonnes RH :")
    print(list(rh_df.columns))

    print("\nColonnes Sport :")
    print(list(sport_df.columns))


if __name__ == "__main__":
    load_excel_files()