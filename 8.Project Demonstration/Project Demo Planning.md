# Project Demo Planning

**Date:** 05 July 2026  
**Team ID:** [Enter Team ID]  
**Project Name:** HDI Predictor  

## Demonstration Sequence Flow

### Step 1: Introduction (2 mins)
* Introduce the motivation: measuring quality of life dynamically rather than standard economic output.
* Introduce project scope and the 7 development indicators.

### Step 2: Data Pipeline & Model Training (3 mins)
* Show `train_model.py` and its execution.
* Explain the auto-selection strategy based on 5-fold cross-validation RMSE.
* Show generated EDA plots.

### Step 3: Web Application & Predictions (4 mins)
* Open local server at `http://127.0.0.1:5000`.
* Enter hypothetical parameters for a developing and a highly developed nation.
* Show instant results (predicted score and classification tier) and active model metrics.

### Step 4: Dockerization & Scalability (1 min)
* Show Docker container execution.
* Outline roadmap and future scalability updates.