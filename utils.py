"""
HDI Predictor — Shared Utilities
=================================

Central home for logic that is consumed by both the Flask application
(app.py) and the training pipeline (train_model.py).  Keeping it here
prevents duplication and guarantees that both sides use identical
classification thresholds.

Functions:
    classify_hdi  – maps a numeric HDI score to a UNDP development category.
"""


def classify_hdi(score: float) -> str:
    """Map a numeric HDI score to its UNDP development category.

    Official UNDP thresholds:
        ≥ 0.800  → Very High Human Development
        ≥ 0.700  → High Human Development
        ≥ 0.550  → Medium Human Development
        <  0.550 → Low Human Development

    Args:
        score: Predicted or actual HDI value, expected in [0, 1].

    Returns:
        A string label matching one of the four UNDP tiers.
    """
    if score >= 0.800:
        return "Very High Human Development"
    elif score >= 0.700:
        return "High Human Development"
    elif score >= 0.550:
        return "Medium Human Development"
    else:
        return "Low Human Development"
