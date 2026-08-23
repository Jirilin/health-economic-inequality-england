import plotly.express as px
import streamlit as st

from dashboard.common import (
    load_enriched,
    load_clusters,
)


df = load_enriched()
profiles = load_clusters()


st.title(
    "Area Segmentation"
)


st.write(
    """
    Local authorities are grouped according
    to similarities in deprivation, health
    and economic indicators.
    """
)


fig = px.scatter(
    df,

    x="healthy_life_expectancy_sex_mean",

    y="economic_inactivity_pct",

    color="segment_name",

    size="vulnerability_score",

    hover_name="area_name",

    labels={
        "healthy_life_expectancy_sex_mean":
            "Healthy life expectancy",

        "economic_inactivity_pct":
            "Economic inactivity (%)",

        "segment_name":
            "Segment",
    },
)


st.plotly_chart(
    fig,
    use_container_width=True,
)


st.subheader(
    "Segment Profiles"
)


st.dataframe(
    profiles,
    use_container_width=True,
)