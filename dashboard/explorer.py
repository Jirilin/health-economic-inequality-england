import plotly.express as px
import streamlit as st

from dashboard.common import (
    load_enriched,
    load_geojson,
)


df = load_enriched()
geojson = load_geojson()


st.title(
    "Local Authority Explorer"
)


area = st.selectbox(
    "Select local authority",
    sorted(
        df["area_name"]
        .dropna()
        .unique()
    ),
)


row = df[
    df["area_name"]
    == area
].iloc[0]


c1, c2, c3, c4 = (
    st.columns(4)
)


c1.metric(
    "HEIVA Score",
    f"""
    {
        row[
            'vulnerability_score'
        ]:.1f
    }
    """,
)


c2.metric(
    "Healthy Life Expectancy",
    f"""
    {
        row[
            'healthy_life_expectancy_sex_mean'
        ]:.1f}
    """,
)


c3.metric(
    "Economic Inactivity",
    f"""
    {
        row[
            'economic_inactivity_pct'
        ]:.1f}%
    """,
)


c4.metric(
    "Area Segment",
    str(
        row[
            "segment_name"
        ]
    ),
)


st.divider()


if geojson is not None:

    st.subheader(
        "Geographic Vulnerability"
    )


    figure = px.choropleth(
        df,

        geojson=geojson,

        locations="area_code",

        featureidkey=(
            "properties.area_code"
        ),

        color="vulnerability_score",

        hover_name="area_name",

        labels={
            "vulnerability_score":
                "HEIVA Score"
        },
    )


    figure.update_geos(
        fitbounds="locations",
        visible=False,
    )


    st.plotly_chart(
        figure,
        use_container_width=True,
    )


else:

    st.info(
        "Add the ONS boundary GeoJSON "
        "to enable the map."
    )