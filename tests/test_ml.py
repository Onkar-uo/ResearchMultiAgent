import pandas as pd

from app.tools.ml_tools import train_regression_model


def test_train_regression_model_returns_metrics():
    n = 200
    x = pd.Series(range(n), name="feature")
    y = 5 + 2 * x
    df = pd.DataFrame({"feature": x, "sales": y})
    result = train_regression_model(df, "sales", ["feature"])
    assert result["problem_type"] == "regression"
    assert result["models"][0]["r2"] >= 0.7
