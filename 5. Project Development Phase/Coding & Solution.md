# Coding & Solution

**Date:** 01 July 2026  
**Team ID:** [Enter Team ID]  
**Project Name:** HDI Predictor  

## Solution Summary

* **Repository Link:** [Local Git Workspace]
* **Programming Languages:** Python (Flask/Scikit-learn), HTML5, CSS3
* **Frameworks Used:** Flask 3.1.3
* **Key Features Implemented:**
  - Automated UNDP dataset long-form wrangling
  - 3-Algorithm comparison (Linear Regression, Random Forest, Gradient Boosting)
  - Auto-selection of best model based on cross-validation RMSE
  - StandardScaler integration
  - Interactive prediction web interface
  - Visualization charts (EDA) outputted to file
* **Pending / Incomplete Features:**
  - confidence intervals calculation (Future Enhancement)
* **Setup / Run Instructions:**
  1. Initialize virtual environment: `python -m venv .venv`
  2. Activate virtual env: `.venv\Scripts\activate`
  3. Install dependencies: `pip install -r requirements.txt`
  4. Run training script to save model: `python train_model.py`
  5. Run Flask server: `python app.py`
  6. Access dashboard at `http://127.0.0.1:5000`

## Code Quality Checklist

| S.No | Criteria | Status (Yes / No) |
|---|---|---|
| 1 | Code is modular and organized into functions / classes | **Yes** |
| 2 | Meaningful variable and function names are used | **Yes** |
| 3 | Code includes comments / documentation where necessary | **Yes** |
| 4 | Error handling is implemented for critical operations | **Yes** |
| 5 | The application runs without critical errors | **Yes** |
| 6 | Code is committed to a version control repository | **Yes** |