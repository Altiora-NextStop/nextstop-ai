import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


def train_crowd_model(dataset_path):
    """
    Train a machine learning model to predict crowd level.
    """

    df = pd.read_csv(dataset_path)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Rename City / Town to City if needed
    if "City / Town" in df.columns:
        df = df.rename(columns={"City / Town": "City"})

    # Fill missing values
    df = df.fillna("N/A")

    # Features used to predict crowd level
    feature_columns = [
        "City",
        "Category",
        "Season",
        "Family Friendly (Y/N)",
        "Estimated Cost",
        "Transit Accessible (Y/N)",
        "Parking Available (Y/N)",
        "Weather Sensitivity"
    ]

    target_column = "Estimated Crowd Level"

    # Keep only needed columns
    df = df[feature_columns + [target_column]]

    # Encode text values into numbers
    encoders = {}

    for column in feature_columns + [target_column]:
        encoder = LabelEncoder()
        df[column] = encoder.fit_transform(df[column].astype(str))
        encoders[column] = encoder

    X = df[feature_columns]
    y = df[target_column]

    # Split data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42
    )

    # Create ML model
    model = DecisionTreeClassifier(random_state=42)

    # Train model
    model.fit(X_train, y_train)

    # Test model accuracy
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return model, encoders, accuracy, feature_columns, target_column


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
    weather_sensitivity
):
    """
    Predict crowd level for a new attraction scenario.
    """

    input_data = {
        "City": city,
        "Category": category,
        "Season": season,
        "Family Friendly (Y/N)": family_friendly,
        "Estimated Cost": estimated_cost,
        "Transit Accessible (Y/N)": transit_accessible,
        "Parking Available (Y/N)": parking_available,
        "Weather Sensitivity": weather_sensitivity
    }

    input_df = pd.DataFrame([input_data])

    # Encode input using same encoders from training
    for column in feature_columns:
        encoder = encoders[column]

        value = str(input_df.loc[0, column])

        # If new unseen value appears, use first known class
        if value not in encoder.classes_:
            value = encoder.classes_[0]

        input_df[column] = encoder.transform([value])

    prediction_encoded = model.predict(input_df)[0]

    prediction_label = encoders[target_column].inverse_transform(
        [prediction_encoded]
    )[0]

    return prediction_label