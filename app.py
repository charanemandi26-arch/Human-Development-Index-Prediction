"""
HDI Predictor - Flask Web Application
======================================

Serves a small web app that predicts a country's Human Development Index
(HDI) score from four socio-economic indicators using a pre-trained
Linear Regression model.

The core prediction logic (feature order, scaling, clamping, and
classification thresholds) is unchanged from the original implementation.
This module adds input validation, structured error handling, logging,
and documentation on top of that logic.

Run with:
    python app.py
"""

import logging
import pickle
from typing import Tuple

import numpy as np
from flask import Flask, render_template, request

# ---------------------------------------------------------------------------
# App & logging configuration
# ---------------------------------------------------------------------------

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("hdi_predictor")

MODEL_PATH = "model/hdi_model.pkl"
SCALER_PATH = "model/scaler.pkl"

# Order matters: this must match the column order used during training in
# train_model.py (Life_Expectancy, Mean_Years_Schooling,
# Expected_Years_Schooling, GNI_per_capita).
FEATURE_FIELDS = (
    "life_expectancy",
    "mean_schooling",
    "expected_schooling",
    "gni",
)

# Reasonable real-world bounds used only for input validation. These do not
# affect the model or the prediction — they simply reject nonsensical input
# (e.g. negative years of schooling) before it reaches the model.
FIELD_BOUNDS = {
    "life_expectancy": (0, 100),
    "mean_schooling": (0, 25),
    "expected_schooling": (0, 25),
    "gni": (0, 200_000),
}

FIELD_LABELS = {
    "life_expectancy": "Life Expectancy",
    "mean_schooling": "Mean Years of Schooling",
    "expected_schooling": "Expected Years of Schooling",
    "gni": "GNI per Capita",
}


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

def load_artifact(path: str):
    """Load a pickled model/scaler artifact from disk.

    Args:
        path: Path to the .pkl file.

    Returns:
        The unpickled Python object.

    Raises:
        FileNotFoundError: If the artifact does not exist.
        RuntimeError: If the artifact cannot be unpickled.
    """
    try:
        with open(path, "rb") as file_handle:
            artifact = pickle.load(file_handle)
        logger.info("Loaded artifact: %s", path)
        return artifact
    except FileNotFoundError:
        logger.error("Artifact not found: %s", path)
        raise
    except Exception as exc:  # noqa: BLE001 - surfaced as a clear runtime error
        logger.error("Failed to load artifact %s: %s", path, exc)
        raise RuntimeError(f"Could not load artifact at {path}") from exc


model = load_artifact(MODEL_PATH)
scaler = load_artifact(SCALER_PATH)


# ---------------------------------------------------------------------------
# Core prediction helpers (unchanged logic)
# ---------------------------------------------------------------------------

def classify_hdi(score: float) -> str:
    """Map a numeric HDI score to its official UNDP development category.

    Categories follow the standard UNDP thresholds:
        >= 0.800             -> Very High Human Development
        0.700 - 0.799         -> High Human Development
        0.550 - 0.699         -> Medium Human Development
        <  0.550             -> Low Human Development

    Args:
        score: Predicted HDI score, expected to be in [0, 1].

    Returns:
        The human-readable development category label.
    """
    if score >= 0.800:
        return "Very High Human Development"
    elif score >= 0.700:
        return "High Human Development"
    elif score >= 0.550:
        return "Medium Human Development"
    else:
        return "Low Human Development"


def predict_hdi(life_exp: float, mean_school: float,
                 exp_school: float, gni: float) -> float:
    """Run the trained model on a single set of indicators.

    Args:
        life_exp: Life expectancy at birth, in years.
        mean_school: Mean years of schooling for adults.
        exp_school: Expected years of schooling for children.
        gni: Gross National Income per capita (PPP $).

    Returns:
        The predicted HDI score, rounded to three decimals and clamped
        to the valid [0, 1] range.
    """
    features = np.array([[life_exp, mean_school, exp_school, gni]])
    features_scaled = scaler.transform(features)

    raw_prediction = model.predict(features_scaled)[0]
    prediction = round(float(raw_prediction), 3)
    prediction = min(max(prediction, 0), 1)  # clamp to valid HDI range
    return prediction


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

class ValidationError(Exception):
    """Raised when submitted form data fails validation."""


def parse_and_validate_form(form) -> Tuple[float, float, float, float]:
    """Extract and validate the four indicator fields from a submitted form.

    Args:
        form: The Flask ``request.form`` mapping.

    Returns:
        A tuple of (life_expectancy, mean_schooling, expected_schooling, gni)
        as floats.

    Raises:
        ValidationError: If a field is missing, non-numeric, or outside its
            expected real-world range.
    """
    values = {}

    for field in FEATURE_FIELDS:
        raw_value = form.get(field, "").strip()

        if not raw_value:
            raise ValidationError(f"{FIELD_LABELS[field]} is required.")

        try:
            numeric_value = float(raw_value)
        except ValueError as exc:
            raise ValidationError(
                f"{FIELD_LABELS[field]} must be a number."
            ) from exc

        low, high = FIELD_BOUNDS[field]
        if not (low <= numeric_value <= high):
            raise ValidationError(
                f"{FIELD_LABELS[field]} must be between {low} and {high}."
            )

        values[field] = numeric_value

    return (
        values["life_expectancy"],
        values["mean_schooling"],
        values["expected_schooling"],
        values["gni"],
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    """Render the landing page with the project overview and prediction form."""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """Validate submitted indicators, run the model, and show the result.

    On invalid input, the user is returned to the home page with an
    error message instead of a stack trace.
    """
    try:
        life_exp, mean_school, exp_school, gni = parse_and_validate_form(
            request.form
        )
    except ValidationError as exc:
        logger.warning("Validation failed: %s", exc)
        return render_template("index.html", error=str(exc)), 400

    try:
        prediction = predict_hdi(life_exp, mean_school, exp_school, gni)
        category = classify_hdi(prediction)
    except Exception as exc:  # noqa: BLE001 - keep the app alive, log the cause
        logger.exception("Prediction failed: %s", exc)
        return render_template(
            "index.html",
            error="Something went wrong while generating the prediction. "
                  "Please try again.",
        ), 500

    logger.info(
        "Prediction served | inputs=(%.1f, %.1f, %.1f, %.0f) -> %.3f (%s)",
        life_exp, mean_school, exp_school, gni, prediction, category,
    )

    return render_template(
        "result.html",
        prediction=prediction,
        category=category,
        life_expectancy=life_exp,
        mean_schooling=mean_school,
        expected_schooling=exp_school,
        gni=gni,
    )


if __name__ == "__main__":
    app.run(debug=True)
