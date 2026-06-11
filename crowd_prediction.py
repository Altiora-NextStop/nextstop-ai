def predict_crowd_level(
    base_crowd,
    season,
    day_type,
    weather,
    category
):
    """
    Predict crowd level based on tourism conditions.
    """

    score = 0

    # Base crowd from dataset
    base_crowd = str(base_crowd).strip().lower()

    if base_crowd == "low":
        score += 1
    elif base_crowd == "medium":
        score += 2
    elif base_crowd == "high":
        score += 3

    # Season impact
    season = str(season).strip().lower()

    if season == "summer":
        score += 2
    elif season == "winter":
        score += 1
    elif season == "all season":
        score += 1

    # Weekend impact
    day_type = str(day_type).strip().lower()

    if day_type == "weekend":
        score += 2
    elif day_type == "weekday":
        score += 0

    # Weather impact
    weather = str(weather).strip().lower()

    if weather in ["sunny", "clear"]:
        score += 1
    elif weather in ["rain", "snow", "storm"]:
        score -= 1

    # Category impact
    category = str(category).strip().lower()

    if category in ["lake", "waterfall", "park", "scenic view", "hiking"]:
        if weather in ["sunny", "clear"]:
            score += 1
        elif weather in ["rain", "snow", "storm"]:
            score -= 1

    if category in ["museum", "science centre", "landmark", "historical site"]:
        if weather in ["rain", "snow"]:
            score += 1

    # Final prediction
    if score <= 3:
        return "Low"
    elif score <= 6:
        return "Medium"
    else:
        return "High"