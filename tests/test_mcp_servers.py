from pathlib import Path
from uuid import uuid4

import pandas as pd

from app.config import UPLOAD_DIR
from app.mcp.client import MCPClient
from app.mcp.registry import list_mcp_registry


def test_mcp_adapter_discovers_safe_tools():
    registry = list_mcp_registry()

    assert any(item["server"] == "data_science" and item["tool"] == "calculate_correlation" for item in registry)
    assert any(item["server"] == "knowledge" and item["tool"] == "search_knowledge" for item in registry)
    assert all(item["status"] in {"configured", "disabled"} for item in registry)


def test_mcp_tool_executes_within_allowed_upload_directory():
    dataset_path = UPLOAD_DIR / f"mcp-test-{uuid4().hex}.csv"
    pd.DataFrame(
        {"sales": [10.0, 20.0, 30.0, 40.0], "quantity": [1.0, 2.0, 3.0, 4.0]}
    ).to_csv(dataset_path, index=False)
    try:
        result, record = MCPClient().call_tool(
            "data_science",
            "calculate_correlation",
            {
                "dataset_path": str(dataset_path),
                "column_a": "sales",
                "column_b": "quantity",
                "method": "pearson",
            },
        )
        assert isinstance(result, dict), repr(result)
        assert result["correlation"] > 0.99
        assert result["sample_size"] == 4
        assert record["status"] == "success"
    finally:
        dataset_path.unlink(missing_ok=True)
