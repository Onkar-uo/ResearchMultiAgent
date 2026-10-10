# Feature importance and interpretation

Tree impurity importance summarizes how a model used features to reduce training impurity. It can favor high-cardinality or correlated features and varies with the data and model. Permutation importance measures the performance change after disrupting a feature, but correlated features can mask one another.

Importance is model-specific predictive evidence, not a standalone explanation of why an outcome changed. Use held-out evaluation, stability checks, domain context, and causal study designs for causal questions.
