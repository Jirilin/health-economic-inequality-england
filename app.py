import streamlit as st


st.set_page_config(
    page_title="HEIVA England",
    page_icon="📊",
    layout="wide",
)


pages = {
    "HEIVA": [

        st.Page(
            "dashboard/overview.py",
            title="Overview",
            icon="🏠",
        ),

        st.Page(
            "dashboard/trends.py",
            title="Historical Trends",
            icon="📈",
        ),

        st.Page(
            "dashboard/segments.py",
            title="Area Segments",
            icon="🧩",
        ),

        st.Page(
            "dashboard/explorer.py",
            title="Area Explorer",
            icon="🗺️",
        ),

        st.Page(
            "dashboard/methodology.py",
            title="Methodology",
            icon="📘",
        ),
    ]
}


navigation = st.navigation(
    pages
)

navigation.run()