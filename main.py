from recommendation_engine import recommend_attractions, find_hidden_gems
from hidden_gem import find_hidden_gems
from ml_crowd_model import train_crowd_model, predict_ml_crowd

DATASET_PATH = "data/tourism_dataset.csv"


print("\n=== ALTÍORA AI TOURISM RECOMMENDATION ENGINE ===\n")

# Test Case 1: Banff lake recommendations
banff_results = recommend_attractions(
    dataset_path=DATASET_PATH,
    city="Banff",
    season="Summer",
    category="Lake",
    crowd_preference="Low",
    cost_preference="Free",
    family_friendly=True,
    transit_required=False,
    parking_required=True,
    top_n=5
)

print("Top Recommended Attractions for a Summer Lake Trip in Banff:\n")
print(banff_results.to_string(index=False))


# Test Case 2: Calgary family-friendly attractions
calgary_results = recommend_attractions(
    dataset_path=DATASET_PATH,
    city="Calgary",
    season="All Season",
    category=None,
    crowd_preference=None,
    cost_preference="Medium",
    family_friendly=True,
    transit_required=True,
    parking_required=True,
    top_n=5
)

print("\n\nTop Recommended Family-Friendly Attractions in Calgary:\n")
print(calgary_results.to_string(index=False))


# Test Case 3: Hidden gems in Banff
hidden_gems = find_hidden_gems(
    dataset_path=DATASET_PATH,
    city="Banff",
    category=None,
    top_n=5
)

print("\n\nHidden Gem Recommendations in Banff:\n")
print(hidden_gems.to_string(index=False))

from crowd_prediction import predict_crowd_level

predicted_crowd = predict_crowd_level(
    base_crowd="Medium",
    season="Summer",
    day_type="Weekend",
    weather="Rain",
    category="Lake"
)

print("\n\nCrowd Prediction Test:\n")
print("Predicted Crowd Level:", predicted_crowd)

hidden_gems = find_hidden_gems(
    dataset_path=DATASET_PATH,
    city="Banff",
    category=None,
    max_crowd_level="Medium",
    top_n=5
)

print("\n\nHidden Gem Recommendations:\n")
print(hidden_gems.to_string(index=False))

print("\n\n=== MACHINE LEARNING CROWD PREDICTION MODEL ===\n")

model, encoders, accuracy, feature_columns, target_column = train_crowd_model(DATASET_PATH)

print("ML Model Accuracy:", round(accuracy * 100, 2), "%")

ml_prediction = predict_ml_crowd(
    model=model,
    encoders=encoders,
    feature_columns=feature_columns,
    target_column=target_column,
    city="Banff",
    category="Lake",
    season="Summer",
    family_friendly="Y",
    estimated_cost="Free",
    transit_accessible="Y",
    parking_available="Y",
    weather_sensitivity="Medium"
)

print("Predicted Crowd Level:", ml_prediction)