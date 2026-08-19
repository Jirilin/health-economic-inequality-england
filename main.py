from src.extract import extract_all
from src.transform import transform_all
from src.load_database import load_database
from src.analyse import run_analysis

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

def main():

    print(
        "\n"
        "=========================================\n"
        " HEIVA ENGLAND\n"
        " Health & Economic Inequality Analytics\n"
        "=========================================\n"
    )

    # 1. Extract
    extract_all()

    # 2. Transform
    transform_all()

    # 3. Load into SQL
    load_database()

    # 4. Analyse
    run_analysis()

    # Reload SQL after vulnerability score has been created.
    load_database()

    print(
        "\n"
        "=========================================\n"
        " PROJECT PIPELINE COMPLETED\n"
        "=========================================\n"
    )

    print(
        "Next step:\n"
        "Open data/processed/analytics_master.csv "
        "in Power BI."
    )


if __name__ == "__main__":
    main()