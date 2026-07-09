# Technology Stack

**Date:** 27 June 2026  
**Team ID:** [Enter Team ID]  
**Project Name:** HDI Predictor  

| S.No | Architecture Component / Layer | Technology Chosen | Justification / Purpose |
|---|---|---|---|
| 1 | Frontend / Client-Side | HTML5 / Vanilla CSS (Google Fonts Inter) | Provides a lightweight, fast-loading, mobile-friendly responsive user interface with glassmorphic visuals and clear input structures. |
| 2 | Backend / Server-Side | Python / Flask | Flask is a micro-framework that is perfectly suited for hosting scikit-learn machine learning models due to its simplicity and fast routing. |
| 3 | Machine Learning & Data | Scikit-learn, Pandas, NumPy | Standard Python data science libraries that facilitate robust modeling (Gradient Boosting, Random Forests) and feature scaling. |
| 4 | Data Storage / Relational | Flat CSV Files (`hdi_dataset.csv`) | The UNDP data is tabular, static, and read-only. Flat files are loaded at startup and do not require heavy database administration. |
| 5 | Cloud / Deployment | Docker / Gunicorn | Containerization via Docker guarantees the project runs identically in dev and production without environmental discrepancy. |
| 6 | Version Control | Git / GitHub | Facilitates version tracking, code backup, and team collaboration. |