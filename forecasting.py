from pathlib import Path

import joblib
import pandas as pd
import numpy as np

from config import FEATURE_COLUMNS


FUTURE_BUSINESS_COLUMNS = [
    "new_registered_users",
    "active_users",
    "platform_visits",
    "paid_enrollments",
    "average_price",
    "discount_rate",
    "marketing_spend"
]

MODEL_ARTIFACT_PATH = Path("models/revenue_model.joblib")


def load_saved_model_artifact(model_path=MODEL_ARTIFACT_PATH):
    if not Path(model_path).exists():
        raise FileNotFoundError(
            f"Файл збереженої моделі не знайдено: {model_path}."
        )

    model_artifact = joblib.load(model_path)

    required_keys = [
        "model",
        "best_ml_model_name",
        "feature_columns",
        "prepared_data"
    ]

    missing_keys = [
        key for key in required_keys
        if key not in model_artifact
    ]

    if missing_keys:
        raise ValueError(
            "Файл моделі має некоректну структуру. "
            "Відсутні ключі: " + ", ".join(missing_keys)
        )

    return model_artifact


def create_future_base_features(df, forecast_start_date, forecast_end_date):
    df = df.copy().sort_values("date").reset_index(drop=True)

    future_dates = pd.date_range(
        start=pd.Timestamp(forecast_start_date),
        end=pd.Timestamp(forecast_end_date),
        freq="D"
    )

    future_df = pd.DataFrame({"date": future_dates})
    recent_data = df.tail(30).copy()

    for column in FUTURE_BUSINESS_COLUMNS:
        recent_mean = recent_data[column].mean()
        recent_std = recent_data[column].std()

        if pd.isna(recent_std):
            recent_std = 0

        values = np.random.default_rng(42).normal(
            loc=recent_mean,
            scale=recent_std * 0.15,
            size=len(future_df)
        )

        if column in [
            "new_registered_users",
            "active_users",
            "platform_visits",
            "paid_enrollments"
        ]:
            values = np.round(values).astype(int)
            values = np.maximum(values, 1)

        elif column == "discount_rate":
            values = np.clip(values, 0.02, 0.35)
            values = np.round(values, 4)

        else:
            values = np.maximum(values, 0)
            values = np.round(values, 2)

        future_df[column] = values

    future_df["platform_visits"] = np.maximum(
        future_df["platform_visits"],
        future_df["active_users"]
    )

    future_df["paid_enrollments"] = np.minimum(
        future_df["paid_enrollments"],
        future_df["active_users"]
    )

    future_df["conversion_rate"] = np.where(
        future_df["active_users"] > 0,
        future_df["paid_enrollments"] / future_df["active_users"],
        0
    )

    future_df["month"] = future_df["date"].dt.month
    future_df["day_of_week"] = future_df["date"].dt.dayofweek

    return future_df


def get_lag_value(revenue_history, lag):
    if len(revenue_history) >= lag:
        return revenue_history[-lag]

    return revenue_history[-1]


def create_single_feature_row(base_row, revenue_history):
    feature_row = base_row.to_dict()

    feature_row["revenue_lag_1"] = get_lag_value(revenue_history, 1)
    feature_row["revenue_lag_7"] = get_lag_value(revenue_history, 7)
    feature_row["revenue_lag_14"] = get_lag_value(revenue_history, 14)
    feature_row["revenue_lag_30"] = get_lag_value(revenue_history, 30)

    feature_row["revenue_rolling_mean_7"] = np.mean(revenue_history[-7:])
    feature_row["revenue_rolling_mean_30"] = np.mean(revenue_history[-30:])

    return feature_row


def iterative_predict_model(model, history_df, future_base_df):
    revenue_history = history_df["revenue"].astype(float).tolist()
    predictions = []

    for _, base_row in future_base_df.iterrows():
        feature_row = create_single_feature_row(base_row, revenue_history)
        x_future = pd.DataFrame([feature_row])[FEATURE_COLUMNS]

        prediction = float(model.predict(x_future)[0])
        prediction = max(prediction, 0)

        predictions.append(prediction)
        revenue_history.append(prediction)

    return np.array(predictions)


def forecast_selected_period_with_saved_model(
    df,
    model_artifact,
    forecast_start_date,
    forecast_end_date
):
    saved_feature_columns = model_artifact["feature_columns"]

    if list(saved_feature_columns) != list(FEATURE_COLUMNS):
        raise ValueError(
            "Список ознак у збереженій моделі не збігається "
            "з поточним списком FEATURE_COLUMNS у config.py."
        )

    saved_model = model_artifact["model"]

    future_base_df = create_future_base_features(
        df,
        forecast_start_date,
        forecast_end_date
    )

    final_prediction = iterative_predict_model(
        saved_model,
        df,
        future_base_df
    )

    future_forecast_table = pd.DataFrame({
        "date": future_base_df["date"].dt.strftime("%Y-%m-%d"),
        "predicted_revenue": np.round(final_prediction, 2)
    })

    return saved_model, future_base_df, future_forecast_table