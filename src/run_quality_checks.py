import pandas as pd
from sqlalchemy import text, inspect

from db import get_engine


def run_quality_checks():
    engine = get_engine()
    results = []

    def add_check(check_name, table_name, failed_rows, description):
        status = "PASS" if failed_rows == 0 else "FAIL"
        results.append({
            "check_name": check_name,
            "table_name": table_name,
            "failed_rows": int(failed_rows),
            "status": status,
            "description": description
        })

    # 1. employees non vide
    q1 = "SELECT COUNT(*) AS cnt FROM employees"
    cnt_employees = pd.read_sql(q1, engine).iloc[0]["cnt"]
    add_check(
        "employees_not_empty",
        "employees",
        0 if cnt_employees > 0 else 1,
        "La table employees doit contenir au moins un salarié"
    )

    # 2. employee_id unique dans employees
    q2 = """
    SELECT COUNT(*) AS cnt
    FROM (
        SELECT employee_id
        FROM employees
        GROUP BY employee_id
        HAVING COUNT(*) > 1
    ) t
    """
    dup_employees = pd.read_sql(q2, engine).iloc[0]["cnt"]
    add_check(
        "employees_employee_id_unique",
        "employees",
        dup_employees,
        "employee_id doit être unique dans employees"
    )

    # 3. commute_mode autorisé
    q3 = """
    SELECT COUNT(*) AS cnt
    FROM employees
    WHERE commute_mode NOT IN (
        'Marche/Running',
        'Transports en commun',
        'Véhicule',
        'Vélo/Trottinette/Autres'
    )
    OR commute_mode IS NULL
    """
    bad_commute_mode = pd.read_sql(q3, engine).iloc[0]["cnt"]
    add_check(
        "employees_commute_mode_allowed",
        "employees",
        bad_commute_mode,
        "commute_mode doit être dans la liste autorisée"
    )

    # 4. sport_activities non vide
    q4 = "SELECT COUNT(*) AS cnt FROM sport_activities"
    cnt_activities = pd.read_sql(q4, engine).iloc[0]["cnt"]
    add_check(
        "sport_activities_not_empty",
        "sport_activities",
        0 if cnt_activities > 0 else 1,
        "La table sport_activities doit contenir des activités"
    )

    # 5. dates activité cohérentes
    q5 = """
    SELECT COUNT(*) AS cnt
    FROM sport_activities
    WHERE activity_end < activity_start
    """
    bad_dates = pd.read_sql(q5, engine).iloc[0]["cnt"]
    add_check(
        "sport_activities_dates_valid",
        "sport_activities",
        bad_dates,
        "activity_end doit être postérieure à activity_start"
    )

    # 6. distance non négative
    q6 = """
    SELECT COUNT(*) AS cnt
    FROM sport_activities
    WHERE distance_m < 0
    """
    bad_distance = pd.read_sql(q6, engine).iloc[0]["cnt"]
    add_check(
        "sport_activities_distance_non_negative",
        "sport_activities",
        bad_distance,
        "distance_m doit être positive ou nulle"
    )

    # 7. employee_id des activités existe dans employees
    q7 = """
    SELECT COUNT(*) AS cnt
    FROM sport_activities sa
    LEFT JOIN employees e
        ON sa.employee_id = e.employee_id
    WHERE e.employee_id IS NULL
    """
    orphan_activities = pd.read_sql(q7, engine).iloc[0]["cnt"]
    add_check(
        "sport_activities_employee_exists",
        "sport_activities",
        orphan_activities,
        "Chaque activité doit référencer un salarié existant"
    )

    # 8. reward_results a le bon nombre de lignes
    q8 = """
    SELECT ABS(
        (SELECT COUNT(*) FROM reward_results) -
        (SELECT COUNT(*) FROM employees)
    ) AS cnt
    """
    mismatch_rewards = pd.read_sql(q8, engine).iloc[0]["cnt"]
    add_check(
        "reward_results_same_count_as_employees",
        "reward_results",
        mismatch_rewards,
        "reward_results doit contenir une ligne par salarié"
    )

    # 9. prime_amount non négative
    q9 = """
    SELECT COUNT(*) AS cnt
    FROM reward_results
    WHERE prime_amount < 0
    """
    bad_prime = pd.read_sql(q9, engine).iloc[0]["cnt"]
    add_check(
        "reward_results_prime_non_negative",
        "reward_results",
        bad_prime,
        "prime_amount doit être positive ou nulle"
    )

    # 10. wellbeing_days_awarded vaut 0 ou 5
    q10 = """
    SELECT COUNT(*) AS cnt
    FROM reward_results
    WHERE wellbeing_days_awarded NOT IN (0, 5)
    """
    bad_wellbeing_days = pd.read_sql(q10, engine).iloc[0]["cnt"]
    add_check(
        "reward_results_wellbeing_days_allowed",
        "reward_results",
        bad_wellbeing_days,
        "wellbeing_days_awarded doit valoir 0 ou 5"
    )

    # 11. validation_status autorisé
    q11 = """
    SELECT COUNT(*) AS cnt
    FROM commute_checks
    WHERE validation_status NOT IN ('VALID', 'TO_REVIEW', 'ERROR', 'NOT_APPLICABLE', 'PENDING_API_KEY')
    """
    bad_validation_status = pd.read_sql(q11, engine).iloc[0]["cnt"]
    add_check(
        "commute_checks_validation_status_allowed",
        "commute_checks",
        bad_validation_status,
        "validation_status doit être dans la liste autorisée"
    )

    results_df = pd.DataFrame(results)

    inspector = inspect(engine)
    if inspector.has_table("quality_checks_results"):
        with engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE quality_checks_results"))

    results_df.to_sql("quality_checks_results", engine, if_exists="append", index=False)

    print("Tests qualité terminés.\n")
    print(results_df)

    nb_pass = (results_df["status"] == "PASS").sum()
    nb_fail = (results_df["status"] == "FAIL").sum()

    print(f"\nPASS : {nb_pass}")
    print(f"FAIL : {nb_fail}")


if __name__ == "__main__":
    run_quality_checks()