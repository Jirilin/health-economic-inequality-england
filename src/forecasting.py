import pandas as pd

from sklearn.linear_model import (
    LinearRegression
)

from config import PROCESSED_DIR


def forecast_economic_inactivity():

    print(
        "\n--- FORECASTING ---"
    )

    history = pd.read_csv(
        PROCESSED_DIR
        / "indicator_history.csv"
    )


    history = history[
        history["indicator"]
        == "economic_inactivity"
    ].copy()


    results = []


    for (
        area_code,
        area_name
    ), group in history.groupby(
        [
            "area_code",
            "area_name",
        ]
    ):

        annual = (
            group
            .groupby(
                "period_end",
                as_index=False,
            )["value"]
            .mean()
            .dropna()
            .sort_values(
                "period_end"
            )
        )


        # Require reasonable history
        if len(annual) < 4:
            continue


        X = annual[
            ["period_end"]
        ]

        y = annual[
            "value"
        ]


        model = LinearRegression()

        model.fit(
            X,
            y,
        )


        latest_year = int(
            annual[
                "period_end"
            ].max()
        )


        score = model.score(
            X,
            y,
        )


        for years_ahead in [
            1,
            2,
        ]:

            year = (
                latest_year
                + years_ahead
            )


            prediction = model.predict(
                pd.DataFrame(
                    {
                        "period_end":
                            [year]
                    }
                )
            )[0]


            # Economic inactivity is a %
            prediction = max(
                0,
                min(
                    100,
                    prediction,
                )
            )


            results.append(
                {
                    "area_code":
                        area_code,

                    "area_name":
                        area_name,

                    "forecast_year":
                        year,

                    "predicted_economic_inactivity":
                        prediction,

                    "historical_r_squared":
                        score,

                    "observations":
                        len(annual),

                    "forecast_type":
                        "Illustrative linear trend projection",
                }
            )


    forecast = pd.DataFrame(
        results
    )


    forecast.to_csv(
        PROCESSED_DIR
        / "economic_inactivity_forecast.csv",
        index=False,
    )


    print(
        f"Forecast rows: "
        f"{len(forecast)}"
    )

    return forecast