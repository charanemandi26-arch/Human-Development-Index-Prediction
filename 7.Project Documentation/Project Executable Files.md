# Project Executable Files

**Date:** 04 July 2026  
**Team ID:** [Enter Team ID]  
**Project Name:** HDI Predictor  

## Step 1: Submission Checklist

| S.No | Item to Submit | Submitted (Yes / No) |
|---|---|---|
| 1 | Complete source code (all files and folders) | **Yes** |
| 2 | README / Setup Guide | **Yes** |
| 3 | requirements.txt | **Yes** |
| 4 | Database / raw dataset (`data/hdi_dataset.csv`) | **Yes** |
| 5 | Saved Model files (`model/scaler.pkl`, `model/best_model.pkl`) | **Yes** |
| 6 | Dockerfile | **Yes** |
| 7 | Notebook plots (EDA images) | **Yes** |

## Step 2: File / Folder Structure

```
HDI_Predictor/
├── data/
│   └── hdi_dataset.csv       # UNDP historical dataset
├── model/
│   ├── best_model.pkl        # Serialized best ML model (joblib)
│   └── scaler.pkl            # Serialized fitted StandardScaler (joblib)
├── notebooks/
│   └── plots/                # Generated EDA scatter/heatmap/trend plots
├── static/
│   └── style.css             # Glassmorphism application stylesheet
├── templates/
│   ├── index.html            # Inputs form view
│   └── result.html           # Prediction outputs view
├── train_model.py            # ML wrangling, training & comparison pipeline
├── app.py                    # Flask web application router
├── Dockerfile                # Deployment instructions container
├── requirements.txt          # Python packaging dependencies
└── README.md                 # Project main user instructions
```

## Step 3: Deployment / Access Details
* **Hosting Provider:** Render / Hugging Face Spaces (using Docker)
* **Local Run Link:** `http://127.0.0.1:5000`

## Step 4: Local Run Instructions
1. Put the raw `hdi_dataset.csv` inside the `data/` directory.
2. Execute `python train_model.py` to auto-compare, select, and save the best model and scaler.
3. Start the Flask application by running `python app.py`.
4. Open the browser and visit `http://127.0.0.1:5000` to test predictions.