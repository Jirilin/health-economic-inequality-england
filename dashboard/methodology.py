import streamlit as st


st.title(
    "Methodology & Limitations"
)


st.header(
    "HEIVA Vulnerability Score"
)


st.write(
    """
    The HEIVA Vulnerability Score combines
    three analytical dimensions:

    - deprivation
    - poor healthy life expectancy
    - economic inactivity

    Each component is normalised before
    being combined using equal weights.
    """
)


st.warning(
    """
    HEIVA is an experimental portfolio
    metric. It is not an official ONS,
    NHS, OHID or UK Government index.
    """
)


st.header(
    "Interpretation"
)


st.write(
    """
    HEIVA should be used as an exploratory
    prioritisation and comparison tool.

    A high score indicates that several
    area-level measures of disadvantage
    overlap. It does not imply that every
    resident of the area experiences those
    circumstances.
    """
)


st.header(
    "Statistical limitations"
)


st.markdown(
    """
    - Correlation does not demonstrate causation.
    - Indicators may cover different reporting periods.
    - Area-level results should not be applied to individuals.
    - Historical trends may not continue into the future.
    - Cluster assignments are analytical segments rather than official classifications.
    """
)