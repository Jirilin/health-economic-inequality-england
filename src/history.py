import re

import pandas as pd

from config import RAW_DIR, PROCESSED_DIR


INDICATOR_FILES = {
    "healthy_life_expectancy":
        "healthy_life_expectancy.csv",

    "life_expectancy":
        "life_expectancy.csv",

    "economic_inactivity":
        "economic_inactivity.csv",
}


def find_column(df, names):
    
    for column in df.columns:

        clean = str(column).strip().lower()

        for name in names:

            if name.lower() == clean:
                return column

    for column in df.columns:

        clean = str(column).strip().lower()

        for name in names:

            if name.lower() in clean:
                return column

    raise KeyError(
        f"Could not find column: {names}"
    )


def parse_period(period):
    """
    Convert periods such as:

    2024
    2024/25
    2022 - 24
    2022 - 2024

    into start and end years.
    """

    text = str(period).strip()

    full_years = re.findall(
        r"(?:19|20)\d{2}",
        text,
    )

    if len(full_years) >= 2:

        return (
            int(full_years[0]),
            int(full_years[-1]),
        )

    shortened = re.search(
        r"((?:19|20)\d{2})\D+(\d{2})\b",
        text,
    )

    if shortened:

        start = int(shortened.group(1))

        short_end = int(
            shortened.group(2)
        )

        century = (
            start // 100
        ) * 100

        end = century + short_end

        if end < start:
            end += 100

        return start, end

    if len(full_years) == 1:

        year = int(full_years[0])

        return year, year

    return None, None


def prepare_indicator_history(
    filename,
    indicator_name,
    valid_codes,
):

    df = pd.read_csv(
        RAW_DIR / filename,
        low_memory=False,
    )

    area_code_col = find_column(
        df,
        ["area code"],
    )

    area_name_col = find_column(
        df,
        ["area name"],
    )

    period_col = find_column(
        df,
        ["time period"],
    )

    value_col = find_column(
        df,
        ["value"],
    )

    try:

        sex_col = find_column(
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


    working = working[
        working["area_code"]
        .isin(valid_codes)
    ].copy()


    working = working.dropna(
        subset=["value"]
    )


    bounds = (
        working["period"]
        .apply(parse_period)
    )

    working["period_start"] = [
        value[0]
        for value in bounds
    ]

    working["period_end"] = [
        value[1]
        for value in bounds
    ]


    working = working.dropna(
        subset=["period_end"]
    )


    keys = [
        "area_code",
        "area_name",
        "period",
        "period_start",
        "period_end",
    ]


    rows = []

    for key, group in working.groupby(
        keys,
        dropna=False,
    ):

        persons = group[
            group["sex"]
            .str.lower()
            .isin(
                [
                    "persons",
                    "person",
                    "all",
                ]
            )
        ]

        if len(persons) > 0:

            value = persons[
                "value"
            ].mean()

        else:

            # If Persons is unavailable,
            # average available sex values.
            value = group[
                "value"
            ].mean()


        rows.append(
            {
                "area_code": key[0],
                "area_name": key[1],
                "period": key[2],
                "period_start": key[3],
                "period_end": key[4],
                "indicator":
                    indicator_name,
                "value": value,
            }
        )


    return pd.DataFrame(rows)


def create_trend_summary(history):

    records = []

    for (
        area_code,
        area_name,
        indicator
    ), group in history.groupby(
        [
            "area_code",
            "area_name",
            "indicator",
        ]
    ):

        group = (
            group
            .sort_values("period_end")
            .dropna(subset=["value"])
        )

        if len(group) < 2:
            continue


        first = group.iloc[0]
        latest = group.iloc[-1]

        change = (
            latest["value"]
            - first["value"]
        )


        years = (
            latest["period_end"]
            - first["period_end"]
        )


        if first["value"] != 0:

            pct_change = (
                change
                / abs(first["value"])
                * 100
            )

        else:

            pct_change = None


        annual_change = (
            change / years
            if years > 0
            else None
        )


        records.append(
            {
                "area_code":
                    area_code,

                "area_name":
                    area_name,

                "indicator":
                    indicator,

                "first_period":
                    first["period"],

                "latest_period":
                    latest["period"],

                "first_value":
                    first["value"],

                "latest_value":
                    latest["value"],

                "absolute_change":
                    change,

                "percentage_change":
                    pct_change,

                "annualised_change":
                    annual_change,

                "observations":
                    len(group),
            }
        )


    return pd.DataFrame(records)


def build_history():

    print(
        "\n--- BUILDING HISTORY ---"
    )

    master = pd.read_csv(
        PROCESSED_DIR
        / "analytics_master.csv"
    )

    valid_codes = set(
        master["area_code"]
        .astype(str)
    )


    datasets = []

    for indicator, filename in (
        INDICATOR_FILES.items()
    ):

        temp = prepare_indicator_history(
            filename,
            indicator,
            valid_codes,
        )

        datasets.append(temp)


    history = pd.concat(
        datasets,
        ignore_index=True,
    )


    history.to_csv(
        PROCESSED_DIR
        / "indicator_history.csv",
        index=False,
    )


    trends = create_trend_summary(
        history
    )


    trends.to_csv(
        PROCESSED_DIR
        / "area_trends.csv",
        index=False,
    )


    print(
        f"Historical observations: "
        f"{len(history)}"
    )

    return history, trends