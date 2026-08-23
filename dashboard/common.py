from pathlib import Path
import json
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


@st.cache_data
def load_enriched():
    primary_file = PROCESSED / "analytics_master.csv"
    fallback_file = PROCESSED / "analytics_enriched.csv"
    
    if primary_file.exists():
        return pd.read_csv(primary_file)
    elif fallback_file.exists():
        return pd.read_csv(fallback_file)
    
    return pd.DataFrame()


@st.cache_data
def load_history():
    file = PROCESSED / "indicator_history.csv"
    fallback = PROCESSED / "indicator_latest_long.csv"
    
    if file.exists():
        return pd.read_csv(file)
    elif fallback.exists():
        return pd.read_csv(fallback)
        
    return pd.DataFrame()


@st.cache_data
def load_trends():
    file = PROCESSED / "area_trends.csv"
    if not file.exists():
        return pd.DataFrame()
    return pd.read_csv(file)


@st.cache_data
def load_forecast():
    file = PROCESSED / "economic_inactivity_forecast.csv"
    if not file.exists():
        return pd.DataFrame()
    return pd.read_csv(file)


@st.cache_data
def load_clusters():
    file = PROCESSED / "cluster_profiles.csv"
    if not file.exists():
        return pd.DataFrame()
    return pd.read_csv(file)


@st.cache_data
def load_geojson():
    file = PROCESSED / "heiva_map.geojson"
    if not file.exists():
        return None

    with open(file, encoding="utf-8") as source:
        return json.load(source)