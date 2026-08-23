import json

import pandas as pd

from sklearn.cluster import KMeans

from sklearn.preprocessing import (
    StandardScaler
)

from sklearn.metrics import (
    silhouette_score
)

from config import (
    PROCESSED_DIR,
    OUTPUT_DIR,
)


FEATURES = [
    "imd_deprivation_percentile",
    "healthy_life_expectancy_sex_mean",
    "economic_inactivity_pct",
    "unhealthy_years_estimate",
]


def segment_names(k):

    if k == 2:

        return [
            "Lower vulnerability",
            "Higher vulnerability",
        ]

    if k == 3:

        return [
            "Lower vulnerability",
            "Moderate vulnerability",
            "Higher vulnerability",
        ]

    if k == 4:

        return [
            "Lower vulnerability",
            "Lower-moderate vulnerability",
            "Upper-moderate vulnerability",
            "Higher vulnerability",
        ]

    return [
        "Lowest vulnerability",
        "Lower vulnerability",
        "Moderate vulnerability",
        "Higher vulnerability",
        "Highest vulnerability",
    ]


def run_clustering():

    print(
        "\n--- CLUSTERING AREAS ---"
    )

    df = pd.read_csv(
        PROCESSED_DIR
        / "analytics_master.csv"
    )


    features = [
        column
        for column in FEATURES
        if column in df.columns
    ]


    X = df[
        features
    ].copy()


    # Median imputation
    X = X.fillna(
        X.median(
            numeric_only=True
        )
    )


    scaler = StandardScaler()

    scaled = scaler.fit_transform(
        X
    )


    max_k = min(
        5,
        len(df) - 1,
    )


    scores = {}


    for k in range(
        2,
        max_k + 1,
    ):

        candidate = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=20,
        )

        labels = (
            candidate.fit_predict(
                scaled
            )
        )


        score = silhouette_score(
            scaled,
            labels,
        )

        scores[k] = score


    best_k = max(
        scores,
        key=scores.get,
    )


    model = KMeans(
        n_clusters=best_k,
        random_state=42,
        n_init=20,
    )


    df["cluster_id"] = (
        model.fit_predict(
            scaled
        )
    )


    profile = (
        df
        .groupby("cluster_id")
        [
            features
            + [
                "vulnerability_score"
            ]
        ]
        .mean()
    )


    ordered_clusters = (
        profile[
            "vulnerability_score"
        ]
        .sort_values()
        .index
        .tolist()
    )


    names = segment_names(
        best_k
    )


    name_mapping = {
        cluster:
            names[index]

        for index, cluster
        in enumerate(
            ordered_clusters
        )
    }


    df["segment_name"] = (
        df["cluster_id"]
        .map(name_mapping)
    )


    profile = (
        df
        .groupby(
            [
                "cluster_id",
                "segment_name",
            ],
            as_index=False,
        )
        [
            features
            + [
                "vulnerability_score"
            ]
        ]
        .mean()
    )


    counts = (
        df["cluster_id"]
        .value_counts()
        .rename("area_count")
        .reset_index()
    )


    profile = profile.merge(
        counts,
        on="cluster_id",
        how="left",
    )


    df.to_csv(
        PROCESSED_DIR
        / "analytics_enriched.csv",
        index=False,
    )


    profile.to_csv(
        PROCESSED_DIR
        / "cluster_profiles.csv",
        index=False,
    )


    metadata = {
        "selected_clusters":
            int(best_k),

        "silhouette_scores":
            {
                str(k):
                    float(value)

                for k, value
                in scores.items()
            },

        "features":
            features,

        "random_state":
            42,
    }


    output_file = (
        OUTPUT_DIR
        / "tables"
        / "clustering_metadata.json"
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metadata,
            file,
            indent=2,
        )


    print(
        f"Selected clusters: "
        f"{best_k}"
    )


    return df, profile