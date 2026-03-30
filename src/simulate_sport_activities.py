import random
from datetime import datetime, timedelta
import uuid
import pandas as pd
from sqlalchemy import text
from db import get_engine

SPORT_RULES = {
    "Course à pied": {"min_per_month": 2, "max_per_month": 8, "distance_min": 3000, "distance_max": 20000},
    "Randonnée": {"min_per_month": 1, "max_per_month": 3, "distance_min": 5000, "distance_max": 25000},
    "Natation": {"min_per_month": 2, "max_per_month": 6, "distance_min": 500, "distance_max": 4000},
    "Vélo": {"min_per_month": 2, "max_per_month": 6, "distance_min": 5000, "distance_max": 50000},
    "Escalade": {"min_per_month": 1, "max_per_month": 4, "distance_min": None, "distance_max": None},
    "Football": {"min_per_month": 2, "max_per_month": 5, "distance_min": 2000, "distance_max": 8000},
    "Tennis": {"min_per_month": 2, "max_per_month": 5, "distance_min": 1000, "distance_max": 5000},
    "Basketball": {"min_per_month": 2, "max_per_month": 5, "distance_min": 1500, "distance_max": 6000},
    "Badminton": {"min_per_month": 2, "max_per_month": 5, "distance_min": 1000, "distance_max": 4000},
    "Boxe": {"min_per_month": 2, "max_per_month": 5, "distance_min": None, "distance_max": None},
    "Judo": {"min_per_month": 2, "max_per_month": 5, "distance_min": None, "distance_max": None},
    "Rugby": {"min_per_month": 1, "max_per_month": 4, "distance_min": 2000, "distance_max": 7000},
    "Triathlon": {"min_per_month": 1, "max_per_month": 3, "distance_min": 10000, "distance_max": 60000},
    "Voile": {"min_per_month": 1, "max_per_month": 3, "distance_min": None, "distance_max": None},
    "Équitation": {"min_per_month": 1, "max_per_month": 4, "distance_min": None, "distance_max": None},
}

COMMENTS = {
    "Course à pied": ["Belle sortie !", "Très bonnes sensations.", "Reprise du sport :)", None],
    "Randonnée": ["Super spot à découvrir !", "Magnifique parcours.", None],
    "Natation": ["Bonne séance piscine.", None],
    "Escalade": ["Séance technique.", "Belle progression.", None],
    "Football": ["Match intense !", None],
    "Tennis": ["Bon entraînement.", None],
}

def random_elapsed_time(distance_m, sport):
    if sport == "Course à pied":
        return random.randint(int(distance_m / 4), int(distance_m / 2.2))
    if sport == "Randonnée":
        return random.randint(int(distance_m / 1.2), int(distance_m / 0.7))
    if sport == "Natation":
        return random.randint(1200, 5400)
    if sport in ["Escalade", "Boxe", "Judo", "Voile", "Équitation"]:
        return random.randint(3600, 9000)
    return random.randint(1800, 7200)

def build_comment(sport):
    values = COMMENTS.get(sport, [None, None, "Bonne séance."])
    return random.choice(values)

def simulate_sport_activities():
    engine = get_engine()

    employees_df = pd.read_sql("SELECT employee_id, full_name FROM employees", engine)
    sports_df = pd.read_sql("""
        SELECT employee_id, main_sport
        FROM employee_sports
        WHERE main_sport IS NOT NULL
    """, engine)

    merged_df = employees_df.merge(sports_df, on="employee_id", how="inner")

    activities = []
    today = datetime.now()
    start_period = today - timedelta(days=365)

    for _, row in merged_df.iterrows():
        employee_id = row["employee_id"]
        sport = row["main_sport"]

        rules = SPORT_RULES.get(
            sport,
            {"min_per_month": 1, "max_per_month": 4, "distance_min": 1000, "distance_max": 10000}
        )

        for month_index in range(12):
            month_start = start_period + timedelta(days=30 * month_index)
            activity_count = random.randint(rules["min_per_month"], rules["max_per_month"])

            for _ in range(activity_count):
                day_offset = random.randint(0, 27)
                start_hour = random.randint(6, 20)
                start_minute = random.choice([0, 10, 15, 20, 30, 40, 45, 50])

                activity_start = month_start + timedelta(days=day_offset, hours=start_hour, minutes=start_minute)

                if rules["distance_min"] is None:
                    distance_m = None
                else:
                    distance_m = random.randint(rules["distance_min"], rules["distance_max"])

                elapsed_time_s = random_elapsed_time(distance_m if distance_m else 5000, sport)
                activity_end = activity_start + timedelta(seconds=elapsed_time_s)

                activities.append({
                    "activity_id": str(uuid.uuid4()),
                    "employee_id": str(employee_id),
                    "activity_start": activity_start,
                    "activity_end": activity_end,
                    "activity_type": sport,
                    "distance_m": distance_m,
                    "elapsed_time_s": elapsed_time_s,
                    "comment": build_comment(sport),
                    "source": "simulation"
                })

    activities_df = pd.DataFrame(activities)

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE sport_activities"))

    activities_df.to_sql("sport_activities", engine, if_exists="append", index=False)

    print("Simulation terminée.")
    print(f"sport_activities : {len(activities_df)} lignes")

    print("\nRépartition des 5 premiers sports :")
    print(activities_df["activity_type"].value_counts().head())

if __name__ == "__main__":
    simulate_sport_activities()
