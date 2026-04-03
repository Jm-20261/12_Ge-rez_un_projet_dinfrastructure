import pandas as pd

from db import get_engine


def capture_kpi_snapshot():
    engine = get_engine()

    df = pd.read_sql("SELECT * FROM vw_kpi_summary", engine)

    df.to_sql("kpi_history", engine, if_exists="append", index=False)

    print("Snapshot KPI enregistré.")
    print(df)


if __name__ == "__main__":
    capture_kpi_snapshot()
