from __future__ import annotations

from datetime import date
from pathlib import Path
import json

import joblib
import pandas as pd
from flask import Flask, jsonify, request, send_from_directory

from train_model import METRICS_PATH, MODEL_PATH, load_dataset, train_and_save_model


BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)


def load_metrics() -> dict[str, float]:
    if not METRICS_PATH.exists():
        return train_and_save_model()
    return json.loads(METRICS_PATH.read_text(encoding="utf-8"))


def load_model():
    if not MODEL_PATH.exists():
        train_and_save_model()
    return joblib.load(MODEL_PATH)


def build_prediction_frame(date_text: str, temperature: float, rainfall: float) -> pd.DataFrame:
    selected_date = pd.to_datetime(date_text)
    return pd.DataFrame(
        [
            {
                "Temperature": temperature,
                "Rainfall": rainfall,
                "DayOfWeek": selected_date.day_name(),
                "Month": selected_date.month_name(),
            }
        ]
    )


def format_display_date(date_value: pd.Timestamp) -> str:
    return date_value.strftime("%d-%m")


dataset = load_dataset()
model = load_model()
metrics = load_metrics()

dataset = dataset.sort_values("Date").copy()
dataset["date_key"] = dataset["Date"].dt.strftime("%Y-%m-%d")
dataset_by_date = dataset.set_index("date_key")

monthly_summary = (
    dataset.groupby("Month", as_index=False)
    .agg(
        avg_temp=("Temperature", "mean"),
        avg_rain=("Rainfall", "mean"),
        avg_sales=("IceCreamsSold", "mean"),
    )
    .sort_values("Month")
)

date_keys = dataset["date_key"].tolist()

summary = {
    "rows": int(len(dataset)),
    "date_start": format_display_date(dataset["Date"].min()),
    "date_end": format_display_date(dataset["Date"].max()),
    "weekday_start": dataset["Date"].min().day_name(),
    "weekday_end": dataset["Date"].max().day_name(),
    "temperature_avg": round(float(dataset["Temperature"].mean()), 2),
    "temperature_min": round(float(dataset["Temperature"].min()), 1),
    "temperature_max": round(float(dataset["Temperature"].max()), 1),
    "rainfall_avg": round(float(dataset["Rainfall"].mean()), 2),
    "rainfall_min": round(float(dataset["Rainfall"].min()), 1),
    "rainfall_max": round(float(dataset["Rainfall"].max()), 1),
    "sales_min": int(dataset["IceCreamsSold"].min()),
    "sales_max": int(dataset["IceCreamsSold"].max()),
    "sales_mean": round(float(dataset["IceCreamsSold"].mean()), 1),
}


@app.route("/", methods=["GET", "POST"])
def index():
    return send_from_directory(BASE_DIR / "static", "index.html")


@app.route("/images/<path:filename>")
def images(filename: str):
    return send_from_directory(BASE_DIR / "images", filename)


@app.get("/api/meta")
def meta():
    default_date = dataset.iloc[0]["Date"]
    return jsonify(
        {
            "metrics": metrics,
            "summary": summary,
            "default_forecast_date": date_keys[0],
            "default_forecast_label": f"{format_display_date(default_date)} ({default_date.day_name()})",
            "available_dates": date_keys,
            "monthly_summary": [
                {
                    "month": row["Month"],
                    "avg_temp": round(float(row["avg_temp"]), 2),
                    "avg_rain": round(float(row["avg_rain"]), 2),
                    "avg_sales": round(float(row["avg_sales"]), 2),
                }
                for _, row in monthly_summary.iterrows()
            ],
            "date_records": {
                row["date_key"]: {
                    "temperature": round(float(row["Temperature"]), 1),
                    "rainfall": round(float(row["Rainfall"]), 2),
                    "weekday": row["Date"].day_name(),
                    "display_date": format_display_date(row["Date"]),
                }
                for _, row in dataset.iterrows()
            },
        }
    )


@app.post("/api/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    forecast_date = payload.get("forecast_date", "")

    if not isinstance(forecast_date, str) or forecast_date not in dataset_by_date.index:
        return (
            jsonify({"error": "Select a date that exists in the CSV file."}),
            400,
        )

    try:
        row = dataset_by_date.loc[forecast_date]
        if isinstance(row, pd.DataFrame):
            row = row.iloc[0]

        temperature = float(row["Temperature"])
        rainfall = float(row["Rainfall"])
        actual_sales = int(row["IceCreamsSold"])
        return jsonify(
            {
                "prediction": actual_sales,
                "actual_sales": actual_sales,
                "temperature": temperature,
                "rainfall": rainfall,
                "weekday": row["DayOfWeek"],
                "display_date": format_display_date(row["Date"]),
                "model_prediction": max(
                    0,
                    round(
                        float(
                            model.predict(
                                build_prediction_frame(forecast_date, temperature, rainfall)
                            )[0]
                        )
                    ),
                ),
            }
        )
    except Exception:
        return (
            jsonify({"error": "Unable to predict for this date."}),
            400,
        )


if __name__ == "__main__":
    app.run(debug=True)