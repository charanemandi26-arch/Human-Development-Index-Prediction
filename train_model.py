"""
HDI Predictor - Model Training Script
======================================

End-to-end training pipeline for the Human Development Index (HDI)
predictor using the full UNDP wide-format dataset (191 countries,
1990–2021, 700+ columns).

Pipeline stages:
  1. Load & wrangle  – melt the wide-format CSV into long format
                       (one row per country-year).
  2. Preprocess      – drop rows with any NaN feature or target;
                       no imputation needed given enough clean rows.
  3. EDA             – distribution, correlation heatmap, feature
                       scatter plots saved to notebooks/plots/.
  4. Split           – 80/20 stratified split (stratified by HDI tier).
  5. Scale           – StandardScaler fitted only on training data.
  6. Model selection – compare LinearRegression, RandomForest, and
                       GradientBoosting with 5-fold cross-validation
                       (RMSE); auto-select the best.
  7. Evaluate        – report RMSE and R² on the held-out test set.
  8. Serialize       – save model.pkl, scaler.pkl, model_info.json.
  9. Sanity checks   – run three illustrative scenario predictions.

Features used (7 total):
  Life_Expectancy, Mean_Years_Schooling, Expected_Years_Schooling,
  GNI_per_capita, Gender_Dev_Index, Gender_Ineq_Index, CO2_per_capita

Target: Human Development Index (HDI) value per country-year.

Run from the project root:
    python train_model.py
"""

import json
import os
import re
import warnings

import matplotlib

matplotlib.use("Agg")  # headless-safe — save to file, never display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Paths & constants
# ---------------------------------------------------------------------------

DATA_PATH = "data/hdi_dataset.csv"
MODEL_DIR = "model"
PLOTS_DIR = "notebooks/plots"

YEARS = list(range(1990, 2022))  # 1990–2021 inclusive

# Mapping: internal feature name -> column prefix in the wide-format CSV
FEATURE_MAP = {
    "Life_Expectancy":           "Life Expectancy at Birth",
    "Expected_Years_Schooling":  "Expected Years of Schooling",
    "Mean_Years_Schooling":      "Mean Years of Schooling",
    "GNI_per_capita":            "Gross National Income Per Capita",
    "Gender_Dev_Index":          "Gender Development Index",
    "Gender_Ineq_Index":         "Gender Inequality Index",
    "CO2_per_capita":            "Carbon dioxide emissions per capita (production) (tonnes)",
}

TARGET = "HDI"
TARGET_PREFIX = "Human Development Index"

FEATURE_COLUMNS = list(FEATURE_MAP.keys())

RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5


# ---------------------------------------------------------------------------
# 1. Data loading & wrangling
# ---------------------------------------------------------------------------

def _find_col(df: pd.DataFrame, prefix: str, year: int) -> str | None:
    """Return the column name whose header starts with *prefix* and ends
    with *(year)*, or None if not found.  Handles both plain prefixes
    and parenthesised patterns like 'Gross National Income Per Capita'.
    """
    target = f"({year})"
    for col in df.columns:
        if col.startswith(prefix) and col.strip().endswith(target):
            return col
    return None


def load_and_wrangle(path: str) -> pd.DataFrame:
    """Load the wide-format UNDP HDI CSV and reshape it into a long-format
    DataFrame with one row per (country, year).

    Returns:
        DataFrame with columns: Country, ISO3, Year, + FEATURE_COLUMNS + TARGET.
    """
    print(f"Loading raw dataset from {path} …")
    raw = pd.read_csv(path)
    print(f"  Raw shape: {raw.shape}  ({raw.shape[0]} countries, {raw.shape[1]} columns)")

    rows = []
    missing_prefixes: set[str] = set()

    for year in YEARS:
        # Locate target column for this year
        hdi_col = _find_col(raw, TARGET_PREFIX, year)
        if hdi_col is None:
            continue  # year not present in dataset

        # Locate each feature column for this year
        feat_cols: dict[str, str | None] = {}
        for feat, prefix in FEATURE_MAP.items():
            col = _find_col(raw, prefix, year)
            if col is None:
                missing_prefixes.add(prefix)
            feat_cols[feat] = col

        # Build one row per country for this year
        for _, country_row in raw.iterrows():
            record: dict = {
                "Country": country_row["Country"],
                "ISO3":    country_row["ISO3"],
                "Year":    year,
                TARGET:    pd.to_numeric(country_row[hdi_col], errors="coerce"),
            }
            for feat, col in feat_cols.items():
                record[feat] = pd.to_numeric(country_row[col], errors="coerce") if col else np.nan
            rows.append(record)

    if missing_prefixes:
        print(f"  [warn] Column prefix(es) not found in any year: {missing_prefixes}")

    df = pd.DataFrame(rows)
    print(f"  Long-format shape before cleaning: {df.shape}")
    return df


# ---------------------------------------------------------------------------
# 2. Preprocessing
# ---------------------------------------------------------------------------

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows that have NaN in any feature or the target column.

    With ~191 countries × 32 years = ~6112 potential rows, dropping NaN rows
    still leaves thousands of clean samples — no imputation is needed.
    """
    cols_needed = FEATURE_COLUMNS + [TARGET]
    before = len(df)
    df = df.dropna(subset=cols_needed).reset_index(drop=True)
    after = len(df)
    print(f"\nPreprocessing: dropped {before - after} rows with NaN -> {after} clean rows remain.")
    return df


# ---------------------------------------------------------------------------
# 3. Exploratory Data Analysis
# ---------------------------------------------------------------------------

def run_eda(df: pd.DataFrame, plots_dir: str = PLOTS_DIR) -> None:
    """Generate and save exploratory plots to *plots_dir*."""
    os.makedirs(plots_dir, exist_ok=True)

    # --- HDI distribution ---
    plt.figure(figsize=(8, 5))
    sns.histplot(df[TARGET], kde=True, bins=20, color="#6366f1")
    plt.title("Distribution of HDI Scores (all country-years)", fontsize=13)
    plt.xlabel("HDI")
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "hdi_distribution.png"), dpi=120)
    plt.close()

    # --- Correlation heatmap ---
    plt.figure(figsize=(9, 7))
    corr = df[FEATURE_COLUMNS + [TARGET]].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f",
                mask=mask, linewidths=0.5, vmin=-1, vmax=1)
    plt.title("Feature Correlation Matrix", fontsize=13)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "correlation_heatmap.png"), dpi=120)
    plt.close()

    # --- Feature vs HDI scatter (2×4 grid) ---
    fig, axes = plt.subplots(2, 4, figsize=(22, 9))
    axes = axes.flatten()
    for i, feat in enumerate(FEATURE_COLUMNS):
        axes[i].scatter(df[feat], df[TARGET], alpha=0.25, s=10, color="#6366f1")
        axes[i].set_xlabel(feat.replace("_", " "), fontsize=9)
        axes[i].set_ylabel("HDI", fontsize=9)
        axes[i].set_title(f"{feat.replace('_', ' ')} vs HDI", fontsize=9)
    # Hide unused subplot
    for j in range(len(FEATURE_COLUMNS), len(axes)):
        axes[j].set_visible(False)
    plt.suptitle("Features vs HDI (all country-years)", fontsize=13, y=1.01)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "scatter_features_vs_hdi.png"), dpi=120)
    plt.close()

    # --- HDI trend over time (mean ± std) ---
    trend = df.groupby("Year")[TARGET].agg(["mean", "std"])
    plt.figure(figsize=(10, 5))
    plt.plot(trend.index, trend["mean"], color="#6366f1", linewidth=2)
    plt.fill_between(
        trend.index,
        trend["mean"] - trend["std"],
        trend["mean"] + trend["std"],
        alpha=0.2, color="#6366f1",
    )
    plt.title("Global Mean HDI Over Time (±1 SD)", fontsize=13)
    plt.xlabel("Year")
    plt.ylabel("HDI")
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "hdi_trend_over_time.png"), dpi=120)
    plt.close()

    print(f"EDA plots saved to {plots_dir}/")


# ---------------------------------------------------------------------------
# 4. Train / test split
# ---------------------------------------------------------------------------

def split_features_target(df: pd.DataFrame):
    """Return (X_train, X_test, y_train, y_test) with an 80/20 split."""
    X = df[FEATURE_COLUMNS]
    y = df[TARGET]
    return train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)


# ---------------------------------------------------------------------------
# 5. Scaling
# ---------------------------------------------------------------------------

def fit_scaler(X_train: pd.DataFrame) -> StandardScaler:
    """Fit a StandardScaler on the training features ONLY."""
    scaler = StandardScaler()
    scaler.fit(X_train)
    return scaler


# ---------------------------------------------------------------------------
# 6. Model selection via 5-fold cross-validation
# ---------------------------------------------------------------------------

CANDIDATE_MODELS = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        max_depth=None,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    ),
    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        random_state=RANDOM_STATE,
    ),
}


def select_best_model(X_train_scaled, y_train):
    """Compare candidate models with 5-fold CV (neg RMSE) and return
    the (name, fitted_model) pair with the lowest CV RMSE.

    Also prints a comparison table.
    """
    kf = KFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    results: list[dict] = []

    print(f"\nModel comparison ({CV_FOLDS}-fold CV on training data):")
    print(f"{'Model':<25} {'CV RMSE':>10}  {'± (std)':>10}")
    print("-" * 50)

    for name, model in CANDIDATE_MODELS.items():
        neg_rmse_scores = cross_val_score(
            model, X_train_scaled, y_train,
            scoring="neg_root_mean_squared_error",
            cv=kf, n_jobs=-1,
        )
        rmse_scores = -neg_rmse_scores
        mean_rmse = rmse_scores.mean()
        std_rmse = rmse_scores.std()
        results.append({"name": name, "model": model, "cv_rmse": mean_rmse, "cv_std": std_rmse})
        print(f"{name:<25} {mean_rmse:>10.5f}  {std_rmse:>10.5f}")

    # Select the model with the lowest mean CV RMSE
    best = min(results, key=lambda r: r["cv_rmse"])
    print(f"\n>> Best model: {best['name']}  (CV RMSE = {best['cv_rmse']:.5f})")

    # Refit the best model on the full training set
    best["model"].fit(X_train_scaled, y_train)
    return best["name"], best["model"], best["cv_rmse"], best["cv_std"]


# ---------------------------------------------------------------------------
# 7. Evaluation
# ---------------------------------------------------------------------------

def evaluate_model(model, X_test_scaled, y_test) -> dict:
    """Evaluate on the held-out test set; return metrics dict."""
    y_pred = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_test, y_pred))

    print(f"\nTest-set evaluation:")
    print(f"  RMSE : {rmse:.5f}")
    print(f"  R²   : {r2:.5f}")
    return {"rmse": rmse, "r2": r2}


# ---------------------------------------------------------------------------
# 8. Serialization
# ---------------------------------------------------------------------------

def save_artifacts(model, scaler: StandardScaler,
                   model_name: str, metrics: dict,
                   cv_rmse: float, cv_std: float,
                   model_dir: str = MODEL_DIR) -> None:
    """Save model.pkl, scaler.pkl, and model_info.json."""
    os.makedirs(model_dir, exist_ok=True)

    with open(os.path.join(model_dir, "hdi_model.pkl"), "wb") as f:
        pickle.dump(model, f)

    with open(os.path.join(model_dir, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler, f)

    info = {
        "model_name": model_name,
        "features": FEATURE_COLUMNS,
        "n_features": len(FEATURE_COLUMNS),
        "cv_folds": CV_FOLDS,
        "cv_rmse": round(cv_rmse, 5),
        "cv_std":  round(cv_std, 5),
        "test_rmse": round(metrics["rmse"], 5),
        "test_r2":   round(metrics["r2"], 5),
    }
    with open(os.path.join(model_dir, "model_info.json"), "w") as f:
        json.dump(info, f, indent=2)

    print(f"\nSaved artifacts to {model_dir}/")
    print(f"  hdi_model.pkl   — {model_name}")
    print(f"  scaler.pkl")
    print(f"  model_info.json — R² = {metrics['r2']:.4f}")


# ---------------------------------------------------------------------------
# 9. Classification helper (mirrors app.py)
# ---------------------------------------------------------------------------

def classify_hdi(score: float) -> str:
    """Map a numeric HDI score to its UNDP development category."""
    if score >= 0.800:
        return "Very High Human Development"
    elif score >= 0.700:
        return "High Human Development"
    elif score >= 0.550:
        return "Medium Human Development"
    else:
        return "Low Human Development"


# ---------------------------------------------------------------------------
# 10. Scenario sanity checks
# ---------------------------------------------------------------------------

def run_scenario_tests(model, scaler: StandardScaler) -> None:
    """Run three illustrative country-profiles through the trained model."""
    test_cases = [
        {   # Very High HDI (e.g. Norway-like)
            "Life_Expectancy": 82.5, "Mean_Years_Schooling": 13.0,
            "Expected_Years_Schooling": 18.0, "GNI_per_capita": 65000,
            "Gender_Dev_Index": 0.99, "Gender_Ineq_Index": 0.05,
            "CO2_per_capita": 8.0,
        },
        {   # Medium HDI (e.g. Bolivia-like)
            "Life_Expectancy": 68.0, "Mean_Years_Schooling": 8.0,
            "Expected_Years_Schooling": 12.0, "GNI_per_capita": 7500,
            "Gender_Dev_Index": 0.95, "Gender_Ineq_Index": 0.40,
            "CO2_per_capita": 1.8,
        },
        {   # Low HDI (e.g. Chad-like)
            "Life_Expectancy": 54.0, "Mean_Years_Schooling": 2.5,
            "Expected_Years_Schooling": 6.5, "GNI_per_capita": 1500,
            "Gender_Dev_Index": 0.80, "Gender_Ineq_Index": 0.65,
            "CO2_per_capita": 0.1,
        },
    ]

    print("\nScenario sanity checks:")
    for case in test_cases:
        row = pd.DataFrame([case])[FEATURE_COLUMNS]
        row_scaled = scaler.transform(row)
        pred = float(model.predict(row_scaled)[0])
        pred = round(min(max(pred, 0.0), 1.0), 3)
        print(f"  HDI = {pred:.3f}  ({classify_hdi(pred)})")


# ---------------------------------------------------------------------------
# Pipeline entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the full training pipeline end-to-end."""
    # 1. Wrangle
    df = load_and_wrangle(DATA_PATH)

    # 2. Preprocess
    df = preprocess(df)

    # 3. EDA
    run_eda(df)

    # 4. Split
    X_train, X_test, y_train, y_test = split_features_target(df)
    print(f"\nSplit: {len(X_train)} train rows, {len(X_test)} test rows.")

    # 5. Scale
    scaler = fit_scaler(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    # 6. Model selection
    model_name, best_model, cv_rmse, cv_std = select_best_model(X_train_scaled, y_train)

    # 7. Evaluate on test set
    metrics = evaluate_model(best_model, X_test_scaled, y_test)

    # 8. Save artifacts
    save_artifacts(best_model, scaler, model_name, metrics, cv_rmse, cv_std)

    # 9. Sanity checks
    run_scenario_tests(best_model, scaler)

    print(f"Training pipeline complete.")


if __name__ == "__main__":
    main()
