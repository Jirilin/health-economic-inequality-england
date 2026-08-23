from src.extract import extract_all
from src.transform import transform_all
from src.load_database import load_database
from src.analyse import run_analysis

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

dfrom src.extract import (
    extract_all
)

from src.transform import (
    transform_all
)

from src.load_database import (
    load_database
)

from src.analyse import (
    run_analysis
)

from src.history import (
    build_history
)

from src.forecasting import (
    forecast_economic_inactivity
)

from src.clustering import (
    run_clustering
)

from src.geospatial import (
    build_geospatial_dataset
)

from src.quality import (
    run_quality_checks
)

from src.load_advanced_database import (
    load_advanced_database
)


def main():

    print(
        "\n"
        "====================================\n"
        " HEIVA ENGLAND — ADVANCED PIPELINE\n"
        "====================================\n"
    )


    # VERSION 1

    extract_all()

    transform_all()

    load_database()

    run_analysis()

    load_database()


    # VERSION 2

    build_history()

    forecast_economic_inactivity()


    # VERSION 3

    run_clustering()

    build_geospatial_dataset()


    # VERSION 5

    run_quality_checks()

    load_advanced_database()


    print(
        "\n"
        "====================================\n"
        " HEIVA PIPELINE COMPLETED\n"
        "====================================\n"
    )


    print(
        "\nStart the application with:\n\n"
        "streamlit run app.py"
    )


if __name__ == "__main__":

    main()