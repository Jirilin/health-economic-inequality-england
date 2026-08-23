import plotly.express as px
import streamlit as st

from dashboard.common import (
    load_history,
    load_forecast,
)


history = load_history()
forecast = load_forecast()


st.title(
    "Historical Trends"
)


areas = sorted(
    history["area_name"]
    .dropna()
    .unique()
)


selected_area = st.selectbox(
    "Select a local authority",
    areas,
)


indicators = sorted(
    history["indicator"]
    .unique()
)


selected_indicator = st.selectbox(
    "Select indicator",
    indicators,
)


filtered = history[
    (
        history["area_name"]
        == selected_area
    )
    &
    (
        history["indicator"]
        == selected_indicator
    )
].sort_values(
    "period_end"
)


fig = px.line(
    filtered,
    x="period_end",
    y="value",
    markers=True,

    labels={
        "period_end":
            "Period end year",

        "value":
            "Indicator value",
    },
)


st.plotly_chart(
    fig,
    use_container_width=True,
)


if (
    selected_indicator
    == "economic_inactivity"
    and not forecast.empty
):

    st.subheader(
        "Illustrative trend projection"
    )


    area_forecast = forecast[
        forecast["area_name"]
        == selected_area
    ]


    st.dataframe(
        area_forecast[
            [
                "forecast_year",
                "predicted_economic_inactivity",
                "historical_r_squared",
            ]
        ],
        use_container_width=True,
    )


    st.warning(
        "These figures are simple trend "
        "projections, not policy or economic "
        "forecasts."
    )