import pandas as pd
from sqlalchemy import text
from db import get_engine

def clean_text(value):
    if pd.isna(value):
        return None
    value = str(value).strip()
    if value == "":
        return None
    return value

def normalize_commute_mode(value):
    value = clean_text(value)
    if value is None:
        return None

    v = value.lower()

    if "marche" in v or "running" in v or "runing" in v:
        return "Marche/Running"
    if "velo" in v or "vélo" in v or "trottinette" in v:
        return "Vélo/Trottinette/Autres"
    if "transport" in v:
        return "Transports en commun"
    if "vehicule" in v or "véhicule" in v or "voiture" in v:
        return "Véhicule"

    return value

def normalize_sport(value):
    value = clean_text(value)
    if value is None:
        return None

    v = value.lower()

    if v in ["runing", "running", "course à pied", "course a pied", "jogging"]:
        return "Course à pied"
    if "randon" in v:
        return "Randonnée"
    if "velo" in v or "vélo" in v:
        return "Vélo"
    if "natation" in v:
        return "Natation"
    if "musculation" in v:
        return "Musculation"
    if "fitness" in v:
        return "Fitness"
    if "escalade" in v:
        return "Escalade"
    if "tennis" in v:
        return "Tennis"
    if "football" in v:
        return "Football"

    return value

def clean_business_data():
    engine = get_engine()

    employees_df = pd.read_sql("SELECT * FROM employees", engine)
    sports_df = pd.read_sql("SELECT * FROM employee_sports", engine)

    employees_df["home_address"] = employees_df["home_address"].apply(clean_text)
    employees_df["commute_mode"] = employees_df["commute_mode"].apply(normalize_commute_mode)

    sports_df["main_sport"] = sports_df["main_sport"].apply(normalize_sport)
    sports_df["has_declared_sport"] = sports_df["main_sport"].notna()

    with engine.begin() as conn:
        conn.execute(text("DELETE FROM employee_sports;"))
        conn.execute(text("DELETE FROM employees;"))

    employees_df.to_sql("employees", engine, if_exists="append", index=False)
    sports_df.to_sql("employee_sports", engine, if_exists="append", index=False)

    print("Nettoyage terminé.")
    print(f"employees : {len(employees_df)} lignes")
    print(f"employee_sports : {len(sports_df)} lignes")

    print("\nValeurs commute_mode après nettoyage :")
    print(sorted([x for x in employees_df["commute_mode"].dropna().unique()]))

    print("\nValeurs main_sport après nettoyage :")
    print(sorted([x for x in sports_df["main_sport"].dropna().unique()]))

    print("\nNombre de sports non déclarés :")
    print(int(sports_df["main_sport"].isna().sum()))

if __name__ == "__main__":
    clean_business_data()
