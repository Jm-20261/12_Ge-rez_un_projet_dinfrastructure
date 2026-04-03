import pandas as pd
from sqlalchemy import text
from db import get_engine

TABLES_TO_TRACK = [
    "rh_raw",
    "sport_raw",
    "employees",
    "employee_sports",
    "sport_activities",
    "commute_checks",
    "reward_results",
    "quality_checks_results"
]

def capture_table_volumes():
    engine = get_engine()
    rows = []

    for table_name in TABLES_TO_TRACK:
        query = f"SELECT COUNT(*) AS cnt FROM {table_name}"
        count_value = int(pd.read_sql(query, engine).iloc[0]["cnt"])
        rows.append({
            "table_name": table_name,
            "row_count": count_value
        })

    df = pd.DataFrame(rows)
    df.to_sql("table_volume_history", engine, if_exists="append", index=False)

    print("Historique de volumétrie enregistré.")
    print(df)

if __name__ == "__main__":
    capture_table_volumes()
