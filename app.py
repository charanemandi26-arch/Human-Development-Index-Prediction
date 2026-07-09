"""
HDI Predictor - Flask Web Application
======================================

Serves a web app that predicts a country's Human Development Index (HDI)
score from seven socio-economic indicators using a pre-trained model
(auto-selected from Linear Regression, Random Forest, and Gradient Boosting
during training — see train_model.py).

Features used (must match train_model.py order exactly):
    1. Life Expectancy at Birth (years)
    2. Mean Years of Schooling (adults)
    3. Expected Years of Schooling (children)
    4. GNI per Capita (PPP $)
    5. Gender Development Index (GDI, 0–2)
    6. Gender Inequality Index (GII, 0–1)
    7. CO₂ Emissions per Capita (tonnes)

Routes:
    GET  /                  Landing page with prediction form.
    POST /predict           Validate inputs, run model, render result page.
    POST /api/predict       JSON API — same logic, returns JSON.
    GET  /api/model-info    Return model metadata as JSON.
    GET  /health            Health-check endpoint (Docker / uptime monitors).

Run with:
    python app.py
"""

import json
import logging
import os
import pickle
import uuid
from typing import Tuple

import numpy as np
from flask import Flask, jsonify, render_template, request

from utils import classify_hdi

# ---------------------------------------------------------------------------
# App & logging
# ---------------------------------------------------------------------------

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("hdi_predictor")

MODEL_PATH      = "model/hdi_model.pkl"
SCALER_PATH     = "model/scaler.pkl"
MODEL_INFO_PATH = "model/model_info.json"

# Feature order MUST match train_model.py FEATURE_COLUMNS exactly.
FEATURE_FIELDS = (
    "life_expectancy",
    "mean_schooling",
    "expected_schooling",
    "gni",
    "gdi",
    "gii",
    "co2",
)

FIELD_BOUNDS = {
    "life_expectancy":    (20,   100),
    "mean_schooling":     (0,    25),
    "expected_schooling": (0,    25),
    "gni":                (0,    200_000),
    "gdi":                (0.0,  2.0),
    "gii":                (0.0,  1.0),
    "co2":                (0.0,  60.0),
}

FIELD_LABELS = {
    "life_expectancy":    "Life Expectancy at Birth",
    "mean_schooling":     "Mean Years of Schooling",
    "expected_schooling": "Expected Years of Schooling",
    "gni":                "GNI per Capita",
    "gdi":                "Gender Development Index (GDI)",
    "gii":                "Gender Inequality Index (GII)",
    "co2":                "CO₂ Emissions per Capita",
}


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

def load_artifact(path: str):
    """Load a pickled artifact from disk.

    Raises:
        FileNotFoundError: If the artifact does not exist.
        RuntimeError:      If unpickling fails.
    """
    try:
        with open(path, "rb") as fh:
            artifact = pickle.load(fh)
        logger.info("Loaded artifact: %s", path)
        return artifact
    except FileNotFoundError:
        logger.error("Artifact not found: %s", path)
        raise
    except Exception as exc:
        logger.error("Failed to load artifact %s: %s", path, exc)
        raise RuntimeError(f"Could not load artifact at {path}") from exc


def load_model_info(path: str) -> dict:
    """Load model_info.json; return empty dict if missing or malformed."""
    try:
        with open(path) as fh:
            return json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


model      = load_artifact(MODEL_PATH)
scaler     = load_artifact(SCALER_PATH)
model_info = load_model_info(MODEL_INFO_PATH)

logger.info(
    "Model loaded: %s  |  test R² = %.4f",
    model_info.get("model_name", "unknown"),
    model_info.get("test_r2", float("nan")),
)


# ---------------------------------------------------------------------------
# Core prediction helpers
# ---------------------------------------------------------------------------

def predict_hdi(
    life_exp: float,
    mean_school: float,
    exp_school: float,
    gni: float,
    gdi: float,
    gii: float,
    co2: float,
) -> float:
    """Run the trained model on a single set of indicators.

    Returns:
        Predicted HDI, rounded to three decimals and clamped to [0, 1].
    """
    features = np.array([[life_exp, mean_school, exp_school, gni, gdi, gii, co2]])
    features_scaled = scaler.transform(features)
    raw = model.predict(features_scaled)[0]
    return round(float(min(max(raw, 0.0), 1.0)), 3)


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

class ValidationError(Exception):
    """Raised when submitted form data fails validation."""


def parse_and_validate_form(form) -> Tuple[float, float, float, float, float, float, float]:
    """Extract and validate all seven indicator fields from the request form.

    Returns:
        (life_expectancy, mean_schooling, expected_schooling, gni, gdi, gii, co2)

    Raises:
        ValidationError: If a field is missing, non-numeric, or out of range.
    """
    values: dict[str, float] = {}

    for field in FEATURE_FIELDS:
        raw = form.get(field, "").strip()

        if not raw:
            raise ValidationError(f"{FIELD_LABELS[field]} is required.")

        try:
            value = float(raw)
        except ValueError:
            raise ValidationError(f"{FIELD_LABELS[field]} must be a number.")

        lo, hi = FIELD_BOUNDS[field]
        if not (lo <= value <= hi):
            raise ValidationError(
                f"{FIELD_LABELS[field]} must be between {lo} and {hi}."
            )

        values[field] = value

    return (
        values["life_expectancy"],
        values["mean_schooling"],
        values["expected_schooling"],
        values["gni"],
        values["gdi"],
        values["gii"],
        values["co2"],
    )


def parse_and_validate_json(data: dict) -> Tuple[float, float, float, float, float, float, float]:
    """Extract and validate all seven indicator fields from a JSON dict.

    Same validation rules as parse_and_validate_form.

    Returns:
        (life_expectancy, mean_schooling, expected_schooling, gni, gdi, gii, co2)

    Raises:
        ValidationError: If a field is missing, non-numeric, or out of range.
    """
    values: dict[str, float] = {}

    for field in FEATURE_FIELDS:
        if field not in data:
            raise ValidationError(f"{FIELD_LABELS[field]} is required.")

        try:
            value = float(data[field])
        except (TypeError, ValueError):
            raise ValidationError(f"{FIELD_LABELS[field]} must be a number.")

        lo, hi = FIELD_BOUNDS[field]
        if not (lo <= value <= hi):
            raise ValidationError(
                f"{FIELD_LABELS[field]} must be between {lo} and {hi}."
            )

        values[field] = value

    return (
        values["life_expectancy"],
        values["mean_schooling"],
        values["expected_schooling"],
        values["gni"],
        values["gdi"],
        values["gii"],
        values["co2"],
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    """Render the landing page with the prediction form."""
    return render_template("index.html", model_info=model_info)


@app.route("/predict", methods=["POST"])
def predict():
    """Validate inputs, run the model, and display the result page."""
    req_id = uuid.uuid4().hex[:8]

    try:
        life_exp, mean_school, exp_school, gni, gdi, gii, co2 = (
            parse_and_validate_form(request.form)
        )
    except ValidationError as exc:
        logger.warning("[%s] Validation failed: %s", req_id, exc)
        return render_template("index.html", error=str(exc), model_info=model_info), 400

    try:
        prediction = predict_hdi(life_exp, mean_school, exp_school, gni, gdi, gii, co2)
        category   = classify_hdi(prediction)
    except Exception as exc:
        logger.exception("[%s] Prediction failed: %s", req_id, exc)
        return render_template(
            "index.html",
            model_info=model_info,
            error="Something went wrong while generating the prediction. Please try again.",
        ), 500

    logger.info(
        "[%s] Prediction | inputs=(%.1f, %.1f, %.1f, %.0f, %.3f, %.3f, %.2f) → %.3f (%s)",
        req_id, life_exp, mean_school, exp_school, gni, gdi, gii, co2, prediction, category,
    )

    return render_template(
        "result.html",
        prediction=prediction,
        category=category,
        life_expectancy=life_exp,
        mean_schooling=mean_school,
        expected_schooling=exp_school,
        gni=gni,
        gdi=gdi,
        gii=gii,
        co2=co2,
        model_info=model_info,
    )


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """JSON API endpoint — accepts JSON body, returns prediction as JSON.

    Request body (JSON):
        {
            "life_expectancy": 78.5,
            "mean_schooling": 10.2,
            "expected_schooling": 15.0,
            "gni": 25000,
            "gdi": 0.98,
            "gii": 0.15,
            "co2": 4.5
        }

    Response (JSON):
        {
            "prediction": 0.842,
            "category": "Very High Human Development",
            "model": "Gradient Boosting"
        }
    """
    req_id = uuid.uuid4().hex[:8]
    data = request.get_json(silent=True) or {}

    try:
        life_exp, mean_school, exp_school, gni, gdi, gii, co2 = (
            parse_and_validate_json(data)
        )
    except ValidationError as exc:
        logger.warning("[%s] API validation failed: %s", req_id, exc)
        return jsonify({"error": str(exc)}), 400

    try:
        prediction = predict_hdi(life_exp, mean_school, exp_school, gni, gdi, gii, co2)
        category   = classify_hdi(prediction)
    except Exception as exc:
        logger.exception("[%s] API prediction failed: %s", req_id, exc)
        return jsonify({"error": "Prediction failed. Please try again."}), 500

    logger.info(
        "[%s] API Prediction → %.3f (%s)", req_id, prediction, category,
    )

    return jsonify({
        "prediction": prediction,
        "category": category,
        "model": model_info.get("model_name", "unknown"),
        "test_r2": model_info.get("test_r2"),
    })


@app.route("/api/model-info")
def api_model_info():
    """Return model metadata as JSON (for programmatic use)."""
    return jsonify(model_info)


@app.route("/health")
def health():
    """Health-check endpoint for Docker and uptime monitors."""
    return jsonify({
        "status": "ok",
        "model": model_info.get("model_name", "unknown"),
        "test_r2": model_info.get("test_r2"),
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port, debug=False)