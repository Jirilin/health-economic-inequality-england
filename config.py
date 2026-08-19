from pathlib import Path

# PROJECT PATHS

ROOT = Path(__file__).resolve().parent

DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
DATABASE_DIR = DATA_DIR / "database"

OUTPUT_DIR = ROOT / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"
TABLE_DIR = OUTPUT_DIR / "tables"
REPORT_DIR = OUTPUT_DIR / "reports"

# Create folders automatically
for folder in [
    RAW_DIR,
    PROCESSED_DIR,
    DATABASE_DIR,
    CHART_DIR,
    TABLE_DIR,
    REPORT_DIR,
]:
    folder.mkdir(parents=True, exist_ok=True)

# DATA SOURCES

IMD_URL = (
    "https://assets.publishing.service.gov.uk/media/"
    "6917414ab49cc44345161802/"
    "File_11_-_IoD2025_Local_Authority_District_"
    "Summaries__upper-tier__v2.xlsx"
)

IMD_RAW_FILE = RAW_DIR / "imd_2025_utla.xlsx"

# Fingertips Public Health API
FINGERTIPS_METADATA_URL = (
    "https://fingertips.phe.org.uk/api/"
    "indicator_metadata/csv/all"
)

FINGERTIPS_DATA_URL = (
    "https://fingertips.phe.org.uk/api/"
    "all_data/csv/for_one_indicator"
)

INDICATOR_SEARCH_TERMS = {
    "healthy_life_expectancy": "Healthy life expectancy at birth",
    "life_expectancy": "Life expectancy at birth",
    "economic_inactivity": "Economic inactivity rate",
}

DATABASE_FILE = DATABASE_DIR / "health_economic_inequality.db"