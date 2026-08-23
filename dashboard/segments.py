import plotly.express as px
import streamlit as st

from dashboard.common import (
    load_enriched,
    load_clusters,
)

df = load_enriched()
profiles = load_clusters()

st.title("Area Segmentation")

st.write(
    """
    Local authorities are grouped according to similarities in deprivation, health, and economic indicators.
    """
)

if not df.empty and "segment_name" in df.columns:
    fig = px.scatter(
        df,
        x="healthy_life_expectancy_sex_mean",
        y="economic_inactivity_pct",
        color="segment_name",
        size="vulnerability_score",
        hover_name="area_name",
        labels={
            "healthy_life_expectancy_sex_mean": "Healthy life expectancy",
            "economic_inactivity_pct": "Economic inactivity (%)",
            "segment_name": "Segment",
        },
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Segmentation analysis data is missing or incomplete.")

st.subheader("Segment Profiles")

if not profiles.empty:
    st.dataframe(profiles, use_container_width=True)
else:
    st.info("Cluster profile profiles dataset (`cluster_profiles.csv`) not found.")