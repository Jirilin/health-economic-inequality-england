import pandas as pd

from config import PROCESSED_DIR


def test_area_codes_unique():

    df = pd.read_csv(
        PROCESSED_DIR
        / "analytics_enriched.csv"
    )

    assert (
        df["area_code"]
        .is_unique
    )


def test_heiva_score_range():

    df = pd.read_csv(
        PROCESSED_DIR
        / "analytics_enriched.csv"
    )

    scores = (
        df["vulnerability_score"]
        .dropna()
    )

    assert scores.between(
        0,
        100,
    ).all()


def test_core_health_data_exists():

    df = pd.read_csv(
        PROCESSED_DIR
        / "analytics_enriched.csv"
    )

    assert (
        df[
            "healthy_life_expectancy_sex_mean"
        ]
        .notna()
        .any()
    )


def test_economic_data_exists():

    df = pd.read_csv(
        PROCESSED_DIR
        / "analytics_enriched.csv"
    )

    assert (
        df[
            "economic_inactivity_pct"
        ]
        .notna()
        .any()
    )