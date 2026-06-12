from recommendation_engine import recommend_attractions
from crowd_prediction import predict_crowd_level
from ml_crowd_model import train_crowd_model, predict_ml_crowd

DATASET_PATH = "data/tourism_dataset.csv"


def get_recommendations(user_preferences):
    results = recommend_attractions(
        dataset_path=DATASET_PATH,
        city=user_preferences.get("city"),
        season=user_preferences.get("season"),
        category=user_preferences.get("category"),
        crowd_preference=user_preferences.get("crowd_preference"),
        cost_preference=user_preferences.get("cost_preference"),
        family_friendly=user_preferences.get("family_friendly", False),
        transit_required=user_preferences.get("transit_required", False),
        parking_required=user_preferences.get("parking_required", False),
        top_n=user_preferences.get("top_n", 5)
    )

    return results.to_dict(orient="records")


def get_rule_based_crowd_prediction(crowd_input):
    prediction = predict_crowd_level(
        base_crowd=crowd_input.get("base_crowd"),
        season=crowd_input.get("season"),
        day_type=crowd_input.get("day_type"),
        weather=crowd_input.get("weather"),
        category=crowd_input.get("category")
    )

    return {
        "predicted_crowd_level": prediction
    }


def get_ml_crowd_prediction(crowd_input):
    model, encoders, accuracy, feature_columns, target_column = train_crowd_model(DATASET_PATH)

    prediction = predict_ml_crowd(
        model=model,
        encoders=encoders,
        feature_columns=feature_columns,
        target_column=target_column,
        city=crowd_input.get("city"),
        category=crowd_input.get("category"),
        season=crowd_input.get("season"),
        family_friendly=crowd_input.get("family_friendly"),
        estimated_cost=crowd_input.get("estimated_cost"),
        transit_accessible=crowd_input.get("transit_accessible"),
        parking_available=crowd_input.get("parking_available"),
        weather_sensitivity=crowd_input.get("weather_sensitivity"),
        indoor_outdoor=crowd_input.get("indoor_outdoor", "Outdoor"),
        reservation_needed=crowd_input.get("reservation_needed", "Usually not required")
    )

    return {
        "predicted_crowd_level": prediction,
        "model_accuracy": round(accuracy * 100, 2)
    }
