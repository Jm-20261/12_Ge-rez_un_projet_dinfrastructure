import pandas as pd
from sqlalchemy import text
from db import get_engine

def build_business_tables():
    engine = get_engine()

    # Lire les tables brutes
    rh_df = pd.read_sql("SELECT * FROM rh_raw", engine)
    sport_df = pd.read_sql("SELECT * FROM sport_raw", engine)

    # Construire employees
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

    # Construire employee_sports
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

    # Créer les tables SQL si besoin
    create_employees_sql = """
    CREATE TABLE IF NOT EXISTS employees (
        employee_id TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        full_name TEXT,
        home_address TEXT,
        commute_mode TEXT,
        salary_annual_gross NUMERIC,
        bu TEXT,
        hire_date TEXT,
        is_active BOOLEAN DEFAULT TRUE
    );
    """

    create_employee_sports_sql = """
    CREATE TABLE IF NOT EXISTS employee_sports (
        employee_sport_id SERIAL PRIMARY KEY,
        employee_id TEXT,
        main_sport TEXT,
        has_declared_sport BOOLEAN,
        source TEXT
    );
    """

    with engine.begin() as conn:
        conn.execute(text(create_employees_sql))
        conn.execute(text(create_employee_sports_sql))
        conn.execute(text("TRUNCATE TABLE employee_sports;"))
        conn.execute(text("DELETE FROM employees;"))

    # Charger les données
    employees_df.to_sql("employees", engine, if_exists="append", index=False)
    employee_sports_df.to_sql("employee_sports", engine, if_exists="append", index=False)

    print("Tables métier créées avec succès.")
    print(f"employees : {len(employees_df)} lignes")
    print(f"employee_sports : {len(employee_sports_df)} lignes")

    print("\nColonnes employees :")
    print(list(employees_df.columns))

    print("\nColonnes employee_sports :")
    print(list(employee_sports_df.columns))

if __name__ == "__main__":
    build_business_tables()
