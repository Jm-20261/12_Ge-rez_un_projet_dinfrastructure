import re
import unicodedata

import pandas as pd
from sqlalchemy import text

from db import get_engine


def normalize_text(value):
    if pd.isna(value):
        return None
    value = str(value).strip()
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"\s+", " ", value).strip()
    return value


def normalize_commute_mode(value):
    normalized = normalize_text(value)

    if normalized in {
        "marche/running",
        "marche / running",
        "marche",
        "running",
    }:
        return "Marche/Running"

    if normalized in {
        "transports en commun",
        "transport en commun",
        "transport publics",
        "transports publics",
        "tram",
        "bus",
    }:
        return "Transports en commun"

    if normalized in {
        "vehicule",
        "vehicule thermique/electrique",
        "vehicule thermique / electrique",
        "voiture",
        "voiture thermique/electrique",
        "voiture",
    }:
        return "Véhicule"

    if normalized in {
        "velo/trottinette/autres",
        "velo / trottinette / autres",
        "velo",
        "trottinette",
        "autres",
    }:
        return "Vélo/Trottinette/Autres"

    return None


def build_business_tables():
    engine = get_engine()

    rh_df = pd.read_sql("SELECT * FROM rh_raw", engine)
    sport_df = pd.read_sql("SELECT * FROM sport_raw", engine)

    employees_df = rh_df.copy()

    employees_df["full_name"] = (
        employees_df["prenom"].fillna("").astype(str).str.strip()
        + " "
        + employees_df["nom"].fillna("").astype(str).str.strip()
    ).str.strip()

    employees_df["is_active"] = True

    employees_df = employees_df.rename(columns={
        "id_salarie": "employee_id",
        "prenom": "first_name",
        "nom": "last_name",
        "adresse_du_domicile": "home_address",
        "moyen_de_deplacement": "commute_mode",
        "salaire_brut": "salary_annual_gross",
        "date_d_embauche": "hire_date",
    })

    employees_df["commute_mode"] = employees_df["commute_mode"].apply(normalize_commute_mode)

    employees_columns = [
        "employee_id",
        "first_name",
        "last_name",
        "full_name",
        "home_address",
        "commute_mode",
        "salary_annual_gross",
        "bu",
        "hire_date",
        "is_active",
    ]
    employees_df = employees_df[employees_columns]

    employee_sports_df = sport_df.copy()

    employee_sports_df = employee_sports_df.rename(columns={
        "id_salarie": "employee_id",
        "pratique_d_un_sport": "main_sport",
    })

    employee_sports_df["has_declared_sport"] = employee_sports_df["main_sport"].notna()
    employee_sports_df["source"] = "excel"

    employee_sports_columns = [
        "employee_id",
        "main_sport",
        "has_declared_sport",
        "source",
    ]
    employee_sports_df = employee_sports_df[employee_sports_columns]

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE sport_activities"))
        conn.execute(text("TRUNCATE TABLE employee_sports RESTART IDENTITY"))
        conn.execute(text("TRUNCATE TABLE commute_checks"))
        conn.execute(text("TRUNCATE TABLE reward_results"))
        conn.execute(text("TRUNCATE TABLE quality_checks_results RESTART IDENTITY"))
        conn.execute(text("TRUNCATE TABLE kpi_history RESTART IDENTITY"))
        conn.execute(text("TRUNCATE TABLE table_volume_history RESTART IDENTITY"))
        conn.execute(text("DELETE FROM employees"))

    employees_df.to_sql("employees", engine, if_exists="append", index=False)
    employee_sports_df.to_sql("employee_sports", engine, if_exists="append", index=False)

    print("Tables métier créées avec succès.")
    print(f"employees : {len(employees_df)} lignes")
    print(f"employee_sports : {len(employee_sports_df)} lignes")

    print("\nRépartition commute_mode après normalisation :")
    print(employees_df["commute_mode"].value_counts(dropna=False))

    print("\nColonnes employees :")
    print(list(employees_df.columns))

    print("\nColonnes employee_sports :")
    print(list(employee_sports_df.columns))


if __name__ == "__main__":
    build_business_tables()