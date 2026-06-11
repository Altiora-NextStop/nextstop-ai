import pandas as pd


def load_dataset(dataset_path):
    """
    Load and clean the tourism dataset.
    This function handles column name issues such as:
    - extra spaces
    - City / Town instead of City
    - missing blank values
    """
    df = pd.read_csv(dataset_path)

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    # Rename City / Town to City if needed
    if "City / Town" in df.columns:
        df = df.rename(columns={"City / Town": "City"})

    # Replace empty cells with N/A
    df = df.fillna("N/A")

    return df


def recommend_attractions(
    dataset_path,
    city=None,
    season=None,
    category=None,
    crowd_preference=None,
    cost_preference=None,
    family_friendly=False,
    transit_required=False,
    parking_required=False,
    top_n=5
):
    """
    Recommend tourist attractions based on user preferences using a scoring model.
    """

    df = load_dataset(dataset_path)

    required_columns = [
        "Attraction Name",
        "City",
        "Province",
        "Category",
        "Season",
        "Estimated Crowd Level",
        "Family Friendly (Y/N)",
        "Estimated Cost",
        "Transit Accessible (Y/N)",
        "Parking Available (Y/N)"
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(
            f"Missing required columns in dataset: {missing_columns}\n"
            f"Available columns are: {list(df.columns)}"
        )

    recommendations = []

    for _, row in df.iterrows():
        score = 0
        reasons = []

        # City match
        if city and str(row["City"]).strip().lower() == city.lower():
            score += 25
            reasons.append("City match")

        # Season match
        if season:
            row_season = str(row["Season"]).strip().lower()
            if row_season == season.lower() or row_season == "all season":
                score += 20
                reasons.append("Season match")

        # Category match
        if category and str(row["Category"]).strip().lower() == category.lower():
            score += 20
            reasons.append("Category match")

        # Crowd preference match
        if crowd_preference and str(row["Estimated Crowd Level"]).strip().lower() == crowd_preference.lower():
            score += 15
            reasons.append("Preferred crowd level")

        # Cost preference match
        if cost_preference and str(row["Estimated Cost"]).strip().lower() == cost_preference.lower():
            score += 15
            reasons.append("Preferred cost")

        # Family friendly preference
        if family_friendly and str(row["Family Friendly (Y/N)"]).strip().lower() == "y":
            score += 10
            reasons.append("Family friendly")

        # Transit preference
        if transit_required and str(row["Transit Accessible (Y/N)"]).strip().lower() == "y":
            score += 10
            reasons.append("Transit available")

        # Parking preference
        if parking_required and str(row["Parking Available (Y/N)"]).strip().lower() == "y":
            score += 10
            reasons.append("Parking available")

        recommendations.append({
            "Attraction Name": row["Attraction Name"],
            "City": row["City"],
            "Province": row["Province"],
            "Category": row["Category"],
            "Season": row["Season"],
            "Crowd Level": row["Estimated Crowd Level"],
            "Estimated Cost": row["Estimated Cost"],
            "Family Friendly": row["Family Friendly (Y/N)"],
            "Transit Accessible": row["Transit Accessible (Y/N)"],
            "Parking Available": row["Parking Available (Y/N)"],
            "Recommendation Score": score,
            "Why Recommended": ", ".join(reasons) if reasons else "General match"
        })

    result = pd.DataFrame(recommendations)

    # Remove zero-score results unless all results are zero
    if result["Recommendation Score"].max() > 0:
        result = result[result["Recommendation Score"] > 0]

    result = result.sort_values(by="Recommendation Score", ascending=False)

    return result.head(top_n)


def find_hidden_gems(dataset_path, city=None, category=None, top_n=5):
    """
    Find lower-crowd attractions that can be recommended as hidden gems.
    """
    df = load_dataset(dataset_path)

    if city:
        df = df[df["City"].str.strip().str.lower() == city.lower()]

    if category:
        df = df[df["Category"].str.strip().str.lower() == category.lower()]

    df = df[df["Estimated Crowd Level"].str.strip().str.lower().isin(["low", "medium"])]

    return df[
        [
            "Attraction Name",
            "City",
            "Category",
            "Estimated Crowd Level",
            "Estimated Cost",
            "Best Visit Time"
        ]
    ].head(top_n)
