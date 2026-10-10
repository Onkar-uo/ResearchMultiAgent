import pandas as pd

from app.tools.statistics_tools import calculate_correlations, group_analysis


def test_calculate_correlations_and_group_analysis():
    df = pd.DataFrame({
        "sales": [100, 200, 300, 400],
        "quantity": [10, 20, 30, 40],
        "region": ["A", "A", "B", "B"],
    })

    corr = calculate_correlations(df, "sales")
    groups = group_analysis(df, "region", "sales")
    assert corr["pearson_top"]
    assert groups
