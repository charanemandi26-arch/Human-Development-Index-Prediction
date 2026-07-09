# Problem-Solution Fit

**Date:** 28 June 2026  
**Team ID:** [Enter Team ID]  
**Project Name:** HDI Predictor  

## Problem-Solution Fit Canvas

### 1. Customer Segment(s) [CS]
* Policy makers, development researchers, international organizations, and economics students.

### 2. Problems / Pains & Frequency [PR]
* Static UNDP tables are published annually with a significant delay.
* Difficult to simulate hypothetical socio-economic targets dynamically. (Frequency: Daily during research phases).

### 3. Triggers to Act [TR]
* Planning national development targets, designing research briefs, or building ML academic projects.

### 4. Emotions Before / After [EM]
* **Before:** Frustrated by messy spreadsheets and complex formulas.
* **After:** Satisfied, informed, and confident with quick predictions and visual insights.

### 5. Available Solutions Pros & Cons [AS]
* **UNDP official database:** Pros: Authoritative. Cons: Very large, static, hard to query, no forecasting tools.

### 6. Customer Limitations [CL]
* Minimal local compute, lack of technical ML knowledge (can't write custom regression scripts).

### 7. Behavior & Its Intensity [BE]
* Searching for easy-to-use simulator web pages (High intensity during project milestones).

### 8. Channels of Behavior [CH]
* **Online:** Google searches, academic GitHub repositories, Hugging Face spaces.
* **Offline:** Direct policy reports.

### 9. Problem Root Cause [RC]
* The index is mathematical but non-linear (logarithmic transformations in GNI index), making manual predictions cumbersome.

### 10. Your Solution [SL]
* **HDI Predictor:** A web application serving an optimized Gradient Boosting Regressor model that inputs 7 features and outputs a prediction in milliseconds.