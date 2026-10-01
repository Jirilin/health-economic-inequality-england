# HEIVA England

## Health & Economic Inequality Vulnerability Analytics

**HEIVA England** is an end-to-end data analytics project examining how
deprivation, health outcomes and economic participation overlap across
English local authorities.

It integrates official public-sector data, standardises geography using
official area codes, builds reusable analytical datasets and a SQLite
database, applies statistical and exploratory analytical methods, and
delivers results through Power BI and Streamlit.

> **Important:** HEIVA is an experimental area-level analytical
> framework. It is not an official government index, an individual risk
> score, or a causal model.

## Project overview

Health, deprivation and labour-market indicators are published across
different systems, formats and reporting periods. HEIVA creates a
reproducible workflow for comparing local authorities and identifying
areas where several forms of disadvantage overlap.

**Workflow:** Official sources → Python ETL → geographic standardisation
→ analytical datasets → SQLite/SQL → statistical analysis → HEIVA
scoring → trends/clustering/geospatial analysis → Power BI & Streamlit →
QA.

The final analytical master dataset covers **153 English local
authorities**.

## Key findings

-   Deprivation vs healthy life expectancy: **r = -0.81**.
-   Deprivation vs overall life expectancy: **r = -0.80**.
-   Healthy life expectancy vs economic inactivity: **r = -0.58**.
-   OLS model: **n = 151, R² = 0.665, adjusted R² = 0.661**.
-   Deprivation coefficient: **β = -0.1005, p \< 0.001**.
-   Economic-inactivity coefficient: **β = -0.0962, p = 0.085**.
-   Highest HEIVA score: **Hartlepool --- 88.50**.
-   Lowest HEIVA score: **Wokingham --- 6.77**.
-   Selected K-Means solution: **K = 2**, silhouette score **0.4561**.
-   Historical analytical layer: **11,095 observations across three
    indicators**.

These findings describe area-level associations and comparative
patterns; they do not establish individual-level risk or causality.

## Objectives

1.  Integrate deprivation, health and economic-participation indicators.
2.  Standardise geography using official codes wherever possible.
3.  Build reusable cross-sectional and historical datasets.
4.  Support reproducible SQL analysis.
5.  Analyse relationships between socioeconomic and health indicators.
6.  Construct a transparent experimental vulnerability score.
7.  Explore trends, segmentation and geospatial patterns.
8.  Deliver results through Power BI and Streamlit.
9.  Apply repeatable QA controls and automated tests.

## Data sources

-   **English Indices of Deprivation 2025** --- Ministry of Housing,
    Communities and Local Government.
-   **OHID Fingertips / Public Health Profiles** --- health indicators
    including healthy life expectancy.
-   **OHID Wider Determinants of Health** --- economic-inactivity
    indicators.
-   **Office for National Statistics (ONS)** --- life expectancy and
    contextual health statistics.
-   **ONS Open Geography Portal** --- geographic boundary data.

Reporting periods differ between indicators. The cross-sectional layer
is therefore a **latest-available-observation analysis**, not a
perfectly contemporaneous snapshot.

## Technology stack

  Area                      Technology
  ------------------------- --------------------------------------
  Programming               Python
  Data manipulation         pandas, NumPy
  Database                  SQLite, SQL
  Statistics                Pearson correlation, OLS regression
  Machine learning          K-Means clustering
  Visualisation             Matplotlib
  BI                        Power BI
  Interactive application   Streamlit
  Geospatial                GeoJSON / Python geospatial workflow
  Testing                   pytest
  Automation                GitHub Actions
  Version control           Git, GitHub

## Repository structure

``` text
health-economic-inequality-england/
├── README.md
├── RUNBOOK.md
├── requirements.txt
├── config.py
├── main.py
├── app.py
├── data/
│   ├── raw/
│   ├── processed/
│   ├── geospatial/
│   └── database/
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load_database.py
│   ├── analyse.py
│   ├── history.py
│   ├── forecasting.py
│   ├── clustering.py
│   ├── geospatial.py
│   ├── quality.py
│   └── load_advanced_database.py
├── dashboard/
│   ├── common.py
│   ├── overview.py
│   ├── trends.py
│   ├── segments.py
│   ├── explorer.py
│   └── methodology.py
├── sql/
│   ├── analysis_queries.sql
│   └── advanced_queries.sql
├── outputs/
│   ├── charts/
│   ├── tables/
│   ├── forecasts/
│   └── quality/
├── tests/
│   └── test_quality.py
├── .github/workflows/
│   └── refresh-heiva.yml
└── .streamlit/
    └── config.toml
```

## Core outputs

  Output                               Purpose
  ------------------------------------ ------------------------------------------
  `analytics_master.csv`               Core cross-sectional analytical dataset
  `analytics_enriched.csv`             HEIVA score and segment-enriched dataset
  `health_economic_inequality.db`      SQLite analytical database
  `indicator_history.csv`              Historical indicator observations
  `area_trends.csv`                    Area-level change metrics
  `economic_inactivity_forecast.csv`   Illustrative projection output
  `cluster_profiles.csv`               Segment summaries
  `heiva_map.geojson`                  Geographic analytical layer
  `quality_report.json`                Machine-readable QA output

## Methodology

### Data engineering

The pipeline ingests selected official data, cleans and standardises
fields, and aligns areas using official geographic identifiers wherever
possible. The processed indicators are combined into a one-row-per-area
analytical layer.

### SQL

Structured outputs are loaded into SQLite. Reusable analytical SQL is
stored under `sql/`, separating analytical logic from ad-hoc
exploration.

### Statistical analysis

The project includes descriptive analysis, area rankings, Pearson
correlation and OLS regression. Statistical relationships are treated as
associations rather than causal effects.

### HEIVA Vulnerability Score

HEIVA combines normalised deprivation risk, health risk and
economic-inactivity risk using equal weighting and expresses the result
on a **0--100 scale**. Normalisation and equal weighting are modelling
choices; the score has not been externally validated for policy
allocation.

### Historical analysis and forecasting

Historical observations are retained separately from the cross-sectional
master dataset. The project derives change metrics and includes an
illustrative linear trend projection for economic inactivity where
sufficient history exists. Forecast outputs are exploratory.

### Clustering

K-Means models were compared using silhouette scores. The selected
solution was **K = 2** with a silhouette score of **0.4561**. Segments
are exploratory and depend on the chosen variables and preprocessing.

### Geospatial analysis

The standard project run expects the official ONS boundary file at:

``` text
data/geospatial/utla_boundaries.geojson
```

### Delivery

Power BI provides stakeholder-facing reporting. Streamlit provides
interactive exploration of headline metrics, trends, segments and
methodology.

## Data quality

Verified final QA evidence includes:

-   **153** areas in the master dataset;
-   **0** duplicate area codes;
-   deprivation missingness: **0.00%**;
-   healthy life expectancy missingness: **1.31%**;
-   economic inactivity missingness: **0.65%**;
-   HEIVA score range validation: **0--100**;
-   **11,095** historical observations; and
-   **3** historical indicators.

Run tests with:

``` bash
python -m pytest -v
```

A generated HEIVA score is not, by itself, evidence that every
underlying component is complete; component-level missingness should be
reviewed separately.

## Quick start

``` bash
git clone https://github.com/Jirilin/health-economic-inequality-england.git
cd health-economic-inequality-england
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Place the required geography file at:

``` text
data/geospatial/utla_boundaries.geojson
```

Then run:

``` bash
python main.py
python -m pytest -v
streamlit run app.py
```

Windows PowerShell virtual-environment activation:

``` powershell
.venv\Scripts\Activate.ps1
```

For the full operating procedure and troubleshooting guide, see
**`RUNBOOK.md`**.

## Governance and limitations

-   Correlation and regression do not establish causality.
-   Local-authority results must not be applied to individuals.
-   Indicators may refer to different reporting periods.
-   Deprivation measures are relative.
-   HEIVA normalisation and equal weighting are modelling choices.
-   Forecasting does not model structural shocks.
-   Clustering depends on feature selection, preprocessing and algorithm
    choice.
-   The project uses aggregate public data rather than personally
    identifiable information.
-   Source licensing and attribution requirements remain applicable.

## Reproducible release sequence

``` text
Environment setup
        ↓
Boundary file check
        ↓
python main.py
        ↓
python -m pytest -v
        ↓
Review QA and outputs
        ↓
streamlit run app.py
        ↓
Refresh Power BI
        ↓
Commit and tag release
```

The GitHub Actions workflow is stored at
`.github/workflows/refresh-heiva.yml`.

## Author

**Jirilin Suresh Babu Rajan**\
MSc Artificial Intelligence, Oxford Brookes University

## Repository

https://github.com/Jirilin/health-economic-inequality-england

## Licence and attribution

HEIVA uses public-sector datasets. Users should comply with the
licensing and attribution requirements of the original data providers,
including applicable Open Government Licence terms. HEIVA outputs and
methodology must not be represented as official statistics produced or
endorsed by those organisations.
