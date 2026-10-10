import pandas as pd

from app.tools.cleaning_tools import clean_dataset


def test_clean_dataset_removes_duplicates_and_writes_file(tmp_path):
    dataset_path = tmp_path / "dirty.csv"
    df = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-01", "2024-01-02"],
            "sales": [100, 100, 150],
            "region": ["North", "North", "South"],
        }
    )
    df.to_csv(dataset_path, index=False)

    cleaned = clean_dataset(dataset_path)
    assert cleaned["removed_duplicates"] >= 1
    assert cleaned["cleaned_dataset_path"].endswith("cleaned_dirty.csv")
