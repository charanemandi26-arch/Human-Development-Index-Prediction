# Data Flow Diagram

**Date:** 27 June 2026  
**Team ID:** [Enter Team ID]  
**Project Name:** HDI Predictor  

## DFD Legend
* **External Entity (Oval):** User (Policy Researcher / General Public)
* **Process (Rectangle with numbered header):** Operations that transform data
* **Data Store (Rectangle, solid fill):** Files containing data (`hdi_dataset.csv`, model serialization files)
* **Data Flow (Labeled Arrow):** Movement of data between entities and processes

## Mermaid Flowchart

```mermaid
flowchart TD
    User([User])
    CSV[(data/hdi_dataset.csv)]
    ModelFile[(model/best_model.pkl)]
    ScalerFile[(model/scaler.pkl)]

    subgraph Offline ML Pipeline
        P4[4.0 Load & Wrangle wide CSV to long table]
        P5[5.0 Preprocess & Fit StandardScaler]
        P6[6.0 Evaluate Models via 5-Fold CV]
        P7[7.0 Auto-Select Best Model & Serialize]
        
        CSV --> P4
        P4 --> P5
        P5 --> P6
        P6 --> P7
        P5 --> ScalerFile
        P7 --> ModelFile
    end

    subgraph Online Web App
        P1[1.0 Validate Web Form Inputs]
        P2[2.0 Scale Inputs]
        P3[3.0 Run ML Model Inference]
        
        User -- "1. Form Inputs" --> P1
        P1 -- "2. Validated Inputs" --> P2
        ScalerFile -- "3. Fitted Scaler" --> P2
        P2 -- "4. Scaled Features" --> P3
        ModelFile -- "5. Trained Model" --> P3
        P3 -- "6. Predicted HDI & Tier" --> User
    end
```