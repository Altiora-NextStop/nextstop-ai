from ai_service import (
    get_recommendations,
    get_combined_crowd_prediction
)


def print_attractions(results):
    if not results:
        print("No matching attractions found. Try different preferences.")
        return

    for index, item in enumerate(results, start=1):
        print(f"\n{index}. {item.get('Attraction Name')}")
        print(f"   City: {item.get('City')}")
        print(f"   Category: {item.get('Category')}")
        print(f"   Crowd Level: {item.get('Crowd Level')}")
        print(f"   Estimated Cost: {item.get('Estimated Cost')}")
        print(f"   Best Visit Time: {item.get('Best Visit Time', 'N/A')}")

        if item.get("Recommendation Score") is not None:
            print(f"   Recommendation Score: {item.get('Recommendation Score')}")

        if item.get("Why Recommended"):
            print(f"   Why Recommended: {item.get('Why Recommended')}")


print("\n==========================================")
print("      ALTÍORA AI TOURISM ASSISTANT")
print("==========================================\n")

# ==========================================
# USER INPUTS
# ==========================================

city = input(
    "Enter city/town (Example: Banff, Calgary, Jasper): "
).strip()

season = input(
    "Enter season (Summer, Winter, Year-round): "
).strip()

category = input(
    "Enter category (Lake, Hiking, Museum, Park, Landmark): "
).strip()

crowd = input(
    "Preferred crowd level (Low, Medium, High): "
).strip()

cost = input(
    "Preferred cost (Free, Paid): "
).strip()

family_friendly = (
    input("Family friendly required? (Y/N): ")
    .strip()
    .lower() == "y"
)

parking_required = (
    input("Parking required? (Y/N): ")
    .strip()
    .lower() == "y"
)

transit_required = (
    input("Transit required? (Y/N): ")
    .strip()
    .lower() == "y"
)

weather = input(
    "Current weather (Sunny, Rain, Snow, Clear): "
).strip()

day_type = input(
    "Day type (Weekday/Weekend): "
).strip()


# ==========================================
# RECOMMENDATION ENGINE
# ==========================================

recommendation_input = {
    "city": city,
    "season": season,
    "category": category,
    "crowd_preference": crowd,
    "cost_preference": cost,
    "family_friendly": family_friendly,
    "parking_required": parking_required,
    "transit_required": transit_required,
    "top_n": 5
}

recommendations = get_recommendations(recommendation_input)

print("\n\n==========================================")
print("TOP RECOMMENDED ATTRACTIONS")
print("==========================================")

print_attractions(recommendations)


# ==========================================
# COMBINED CROWD PREDICTION
# ==========================================

combined_input = {
    "base_crowd": crowd,
    "city": city,
    "category": category,
    "season": season,
    "day_type": day_type,
    "weather": weather,
    "family_friendly": "Y" if family_friendly else "N",
    "estimated_cost": cost,
    "transit_accessible": "Y" if transit_required else "N",
    "parking_available": "Y" if parking_required else "N",
    "weather_sensitivity": "Medium",
    "indoor_outdoor": "Outdoor",
    "reservation_needed": "Usually not required"
}

combined_prediction = get_combined_crowd_prediction(
    combined_input
)

print("\n\n==========================================")
print("COMBINED CROWD PREDICTION")
print("==========================================")

print(
    f"Rule-Based Prediction: "
    f"{combined_prediction['rule_based_prediction']}"
)

print(
    f"ML Prediction: "
    f"{combined_prediction['ml_prediction']}"
)

print(
    f"Final Crowd Estimate: "
    f"{combined_prediction['final_crowd_estimate']}"
)

print(
    f"ML Model Accuracy: "
    f"{combined_prediction['model_accuracy']}%"
)


print("\n==========================================")
print("Thank you for using AltÍora AI!")
print("==========================================")