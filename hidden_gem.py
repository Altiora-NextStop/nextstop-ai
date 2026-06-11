import pandas as pd


def find_hidden_gems(
    dataset_path,
    city=None,
    category=None,
    max_crowd_level="Medium",
    top_n=5
):
    """
    Finds lower-crowd attractions that can be recommended as hidden gems.
    """

    df = pd.read_csv(dataset_path)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Rename City / Town to City if needed
    if "City / Town" in df.columns:
        df = df.rename(columns={"City / Town": "City"})

    # Fill blank cells
    df = df.fillna("N/A")

    # Filter by city if provided
    if city:
        df = df[df["City"].str.strip().str.lower() == city.lower()]

    # Filter by category if provided
    if category:
        df = df[df["Category"].str.strip().str.lower() == category.lower()]

    # Crowd filter
    allowed_crowds = ["low"]

    if max_crowd_level.lower() == "medium":
        allowed_crowds = ["low", "medium"]

    df = df[
        df["Estimated Crowd Level"]
        .str.strip()
        .str.lower()
        .isin(allowed_crowds)
    ]

    # Prefer free/low-cost places first
    cost_priority = {
        "free": 1,
        "low": 2,
        "medium": 3,
        "high": 4
    }

    df["Cost Priority"] = (
        df["Estimated Cost"]
        .str.strip()
        .str.lower()
        .map(cost_priority)
        .fillna(5)
    )

    df = df.sort_values(
        by=["Estimated Crowd Level", "Cost Priority", "Attraction Name"],
        ascending=[True, True, True]
    )

    return df[
        [
            "Attraction Name",
            "City",
            "Category",
            "Estimated Crowd Level",
            "Estimated Cost",
            "Family Friendly (Y/N)",
            "Parking Available (Y/N)",
            "Best Visit Time"
        ]
    ].head(top_n)