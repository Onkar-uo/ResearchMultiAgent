# Cross-validation

Cross-validation estimates variability in model performance across data splits. Use folds that respect the sampling structure: grouped splits for repeated entities and chronological splits for time series. Random shuffling can leak future or related observations.

Feature selection and preprocessing must happen inside each training fold. Keep a final untouched test set when making model-selection decisions, and report fold variability rather than only the best score.
