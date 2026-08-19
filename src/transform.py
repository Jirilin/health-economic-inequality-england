import re

import numpy as np
import pandas as pd

from config import (
    RAW_DIR,
    PROCESSED_DIR,
    IMD_RAW_FILE,
)

def normalise_text(value):
    return (
        str(value)
        .strip()
        .lower()
        .replace("\n", " ")
    )

def find_column(df, required_terms):
    
    for column in df.columns:

        text = normalise_text(column)

        if all(
            term.lower() in text
            for term in required_terms
        ):
            return column

    raise KeyError(
        f"Unable to find column containing: {required_terms}"
    )

def detect_imd_table():
    
    workbook = pd.ExcelFile(IMD_RAW_FILE)

    for sheet in workbook.sheet_names:

        raw = pd.read_excel(
            IMD_RAW_FILE,
            sheet_name=sheet,
            header=None,
        )

        # Examine first 20 rows looking for the header
        for row_index in range(min(20, len(raw))):

            row_text = " ".join(
                raw.iloc[row_index]
                .dropna()
                .astype(str)
                .tolist()
            ).lower()

            if (
                "upper tier" in row_text
                and "local authority" in row_text
                and "code" in row_text
            ):

                df = pd.read_excel(
                    IMD_RAW_FILE,
                    sheet_name=sheet,
                    header=row_index,
                )

                return df

    raise RuntimeError(
        "Could not automatically identify IMD table."
    )


def transform_imd():
    # Detect the correct header row using the built-in function
    df = detect_imd_table()

    # 1. Locate the Local Authority Code column
    code_col = find_column(
        df, 
        ["local authority", "code"]
    )

    # 2. Locate the Local Authority Name column
    name_col = find_column(
        df, 
        ["local authority", "name"]
    )

    # 3. Locate the IMD Rank column
    rank_col = find_column(
        df, 
        [
            "rank of average score",
        ]
    )

    # 4. Locate Proportion of LSOAs in 10% most deprived
    proportion_col = find_column(
        df,
        [
            "proportion of lsoas",
        ],
    )

    result = df[
        [
            code_col,
            name_col,
            rank_col,
            proportion_col,
        ]
    ].copy()

    result.columns = [
        "area_code",
        "area_name",
        "imd_average_score_rank",
        "imd_most_deprived_10pct_share",
    ]

    result["area_code"] = (
        result["area_code"]
        .astype(str)
        .str.strip()
    )

    result["area_name"] = (
        result["area_name"]
        .astype(str)
        .str.strip()
    )

    result["imd_average_score_rank"] = pd.to_numeric(
        result["imd_average_score_rank"],
        errors="coerce",
    )

    result[
        "imd_most_deprived_10pct_share"
    ] = pd.to_numeric(
        result["imd_most_deprived_10pct_share"],
        errors="coerce",
    )

    result = result.dropna(
        subset=[
            "area_code",
            "imd_average_score_rank",
        ]
    )

    # Convert proportions from 0-1 to percentage if necessary
    if (
        result["imd_most_deprived_10pct_share"].max()
        <= 1
    ):
        result[
            "imd_most_deprived_10pct_share"
        ] *= 100

    # Higher value = MORE deprived
    number_of_areas = (
        result["imd_average_score_rank"]
        .nunique()
    )

    result["imd_deprivation_percentile"] = (
        (
            number_of_areas
            - result["imd_average_score_rank"]
        )
        / max(number_of_areas - 1, 1)
        * 100
    )

    result.to_csv(
        PROCESSED_DIR / "deprivation_utla.csv",
        index=False,
    )

    return result


def get_column(df, search_terms):

    for column in df.columns:

        text = normalise_text(column)

        for search in search_terms:

            if search.lower() == text:
                return column

    for column in df.columns:

        text = normalise_text(column)

        for search in search_terms:

            if search.lower() in text:
                return column

    raise KeyError(
        f"Column not found: {search_terms}"
    )


def period_number(period):

    # Sorting the year
    match = re.search(
        r"(19|20)\d{2}",
        str(period),
    )

    if match:
        return int(match.group())

    return -1


def prepare_indicator(
    filename,
    slug,
    valid_area_codes,
):
    
    df = pd.read_csv(
        RAW_DIR / filename,
        low_memory=False,
    )

    area_code_col = get_column(
        df,
        ["area code"],
    )

    area_name_col = get_column(
        df,
        ["area name"],
    )

    period_col = get_column(
        df,
        ["time period"],
    )

    value_col = get_column(
        df,
        ["value"],
    )

    try:
        sex_col = get_column(
            df,
            ["sex"],
        )
    except KeyError:
        sex_col = None

    working = pd.DataFrame()

    working["area_code"] = (
        df[area_code_col]
        .astype(str)
        .str.strip()
    )

    working["area_name"] = (
        df[area_name_col]
        .astype(str)
        .str.strip()
    )

    working["period"] = (
        df[period_col]
        .astype(str)
        .str.strip()
    )

    working["value"] = pd.to_numeric(
        df[value_col],
        errors="coerce",
    )

    if sex_col:
        working["sex"] = (
            df[sex_col]
            .astype(str)
            .str.strip()
        )
    else:
        working["sex"] = "Persons"

    # Only keep areas appearing in the UTLA deprivation dataset.
    working = working[
        working["area_code"].isin(
            valid_area_codes
        )
    ].copy()

    working = working.dropna(
        subset=["value"]
    )

    working["_period_order"] = (
        working["period"]
        .apply(period_number)
    )

    # Latest observation for each area + sex
    working = (
        working
        .sort_values("_period_order")
        .groupby(
            ["area_code", "sex"],
            as_index=False,
        )
        .tail(1)
    )

    working["indicator"] = slug

    return working[
        [
            "area_code",
            "area_name",
            "indicator",
            "period",
            "sex",
            "value",
        ]
    ]

def indicator_to_wide(df, slug):

    temp = df.copy()

    temp["sex_clean"] = (
        temp["sex"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    pivot = temp.pivot_table(
        index=["area_code", "area_name"],
        columns="sex_clean",
        values="value",
        aggfunc="mean",
    ).reset_index()

    pivot.columns.name = None

    rename = {}

    for col in pivot.columns:

        if col == "male":
            rename[col] = f"{slug}_male"

        elif col == "female":
            rename[col] = f"{slug}_female"

        elif col in ["persons", "person"]:
            rename[col] = f"{slug}_persons"

    pivot = pivot.rename(columns=rename)

    candidate_cols = [
        c
        for c in pivot.columns
        if c.startswith(f"{slug}_")
    ]

    persons_col = f"{slug}_persons"

    if persons_col in pivot.columns:

        pivot[f"{slug}_sex_mean"] = (
            pivot[persons_col]
        )

    else:

        sex_cols = [
            c
            for c in [
                f"{slug}_male",
                f"{slug}_female",
            ]
            if c in pivot.columns
        ]

        pivot[f"{slug}_sex_mean"] = (
            pivot[sex_cols]
            .mean(axis=1)
        )

    periods = (
        temp.groupby("area_code")["period"]
        .first()
        .rename(f"{slug}_period")
        .reset_index()
    )

    pivot = pivot.merge(
        periods,
        on="area_code",
        how="left",
    )

    return pivot


def transform_all():

    print("\n--- TRANSFORMING DATA ---")

    deprivation = transform_imd()

    area_codes = set(
        deprivation["area_code"]
    )

    indicators = []

    for filename, slug in [
        (
            "healthy_life_expectancy.csv",
            "healthy_life_expectancy",
        ),
        (
            "life_expectancy.csv",
            "life_expectancy",
        ),
        (
            "economic_inactivity.csv",
            "economic_inactivity",
        ),
    ]:

        indicator = prepare_indicator(
            filename,
            slug,
            area_codes,
        )

        indicators.append(indicator)

    indicator_long = pd.concat(
        indicators,
        ignore_index=True,
    )

    indicator_long.to_csv(
        PROCESSED_DIR
        / "indicator_latest_long.csv",
        index=False,
    )

    hle = indicator_to_wide(
        indicators[0],
        "healthy_life_expectancy",
    )

    le = indicator_to_wide(
        indicators[1],
        "life_expectancy",
    )

    inactivity = indicator_to_wide(
        indicators[2],
        "economic_inactivity",
    )

    master = deprivation.copy()

    master = master.merge(
        hle.drop(
            columns=["area_name"],
            errors="ignore",
        ),
        on="area_code",
        how="left",
    )

    master = master.merge(
        le.drop(
            columns=["area_name"],
            errors="ignore",
        ),
        on="area_code",
        how="left",
    )

    master = master.merge(
        inactivity.drop(
            columns=["area_name"],
            errors="ignore",
        ),
        on="area_code",
        how="left",
    )

    master = master.rename(
        columns={
            "economic_inactivity_sex_mean":
                "economic_inactivity_pct"
        }
    )

    # Analytical derived metric
    master["unhealthy_years_estimate"] = (
        master["life_expectancy_sex_mean"]
        - master[
            "healthy_life_expectancy_sex_mean"
        ]
    )

    master.to_csv(
        PROCESSED_DIR / "analytics_master.csv",
        index=False,
    )

    print(
        f"Master dataset contains "
        f"{len(master)} areas."
    )

    return (
        deprivation,
        indicator_long,
        master,
    )