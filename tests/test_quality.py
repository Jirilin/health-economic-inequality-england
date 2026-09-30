import pandas as pd

from config import PROCESSED_DIR


DATA_FILE = (
    PROCESSED_DIR
    / "analytics_enriched.csv"
)


def load_data():
    assert DATA_FILE.exists(), (
        f"Processed dataset not found: {DATA_FILE}"
    )

    return pd.read_csv(DATA_FILE)


def test_dataset_not_empty():
    df = load_data()

    assert not df.empty


def test_required_columns_exist():
    df = load_data()

    required = {
        "area_code",
        "area_name",
        "imd_deprivation_percentile",
        "healthy_life_expectancy_sex_mean",
        "economic_inactivity_pct",
        "vulnerability_score",
    }

    missing = required - set(df.columns)

    assert not missing, (
        f"Missing required columns: {missing}"
    )


def test_area_codes_not_missing():
    df = load_data()

    assert df["area_code"].notna().all()


def test_area_codes_unique():
    df = load_data()

    duplicates = (
        df.loc[
            df["area_code"].duplicated(False),
            ["area_code", "area_name"],
        ]
    )

    assert duplicates.empty, (
        "Duplicate area codes found:\n"
        f"{duplicates.to_string(index=False)}"
    )


def test_area_names_not_missing():
    df = load_data()

    assert df["area_name"].notna().all()


def test_deprivation_range():
    df = load_data()

    values = (
        df["imd_deprivation_percentile"]
        .dropna()
    )

    assert values.between(0, 100).all()


def test_economic_inactivity_range():
    df = load_data()

    values = (
        df["economic_inactivity_pct"]
        .dropna()
    )

    assert values.between(0, 100).all()


def test_heiva_score_range():
    df = load_data()

    values = (
        df["vulnerability_score"]
        .dropna()
    )

    assert values.between(0, 100).all()


def test_deprivation_missingness():
    df = load_data()

    missing_rate = (
        df["imd_deprivation_percentile"]
        .isna()
        .mean()
    )

    assert missing_rate == 0


def test_hle_missingness_below_threshold():
    df = load_data()

    missing_rate = (
        df["healthy_life_expectancy_sex_mean"]
        .isna()
        .mean()
    )

    assert missing_rate <= 0.02, (
        f"HLE missingness is "
        f"{missing_rate:.2%}"
    )


def test_economic_missingness_below_threshold():
    df = load_data()

    missing_rate = (
        df["economic_inactivity_pct"]
        .isna()
        .mean()
    )

    assert missing_rate <= 0.01, (
        f"Economic inactivity missingness is "
        f"{missing_rate:.2%}"
    )