from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate_demo_dataset(path: str | Path = "data/uploads/sales_demo.csv", rows: int = 10_000) -> Path:
    rng = np.random.default_rng(42)
    dates = pd.date_range("2022-01-01", periods=rows, freq="D")
    regions = ["North", "South", "East", "West", "Central"]
    products = ["Laptop", "Phone", "Tablet", "Monitor", "Accessory"]
    region_series = rng.choice(regions, size=rows)
    product_series = rng.choice(products, size=rows)
    quantity = rng.integers(5, 45, size=rows)
    price = rng.uniform(100, 2200, size=rows)
    trend = np.linspace(0, 300, rows)
    seasonality = np.sin(np.arange(rows) / 30) * 120
    region_effect = np.array([120 if region == "North" else 80 if region == "South" else 60 if region == "East" else 90 if region == "West" else 70 for region in region_series])
    product_effect = np.array([180 if product == "Laptop" else 120 if product == "Phone" else 90 if product == "Tablet" else 50 if product == "Monitor" else 25 for product in product_series])
    sales = (quantity * price * (0.75 + rng.uniform(0.1, 0.4, size=rows))) + trend + seasonality + region_effect + product_effect
    discount = np.clip(rng.normal(0.12, 0.06, size=rows), 0, 0.5)
    sales = sales * (1 - discount)
    marketing_spend = rng.uniform(20, 300, size=rows)
    customer_count = rng.integers(10, 200, size=rows)
    profit = sales * 0.2 + marketing_spend * 0.05

    df = pd.DataFrame({
        "date": dates,
        "region": region_series,
        "product": product_series,
        "sales": sales,
        "quantity": quantity,
        "price": price,
        "discount": discount,
        "marketing_spend": marketing_spend,
        "customer_count": customer_count,
        "profit": profit,
    })

    df.loc[rng.choice(rows, 500, replace=False), "sales"] = np.nan
    df.loc[rng.choice(rows, 200, replace=False), "discount"] = np.nan
    df.loc[rng.choice(rows, 100, replace=False), "product"] = np.nan
    df.loc[rng.choice(rows, 30, replace=False), "sales"] = df.loc[rng.choice(rows, 30, replace=False), "sales"] * 5
    df = pd.concat([df, df.iloc[:80].copy()], ignore_index=True)
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    return out


if __name__ == "__main__":
    generate_demo_dataset()
