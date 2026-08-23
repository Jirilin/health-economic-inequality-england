import sqlite3

import pandas as pd

from config import (
    PROCESSED_DIR,
    DATABASE_FILE,
)


TABLES = {

    "analytics_enriched":
        "analytics_enriched.csv",

    "indicator_history":
        "indicator_history.csv",

    "area_trends":
        "area_trends.csv",

    "cluster_profiles":
        "cluster_profiles.csv",

    "economic_inactivity_forecast":
        "economic_inactivity_forecast.csv",
}


def load_advanced_database():

    print(
        "\n--- LOADING ADVANCED TABLES ---"
    )


    connection = sqlite3.connect(
        DATABASE_FILE
    )


    for table, filename in (
        TABLES.items()
    ):

        file = (
            PROCESSED_DIR
            / filename
        )


        if not file.exists():
            continue


        df = pd.read_csv(
            file
        )


        df.to_sql(
            table,
            connection,
            if_exists="replace",
            index=False,
        )


        print(
            f"Loaded: {table}"
        )


    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_history_area
        ON indicator_history(area_code);
        """
    )


    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_history_indicator
        ON indicator_history(indicator);
        """
    )


    connection.commit()

    connection.close()