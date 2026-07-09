# Solution Architecture

**Date:** 28 June 2026  
**Team ID:** [Enter Team ID]  
**Project Name:** HDI Predictor  

## Solution Architecture Diagram

```
+-------------------------------------------------------------+
|                     Presentation Layer                      |
|  - HTML5 & CSS3 Web Frontend                                |
|  - Responsive input form (7 fields)                         |
|  - Predictions dashboard with model performance statistics  |
+--------------------------------------------^---------v------+
                                             |         |
                                         HTTP|         |JSON/HTML
                                         Post|         |Response
                                             |         |
+--------------------------------------------+---------^------+
|                      Application Layer                      |
|  - Flask web server (app.py) routing                        |
|  - Input validation & scaling (scaler.pkl)                  |
|  - ML Inference engine (best_model.pkl)                     |
+--------------------------------------------^---------v------+
                                             |         |
                                       Loads |         | Saves
                                      Models |         | Plots
                                             |         |
+--------------------------------------------+---------^------+
|                         Data Layer                          |
|  - Raw Data Store: data/hdi_dataset.csv                     |
|  - Model Store: model/best_model.pkl, model/scaler.pkl      |
|  - Plots Store: notebooks/plots/ (EDA charts)               |
+-------------------------------------------------------------+
```

## Component Description Table

| Component Name | Description / Role in Architecture | Technologies Used |
|---|---|---|
| **Presentation Layer** | Renders input forms, visualizes prediction outputs, and displays model statistics. | HTML5, CSS3, Inter Font |
| **Flask Router** | Handles web routing (`/` and `/predict`), validates form inputs, and returns rendered pages. | Python, Flask |
| **ML Inference Engine** | Receives scaled features, evaluates using serialized model, and outputs predicted score. | Scikit-learn, joblib |
| **Data Processing Pipeline** | Preprocesses raw UNDP CSV data, scales features, fits and compares algorithms. | Pandas, NumPy, StandardScaler |
| **Data Store** | Stores historical development datasets, serialized scaler, and regression models. | CSV, Joblib PKL files |