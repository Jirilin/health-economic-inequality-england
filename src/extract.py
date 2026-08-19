from io import StringIO

import pandas as pd
import requests

from config import (
    RAW_DIR,
    IMD_URL,
    IMD_RAW_FILE,
    FINGERTIPS_METADATA_URL,
    FINGERTIPS_DATA_URL,
    INDICATOR_SEARCH_TERMS,
)

def download_binary_file(url, destination):
   
    print(f"Downloading: {url}")

    response = requests.get(url, timeout=120)
    response.raise_for_status()

    destination.write_bytes(response.content)

    print(f"Saved: {destination}")

def download_imd():
    
    if IMD_RAW_FILE.exists():
        print("IMD file already exists.")
        return

    download_binary_file(IMD_URL, IMD_RAW_FILE)


def download_fingertips_metadata():
    
    response = requests.get(
        FINGERTIPS_METADATA_URL,
        timeout=120,
    )

    response.raise_for_status()

    return pd.read_csv(StringIO(response.text))


def find_column(df, possible_terms):
    
    for column in df.columns:
        lower = str(column).strip().lower()

        for term in possible_terms:
            if term.lower() in lower:
                return column

    raise KeyError(
        f"Could not locate column matching: {possible_terms}"
    )


def clean_indicator_name(name):
    
    name = str(name).strip()

    if " - " in name:
        name = name.split(" - ", 1)[1]

    return name.strip().lower()


def resolve_indicator_id(metadata, search_term):
    
    id_column = find_column(
        metadata,
        ["indicator id"],
    )

    name_column = find_column(
        metadata,
        ["indicator name", "indicator"],
    )

    working = metadata.copy()

    working["_clean_name"] = (
        working[name_column]
        .astype(str)
        .apply(clean_indicator_name)
    )

    target = search_term.strip().lower()

    # First attempt exact match
    exact = working[
        working["_clean_name"] == target
    ]

    if not exact.empty:
        row = exact.iloc[0]

        return int(row[id_column]), row[name_column]

    # Then attempt contains
    matches = working[
        working["_clean_name"].str.contains(
            target,
            case=False,
            regex=False,
            na=False,
        )
    ]

    if matches.empty:
        raise ValueError(
            f"No Fingertips indicator found for: {search_term}"
        )

    # Prefer shortest matching name
    matches = matches.copy()

    matches["_length"] = (
        matches["_clean_name"].str.len()
    )

    row = matches.sort_values("_length").iloc[0]

    return int(row[id_column]), row[name_column]


def download_indicator(slug, indicator_id):
    
    response = requests.get(
        FINGERTIPS_DATA_URL,
        params={"indicator_id": indicator_id},
        timeout=120,
    )

    response.raise_for_status()

    df = pd.read_csv(
        StringIO(response.text),
        low_memory=False,
    )

    destination = RAW_DIR / f"{slug}.csv"

    df.to_csv(destination, index=False)

    print(
        f"Downloaded {slug}: "
        f"{indicator_id} -> {destination}"
    )

    return df


def extract_all():
    
    print("\n--- EXTRACTING DATA ---")

    download_imd()

    metadata = download_fingertips_metadata()

    manifest = []

    for slug, search_term in INDICATOR_SEARCH_TERMS.items():

        indicator_id, official_name = resolve_indicator_id(
            metadata,
            search_term,
        )

        print(
            f"{slug}: {indicator_id} | {official_name}"
        )

        download_indicator(
            slug,
            indicator_id,
        )

        manifest.append(
            {
                "slug": slug,
                "indicator_id": indicator_id,
                "indicator_name": official_name,
            }
        )

    pd.DataFrame(manifest).to_csv(
        RAW_DIR / "indicator_manifest.csv",
        index=False,
    )

    print("Extraction completed.")