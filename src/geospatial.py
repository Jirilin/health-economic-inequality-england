import geopandas as gpd
import pandas as pd

from config import (
    DATA_DIR,
    PROCESSED_DIR,
)


BOUNDARY_FILE = (
    DATA_DIR
    / "geospatial"
    / "utla_boundaries.geojson"
)


OUTPUT_FILE = (
    PROCESSED_DIR
    / "heiva_map.geojson"
)


def detect_code_column(
    geo_df,
    valid_codes,
):
    """
    Identify geographic code column by
    finding the column with the largest
    overlap with HEIVA area codes.
    """

    best_column = None
    best_matches = 0


    for column in geo_df.columns:

        if column == "geometry":
            continue


        values = set(
            geo_df[column]
            .astype(str)
            .str.strip()
        )


        matches = len(
            values.intersection(
                valid_codes
            )
        )


        if matches > best_matches:

            best_column = column
            best_matches = matches


    if (
        best_column is None
        or best_matches == 0
    ):

        raise ValueError(
            "Unable to identify the "
            "geographic area-code column."
        )


    print(
        f"Boundary code column: "
        f"{best_column}"
    )

    print(
        f"Matched areas: "
        f"{best_matches}"
    )


    return best_column


def build_geospatial_dataset():

    print(
        "\n--- GEOSPATIAL ANALYSIS ---"
    )


    if not BOUNDARY_FILE.exists():

        print(
            "Boundary file not found. "
            "Skipping geographic build."
        )

        return None


    data = pd.read_csv(
        PROCESSED_DIR
        / "analytics_enriched.csv"
    )


    geo = gpd.read_file(
        BOUNDARY_FILE
    )


    valid_codes = set(
        data["area_code"]
        .astype(str)
    )


    code_column = (
        detect_code_column(
            geo,
            valid_codes,
        )
    )


    geo["area_code"] = (
        geo[code_column]
        .astype(str)
        .str.strip()
    )


    # Keep England HEIVA areas only
    geo = geo[
        geo["area_code"]
        .isin(valid_codes)
    ].copy()


    joined = geo.merge(
        data,
        on="area_code",
        how="inner",
    )


    # Browser-friendly coordinate system
    joined = joined.to_crs(
        epsg=4326
    )


    joined.to_file(
        OUTPUT_FILE,
        driver="GeoJSON",
    )


    print(
        f"Geographic areas exported: "
        f"{len(joined)}"
    )


    return joined