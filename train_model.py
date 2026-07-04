"""
HDI Predictor - Model Training Script
======================================

End-to-end training pipeline for the Human Development Index (HDI)
predictor: data loading, cleaning, exploratory data analysis (EDA),
feature scaling, Linear Regression training, evaluation, and
serialization of the model and scaler.

The modelling approach (Linear Regression on the four raw features,
scaled with StandardScaler) is unchanged from the original script.
This version reorganizes the same steps into small, documented
functions so each stage can be read, tested, or reused independently.

Run once from the project root to (re)generate:
    model/hdi_model.pkl
    model/scaler.pkl
    notebooks/plots/*.png

Usage:
    python train_model.py
"""

import os

import matplotlib
matplotlib.use("Agg")  # save plots to file instead of displaying (headless-safe)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

DATA_PATH = "data/hdi_dataset.csv"
MODEL_DIR = "model"
PLOTS_DIR = "notebooks/plots"

FEATURE_COLUMNS = [
    "Life_Expectancy",
    "Mean_Years_Schooling",
    "Expected_Years_Schooling",
    "GNI_per_capita",
]
TARGET_COLUMN = "HDI"

RANDOM_STATE = 42
TEST_SIZE = 0.2


# ---------------------------------------------------------------------------
# 1. Data loading
# ---------------------------------------------------------------------------

def load_dataset(path: str) -> pd.DataFrame:
    """Load the HDI dataset from CSV and print a quick summary.

    Args:
        path: Path to the dataset CSV file.

    Returns:
        The loaded DataFrame.
    """
    df = pd.read_csv(path)
    print("Dataset shape:", df.shape)
    print(df.head())
    print(df.info())
    print("\nMissing values per column:")
    print(df.isnull().sum())
    return df


# ---------------------------------------------------------------------------
# 2. Preprocessing
# ---------------------------------------------------------------------------

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing numeric values with the column mean.

    Args:
        df: Raw input DataFrame.

    Returns:
        A copy of the DataFrame with numeric NaNs replaced by the column mean.
    """
    df = df.copy()
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    return df


# ---------------------------------------------------------------------------
# 3. Exploratory Data Analysis
# ---------------------------------------------------------------------------

def run_eda(df: pd.DataFrame, plots_dir: str = PLOTS_DIR) -> None:
    """Generate and save exploratory plots: distribution, correlation,
    and per-feature scatter plots against the target.

    Args:
        df: Cleaned DataFrame containing feature and target columns.
        plots_dir: Directory where plot images are written.
    """
    os.makedirs(plots_dir, exist_ok=True)

    # Distribution of the target variable
    plt.figure(figsize=(8, 5))
    sns.histplot(df[TARGET_COLUMN], kde=True, bins=15)
    plt.title("Distribution of HDI Scores")
    plt.xlabel("HDI")
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "hdi_distribution.png"))
    plt.close()

    # Correlation heatmap across all numeric columns
    plt.figure(figsize=(8, 6))
    corr = df.select_dtypes(include="number").corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "correlation_heatmap.png"))
    plt.close()

    # Strip plot: spread of life expectancy against HDI category-free view
    plt.figure(figsize=(8, 5))
    sns.stripplot(x=df[TARGET_COLUMN].round(1), y=df["Life_Expectancy"])
    plt.title("Life Expectancy Spread Across HDI Bands")
    plt.xlabel("HDI (rounded)")
    plt.ylabel("Life Expectancy")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "strip_life_expectancy.png"))
    plt.close()

    # Feature vs target scatter plots
    fig, axes = plt.subplots(1, len(FEATURE_COLUMNS), figsize=(22, 5))
    for ax, feature in zip(axes, FEATURE_COLUMNS):
        sns.scatterplot(x=feature, y=TARGET_COLUMN, data=df, ax=ax)
        ax.set_title(f"{feature} vs {TARGET_COLUMN}")
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "scatter_features_vs_hdi.png"))
    plt.close()

    print(f"EDA plots saved to {plots_dir}/")


# ---------------------------------------------------------------------------
# 4. Feature/target split
# ---------------------------------------------------------------------------

def split_features_target(df: pd.DataFrame):
    """Separate the DataFrame into feature matrix X and target vector y,
    then perform a train/test split.

    Args:
        df: Cleaned DataFrame containing FEATURE_COLUMNS and TARGET_COLUMN.

    Returns:
        Tuple of (X_train, X_test, y_train, y_test).
    """
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    return train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )


# ---------------------------------------------------------------------------
# 5. Scaling
# ---------------------------------------------------------------------------

def fit_scaler(X_train: pd.DataFrame) -> StandardScaler:
    """Fit a StandardScaler on the training features only, to avoid
    leaking test-set statistics into the scaling parameters.

    Args:
        X_train: Training feature matrix.

    Returns:
        A fitted StandardScaler instance.
    """
    scaler = StandardScaler()
    scaler.fit(X_train)
    return scaler


# ---------------------------------------------------------------------------
# 6. Model training
# ---------------------------------------------------------------------------

def train_linear_regression(X_train_scaled, y_train) -> LinearRegression:
    """Fit a Linear Regression model on scaled training data.

    Args:
        X_train_scaled: Scaled training feature matrix.
        y_train: Training target vector.

    Returns:
        The fitted LinearRegression model.
    """
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    return model


# ---------------------------------------------------------------------------
# 7. Evaluation
# ---------------------------------------------------------------------------

def evaluate_model(model: LinearRegression, X_test_scaled, y_test) -> dict:
    """Evaluate the model on held-out test data using RMSE and R^2.

    Args:
        model: Trained LinearRegression model.
        X_test_scaled: Scaled test feature matrix.
        y_test: True test target values.

    Returns:
        A dict with keys "mse", "rmse", and "r2".
    """
    y_pred = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print("\nModel Evaluation:")
    print(f"MSE:  {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R^2:  {r2:.4f}")

    return {"mse": mse, "rmse": rmse, "r2": r2}


# ---------------------------------------------------------------------------
# 8. Serialization
# ---------------------------------------------------------------------------

def save_artifacts(model: LinearRegression, scaler: StandardScaler,
                    model_dir: str = MODEL_DIR) -> None:
    """Persist the trained model and scaler to disk with pickle.

    Args:
        model: Trained LinearRegression model.
        scaler: Fitted StandardScaler.
        model_dir: Directory to write the .pkl files into.
    """
    os.makedirs(model_dir, exist_ok=True)

    with open(os.path.join(model_dir, "hdi_model.pkl"), "wb") as f:
        pickle.dump(model, f)

    with open(os.path.join(model_dir, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler, f)

    print(f"\nSaved {model_dir}/hdi_model.pkl and {model_dir}/scaler.pkl")


# ---------------------------------------------------------------------------
# 9. Classification helper (mirrors the logic used in app.py)
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

def run_scenario_tests(model: LinearRegression, scaler: StandardScaler) -> None:
    """Run the model on a few illustrative countries to sanity-check output.

    Args:
        model: Trained LinearRegression model.
        scaler: Fitted StandardScaler used at training time.
    """
    test_cases = [
        {  # Very High HDI, e.g. a wealthy, highly educated country
            "Life_Expectancy": 82, "Mean_Years_Schooling": 13.5,
            "Expected_Years_Schooling": 17, "GNI_per_capita": 55000,
        },
        {  # Medium HDI, e.g. an upper-middle-income country
            "Life_Expectancy": 68, "Mean_Years_Schooling": 7.5,
            "Expected_Years_Schooling": 11, "GNI_per_capita": 8000,
        },
        {  # Low HDI, e.g. a low-income country with limited schooling
            "Life_Expectancy": 58, "Mean_Years_Schooling": 4,
            "Expected_Years_Schooling": 7, "GNI_per_capita": 1800,
        },
    ]

    print("\nScenario Tests:")
    for case in test_cases:
        row = pd.DataFrame([case])
        row_scaled = scaler.transform(row)
        pred = model.predict(row_scaled)[0]
        print(f"{case} -> HDI: {pred:.3f} ({classify_hdi(pred)})")


# ---------------------------------------------------------------------------
# Pipeline entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the full training pipeline end to end."""
    df = load_dataset(DATA_PATH)
    df = handle_missing_values(df)

    run_eda(df)

    X_train, X_test, y_train, y_test = split_features_target(df)

    scaler = fit_scaler(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = train_linear_regression(X_train_scaled, y_train)
    evaluate_model(model, X_test_scaled, y_test)

    save_artifacts(model, scaler)
    run_scenario_tests(model, scaler)


if __name__ == "__main__":
    main()
