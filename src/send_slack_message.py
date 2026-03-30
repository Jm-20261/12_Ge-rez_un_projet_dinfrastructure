import os
from pathlib import Path
import requests
import pandas as pd
from dotenv import load_dotenv
from db import get_engine

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def format_distance(distance_m):
    if distance_m is None or pd.isna(distance_m):
        return None
    return round(float(distance_m) / 1000, 1)

def format_duration(elapsed_time_s):
    if elapsed_time_s is None or pd.isna(elapsed_time_s):
        return None
    return f"{int(elapsed_time_s) // 60} min"

def build_message(employee_name, activity_type, distance_m, elapsed_time_s, comment):
    distance_km = format_distance(distance_m)
    duration_text = format_duration(elapsed_time_s)

    if activity_type == "Course à pied" and distance_km is not None and duration_text:
        text = f"Bravo {employee_name} ! Tu viens de courir {distance_km} km en {duration_text} ! Quelle énergie ! 🔥🏅"
    elif activity_type == "Randonnée" and distance_km is not None:
        text = f"Magnifique {employee_name} ! Une randonnée de {distance_km} km terminée ! 🌄🏕️"
    elif distance_km is not None and duration_text:
        text = f"Bravo {employee_name} ! Nouvelle activité : {activity_type}, {distance_km} km en {duration_text}. 💪"
    elif duration_text:
        text = f"Bravo {employee_name} ! Nouvelle activité : {activity_type}, durée {duration_text}. 💪"
    else:
        text = f"Bravo {employee_name} ! Nouvelle activité sportive enregistrée : {activity_type}. 💪"

    if comment and str(comment).strip():
        text += f'\n💬 Note du salarié : “{comment}”'

    return text

def send_latest_activity_to_slack():
    if not SLACK_WEBHOOK_URL:
        raise ValueError("SLACK_WEBHOOK_URL manquant dans le fichier .env")

    engine = get_engine()

    query = """
    SELECT
        sa.activity_id,
        sa.employee_id,
        e.full_name AS employee_name,
        sa.activity_type,
        sa.distance_m,
        sa.elapsed_time_s,
        sa.comment,
        sa.activity_start
    FROM sport_activities sa
    JOIN employees e
      ON sa.employee_id = e.employee_id
    ORDER BY sa.activity_start DESC
    LIMIT 1
    """

    df = pd.read_sql(query, engine)

    if df.empty:
        raise ValueError("Aucune activité trouvée dans sport_activities")

    row = df.iloc[0]

    message = build_message(
        employee_name=row["employee_name"],
        activity_type=row["activity_type"],
        distance_m=row["distance_m"],
        elapsed_time_s=row["elapsed_time_s"],
        comment=row["comment"]
    )

    response = requests.post(
        SLACK_WEBHOOK_URL,
        json={"text": message},
        timeout=30
    )

    print("HTTP status:", response.status_code)
    print("Réponse Slack:", response.text)
    response.raise_for_status()

    print("\nMessage envoyé :")
    print(message)

if __name__ == "__main__":
    send_latest_activity_to_slack()
