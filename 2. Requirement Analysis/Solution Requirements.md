# Solution Requirements

**Date:** 27 June 2026  
**Team ID:** [Enter Team ID]  
**Project Name:** HDI Predictor  

## Step 1: Functional Requirements (FR)

| S.No | Requirement Category | Requirement Description | Priority (High/Medium/Low) |
|---|---|---|---|
| 1 | Authentication | N/A (Web interface is public for accessibility by researchers). | Low |
| 2 | Authorization levels | N/A (Standard users can run predictions; server admins manage file updates). | Low |
| 3 | External interfaces | The system reads the official UNDP CSV dataset `hdi_dataset.csv` from the file system. | High |
| 4 | Transactions processing | The system accepts 7 features via Web Form, pre-processes and scales them, performs model prediction, and outputs a continuous score. | High |
| 5 | Reporting | Displays prediction results, development classification tier, and active model performance metrics (RMSE, MAE, R²). | High |
| 6 | Business rules | Target HDI score must be strictly bounded in $[0, 1]$. Classification tiers: Low (< 0.55), Medium (0.55-0.699), High (0.7-0.799), Very High (>= 0.8). | High |
| 7 | Compliance | Adheres to standard data privacy since all data is aggregated country-level and anonymous. | Medium |
| 8 | Visualizations | Static exploratory plots (EDA) are generated and saved to directories for documentation. | Medium |

## Step 2: Non-Functional Requirements (NFR)

| S.No | NFR Category | Requirement Description | Target Metric / Acceptance Criteria |
|---|---|---|---|
| 1 | Performance & Speed | Rapid response time for prediction outputs. | UI response time < 100ms; backend inference < 10ms. |
| 2 | Scalability | Handles requests concurrently on minimal server setups. | Support up to 100 concurrent requests without failure. |
| 3 | Security & Data Privacy | Sanitize all web inputs to ensure safety. | Form inputs must validate numeric bounds (e.g. Life expectancy > 0). |
| 4 | Reliability & Availability | High uptime for public researcher use. | 99.9% uptime when deployed on cloud platform (e.g., Render/Docker). |
| 5 | Usability & Accessibility | Responsive HTML/CSS UI with readable typography. | WCAG 2.1 compliant contrast; mobile-responsive layout. |
| 6 | Portability | Runs reliably across systems. | Dockerized container setup with automated setup. |