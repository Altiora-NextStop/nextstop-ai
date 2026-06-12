import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from recommendation_engine import load_dataset, normalize_crowd


def train_crowd_model(dataset_path):
    df = load_dataset(dataset_path)

    df["Crowd Target"] = df["Crowd Demand"].apply(normalize_crowd)

    feature_columns = [
        "City",
        "Category",
        "Season",
        "Family Friendly",
        "Cost",
        "Transit Access",
        "Parking",
        "Weather Sensitivity",
        "Indoor/Outdoor",
        "Reservation Needed"
    ]

    target_column = "Crowd Target"

    available_features = [col for col in feature_columns if col in df.columns]
    df = df[available_features + [target_column]].fillna("N/A")

    encoders = {}

    for column in available_features + [target_column]:
        encoder = LabelEncoder()
        df[column] = encoder.fit_transform(df[column].astype(str))
        encoders[column] = encoder

    X = df[available_features]
    y = df[target_column]

    # If dataset is too small or too unbalanced, still train safely.
    stratify = y if y.nunique() > 1 and y.value_counts().min() >= 2 else None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=stratify
    )

    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return model, encoders, accuracy, available_features, target_column


def safe_encode(encoder, value):
    value = str(value)
    if value not in encoder.classes_:
        return encoder.transform([encoder.classes_[0]])[0]
    return encoder.transform([value])[0]


def predict_ml_crowd(
    model,
    encoders,
    feature_columns,
    target_column,
    city,
    category,
    season,
    family_friendly,
    estimated_cost,
    transit_accessible,
    parking_available,
    weather_sensitivity,
    indoor_outdoor="Outdoor",
    reservation_needed="Usually not required"
):
    input_data = {
        "City": city,
        "Category": category,
        "Season": season,
        "Family Friendly": family_friendly,
        "Cost": estimated_cost,
        "Transit Access": transit_accessible,
        "Parking": parking_available,
        "Weather Sensitivity": weather_sensitivity,
        "Indoor/Outdoor": indoor_outdoor,
        "Reservation Needed": reservation_needed
    }

    encoded = {}

    for column in feature_columns:
        encoded[column] = safe_encode(encoders[column], input_data.get(column, "N/A"))

    input_df = pd.DataFrame([encoded])
    prediction_encoded = model.predict(input_df)[0]

    prediction_label = encoders[target_column].inverse_transform([prediction_encoded])[0]

    return prediction_label
