"""Observable Framework data loader — joins the per-comment tables into a
single wide CSV that the site's pages can consume.

Runs at build time; stdout becomes src/data/comments.csv.

Columns:
    Document ID, Organization Name, Country, State/Province, Posted Date,
    stakeholder_type, cluster_size, full_text_chars,
    <12 codebook fields from comments_coded>,
    <topic area engagement + primary_topic_area + 5 excerpts>,
    regulations_url (direct link to the source)
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

BASE = Path(__file__).parent
STAKE = BASE / "comments_with_stakeholder.csv"
CODED = BASE / "comments_coded.csv"
TOPICS = BASE / "comments_topic_areas.csv"


def main() -> None:
    stake = pd.read_csv(STAKE, dtype=str, keep_default_na=False)
    coded = pd.read_csv(CODED, dtype=str, keep_default_na=False)
    topics = pd.read_csv(TOPICS, dtype=str, keep_default_na=False)

    # Reps = one row per cluster. Use longest full_text as canonical row.
    stake["full_text_chars_i"] = pd.to_numeric(stake["full_text_chars"], errors="coerce").fillna(0).astype(int)
    reps = (stake
        .sort_values(["cluster_id", "full_text_chars_i"], ascending=[True, False])
        .groupby("cluster_id", as_index=False).head(1)
    )
    keep = ["Document ID", "Organization Name", "Country", "State/Province",
            "Posted Date", "stakeholder_type", "cluster_size", "full_text_chars"]
    reps = reps[keep]

    # Join codebook
    merged = reps.merge(coded, on="Document ID", how="left", suffixes=("", "_c"))
    # Join topic-area engagement
    merged = merged.merge(topics, on="Document ID", how="left", suffixes=("", "_t"))

    # Build regulations.gov URL
    merged["regulations_url"] = (
        "https://www.regulations.gov/comment/" + merged["Document ID"].fillna("")
    )

    # Drop duplicate cluster_size columns if any
    if "cluster_size_c" in merged.columns:
        merged = merged.drop(columns=["cluster_size_c"])

    merged.to_csv(sys.stdout, index=False)


if __name__ == "__main__":
    main()
