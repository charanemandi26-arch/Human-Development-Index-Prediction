# Project Planning

**Date:** 29 June 2026  
**Team ID:** [Enter Team ID]  
**Project Name:** HDI Predictor  

## Product Backlog, Sprint Schedule, and Estimation

| Sprint | Epic | User Story Number | User Story / Task | Story Points | Priority | Assigned To | Planned Start | Planned End |
|---|---|---|---|---|---|---|---|---|
| **Sprint-1** | Setup & Data | USN-1 | As a developer, I can load and clean the UNDP CSV dataset into a long table so that it is ready for ML models. | 3 | High | Hari Charan Emandi | 30 June 2026 | 01 July 2026 |
| **Sprint-1** | ML Pipeline | USN-2 | As a developer, I can scale features and compare Linear Regression, Random Forest, and Gradient Boosting models. | 5 | High | Hari Charan Emandi | 01 July 2026 | 02 July 2026 |
| **Sprint-1** | ML Serialization| USN-3 | As a developer, I can auto-select the best model based on CV RMSE and serialize it and the scaler to files. | 2 | High | Hari Charan Emandi | 02 July 2026 | 02 July 2026 |
| **Sprint-2** | Backend Flask | USN-4 | As a user, I can access a Flask web server that handles input requests and queries the serialized ML model. | 3 | High | Hari Charan Emandi | 03 July 2026 | 03 July 2026 |
| **Sprint-2** | Frontend UI | USN-5 | As a user, I can input 7 features into a responsive HTML form and see predictions dynamically. | 5 | Medium | Hari Charan Emandi | 03 July 2026 | 04 July 2026 |
| **Sprint-2** | Dockerization | USN-6 | As an operator, I can run the application inside a Docker container for consistent deployments. | 2 | Low | Hari Charan Emandi | 04 July 2026 | 05 July 2026 |