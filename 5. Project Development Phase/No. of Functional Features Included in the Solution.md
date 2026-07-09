# No. of Functional Features Included in the Solution

**Date:** 02 July 2026  
**Team ID:** [Enter Team ID]  
**Project Name:** HDI Predictor  

## Functional Features Overview

| S.No | Feature Name | Feature Description | Module / Component | Status (Done / In Progress) | Marks Contribution |
|---|---|---|---|---|---|
| 1 | Data Wrangling | Converts UNDP wide dataset to 4500 rows long training set. | `train_model.py` | Done | 1.0 |
| 2 | Model Comparison | Evaluates 3 regression algorithms using 5-fold cross validation. | `train_model.py` | Done | 1.0 |
| 3 | Auto-Select & Train | Picks model with lowest CV RMSE and fits full train set. | `train_model.py` | Done | 1.0 |
| 4 | Web UI Forms | Inputs 7 development features via responsive layout. | `templates/index.html` | Done | 1.0 |
| 5 | Inference Engine | Scales inputs and executes prediction via serialized files. | `app.py` | Done | 0.5 |
| 6 | EDA Visualization | Generates and saves scatter, correlation, and trend charts. | `train_model.py` | Done | 0.5 |

## Feature Summary

* **Total Features Planned:** 6
* **Total Features Implemented:** 6
* **Core / Must-Have Features:** 5
* **Additional / Nice-to-Have Features:** 1 (Visualization graphs)
* **Features Tested & Verified:** 6

## Feature Category Breakdown

* **User Interface (UI):** Web input form, results dashboard.
* **Backend / Logic:** Flask routing, validation checks.
* **Database / Storage:** Tabular UNDP CSV reading, serialization of PKL binaries.
* **API / Integration:** Model inference hooks.