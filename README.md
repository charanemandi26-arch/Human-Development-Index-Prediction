# HDI Predictor

A machine learning web application that predicts a country's **Human
Development Index (HDI)** score and development category from four
socio-economic indicators, built with **Python, Flask, and Scikit-learn**.

---

## Project Overview

The Human Development Index is the United Nations Development
Programme's composite measure of a country's health, education, and
standard of living. This project trains a **Linear Regression** model
on historical HDI data and serves it through a Flask web application,
so a user can enter a country's indicators and instantly see a
predicted HDI score, its development category, and a short
interpretation.

## Problem Statement

GDP and income figures alone don't capture how well a country's
economic output translates into actual quality of life. The HDI
addresses this by combining health, education, and income into a
single number — but computing it requires pulling together multiple
data sources and applying the UNDP's methodology. This project
demonstrates that the relationship between the underlying indicators
and the final HDI score can be approximated well by a simple,
interpretable regression model, and packages that model behind an
accessible web interface.

## Objectives

- Build a clean, reproducible ML pipeline: load data → clean → explore
  → train → evaluate → serialize.
- Predict a continuous HDI score using Linear Regression.
- Classify the predicted score into one of the four official UNDP
  development tiers.
- Serve predictions through a Flask web application with a modern,
  responsive interface.
- Write code that is validated, logged, documented, and safe against
  malformed input.

## Dataset

The dataset (`data/hdi_dataset.csv`) contains one row per country with
the following columns:

| Column                      | Description                                              |
|------------------------------|-----------------------------------------------------------|
| `Country`                    | Country name                                              |
| `Life_Expectancy`            | Life expectancy at birth, in years                         |
| `Mean_Years_Schooling`       | Average years of schooling completed by adults             |
| `Expected_Years_Schooling`   | Expected years of schooling for a child starting school    |
| `GNI_per_capita`             | Gross National Income per capita (PPP $)                   |
| `HDI`                        | Human Development Index score (target variable, 0–1)       |

Missing numeric values are filled with the column mean before training.

## Machine Learning Pipeline

The pipeline lives in `train_model.py` and follows these stages:

1. **Load** the dataset and inspect its shape, types, and missing values.
2. **Clean** the data by filling missing numeric values with the column mean.
3. **Explore** the data (EDA): distribution plot, correlation heatmap,
   strip plot, and feature-vs-target scatter plots, saved to
   `notebooks/plots/`.
4. **Split** the data into training and test sets (80/20).
5. **Scale** the four input features with `StandardScaler`, fitted
   only on the training set.
6. **Train** a `LinearRegression` model on the scaled training data.
7. **Evaluate** the model on the held-out test set using **RMSE** and
   **R²**.
8. **Serialize** the trained model and scaler with `pickle` to
   `model/hdi_model.pkl` and `model/scaler.pkl`.
9. **Sanity-check** the model against three illustrative scenarios
   (Very High, Medium, and Low HDI profiles).

The Flask app (`app.py`) reuses this exact same feature order and
scaling logic at inference time, so predictions are consistent with
training.

## Technologies

- **Python 3**
- **Flask** — web application framework
- **Scikit-learn** — Linear Regression model, `StandardScaler`
- **Pandas / NumPy** — data loading and preprocessing
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
2. Enter values for life expectancy, mean years of schooling, expected
   years of schooling, and GNI per capita.
3. Submit the form to view the predicted HDI score, its development
   category, and a short interpretation and recommendation.
4. Use **Predict Again** to try another set of values.

## Screenshots

> _Add screenshots of the home page, prediction form, and result page
> here before publishing._

- `docs/screenshot-home.png`
- `docs/screenshot-form.png`
- `docs/screenshot-result.png`

## Project Structure

```
HDI_Predictor/
├── app.py                  # Flask application: routes, validation, inference
├── train_model.py          # Full training pipeline (EDA, training, evaluation)
├── requirements.txt        # Python dependencies
├── data/
│   └── hdi_dataset.csv     # Training dataset
├── model/
│   ├── hdi_model.pkl       # Trained Linear Regression model
│   └── scaler.pkl          # Fitted StandardScaler
├── notebooks/
│   ├── HDI_Analysis.ipynb  # Exploratory notebook
│   └── plots/              # Saved EDA plots (generated by train_model.py)
├── static/
│   └── style.css           # Application stylesheet
├── templates/
│   ├── index.html          # Landing page + prediction form
│   └── result.html         # Prediction result page
└── README.md
```

## Future Improvements

- Add automated tests (e.g. `pytest`) covering validation edge cases
  and known scenario predictions.
- Experiment with additional models (Ridge, Random Forest, Gradient
  Boosting) and compare against the Linear Regression baseline.
- Add confidence intervals or a residual-based error estimate to each
  prediction.
- Support batch predictions from an uploaded CSV of countries.
- Containerize the app with Docker for easier deployment.
- Add a REST API endpoint (`/api/predict`) returning JSON, for
  programmatic use alongside the HTML interface.

---

Built as a personal machine learning and Flask development project.
