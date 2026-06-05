import pandas as pd


def recommend_attractions(
    dataset_path,
    city=None,
    season=None,
    category=None,
    crowd_preference=None,
    cost_preference=None,
    family_friendly=False,
    transit_required=False,
    parking_required=False
):
    """
    Recommend tourist attractions based on user preferences.
    """

    # Load dataset
    df = pd.read_csv(dataset_path)
    df.columns = df.columns.str.strip()

    recommendations = []

    for _, row in df.iterrows():
        score = 0

        # City match
        if city and str(row["City / Town"]).strip().lower() == city.lower():
            score += 25

        # Season match
        if season:
            row_season = str(row["Season"]).strip().lower()
            if row_season == season.lower() or row_season == "all season":
                score += 20

        # Category match
        if category and str(row["Category"]).strip().lower() == category.lower():
            score += 20

        # Crowd preference match
        if crowd_preference and str(row["Estimated Crowd Level"]).strip().lower() == crowd_preference.lower():
            score += 15

        # Cost preference match
        if cost_preference and str(row["Estimated Cost"]).strip().lower() == cost_preference.lower():
            score += 15

        # Family friendly preference
        if family_friendly and str(row["Family Friendly (Y/N)"]).strip().lower() == "y":
            score += 10

        # Transit preference
        if transit_required and str(row["Transit Accessible (Y/N)"]).strip().lower() == "y":
            score += 10

        # Parking preference
        if parking_required and str(row["Parking Available (Y/N)"]).strip().lower() == "y":
            score += 10

        recommendations.append({
            "Attraction Name": row["Attraction Name"],
            "City": row["City / Town"],
            "Category": row["Category"],
            "Season": row["Season"],
            "Crowd Level": row["Estimated Crowd Level"],
            "Estimated Cost": row["Estimated Cost"],
            "Family Friendly": row["Family Friendly (Y/N)"],
            "Transit Accessible": row["Transit Accessible (Y/N)"],
            "Parking Available": row["Parking Available (Y/N)"],
            "Recommendation Score": score
        })

    result = pd.DataFrame(recommendations)

    # Sort highest scores first
    result = result.sort_values(by="Recommendation Score", ascending=False)

    # Return top 5 results
    return result.head(5)