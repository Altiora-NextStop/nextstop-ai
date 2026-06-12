from ai_service import (
    get_recommendations,
    get_rule_based_crowd_prediction,
    get_ml_crowd_prediction
)


def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def print_attractions(results):
    for index, item in enumerate(results, start=1):
        print(f"\n{index}. {item.get('Attraction Name')}")
        print(f"   City: {item.get('City')}")
        print(f"   Category: {item.get('Category')}")
        print(f"   Crowd Level: {item.get('Crowd Level') or item.get('Estimated Crowd Level')}")
        print(f"   Cost: {item.get('Estimated Cost')}")
        print(f"   Best Visit Time: {item.get('Best Visit Time', 'N/A')}")
        if item.get("Recommendation Score") is not None:
            print(f"   Recommendation Score: {item.get('Recommendation Score')}")
        if item.get("Why Recommended"):
            print(f"   Why Recommended: {item.get('Why Recommended')}")


print_section("ALTÍORA API TEST 1: TOURISM RECOMMENDATIONS")

recommendation_input = {
    "city": "Banff",
    "season": "Summer",
    "category": "Lake",
    "crowd_preference": "Low",
    "cost_preference": "Free",
    "family_friendly": True,
    "transit_required": False,
    "parking_required": True,
    "top_n": 5
}

print_attractions(get_recommendations(recommendation_input))


print_section("ALTÍORA API TEST 2: HIDDEN GEM RECOMMENDATIONS")

hidden_gem_input = {
    "city": "Banff",
    "category": None,
    "max_crowd_level": "Medium",
    "top_n": 5
}



print_section("ALTÍORA API TEST 3: RULE-BASED CROWD PREDICTION")

rule_crowd_input = {
    "base_crowd": "Medium",
    "season": "Summer",
    "day_type": "Weekend",
    "weather": "Sunny",
    "category": "Lake"
}

rule_prediction = get_rule_based_crowd_prediction(rule_crowd_input)
print(f"Predicted Crowd Level: {rule_prediction['predicted_crowd_level']}")


print_section("ALTÍORA API TEST 4: MACHINE LEARNING CROWD PREDICTION")

ml_crowd_input = {
    "city": "Banff",
    "category": "Lake",
    "season": "Summer",
    "family_friendly": "Y",
    "estimated_cost": "Free",
    "transit_accessible": "Y",
    "parking_available": "Y",
    "weather_sensitivity": "Medium",
    "indoor_outdoor": "Outdoor",
    "reservation_needed": "Usually not required"
}

ml_prediction = get_ml_crowd_prediction(ml_crowd_input)
print(f"Predicted Crowd Level: {ml_prediction['predicted_crowd_level']}")
print(f"Model Accuracy: {ml_prediction['model_accuracy']}%")
