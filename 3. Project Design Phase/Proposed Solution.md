# Proposed Solution

**Date:** 28 June 2026  
**Team ID:** [Enter Team ID]  
**Project Name:** HDI Predictor  

## Project Overview
A machine learning web application that predicts a country's Human Development Index (HDI) score and development tier from 7 socio-economic indicators.

## Objectives
1. Build a clean, reproducible ML pipeline: load $\rightarrow$ preprocess $\rightarrow$ cross-validate $\rightarrow$ select $\rightarrow$ serialize.
2. Auto-select the best algorithm out of Linear Regression, Random Forest, and Gradient Boosting based on RMSE.
3. Serve predictions through a Flask web application with a responsive dashboard interface.

## Resource Requirements

| Resource Type | Description | Specification/Allocation |
|---|---|---|
| **Hardware** | Computing Resources | Local Development Machine (Intel Core i5 or similar) |
| **Memory** | RAM | Minimum 8 GB |
| **Storage** | Disk space | 1 GB available disk space |
| **Software** | Backend Framework | Python 3.10+ / Flask |
| **Libraries** | Machine Learning & Data | scikit-learn, pandas, numpy, matplotlib, seaborn |
| **Dev Environment** | IDE / Notebooks | VS Code, Jupyter Notebook |
| **Data** | Data Source | UNDP HDI historical dataset (191 countries, 1990–2021), CSV format, ~4,500 training rows |