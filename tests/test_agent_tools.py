import pandas as pd
import pytest
from uuid import uuid4

from app.config import UPLOAD_DIR
from app.agents.planner import AnalysisPlannerAgent
from app.tools.agent_tools import execute_analysis_tool


class ToolCallingLLM:
    def call_tools(self, messages, tools):
        return [
            {
                "function": {
                    "name": "group_analysis",
                    "arguments": {"group_column": "region", "value_column": "sales"},
                }
            }
        ]

    def generate_structured(self, prompt, output_model, system_prompt):
        return None


def test_tool_call_is_validated_and_executed(tmp_path):
    dataset_path = tmp_path / "sales.csv"
    pd.DataFrame({"region": ["north", "south"], "sales": [10.0, 20.0]}).to_csv(dataset_path, index=False)

    result = execute_analysis_tool(
        "compare_groups",
        {"group_column": "region", "value_column": "sales"},
        dataset_path,
    )

    assert result["tool"] == "compare_groups"
    assert len(result["result"]) == 2


def test_tool_call_rejects_unknown_tools_and_columns(tmp_path):
    dataset_path = tmp_path / "sales.csv"
    pd.DataFrame({"region": ["north"], "sales": [10.0]}).to_csv(dataset_path, index=False)

    with pytest.raises(ValueError, match="not available"):
        execute_analysis_tool("run_shell", {}, dataset_path)
    with pytest.raises(ValueError, match="not found"):
        execute_analysis_tool(
            "compare_groups",
            {"group_column": "missing", "value_column": "sales"},
            dataset_path,
        )


def test_planner_runs_only_registered_tools(tmp_path, monkeypatch):
    monkeypatch.setattr("app.mcp.client.MCP_ENABLED", False)
    monkeypatch.setattr("app.agents.planner.MCP_ENABLED", False)
    dataset_path = UPLOAD_DIR / f"planner-{uuid4().hex}.csv"
    pd.DataFrame({"region": ["north", "south"], "sales": [10.0, 20.0]}).to_csv(dataset_path, index=False)
    state = {
        "dataset_path": str(dataset_path),
        "cleaned_dataset_path": str(dataset_path),
        "session_id": "planner-test",
        "user_question": "Compare average sales by region",
        "data_profile": {"categorical_columns": ["region"], "numerical_columns": ["sales"]},
        "errors": [],
        "execution_trace": [],
        "iteration": 0,
        "max_iterations": 3,
    }

    try:
        result = AnalysisPlannerAgent(ToolCallingLLM()).run(state)
    finally:
        dataset_path.unlink(missing_ok=True)

    assert len(result["tool_results"][0]["groups"]) == 2
    assert result["execution_trace"][0]["tools_used"] == ["group_analysis"]
