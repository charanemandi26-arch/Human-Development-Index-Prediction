# Scalability & Future Plan

**Date:** 05 July 2026  
**Team ID:** [Enter Team ID]  
**Project Name:** HDI Predictor  

## Current System Limitations
1. **Static Dataset:** Model is trained on UNDP historical values up to 2021.
2. **Single Predictions:** Users can only predict one country-year scenario at a time.
3. **No Confidence Estimates:** Predictions output point-estimates without prediction intervals.

## Scalability Plan

| S.No | Scalability Aspect | Current State | Proposed Upgrade / Solution |
|---|---|---|---|
| 1 | User Load | Lightweight Flask thread | Deploy using a WSGI server like Gunicorn behind Nginx. |
| 2 | Data Storage | Tabular CSV | Migrate historical raw inputs to a structured PostgreSQL DB. |
| 3 | Performance | Sub-50ms inference | Cache repeated input coordinates using Redis cache. |

## Future Roadmap
* **Phase 2:** Implement batch prediction uploads via CSV files.
* **Phase 3:** Introduce an interactive timeseries dashboard (using Chart.js or D3.js) showing historical patterns per country.
* **Phase 4:** Expand modeling to include Deep Learning Multi-Layer Perceptrons (MLPs) and compare performance.