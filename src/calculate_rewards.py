import pandas as pd
from sqlalchemy import text
from db import get_engine

def calculate_rewards():
    engine = get_engine()

    employees_df = pd.read_sql("""
        SELECT employee_id, full_name, commute_mode, salary_annual_gross
        FROM employees
    """, engine)

    activities_df = pd.read_sql("""
        SELECT employee_id, COUNT(*) AS sports_activity_count
        FROM sport_activities
        GROUP BY employee_id
    """, engine)

    parameters_df = pd.read_sql("SELECT * FROM reward_parameters", engine)
    params = dict(zip(parameters_df["parameter_name"], parameters_df["parameter_value"]))

    commute_checks_df = pd.read_sql("""
        SELECT employee_id, validation_status
        FROM commute_checks
    """, engine)

    prime_rate = float(params["PRIME_RATE"])
    min_activities = int(params["MIN_ACTIVITIES_FOR_WELLBEING"])

    result_df = employees_df.merge(activities_df, on="employee_id", how="left")
    result_df = result_df.merge(commute_checks_df, on="employee_id", how="left")

    result_df["sports_activity_count"] = result_df["sports_activity_count"].fillna(0).astype(int)
    result_df["validation_status"] = result_df["validation_status"].fillna("NOT_CHECKED")

    result_df["commute_eligible"] = result_df["validation_status"].eq("VALID")
    result_df["wellbeing_days_eligible"] = result_df["sports_activity_count"] >= min_activities
    result_df["wellbeing_days_awarded"] = result_df["wellbeing_days_eligible"].apply(lambda x: 5 if x else 0)

    result_df["prime_rate"] = result_df["commute_eligible"].apply(lambda x: prime_rate if x else 0.0)
    result_df["prime_amount"] = result_df["salary_annual_gross"] * result_df["prime_rate"]
    result_df["estimated_total_cost"] = result_df["prime_amount"]

    final_df = result_df[[
        "employee_id",
        "full_name",
        "salary_annual_gross",
        "commute_mode",
        "validation_status",
        "commute_eligible",
        "sports_activity_count",
        "wellbeing_days_eligible",
        "wellbeing_days_awarded",
        "prime_rate",
        "prime_amount",
        "estimated_total_cost"
    ]].copy()

    final_df = final_df.rename(columns={"full_name": "employee_name"})
    final_df["year_ref"] = pd.Timestamp.now().year

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE reward_results"))

    final_df.to_sql("reward_results", engine, if_exists="append", index=False)

    print("Calcul des avantages terminé.")
    print(f"reward_results : {len(final_df)} lignes")
    print(f"Coût total estimé des primes : {final_df['prime_amount'].sum():,.2f} €")
    print(f"Salariés éligibles à la prime : {final_df['commute_eligible'].sum()}")
    print(f"Salariés éligibles aux 5 jours : {final_df['wellbeing_days_eligible'].sum()}")

if __name__ == "__main__":
    calculate_rewards()
