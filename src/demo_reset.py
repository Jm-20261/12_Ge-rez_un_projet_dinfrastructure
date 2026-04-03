import subprocess
import sys
from sqlalchemy import text

from db import get_engine

PYTHON_BIN = sys.executable
TARGET_EMPLOYEE_ID = "51328"


def delete_demo_activities():
    engine = get_engine()

    with engine.begin() as conn:
        result = conn.execute(
            text(
                """
                DELETE FROM sport_activities
                WHERE employee_id = :employee_id
                  AND source = 'demo_live'
                """
            ),
            {"employee_id": TARGET_EMPLOYEE_ID},
        )

    print(f"Activités demo supprimées pour employee_id={TARGET_EMPLOYEE_ID}")
    print(f"Lignes supprimées : {result.rowcount}")


def run_step(command: str):
    print(f"\n--- Exécution : {command} ---")
    result = subprocess.run(command, shell=True, text=True)

    if result.returncode != 0:
        print("\nLe reset démo s'est arrêté sur une erreur.")
        sys.exit(result.returncode)


def main():
    delete_demo_activities()

    steps = [
        f"{PYTHON_BIN} src/calculate_rewards.py",
        f"{PYTHON_BIN} src/run_quality_checks.py",
        f"{PYTHON_BIN} src/capture_kpi_snapshot.py",
        f"{PYTHON_BIN} src/capture_table_volumes.py",
    ]

    for step in steps:
        run_step(step)

    print("\nReset démo terminé avec succès.")


if __name__ == "__main__":
    main()