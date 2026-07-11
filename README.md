---
title: Hdi Predictor
emoji: 🌍
colorFrom: purple
colorTo: red
sdk: docker
pinned: false
license: mit
---

# HDI Predictor

**🚀 Live Demo:** [Hugging Face Space](https://huggingface.co/spaces/Haricharan26/hdi-predictor) | [Direct Web App](https://haricharan26-hdi-predictor.hf.space)

A machine learning web application that predicts a country's **Human
Development Index (HDI)** score and development category from seven
socio-economic indicators, built with **Python, Flask, and Scikit-learn**.

The best-performing model is **auto-selected** from three algorithms
(Linear Regression, Random Forest, Gradient Boosting) using 5-fold
cross-validation on the full UNDP historical dataset (191 countries,
1990–2021).

---

## Project Overview

The Human Development Index is the United Nations Development
Programme's composite measure of a country's health, education, and
standard of living. This project trains machine learning models on the
full UNDP HDI time-series dataset and serves them through a Flask web
application, so a user can enter a country's indicators and instantly
see a predicted HDI score, its development category, and a short
interpretation.

## Problem Statement

GDP and income figures alone don't capture how well a country's
economic output translates into actual quality of life. The HDI
addresses this by combining health, education, and income into a
single number — but computing it requires pulling together multiple
data sources and applying the UNDP's methodology. This project
demonstrates that the relationship between the underlying indicators
and the final HDI score can be approximated with very high accuracy
(R² ≈ 0.999) by a Gradient Boosting model trained on historical
cross-country data, and packages that model behind an accessible web
interface.

## Objectives

- Build a clean, reproducible ML pipeline: load → wrangle → explore
  → compare models → train → evaluate → serialize.
- Wrangle the wide-format UNDP CSV (191 countries × 1990–2021, 880 columns)
  into a long-format training table (~4,500 clean country-year rows).
- Use **7 features** spanning health, education, income, gender equity,
  and environmental footprint.
- Auto-select the best algorithm (Linear Regression, Random Forest, or
  Gradient Boosting) using 5-fold cross-validation RMSE.
- Predict a continuous HDI score and classify it into one of the four
  official UNDP development tiers.
- Serve predictions through a Flask web application with a modern,
  responsive interface that shows the active model's metrics.

## Dataset

The dataset (`data/hdi_dataset.csv`) is the official UNDP Human
Development Report dataset in wide format: one row per country and one
column per indicator-year combination (e.g. `Life Expectancy at Birth (2015)`).

The training script reshapes this into long format, extracting the
following columns per year:

| Internal Name | Source Column Prefix |
|---|---|
| `Life_Expectancy` | Life Expectancy at Birth |
| `Mean_Years_Schooling` | Mean Years of Schooling |
| `Expected_Years_Schooling` | Expected Years of Schooling |
| `GNI_per_capita` | Gross National Income Per Capita |
| `Gender_Dev_Index` | Gender Development Index |
| `Gender_Ineq_Index` | Gender Inequality Index |
| `CO2_per_capita` | Carbon dioxide emissions per capita (production) (tonnes) |
| `HDI` *(target)* | Human Development Index |

Rows with any missing value in the above columns are dropped before training.

## Machine Learning Pipeline

The pipeline lives in `train_model.py` and follows these stages:

1. **Load & wrangle** the wide-format CSV into long format (one row per
   country-year).
2. **Preprocess** by dropping rows with NaN in any feature or target column.
3. **Explore** the data (EDA): HDI distribution, correlation heatmap,
   feature scatter plots, and HDI trend over time — saved to
   `notebooks/plots/`.
4. **Split** the data into training and test sets (80/20).
5. **Scale** the seven input features with `StandardScaler`, fitted
   only on the training set.
6. **Compare models** using 5-fold cross-validation (neg RMSE):
   `LinearRegression`, `RandomForestRegressor`, `GradientBoostingRegressor`.
7. **Auto-select** the model with the lowest mean CV RMSE and refit it
   on all training data.
8. **Evaluate** the best model on the held-out test set (RMSE and R²).
9. **Serialize** the trained model, scaler, and metadata to
   `model/hdi_model.pkl`, `model/scaler.pkl`, and `model/model_info.json`.
10. **Sanity-check** the model against three illustrative scenarios
    (Very High, Medium, and Low HDI profiles).

### Model Comparison Results

| Model | CV RMSE (5-fold) | ± Std |
|---|---|---|
| Linear Regression | 0.01961 | ±0.00036 |
| Random Forest | 0.00567 | ±0.00038 |
| **Gradient Boosting** ✓ | **0.00534** | **±0.00027** |

**Auto-selected: Gradient Boosting — Test R² = 0.9991, Test RMSE = 0.00507**

## Technologies

- **Python 3**
- **Flask** — web application framework
- **Scikit-learn** — GradientBoostingRegressor, RandomForestRegressor,
  LinearRegression, StandardScaler, KFold cross-validation
- **Pandas / NumPy** — data wrangling and preprocessing
- **Matplotlib / Seaborn** — exploratory data visualization
- **HTML / CSS** — responsive front-end interface

## Installation

```bash
# 1. Clone or unzip the project, then move into it
cd HDI_Predictor

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Retrain the model — pre-trained artifacts are already included
python train_model.py

# 5. Run the web application
python app.py
```

The app will be available at `http://127.0.0.1:5000/`.

## Usage

1. Open the home page and scroll to the **Predict HDI Score** section.
2. Fill in all seven indicators:
   - **Core HDI**: life expectancy, mean years of schooling, expected
     years of schooling, GNI per capita.
   - **Gender & Environment**: Gender Development Index (GDI), Gender
     Inequality Index (GII), CO₂ emissions per capita.
3. Submit the form to view the predicted HDI score, its development
   category, the active model's metrics, and a short interpretation
   and recommendation.
4. Use **Predict Again** to try another set of values.

The home page also displays a **model info badge** in the hero section
and an **active model panel** next to the form, showing the auto-selected
algorithm name, test R², and test RMSE.

## Project Structure

```
HDI_Predictor/
├── app.py                  # Flask application: routes, validation, inference
├── train_model.py          # Full training pipeline (wrangle, EDA, CV, training, evaluation)
├── requirements.txt        # Python dependencies
├── data/
│   └── hdi_dataset.csv     # UNDP wide-format HDI dataset (191 countries, 1990–2021)
├── model/
│   ├── hdi_model.pkl       # Auto-selected trained model (Gradient Boosting)
│   ├── scaler.pkl          # Fitted StandardScaler (7 features)
│   └── model_info.json     # Model metadata (name, RMSE, R², CV details)
├── notebooks/
│   ├── HDI_Analysis.ipynb  # Exploratory notebook
│   └── plots/              # Saved EDA plots (generated by train_model.py)
│       ├── hdi_distribution.png
│       ├── correlation_heatmap.png
│       ├── scatter_features_vs_hdi.png
│       └── hdi_trend_over_time.png
├── static/
│   └── style.css           # Application stylesheet
├── templates/
│   ├── index.html          # Landing page + 7-field prediction form
│   └── result.html         # Prediction result page (split input summary + model info)
└── README.md
```

## Future Improvements

- Add automated tests (e.g. `pytest`) covering validation edge cases
  and known scenario predictions.
- Add confidence intervals or a residual-based error estimate to each
  prediction.
- Support batch predictions from an uploaded CSV of countries.
- Containerize the app with Docker for easier deployment.
- Add a REST API endpoint (`/api/predict`) returning JSON, for
  programmatic use alongside the HTML interface.
- Add an interactive country explorer showing historical HDI trends
  from the full time-series dataset.

---

Built as a personal machine learning and Flask development project.
