import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import text

from db import get_engine

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def load_reward_parameters():
    engine = get_engine()

    parameters = [
        {
            "parameter_name": "PRIME_RATE",
            "parameter_value": float(os.getenv("PRIME_RATE", "0.05")),
            "description": "Taux de prime sportive"
        },
        {
            "parameter_name": "MIN_ACTIVITIES_FOR_WELLBEING",
            "parameter_value": float(os.getenv("MIN_ACTIVITIES_FOR_WELLBEING", "15")),
            "description": "Nombre minimal d'activités pour obtenir 5 jours bien-être"
        },
        {
            "parameter_name": "MAX_DISTANCE_WALK_RUN_KM",
            "parameter_value": float(os.getenv("MAX_DISTANCE_WALK_RUN_KM", "15")),
            "description": "Distance maximale marche/running"
        },
        {
            "parameter_name": "MAX_DISTANCE_BIKE_OTHER_KM",
            "parameter_value": float(os.getenv("MAX_DISTANCE_BIKE_OTHER_KM", "25")),
            "description": "Distance maximale vélo/trottinette/autres"
        },
    ]

    df = pd.DataFrame(parameters)

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE reward_parameters"))

    df.to_sql("reward_parameters", engine, if_exists="append", index=False)

    print("Paramètres chargés.")
    print(df)


if __name__ == "__main__":
    load_reward_parameters()