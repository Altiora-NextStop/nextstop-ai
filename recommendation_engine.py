import pandas as pd


def load_dataset(dataset_path):
    df = pd.read_csv(dataset_path)
    df.columns = df.columns.str.strip()

    rename_map = {
        "City / Town": "City",
        "Verified Season / Operating Pattern": "Season",
        "Crowd Demand Indicator": "Crowd Demand",
        "Cost / Admission Type": "Cost",
        "Transit Access": "Transit Access",
        "Parking Availability": "Parking",
        "Recommended Visit Duration": "Visit Duration",
        "Official / Reference Source": "Data Source",
    }

    df = df.rename(columns=rename_map)
    df = df.fillna("N/A")

    return df


def normalize_crowd(value):
    text = str(value).lower()

    if "very high" in text or "high" in text:
        return "High"
    if "moderate" in text or "medium" in text:
        return "Medium"
    if "low" in text:
        return "Low"

    return "Medium"


def is_yes(value):
    text = str(value).strip().lower()
    return text.startswith("y") or "yes" in text or "available" in text


def is_no(value):
    text = str(value).strip().lower()
    return text.startswith("n") or "no" in text or "not available" in text


def preference_matches(text_value, preference):
    if not preference:
        return False

    text_value = str(text_value).lower()
    preference = str(preference).lower()

    if preference in text_value:
        return True

    if preference == "free" and "free" in text_value:
        return True

    if preference in ["paid", "medium", "high"] and ("paid" in text_value or "ticket" in text_value or "admission" in text_value):
        return True

    return False


def season_matches(row_season, user_season):
    if not user_season:
        return False

    row_season = str(row_season).lower()
    user_season = str(user_season).lower()

    if user_season in row_season:
        return True

    if "year-round" in row_season or "year round" in row_season or "all season" in row_season:
        return True

    return False


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
    df = load_dataset(dataset_path)

    recommendations = []

    for _, row in df.iterrows():
        score = 0
        reasons = []

        row_city = str(row.get("City", "")).strip()
        row_category = str(row.get("Category", "")).strip()
        row_season = str(row.get("Season", "")).strip()
        row_crowd = normalize_crowd(row.get("Crowd Demand", "Medium"))

        if city and row_city.lower() == city.lower().strip():
            score += 25
            reasons.append("City match")

        if season and season_matches(row_season, season):
            score += 20
            reasons.append("Season match")

        if category and row_category.lower() == category.lower().strip():
            score += 20
            reasons.append("Category match")

        if crowd_preference and row_crowd.lower() == crowd_preference.lower().strip():
            score += 15
            reasons.append("Preferred crowd level")

        if cost_preference and preference_matches(row.get("Cost", ""), cost_preference):
            score += 15
            reasons.append("Cost preference match")

        if family_friendly and is_yes(row.get("Family Friendly", "")):
            score += 10
            reasons.append("Family friendly")

        if transit_required and not is_no(row.get("Transit Access", "")):
            score += 10
            reasons.append("Transit option available")

        if parking_required and not is_no(row.get("Parking", "")):
            score += 10
            reasons.append("Parking available")

        recommendations.append({
            "Attraction Name": row.get("Attraction Name", "N/A"),
            "City": row_city,
            "Province": row.get("Province", "N/A"),
            "Category": row_category,
            "Season": row_season,
            "Crowd Level": row_crowd,
            "Crowd Detail": row.get("Crowd Demand", "N/A"),
            "Estimated Cost": row.get("Cost", "N/A"),
            "Family Friendly": row.get("Family Friendly", "N/A"),
            "Transit Access": row.get("Transit Access", "N/A"),
            "Parking": row.get("Parking", "N/A"),
            "Best Visit Time": row.get("Best Visit Time", "N/A"),
            "Visit Duration": row.get("Visit Duration", "N/A"),
            "Recommendation Score": score,
            "Why Recommended": ", ".join(reasons) if reasons else "General match"
        })

    result = pd.DataFrame(recommendations)

    if not result.empty and result["Recommendation Score"].max() > 0:
        result = result[result["Recommendation Score"] > 0]

    result = result.sort_values(
        by=["Recommendation Score", "Attraction Name"],
        ascending=[False, True]
    )

    return result.head(top_n)
