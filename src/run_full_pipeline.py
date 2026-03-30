import subprocess
import pandas as pd
from sqlalchemy import text
from db import get_engine

STEPS = [
    ("load_raw_data", "python src/load_raw_data.py", "rh_raw", "sport_raw"),
    ("build_business_tables", "python src/build_business_tables.py", "employees", "employee_sports"),
    ("clean_business_data", "python src/clean_business_data.py", "employees", "employee_sports"),
    ("simulate_sport_activities", "python src/simulate_sport_activities.py", "sport_activities", None),
    ("load_reward_parameters", "python src/load_reward_parameters.py", "reward_parameters", None),
    ("check_commutes", "python src/check_commutes.py", "commute_checks", None),
    ("calculate_rewards", "python src/calculate_rewards.py", "reward_results", None),
    ("run_quality_checks", "python src/run_quality_checks.py", "quality_checks_results", None),
]

def count_rows(table_name, engine):
    if not table_name:
        return 0
    q = f"SELECT COUNT(*) AS cnt FROM {table_name}"
    return int(pd.read_sql(q, engine).iloc[0]["cnt"])

def log_run(step_name, status, rows_processed, message, engine):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO pipeline_runs (step_name, status, rows_processed, message)
                VALUES (:step_name, :status, :rows_processed, :message)
            """),
            {
                "step_name": step_name,
                "status": status,
                "rows_processed": rows_processed,
                "message": message[:500] if message else None
            }
        )

def run_pipeline():
    engine = get_engine()

    for step_name, command, table_1, table_2 in STEPS:
        print(f"\n--- Lancement : {step_name} ---")

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        output = (result.stdout or "") + "\n" + (result.stderr or "")

        if result.returncode == 0:
            rows_processed = count_rows(table_1, engine)
            if table_2:
                rows_processed += count_rows(table_2, engine)

            log_run(
                step_name=step_name,
                status="SUCCESS",
                rows_processed=rows_processed,
                message=output.strip(),
                engine=engine
            )
            print(f"SUCCESS - {step_name}")
        else:
            log_run(
                step_name=step_name,
                status="FAILED",
                rows_processed=0,
                message=output.strip(),
                engine=engine
            )
            print(f"FAILED - {step_name}")
            print(output)
            break

    print("\nPipeline terminé.")

if __name__ == "__main__":
    run_pipeline()
