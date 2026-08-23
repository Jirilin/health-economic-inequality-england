import json

import pandas as pd

from config import (
    PROCESSED_DIR,
    OUTPUT_DIR,
)


def run_quality_checks():

    print(
        "\n--- DATA QUALITY ---"
    )


    df = pd.read_csv(
        PROCESSED_DIR
        / "analytics_enriched.csv"
    )


    history = pd.read_csv(
        PROCESSED_DIR
        / "indicator_history.csv"
    )


    report = {}


    # Duplicate geography

    duplicate_codes = (
        df["area_code"]
        .duplicated()
        .sum()
    )


    report[
        "duplicate_area_codes"
    ] = int(
        duplicate_codes
    )


    # Core missingness

    columns = [
        "imd_deprivation_percentile",
        "healthy_life_expectancy_sex_mean",
        "economic_inactivity_pct",
        "vulnerability_score",
    ]


    missing = {}


    for column in columns:

        if column in df.columns:

            missing[column] = float(
                df[column]
                .isna()
                .mean()
            )


    report[
        "missingness_rate"
    ] = missing


    # Score range

    score_valid = (
        df["vulnerability_score"]
        .dropna()
        .between(
            0,
            100,
        )
        .all()
    )


    report[
        "vulnerability_score_valid"
    ] = bool(
        score_valid
    )


    # History

    report[
        "historical_observations"
    ] = int(
        len(history)
    )


    report[
        "historical_indicators"
    ] = int(
        history[
            "indicator"
        ]
        .nunique()
    )


    report[
        "areas_in_master"
    ] = int(
        df[
            "area_code"
        ]
        .nunique()
    )


    quality_folder = (
        OUTPUT_DIR
        / "quality"
    )


    quality_folder.mkdir(
        parents=True,
        exist_ok=True,
    )


    with open(
        quality_folder
        / "quality_report.json",
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            report,
            file,
            indent=2,
        )


    # Critical failures
    assert (
        duplicate_codes == 0
    ), (
        "Duplicate area codes found."
    )


    assert score_valid, (
        "HEIVA scores outside 0-100."
    )


    print(
        "Quality checks passed."
    )


    return report