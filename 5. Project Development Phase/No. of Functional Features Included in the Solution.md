# No. of Functional Features Included in the Solution

**Date:** 02 July 2026  
**Team ID:** [Enter Team ID]  
**Project Name:** HDI Predictor  

## Functional Features Overview

| S.No | Feature Name | Feature Description | Module / Component | Status (Done / In Progress) | Marks Contribution |
|---|---|---|---|---|---|
| 1 | Data Wrangling | Converts UNDP wide dataset to ~4500 rows long training set. | `train_model.py` | Done | 1.0 |
| 2 | Model Comparison | Evaluates 3 regression algorithms using 5-fold cross validation. | `train_model.py` | Done | 1.0 |
| 3 | Auto-Select & Train | Picks model with lowest CV RMSE and fits full train set. | `train_model.py` | Done | 1.0 |
| 4 | Web UI Forms | Inputs 7 development features via responsive layout with loading state. | `templates/index.html` | Done | 1.0 |
| 5 | Inference Engine | Scales inputs and executes prediction via serialized files. | `app.py` | Done | 0.5 |
| 6 | EDA Visualization | Generates and saves scatter, correlation, trend, and feature importance charts. | `train_model.py` | Done | 0.5 |
| 7 | JSON REST API | `POST /api/predict` endpoint accepts JSON body, returns prediction as JSON. | `app.py` | Done | 0.5 |
| 8 | Health Check Endpoint | `GET /health` returns model status for Docker and uptime monitors. | `app.py` | Done | 0.5 |
| 9 | Scenario Auto-Fill | Clicking "Use these values" in Examples populates all 7 form fields instantly. | `templates/index.html` (JS) | Done | 0.5 |
| 10 | Mobile Navigation | Hamburger menu exposes navigation on screens narrower than 860px. | `templates/`, `static/style.css` | Done | 0.5 |

## Feature Summary

* **Total Features Planned:** 6
* **Total Features Implemented:** 10
* **Core / Must-Have Features:** 5
* **Additional / Nice-to-Have Features:** 5 (JSON API, health check, auto-fill, mobile nav, feature importance)
* **Features Tested & Verified:** 10

## Feature Category Breakdown

* **User Interface (UI):** Web input form with loading state, results dashboard with score animation, scenario auto-fill, mobile hamburger menu.
* **Backend / Logic:** Flask routing, validation checks, request-ID log correlation, JSON API endpoint, health-check.
* **Database / Storage:** Tabular UNDP CSV reading, serialization of PKL binaries, shared `utils.py`.
* **API / Integration:** `/api/predict` JSON endpoint, `/health` monitor endpoint, `/api/model-info` metadata.