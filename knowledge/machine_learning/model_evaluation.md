# Model evaluation

Evaluate on observations not used to fit or select the model. Compare against a transparent baseline and report metrics with their units and data split. R-squared can be negative on held-out data; RMSE is sensitive to large errors.

Check leakage, drift, subgroup performance, and whether the test set resembles intended future use. A good predictive score does not identify causal drivers.
