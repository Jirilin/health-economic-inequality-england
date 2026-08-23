import plotly.express as px
import streamlit as st

from dashboard.common import (
    load_enriched,
)


df = load_enriched()


st.title("HEIVA England")

st.caption("Health & Economic Inequality Vulnerability Analytics")


# KPIs

c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "Areas analysed",
    f"{df['area_code'].nunique():,}",
)


c2.metric(
    "Average HLE",
    f"{df['healthy_life_expectancy_sex_mean'].mean():.1f} years",
)


c3.metric(
    "Economic inactivity",
    f"{df['economic_inactivity_pct'].mean():.1f}%",
)


c4.metric(
    "Average HEIVA Score",
    f"{df['vulnerability_score'].mean():.1f}",
)


st.divider()


# TOP VULNERABILITY AREAS

st.subheader("Highest combined vulnerability")


top = (
    df.nlargest(
        15,
        "vulnerability_score",
    ).sort_values("vulnerability_score")
)


fig = px.bar(
    top,
    x="vulnerability_score",
    y="area_name",
    orientation="h",
    labels={
        "vulnerability_score": "HEIVA Score",
        "area_name": "Local Authority",
    },
)


st.plotly_chart(
    fig,
    use_container_width=True,
)

# RELATIONSHIP ANALYSIS

st.subheader("Deprivation and healthy life expectancy")

# Safe check in case 'segment_name' column was not created during transform
color_col = "segment_name" if "segment_name" in df.columns else None

scatter = px.scatter(
    df,
    x="imd_deprivation_percentile",
    y="healthy_life_expectancy_sex_mean",
    color=color_col,
    hover_name="area_name",
    labels={
        "imd_deprivation_percentile": "Deprivation percentile",
        "healthy_life_expectancy_sex_mean": "Healthy life expectancy",
        "segment_name": "Area segment",
    },
)


st.plotly_chart(
    scatter,
    use_container_width=True,
)


st.info(
    "The HEIVA score is an experimental "
    "analytical index and is not an "
    "official government statistic."
)