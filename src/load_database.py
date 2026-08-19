import sqlite3

import pandas as pd

from config import (
    PROCESSED_DIR,
    DATABASE_FILE,
)

def load_database():
    
    print("\n--- LOADING DATABASE ---")

    deprivation = pd.read_csv(
        PROCESSED_DIR / "deprivation_utla.csv"
    )

    indicators = pd.read_csv(
        PROCESSED_DIR
        / "indicator_latest_long.csv"
    )

    master = pd.read_csv(
        PROCESSED_DIR / "analytics_master.csv"
    )

    areas = (
        master[
            [
                "area_code",
                "area_name",
            ]
        ]
        .drop_duplicates()
    )

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    areas.to_sql(
        "dim_area",
        connection,
        if_exists="replace",
        index=False,
    )

    deprivation.to_sql(
        "fact_deprivation",
        connection,
        if_exists="replace",
        index=False,
    )

    indicators.to_sql(
        "fact_indicator_latest",
        connection,
        if_exists="replace",
        index=False,
    )

    master.to_sql(
        "analytics_snapshot",
        connection,
        if_exists="replace",
        index=False,
    )

    connection.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS
        idx_area_code
        ON dim_area(area_code);
        """
    )

    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_indicator_area
        ON fact_indicator_latest(area_code);
        """
    )

    connection.commit()
    connection.close()

    print(
        f"Database created: {DATABASE_FILE}"
    )