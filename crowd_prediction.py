def predict_crowd_level(
    base_crowd,
    season,
    day_type,
    weather,
    category
):
    score = 0

    base = str(base_crowd).lower()
    if "high" in base:
        score += 3
    elif "medium" in base or "moderate" in base:
        score += 2
    else:
        score += 1

    season = str(season).lower()
    if "summer" in season or "may-oct" in season:
        score += 2
    elif "winter" in season:
        score += 1
    elif "year" in season or "all" in season:
        score += 1

    day_type = str(day_type).lower()
    if day_type == "weekend":
        score += 2

    weather = str(weather).lower()
    category = str(category).lower()

    outdoor_categories = ["lake", "hiking", "park", "waterfall", "scenic view", "mountain", "garden", "beach"]
    indoor_categories = ["museum", "science centre", "landmark", "historical site", "shopping"]

    if weather in ["sunny", "clear"]:
        if category in outdoor_categories:
            score += 2
        else:
            score += 1

    if weather in ["rain", "snow", "storm"]:
        if category in outdoor_categories:
            score -= 1
        if category in indoor_categories:
            score += 1

    if score <= 3:
        return "Low"
    elif score <= 6:
        return "Medium"
    else:
        return "High"
