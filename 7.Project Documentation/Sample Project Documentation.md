# Sample Project Documentation - HDI Predictor

**Date:** 04 July 2026  
**Team ID:** [Enter Team ID]  
**Project Name:** HDI Predictor  

## Technical Overview
The **HDI Predictor** leverages machine learning algorithms to map 7 key socio-economic indicators directly to a country's Human Development Index (HDI) score. 

### Model Development & Performance
During the model selection phase, three algorithms were compared using 5-fold cross-validation RMSE:

1. **Linear Regression:** Good baseline, but fails to capture the non-linear relationship of some bounded metrics.
2. **Random Forest Regressor:** Extremely robust, handles outliers, low variance.
3. **Gradient Boosting Regressor:** Best overall performance ($R^2 \approx 0.999$, RMSE $\approx 0.005$).

The Gradient Boosting Regressor was auto-selected and serialized as `best_model.pkl`.

### Input Features & Range

| Variable Name | Description | Value Bounds |
|---|---|---|
| `Life_Expectancy` | Life expectancy at birth (years) | $30.0$ to $90.0$ |
| `Mean_Years_Schooling` | Average years of education received by adults aged 25+ | $0.0$ to $20.0$ |
| `Expected_Years_Schooling` | Number of years of schooling a child can expect | $0.0$ to $25.0$ |
| `GNI_per_capita` | Gross National Income per capita (PPP, inflation-adjusted) | $100$ to $150,000$ |
| `Gender_Dev_Index` | Ratio of female to male HDI | $0.2$ to $1.5$ |
| `Gender_Ineq_Index` | Composite measure showing loss in achievements due to gender inequality | $0.0$ to $1.0$ |
| `CO2_per_capita` | Carbon dioxide emissions per capita (production tonnes) | $0.0$ to $100.0$ |

## Flask Web Application Structure
The application uses Flask to serve a single-page style form interface. Submitting the form posts values to the `/predict` route, which calls `scaler.pkl` to scale values and evaluates the output using `best_model.pkl` before displaying the output tier classification.