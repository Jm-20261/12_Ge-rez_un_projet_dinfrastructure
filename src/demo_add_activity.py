import uuid
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import text
from db import get_engine

TARGET_EMPLOYEE = "Adèle Albert"
THRESHOLD = 15

def get_employee(engine):
    query = """
    SELECT
        rr.employee_id,
        rr.employee_name,
        rr.sports_activity_count
    FROM reward_results rr
    WHERE rr.employee_name = :employee_name
    """
    with engine.begin() as conn:
        df = pd.read_sql(text(query), conn, params={"employee_name": TARGET_EMPLOYEE})
    if df.empty:
        raise ValueError(f"Salarié introuvable : {TARGET_EMPLOYEE}")
    return df.iloc[0]

def build_activity(employee_id, offset_days):
    start_time = datetime.now().replace(second=0, microsecond=0) - timedelta(days=offset_days)
    elapsed_time_s = 42 * 60
    distance_m = 8500

    return {
        "activity_id": str(uuid.uuid4()),
        "employee_id": str(employee_id),
        "activity_start": start_time,
        "activity_end": start_time + timedelta(seconds=elapsed_time_s),
        "activity_type": "Course à pied",
        "distance_m": distance_m,
        "elapsed_time_s": elapsed_time_s,
        "comment": "Course ajoutée pendant la démonstration live.",
        "source": "demo_live"
    }

def insert_activity(engine, activity):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO sport_activities (
                    activity_id,
                    employee_id,
                    activity_start,
                    activity_end,
                    activity_type,
                    distance_m,
                    elapsed_time_s,
                    comment,
                    source
                )
                VALUES (
                    :activity_id,
                    :employee_id,
                    :activity_start,
                    :activity_end,
                    :activity_type,
                    :distance_m,
                    :elapsed_time_s,
                    :comment,
                    :source
                )
            """),
            activity
        )

def main():
    engine = get_engine()
    employee = get_employee(engine)

    before_count = int(employee["sports_activity_count"])
    missing = max(0, THRESHOLD - before_count)

    if missing == 0:
        print(f"{TARGET_EMPLOYEE} a déjà {before_count} activités ou plus.")
        return

    print(f"Salariée : {TARGET_EMPLOYEE}")
    print(f"Activités avant ajout : {before_count}")
    print(f"Activités à ajouter pour atteindre {THRESHOLD} : {missing}\n")

    for i in range(missing):
        activity = build_activity(employee["employee_id"], i + 1)
        insert_activity(engine, activity)

    print("Activités ajoutées avec succès.")
    print(f"Total ajouté : {missing}")

if __name__ == "__main__":
    main()
