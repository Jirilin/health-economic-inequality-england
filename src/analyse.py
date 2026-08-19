import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

from config import (
    PROCESSED_DIR,
    CHART_DIR,
    TABLE_DIR,
    REPORT_DIR,
)


def minmax(series, reverse=False):
    """
    Convert values to range 0-1.

    reverse=True means low original values
    produce high risk scores.
    """

    series = pd.to_numeric(
        series,
        errors="coerce",
    )

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        result = pd.Series(
            0.5,
            index=series.index,
        )

    else:
        result = (
            (series - minimum)
            / (maximum - minimum)
        )

    if reverse:
        result = 1 - result

    return result


def create_vulnerability_score(df):
    """
    Experimental composite score.

    IMPORTANT:
    This is a project-defined analytical score,
    not an official government statistic.
    """

    result = df.copy()

    result["deprivation_risk"] = minmax(
        result["imd_deprivation_percentile"]
    )

    result["health_risk"] = minmax(
        result[
            "healthy_life_expectancy_sex_mean"
        ],
        reverse=True,
    )

    result["economic_risk"] = minmax(
        result["economic_inactivity_pct"]
    )

    # Equal weighting
    result["vulnerability_score"] = (
        result[
            [
                "deprivation_risk",
                "health_risk",
                "economic_risk",
            ]
        ]
        .mean(axis=1)
        * 100
    )

    result["vulnerability_percentile"] = (
        result["vulnerability_score"]
        .rank(pct=True)
        * 100
    )

    result["vulnerability_band"] = pd.cut(
        result["vulnerability_percentile"],
        bins=[0, 25, 50, 75, 100],
        labels=[
            "Lower",
            "Moderate",
            "High",
            "Very High",
        ],
        include_lowest=True,
    )

    return result


def run_correlations(df):

    columns = [
        "imd_deprivation_percentile",
        "healthy_life_expectancy_sex_mean",
        "life_expectancy_sex_mean",
        "economic_inactivity_pct",
        "unhealthy_years_estimate",
    ]

    available = [
        column
        for column in columns
        if column in df.columns
    ]

    correlation = (
        df[available]
        .corr(method="pearson")
    )

    correlation.to_csv(
        TABLE_DIR / "correlation_matrix.csv"
    )

    return correlation


def run_regression(df):
    """
    Exploratory association model.

    HLE =
        deprivation
        + economic inactivity

    This must NOT be described as causal.
    """

    model_data = df[
        [
            "healthy_life_expectancy_sex_mean",
            "imd_deprivation_percentile",
            "economic_inactivity_pct",
        ]
    ].dropna()

    if len(model_data) < 10:

        print(
            "Not enough observations "
            "for regression."
        )

        return None

    y = model_data[
        "healthy_life_expectancy_sex_mean"
    ]

    X = model_data[
        [
            "imd_deprivation_percentile",
            "economic_inactivity_pct",
        ]
    ]

    X = sm.add_constant(X)

    model = sm.OLS(
        y,
        X,
    ).fit()

    with open(
        REPORT_DIR / "regression_summary.txt",
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            model.summary().as_text()
        )

    return model


def create_charts(df, correlation):

    clean = df.dropna(
        subset=[
            "imd_deprivation_percentile",
            "healthy_life_expectancy_sex_mean",
        ]
    )

    # -------------------------------------
    # Chart 1
    # -------------------------------------

    plt.figure(figsize=(9, 6))

    plt.scatter(
        clean["imd_deprivation_percentile"],
        clean[
            "healthy_life_expectancy_sex_mean"
        ],
        alpha=0.7,
    )

    plt.xlabel(
        "Deprivation percentile "
        "(higher = more deprived)"
    )

    plt.ylabel(
        "Healthy life expectancy (years)"
    )

    plt.title(
        "Deprivation vs Healthy Life Expectancy"
    )

    plt.tight_layout()

    plt.savefig(
        CHART_DIR / "deprivation_vs_hle.png",
        dpi=300,
    )

    plt.close()


    # -------------------------------------
    # Chart 2
    # -------------------------------------

    clean = df.dropna(
        subset=[
            "healthy_life_expectancy_sex_mean",
            "economic_inactivity_pct",
        ]
    )

    plt.figure(figsize=(9, 6))

    plt.scatter(
        clean[
            "healthy_life_expectancy_sex_mean"
        ],
        clean["economic_inactivity_pct"],
        alpha=0.7,
    )

    plt.xlabel(
        "Healthy life expectancy (years)"
    )

    plt.ylabel(
        "Economic inactivity (%)"
    )

    plt.title(
        "Healthy Life Expectancy "
        "vs Economic Inactivity"
    )

    plt.tight_layout()

    plt.savefig(
        CHART_DIR / "health_vs_inactivity.png",
        dpi=300,
    )

    plt.close()


    # -------------------------------------
    # Chart 3
    # -------------------------------------

    top = (
        df.dropna(
            subset=["vulnerability_score"]
        )
        .nlargest(
            15,
            "vulnerability_score",
        )
        .sort_values(
            "vulnerability_score"
        )
    )

    plt.figure(figsize=(10, 7))

    plt.barh(
        top["area_name"],
        top["vulnerability_score"],
    )

    plt.xlabel(
        "Vulnerability Score (0-100)"
    )

    plt.ylabel(
        "Upper-tier Local Authority"
    )

    plt.title(
        "Highest Combined Health "
        "and Economic Vulnerability"
    )

    plt.tight_layout()

    plt.savefig(
        CHART_DIR
        / "top_vulnerability_areas.png",
        dpi=300,
    )

    plt.close()


    # -------------------------------------
    # Chart 4 - correlation matrix
    # -------------------------------------

    plt.figure(figsize=(9, 7))

    plt.imshow(
        correlation,
        aspect="auto",
    )

    plt.colorbar(
        label="Pearson correlation"
    )

    plt.xticks(
        range(len(correlation.columns)),
        correlation.columns,
        rotation=45,
        ha="right",
    )

    plt.yticks(
        range(len(correlation.index)),
        correlation.index,
    )

    for i in range(len(correlation.index)):
        for j in range(
            len(correlation.columns)
        ):

            value = correlation.iloc[i, j]

            plt.text(
                j,
                i,
                f"{value:.2f}",
                ha="center",
                va="center",
            )

    plt.title(
        "Correlation Matrix"
    )

    plt.tight_layout()

    plt.savefig(
        CHART_DIR
        / "correlation_matrix.png",
        dpi=300,
    )

    plt.close()


def run_analysis():

    print("\n--- RUNNING ANALYSIS ---")

    df = pd.read_csv(
        PROCESSED_DIR
        / "analytics_master.csv"
    )

    df = create_vulnerability_score(df)

    # Replace master dataset with
    # vulnerability measures included.
    df.to_csv(
        PROCESSED_DIR
        / "analytics_master.csv",
        index=False,
    )

    ranking = (
        df.sort_values(
            "vulnerability_score",
            ascending=False,
        )
    )

    ranking.to_csv(
        TABLE_DIR
        / "vulnerability_ranking.csv",
        index=False,
    )

    ranking.head(20).to_csv(
        TABLE_DIR
        / "top_vulnerability_areas.csv",
        index=False,
    )

    correlation = run_correlations(df)

    model = run_regression(df)

    create_charts(
        df,
        correlation,
    )

    print("Analysis completed.")

    if model is not None:

        print(
            f"Regression R-squared: "
            f"{model.rsquared:.3f}"
        )

    return df