# HEIVA England

## Health & Economic Inequality Vulnerability Analytics

**HEIVA England** is an end-to-end data analytics platform developed to explore how **deprivation, health outcomes and economic participation overlap across English local authorities**. The project integrates official public-sector datasets, standardises them through a reproducible Python ETL pipeline, stores analytical outputs in SQLite, applies statistical and segmentation methods, and delivers the results through Power BI and Streamlit.

> **Purpose:** turn fragmented public data into a coherent, place-based analytical view that helps identify areas experiencing overlapping health and socioeconomic vulnerability.

> **Important:** the **HEIVA Vulnerability Score** is an experimental analytical index developed for this portfolio project. It is **not** an official ONS, NHS, OHID or UK Government statistic and should be used for exploratory comparison and prioritisation only.

---

## Project at a Glance

| Area | Implementation |
|---|---|
| Data ingestion | Python, Requests, official public-data endpoints/files |
| Data transformation | Pandas, NumPy, geographic-code standardisation |
| Storage | SQLite / SQL |
| Statistical analysis | Descriptive statistics, correlation, OLS regression |
| Composite analytics | HEIVA Vulnerability Score |
| Historical analytics | Indicator time-series and change metrics |
| Trend projection | Illustrative linear projection for economic inactivity |
| Segmentation | K-Means with silhouette-score model selection |
| Geospatial analysis | GeoPandas / GeoJSON / official ONS geography |
| BI delivery | Power BI |
| Interactive product | Streamlit + Plotly |
| Quality assurance | Automated validation checks + pytest |
| Automation | GitHub Actions scheduled/manual refresh workflow |

---

## Business Problem

Health, deprivation and labour-market indicators are often published through different public-sector datasets and reporting systems. This makes it difficult to answer a simple place-based question:

> **Which areas of England experience multiple forms of health and socioeconomic disadvantage at the same time?**

HEIVA England addresses this by bringing the indicators into one analytical workflow and providing a consistent view at local-authority level.

The project is designed around five analytical questions:

1. Do more deprived areas tend to have lower healthy life expectancy?
2. Is greater deprivation associated with higher economic inactivity?
3. Are poorer health outcomes associated with lower economic participation?
4. Which local authorities experience multiple dimensions of vulnerability simultaneously?
5. Which areas perform materially better or worse than their broader socioeconomic profile would suggest?

---

## Data Sources

HEIVA uses official UK public-sector sources.

### 1. English Indices of Deprivation 2025

**Source:** Ministry of Housing, Communities and Local Government  
**Use in HEIVA:** area-level deprivation measures and upper-tier local-authority summaries.

- English Indices of Deprivation 2025: https://www.gov.uk/government/statistics/english-indices-of-deprivation-2025
- The release includes **File 11: Local Authority District summaries - upper tier**.

The Index of Multiple Deprivation is a **relative** measure of deprivation. HEIVA therefore treats it as a comparative area-level indicator rather than an absolute measure of poverty.

### 2. OHID Fingertips / Public Health Profiles

**Source:** Office for Health Improvement & Disparities, Department of Health and Social Care  
**Use in HEIVA:** healthy life expectancy, life expectancy and economic-inactivity indicators.

- Fingertips: https://fingertips.phe.org.uk/
- API guidance: https://fingertips.phe.org.uk/profile/guidance/supporting-information/api

The Fingertips API supports public-health data retrieval in **CSV or JSON** and is used by the ingestion layer to create a reproducible pipeline.

### 3. Office for National Statistics

**Source:** Office for National Statistics  
**Use in HEIVA:** official life-expectancy context and local-area health statistics.

- Life expectancy for local areas: https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/bulletins/lifeexpectancyforlocalareasoftheuk/latest
- Healthy life expectancy: https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/bulletins/healthstatelifeexpectanciesuk/between2011to2013and2022to2024

### 4. ONS Open Geography Portal

**Use in HEIVA:** official geographic boundaries / GeoJSON joined using geographic codes rather than local-authority names.

- https://geoportal.statistics.gov.uk/

---

## Solution Architecture

```text
Official Public Data
      |
      v
Python Extraction Layer
      |
      v
Cleaning + Validation + Geography Standardisation
      |
      +--------------------------+
      |                          |
      v                          v
Latest Analytical Snapshot   Historical Indicator Store
      |                          |
      v                          v
SQLite / SQL               Trends + Change Analysis
      |                          |
      |                    Linear Trend Projection
      |                          |
      +-------------+------------+
                    |
                    v
          Statistical Analytics
       Correlation | OLS Regression
                    |
                    v
          HEIVA Vulnerability Score
                    |
              +-----+------+
              |            |
              v            v
         K-Means       Geospatial
        Segments         Layer
              |            |
              +-----+------+
                    |
           +--------+--------+
           |                 |
           v                 v
        Power BI          Streamlit
           |                 |
           +--------+--------+
                    |
                    v
          Portfolio / Decision Support
```

---

## Repository Structure

```text
health-economic-inequality-england/
|
|-- README.md
|-- requirements.txt
|-- config.py
|-- main.py
|-- app.py
|
|-- data/
|   |-- raw/
|   |-- processed/
|   |   |-- deprivation_utla.csv
|   |   |-- analytics_master.csv
|   |   |-- analytics_enriched.csv
|   |   |-- indicator_history.csv
|   |   |-- area_trends.csv
|   |   |-- cluster_profiles.csv
|   |   |-- economic_inactivity_forecast.csv
|   |   `-- heiva_map.geojson
|   |-- geospatial/
|   |   `-- utla_boundaries.geojson
|   `-- database/
|       `-- health_economic_inequality.db
|
|-- src/
|   |-- __init__.py
|   |-- extract.py
|   |-- transform.py
|   |-- load_database.py
|   |-- analyse.py
|   |-- history.py
|   |-- forecasting.py
|   |-- clustering.py
|   |-- geospatial.py
|   |-- quality.py
|   `-- load_advanced_database.py
|
|-- dashboard/
|   |-- __init__.py
|   |-- common.py
|   |-- overview.py
|   |-- trends.py
|   |-- segments.py
|   |-- explorer.py
|   `-- methodology.py
|
|-- sql/
|   |-- analysis_queries.sql
|   `-- advanced_queries.sql
|
|-- outputs/
|   |-- charts/
|   |-- tables/
|   |-- forecasts/
|   `-- quality/
|
|-- tests/
|   `-- test_quality.py
|
|-- .github/
|   `-- workflows/
|       `-- refresh-heiva.yml
|
`-- .streamlit/
    `-- config.toml
```

---

## End-to-End Pipeline

Running the master pipeline performs the following workflow:

```text
Extract
  -> Transform
  -> Load SQLite
  -> Exploratory / Statistical Analysis
  -> HEIVA Scoring
  -> Historical Dataset Build
  -> Trend Analysis
  -> Economic-Inactivity Trend Projection
  -> K-Means Segmentation
  -> Geospatial Join
  -> Data-Quality Checks
  -> Advanced SQL Tables
```

### Run the complete pipeline

```bash
python main.py
```

### Launch the Streamlit application

```bash
streamlit run app.py
```

### Run automated tests

```bash
pytest -v
```

---

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd health-economic-inequality-england
```

### 2. Create a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the official geography boundary file

Place the appropriate upper-tier / county and unitary-authority GeoJSON file from the ONS Open Geography Portal at:

```text
data/geospatial/utla_boundaries.geojson
```

### 5. Run

```bash
python main.py
```

---

## Core Data Engineering Decisions

### Geographic joins use official codes

The project joins data primarily using `area_code` rather than area names. This reduces errors caused by spelling, naming conventions and boundary labels across independent datasets.

### Raw and processed data are separated

```text
data/raw/        -> source data, not manually edited
data/processed/  -> cleaned analytical outputs
```

This preserves lineage and makes the analytical workflow reproducible.

### Indicator metadata are resolved programmatically

The ingestion layer uses Fingertips metadata to locate required indicators rather than permanently relying on manually copied IDs wherever possible.

---

## Analytical Dataset

The primary analytical dataset is:

```text
data/processed/analytics_master.csv
```

The enriched version used by the advanced analytics layer is:

```text
data/processed/analytics_enriched.csv
```

Typical analytical fields include:

- `area_code`
- `area_name`
- `imd_average_score_rank`
- `imd_deprivation_percentile`
- `imd_most_deprived_10pct_share`
- `healthy_life_expectancy_male`
- `healthy_life_expectancy_female`
- `healthy_life_expectancy_sex_mean`
- `life_expectancy_sex_mean`
- `economic_inactivity_pct`
- `unhealthy_years_estimate`
- `deprivation_risk`
- `health_risk`
- `economic_risk`
- `vulnerability_score`
- `vulnerability_percentile`
- `vulnerability_band`
- `cluster_id`
- `segment_name`

---

## HEIVA Vulnerability Score

The project creates an experimental composite score to summarise overlapping area-level vulnerability.

### Components

1. **Deprivation risk** - higher deprivation produces higher risk.
2. **Health risk** - lower healthy life expectancy produces higher risk.
3. **Economic risk** - higher economic inactivity produces higher risk.

Each component is min-max normalised to a `0-1` scale.

```text
HEIVA Score = mean(
    deprivation_risk,
    health_risk,
    economic_risk
) * 100
```

For the portfolio implementation, the three dimensions use **equal weights**. This keeps the methodology transparent and avoids implying that one dimension is inherently more important without an externally validated weighting framework.

### Interpretation

A higher HEIVA score indicates that multiple area-level vulnerability measures overlap more strongly relative to the other areas in the analytical dataset.

It **does not** mean that every individual resident experiences those conditions.

---

## Statistical Analysis

The statistical layer includes:

### Exploratory Data Analysis

- missingness review
- distributions and descriptive statistics
- ranking and comparative analysis
- scatterplots and relationship inspection

### Correlation

Pearson correlation is used to examine linear relationships between selected area-level indicators, including deprivation, healthy life expectancy, life expectancy and economic inactivity.

### OLS Regression

The project includes an exploratory regression model of the form:

```text
Healthy Life Expectancy
    = beta0
    + beta1(Deprivation)
    + beta2(Economic Inactivity)
    + error
```

The regression is interpreted as an **association model**, not a causal model.

---

## Historical and Trend Analytics

`indicator_history.csv` preserves historical observations for the selected health/economic indicators.

The trend layer calculates:

- first observed value
- latest observed value
- absolute change
- percentage change
- annualised change
- number of available observations

This extends HEIVA from a point-in-time dashboard to a longitudinal analytical product.

---

## Illustrative Trend Projection

The project includes a transparent linear model for short-horizon **economic-inactivity trend projection** where sufficient history is available.

This is deliberately described as an **illustrative trend projection**, not a policy/economic forecast.

The model records:

- projected year
- projected economic-inactivity rate
- number of historical observations
- historical model R-squared

---

## Area Segmentation

K-Means clustering is used to identify local authorities with similar analytical profiles.

The clustering layer:

1. selects relevant variables;
2. imputes missing numeric values using the median;
3. standardises features;
4. evaluates candidate values of `k`;
5. uses the **silhouette score** to support model selection;
6. assigns interpretable segment labels based on cluster profiles.

Cluster membership is an analytical segmentation and should not be interpreted as an official classification.

---

## Geospatial Analytics

The project uses an official ONS geographic boundary file and joins it to HEIVA using area codes.

Output:

```text
data/processed/heiva_map.geojson
```

This enables interactive vulnerability mapping in Streamlit and supports place-based exploration.

---

## SQL Analytical Layer

The SQLite database is stored at:

```text
data/database/health_economic_inequality.db
```

Core / advanced analytical tables include:

- `dim_area`
- `fact_deprivation`
- `fact_indicator_latest`
- `analytics_snapshot`
- `analytics_enriched`
- `indicator_history`
- `area_trends`
- `cluster_profiles`
- `economic_inactivity_forecast`

Example analytical questions implemented through SQL include:

- Which areas have the highest combined vulnerability?
- Which areas have below-average healthy life expectancy and above-average economic inactivity?
- Which segments contain the highest average HEIVA scores?
- Which areas have experienced increasing economic inactivity?
- Which high-vulnerability areas are also showing adverse historical economic trends?

See:

```text
sql/analysis_queries.sql
sql/advanced_queries.sql
```

---

## Power BI Dashboard

The Power BI deliverable is designed around four core views:

### 1. England Overview

- headline KPIs
- vulnerability ranking
- deprivation vs healthy-life-expectancy relationship
- geographic overview

### 2. Health Inequality

- healthy life expectancy
- life expectancy
- estimated years outside good health
- sex-level comparisons where available

### 3. Economy & Deprivation

- economic inactivity
- deprivation metrics
- comparative relationship analysis

### 4. Local Authority Explorer

- authority-level slicer
- HEIVA score
- health metrics
- economic participation
- deprivation
- comparison against broader benchmarks

> **Add dashboard screenshot here before publishing:** `docs/images/dashboard-overview.png`

---

## Streamlit Application

The Python data application contains the following pages:

- **Overview** - KPIs and cross-sectional relationships
- **Historical Trends** - local-authority indicator history
- **Area Segments** - clustering output and segment profiles
- **Area Explorer** - selected-area metrics and geography
- **Methodology** - score construction, interpretation and limitations

Run locally with:

```bash
streamlit run app.py
```

> **Live app:** `<ADD_STREAMLIT_URL>`

---

## Data Quality & Testing

The project includes explicit QA checks for:

- duplicate geography codes
- core-indicator missingness
- HEIVA score range (`0-100`)
- presence of core health and economic data
- historical-observation availability

Tests are located in:

```text
tests/test_quality.py
```

Run:

```bash
pytest -v
```

A machine-readable QA output is written to:

```text
outputs/quality/quality_report.json
```

---

## Automation

A GitHub Actions workflow is included to support manual or scheduled data refresh:

```text
.github/workflows/refresh-heiva.yml
```

The workflow can:

1. check out the repository;
2. create a Python environment;
3. install dependencies;
4. run the HEIVA pipeline;
5. regenerate processed outputs;
6. commit refreshed analytical outputs when configured to do so.

Government indicators are updated periodically rather than continuously, so the refresh cadence should remain proportionate to source-data update frequency.

---

## Key Deliverables

| Deliverable | Purpose |
|---|---|
| `analytics_master.csv` | Core cross-sectional analytical dataset |
| `analytics_enriched.csv` | HEIVA score + segment-enriched analytical dataset |
| SQLite database | Structured analytical query layer |
| `indicator_history.csv` | Historical observations |
| `area_trends.csv` | Change and trend metrics |
| `cluster_profiles.csv` | Data-driven segment summaries |
| `economic_inactivity_forecast.csv` | Illustrative trend projections |
| `heiva_map.geojson` | Geospatial analytical layer |
| Power BI dashboard | BI / decision-support presentation |
| Streamlit application | Interactive Python analytics product |
| QA report + pytest | Reproducibility and data-quality evidence |

---

## Results

The project is designed to surface three classes of insight:

1. **cross-sectional relationships** between deprivation, health and economic participation;
2. **place-based vulnerability** through the HEIVA composite index and ranking;
3. **longitudinal and segment-level patterns** through trend analysis and clustering.

### Add your final verified project results here

Before public release, replace the placeholders below with values produced by your final pipeline:

```text
Areas analysed:                         <VALUE>
Rows processed / final analytical rows:<VALUE>
Correlation: deprivation vs HLE:       <VALUE>
Correlation: HLE vs inactivity:        <VALUE>
Regression R-squared:                  <VALUE>
Highest HEIVA area:                    <VALUE>
Lowest HEIVA area:                     <VALUE>
Selected number of clusters:           <VALUE>
Best silhouette score:                 <VALUE>
```

Do not publish invented values. Use only outputs generated by the final repository version.

---

## External Benchmark Context

The project's indicators sit within a wider national context. At England level, official sources report:

- healthy life expectancy at birth in **2022-24** of **60.9 years for males** and **61.3 years for females**;
- economic inactivity among people aged **16-64** of **21.2% in 2024/25**;
- life expectancy at birth in **2022-24** of approximately **79.5 years for males** and **83.3 years for females**.

These are national reference values and **not HEIVA project results**.

---

## Responsible Interpretation & Limitations

### Correlation is not causation

Associations between deprivation, health and economic inactivity do not establish causal direction.

### Mixed reporting periods

The latest suitable observations for different indicators may cover different periods. Comparisons should therefore be described as a **latest-available cross-sectional analysis** rather than perfectly contemporaneous measurement.

### Ecological fallacy

The project analyses geographic areas. Area-level patterns cannot be assumed to describe every individual resident.

### Relative deprivation

The Index of Multiple Deprivation is a relative measure and should not be interpreted as an absolute poverty scale.

### Experimental score

HEIVA is a transparent portfolio methodology, not a validated policy index. Equal weighting improves interpretability but is itself a modelling assumption.

### Forecasting limitations

Linear projections assume continuation of historical direction and do not model policy interventions, structural economic changes, demographic shifts or shocks.

### Clustering limitations

Segments depend on variable selection, preprocessing and the clustering algorithm. They should be interpreted as exploratory analytical groups.

---

## Skills Demonstrated

### Data Analysis

- exploratory data analysis
- descriptive statistics
- correlation
- regression
- trend analysis
- composite scoring
- segmentation
- geospatial analysis

### Data Engineering

- API / file ingestion
- reusable ETL design
- data validation
- geographic standardisation
- analytical dataset design
- reproducible processing

### SQL & Data Modelling

- SQLite
- analytical tables
- joins
- aggregations
- subqueries
- trend and ranking queries

### Business Intelligence & Communication

- Power BI
- Streamlit
- KPI design
- visual analytics
- data storytelling
- responsible interpretation

### Engineering Practice

- modular Python
- Git / GitHub
- automated tests
- scheduled workflow automation
- documentation

---


---

## Future Development

Potential extensions include:

- additional public-health and wider-determinant indicators;
- population-weighted analysis;
- formal uncertainty / sensitivity analysis for HEIVA weights;
- time-aware geographies and boundary harmonisation;
- richer forecasting methods where the reporting cadence supports them;
- cloud-hosted data storage;
- automated Power BI refresh integration;
- downloadable stakeholder briefing reports.

---

## Author

**Jirilin Suresh Babu Rajan**  
Data Analytics | Artificial Intelligence | Software Engineering

- LinkedIn: https://www.linkedin.com/in/s-jirilin-babu-6a2b49249
- GitHub: https://github.com/Jirilin

---

## Licence & Data Reuse

The code in this repository should be licensed separately from the underlying public datasets. Source data remain subject to the licensing and reuse conditions published by the relevant UK public-sector provider, including the Open Government Licence where applicable.

---

## Acknowledgements

- Ministry of Housing, Communities and Local Government
- Office for Health Improvement & Disparities / Department of Health and Social Care
- Office for National Statistics
- ONS Open Geography Portal

---

**HEIVA England** - turning public data into place-based insight.
