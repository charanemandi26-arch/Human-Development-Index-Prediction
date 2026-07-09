# Communication

**Date:** 05 July 2026  
**Team ID:** [Enter Team ID]  
**Project Name:** HDI Predictor  

## Communication Plan
As a solo developer project, communication focused on logging commits, documenting requirements, and keeping external guides updated.

| S.No | Communication Type | Frequency | Channel / Tool | Participants | Purpose |
|---|---|---|---|---|---|
| 1 | Git Commit Messages | Daily | Git / GitHub | Hari Charan Emandi | Track incremental code additions and bug fixes. |
| 2 | Documentation Logs | Weekly | Markdown files | Hari Charan Emandi | Keep track of model metrics and pipeline changes. |
| 3 | User Verification Logs | Once | Walkthroughs | Hari Charan Emandi | Document setup and validation steps. |

## Communication Challenges & Resolutions
* **Challenge:** Tracking multi-model metrics changes across training runs.
* **Resolution:** Implemented stdout logs in `train_model.py` summarizing model metrics, and saving cross-validation reports directly inside the `notebooks/` directory.