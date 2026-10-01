# HEIVA England --- RUNBOOK

## Beginner-friendly setup, execution, QA and release guide

Use this runbook to set up HEIVA on a new computer, run the pipeline,
verify the outputs, launch Streamlit, refresh Power BI and prepare a
release.

## 1. The normal run sequence

``` text
OPEN REPOSITORY
      ↓
ACTIVATE .venv
      ↓
CHECK DEPENDENCIES
      ↓
CHECK BOUNDARY FILE
      ↓
python main.py
      ↓
python -m pytest -v
      ↓
REVIEW QA + OUTPUTS
      ↓
streamlit run app.py
      ↓
REFRESH POWER BI
      ↓
COMMIT / TAG RELEASE
```

The three commands to remember are:

``` bash
python main.py
python -m pytest -v
streamlit run app.py
```

Think of them as **BUILD → VERIFY → VIEW**.

## 2. Requirements

You need Python, Git, the repository, packages in `requirements.txt`,
the required ONS boundary file and Power BI Desktop if you want to
refresh the Power BI report.

Repository:

``` text
https://github.com/Jirilin/health-economic-inequality-england
```

Check Python:

``` bash
python3 --version
```

The project has been run locally with Python 3.9.x. If you change Python
versions, rerun the complete pipeline and tests before treating the
outputs as final.

## 3. Get the repository

``` bash
git clone https://github.com/Jirilin/health-economic-inequality-england.git
cd health-economic-inequality-england
```

For an existing copy, open Terminal and `cd` into the repository.

Confirm the root contains:

``` text
README.md
requirements.txt
config.py
main.py
app.py
src/
tests/
sql/
data/
```

**Run project commands from the repository root, not from `src/` or
`tests/`.**

## 4. Create and activate the virtual environment

### macOS/Linux

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

``` powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

To leave the environment later:

``` bash
deactivate
```

## 5. Install dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Optional check:

``` bash
pip list
```

## 6. Check configuration

`config.py` should use repository-relative paths rather than personal
absolute paths such as `/Users/name/...`.

This is required for portability to another computer and CI/GitHub
Actions.

## 7. Check the geography file

The standard run expects:

``` text
data/geospatial/utla_boundaries.geojson
```

macOS/Linux:

``` bash
ls data/geospatial/
```

Windows:

``` powershell
Get-ChildItem data/geospatial
```

Do not rename an unrelated GeoJSON file simply to satisfy the filename.
It must contain the geography expected by the HEIVA geospatial workflow.

## 8. Run the complete pipeline

``` bash
python main.py
```

Watch the terminal for exceptions, missing files, source failures, merge
warnings, empty datasets or failed output writes.

Do not publish merely because `main.py` reaches the end. Continue to QA.

## 9. Check outputs

Important project artefacts include:

``` text
analytics_master.csv
analytics_enriched.csv
health_economic_inequality.db
indicator_history.csv
area_trends.csv
economic_inactivity_forecast.csv
cluster_profiles.csv
heiva_map.geojson
quality_report.json
```

They are normally stored under `data/processed/`, `data/database/` and
`outputs/`, according to `config.py`.

Verified final project benchmarks include:

``` text
Areas in master dataset:       153
Duplicate area codes:            0
Historical observations:    11,095
Historical indicators:           3
```

Unexpected changes should be investigated.

## 10. Run pytest

``` bash
python -m pytest -v
```

Use `python -m pytest` so pytest runs through the active interpreter.

A successful run should show collected tests ending in `PASSED`. The
exact number of tests may change as the suite evolves.

### If `config` cannot be imported

Confirm you are at the repository root and the virtual environment is
active:

``` bash
pwd
which python
ls config.py
```

If the repository uses `pytest.ini`, it should contain:

``` ini
[pytest]
pythonpath = .
testpaths = tests
```

Then rerun:

``` bash
python -m pytest -v
```

Do not add machine-specific absolute paths to the test file.

## 11. Review QA

Locate `quality_report.json`.

Verified project QA results:

  Check                                   Result
  ------------------------------------- --------
  Master areas                               153
  Duplicate area codes                         0
  Deprivation missingness                  0.00%
  Healthy life expectancy missingness      1.31%
  Economic inactivity missingness          0.65%
  Historical observations                 11,095
  Historical indicators                        3

HEIVA values should satisfy the expected **0--100 range**.

A non-null HEIVA score alone does not establish that every component is
complete. Review component-level missingness separately and keep the
scoring treatment of incomplete rows consistent with the documented
methodology.

## 12. Verify headline analytics

### Correlations

``` text
Deprivation vs healthy life expectancy:  r ≈ -0.81
Deprivation vs life expectancy:          r ≈ -0.80
Healthy life expectancy vs inactivity:   r ≈ -0.58
```

### Regression

``` text
Observations:                         151
R²:                                  0.665
Adjusted R²:                         0.661
Deprivation coefficient:            -0.1005
Deprivation p-value:                 < 0.001
Economic inactivity coefficient:    -0.0962
Economic inactivity p-value:         0.085
```

Do not describe this model as causal.

### HEIVA ranking

``` text
Highest: Hartlepool — 88.50
Lowest:  Wokingham  — 6.77
```

### Clustering

``` text
Selected K:       2
Silhouette score: 0.4561
```

The clustering result represents moderate exploratory separation, not
definitive natural categories.

If these values change after a future source refresh or methodology
change, investigate and then update the README/report rather than
forcing the new output to match old values.

## 13. Check SQLite

Database:

``` text
health_economic_inequality.db
```

SQL scripts:

``` text
sql/analysis_queries.sql
sql/advanced_queries.sql
```

If SQLite CLI is installed, an example is:

``` bash
sqlite3 data/database/health_economic_inequality.db
```

Then:

``` sql
.tables
```

Exit:

``` sql
.quit
```

Use the actual database path from `config.py` if it differs.

## 14. Launch Streamlit

``` bash
streamlit run app.py
```

Review headline metrics, charts, area selection, trends, segments and
methodology. Confirm there are no stack traces.

Stop it with `Ctrl + C`.

## 15. Refresh Power BI

After the pipeline and tests pass:

1.  Open the HEIVA Power BI report.
2.  Confirm the source points to the current processed dataset/database.
3.  Select **Refresh**.
4.  Wait for completion.
5.  Check all pages, slicers and filters.
6.  Compare headline values with Python/SQL outputs.
7.  Save the refreshed report.

Never manually edit dashboard values to make them agree with the report.
Investigate source paths, filters, aggregation or refresh state instead.

## 16. Final QA checklist

### Data

-   [ ] `analytics_master.csv` exists.
-   [ ] `analytics_enriched.csv` exists.
-   [ ] Area codes are unique.
-   [ ] Missingness is reviewed.
-   [ ] HEIVA values follow the documented scoring rules.

### Analytics

-   [ ] Correlations regenerated.
-   [ ] Regression regenerated.
-   [ ] HEIVA ranking regenerated.
-   [ ] Trends regenerated.
-   [ ] Clusters regenerated.
-   [ ] Geospatial output regenerated.

### Quality

-   [ ] `python -m pytest -v` passes.
-   [ ] `quality_report.json` reviewed.
-   [ ] No unresolved warnings ignored.

### Delivery

-   [ ] Streamlit works.
-   [ ] Power BI refresh succeeds.
-   [ ] README metrics match outputs.
-   [ ] Report metrics match outputs.
-   [ ] Screenshots match the current release.

## 17. Git update workflow

``` bash
git status
git add .
git commit -m "Update HEIVA analytics outputs"
git push
```

Review `git status`/the diff before committing. Do not commit
credentials, tokens, secret `.env` contents or unrelated local files.

## 18. Release procedure

1.  Pull the latest repository.
2.  Activate `.venv`.
3.  Install/check requirements.
4.  Confirm the boundary file.
5.  Run `python main.py`.
6.  Run `python -m pytest -v`.
7.  Review `quality_report.json`.
8.  Verify headline results.
9.  Test Streamlit.
10. Refresh/test Power BI.
11. Update README/report/screenshots if results changed.
12. Review Git changes.
13. Commit and push.
14. Tag the release.

Example:

``` bash
git tag -a v1.0.0 -m "HEIVA England v1.0.0"
git push origin v1.0.0
```

Only tag after the pipeline and QA gates pass.

## 19. Troubleshooting

### `python` not found

Try:

``` bash
python3 --version
```

### Virtual environment not active

macOS/Linux:

``` bash
source .venv/bin/activate
```

Windows:

``` powershell
.venv\Scripts\Activate.ps1
```

### Missing Python package

``` bash
pip install -r requirements.txt
```

### `ModuleNotFoundError: No module named 'config'`

Run from the repository root:

``` bash
python -m pytest -v
```

Check `config.py` exists and check `pytest.ini` if used.

### Boundary file missing

Confirm:

``` text
data/geospatial/utla_boundaries.geojson
```

### Results changed unexpectedly

Check whether:

1.  an upstream dataset changed;
2.  a reporting period changed;
3.  a merge lost areas;
4.  a column definition changed;
5.  HEIVA scoring changed;
6.  missingness changed; or
7.  geography changed.

Then rerun QA and document the reason.

### Power BI differs from Python

Check refresh status, source path, filters, aggregation, duplicates,
data types and whether Power BI is reading an older CSV.

### Streamlit fails

Run `streamlit run app.py` and read the first meaningful terminal
exception. Confirm `main.py` generated the files required by the
dashboard.

## 20. Safe operating rules

1.  Never hand-edit analytical outputs to force a result.
2.  Never commit secrets or credentials.
3.  Do not apply area-level results to individuals.
4.  Do not describe association as causation.
5.  Do not present HEIVA as an official government index.
6.  Document source/methodology changes that alter results.
7.  Run QA before refreshing public-facing outputs.
8.  Preserve source attribution and licensing information.

## 21. First-time user: shortest procedure

``` bash
git clone https://github.com/Jirilin/health-economic-inequality-england.git
cd health-economic-inequality-england
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Confirm `data/geospatial/utla_boundaries.geojson`, then:

``` bash
python main.py
python -m pytest -v
streamlit run app.py
```

If **BUILD** and **VERIFY** pass and **VIEW** works, refresh Power BI
and complete the final QA checklist.

## Project owner

**Jirilin Suresh Babu Rajan**

Repository:
https://github.com/Jirilin/health-economic-inequality-england

For methodology, findings, limitations and source attribution, see
`README.md` and the HEIVA England project report.
