import pandas as pd
from sqlalchemy import text

from db import get_engine

TARGET_EMPLOYEE_ID = "51328"


def main():
    engine = get_engine()

    query = """
    SELECT
        employee_id,
        employee_name,
        sports_activity_count,
        wellbeing_days_eligible,
        wellbeing_days_awarded,
        prime_amount
    FROM reward_results
    WHERE employee_id = :employee_id
    """

    with engine.begin() as conn:
        df = pd.read_sql(text(query), conn, params={"employee_id": TARGET_EMPLOYEE_ID})

    if df.empty:
        print(f"Aucun résultat trouvé pour employee_id={TARGET_EMPLOYEE_ID}")
        return

    row = df.iloc[0]

    print("\nÉtat actuel du salarié pour la démo :")
    print(f"Employee ID : {row['employee_id']}")
    print(f"Nom : {row['employee_name']}")
    print(f"Activités sportives : {row['sports_activity_count']}")
    print(f"Éligible bien-être : {row['wellbeing_days_eligible']}")
    print(f"Jours bien-être accordés : {row['wellbeing_days_awarded']}")
    print(f"Montant prime : {row['prime_amount']}")


if __name__ == "__main__":
    main()