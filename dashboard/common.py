from pathlib import Path
import json

import pandas as pd
import streamlit as st


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)


PROCESSED = (
    ROOT
    / "data"
    / "processed"
)


@st.cache_data
def load_enriched():

    return pd.read_csv(
        PROCESSED
        / "analytics_enriched.csv"
    )


@st.cache_data
def load_history():

    return pd.read_csv(
        PROCESSED
        / "indicator_history.csv"
    )


@st.cache_data
def load_trends():

    return pd.read_csv(
        PROCESSED
        / "area_trends.csv"
    )


@st.cache_data
def load_forecast():

    file = (
        PROCESSED
        / "economic_inactivity_forecast.csv"
    )

    if not file.exists():

        return pd.DataFrame()

    return pd.read_csv(file)


@st.cache_data
def load_clusters():

    return pd.read_csv(
        PROCESSED
        / "cluster_profiles.csv"
    )


@st.cache_data
def load_geojson():

    file = (
        PROCESSED
        / "heiva_map.geojson"
    )

    if not file.exists():

        return None

    with open(
        file,
        encoding="utf-8",
    ) as source:

        return json.load(source)