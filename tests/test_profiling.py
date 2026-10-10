from pathlib import Path

import pandas as pd

from app.tools.profiling_tools import profile_dataset
from scripts.generate_demo_dataset import generate_demo_dataset


def test_profile_dataset_detects_key_fields(tmp_path):
    dataset_path = tmp_path / "sales.csv"
    generate_demo_dataset(dataset_path)
    profile = profile_dataset(dataset_path)
    assert profile["row_count"] > 0
    assert "sales" in profile["numerical_columns"]
    assert "region" in profile["categorical_columns"]


def test_numeric_columns_are_not_classified_as_datetimes(tmp_path):
    dataset_path = tmp_path / "numeric.csv"
    pd.DataFrame({"sales": [20240101, 20240102, 20240103], "count": [1, 2, 3]}).to_csv(
        dataset_path, index=False
    )

    profile = profile_dataset(dataset_path)

    assert profile["datetime_columns"] == []
