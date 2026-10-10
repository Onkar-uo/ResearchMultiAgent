from unittest.mock import patch
from uuid import uuid4

from app.config import UPLOAD_DIR
from app.services.analysis_service import run_analysis
from scripts.generate_demo_dataset import generate_demo_dataset


class OfflineLLM:
    def call_tools(self, _messages, _tools):
        return []

    def generate_structured(self, _prompt, _output_model, _system_prompt):
        return None


def test_orchestrator_workflow_runs(tmp_path, monkeypatch):
    monkeypatch.setattr("app.mcp.client.MCP_ENABLED", False)
    monkeypatch.setattr("app.agents.planner.MCP_ENABLED", False)

    def no_knowledge_results(_agent, _state, _server, _tool, _arguments, fallback=None):
        return {"results": []}

    monkeypatch.setattr("app.agents.knowledge.AnalysisAgent.call_mcp_tool", no_knowledge_results)
    dataset_path = UPLOAD_DIR / f"sales-{uuid4().hex}.csv"
    generate_demo_dataset(dataset_path)
    session_id = f"test-{uuid4().hex}"
    try:
        with patch("app.orchestrator.graph.get_ollama_client", return_value=OfflineLLM()):
            result = run_analysis(dataset_path, "Why are sales declining?", session_id=session_id)
    finally:
        dataset_path.unlink(missing_ok=True)
        dataset_path.with_name(f"cleaned_{dataset_path.name}").unlink(missing_ok=True)
    assert result["final_report"]
    assert "Final Conclusion" in result["final_report"] or "Executive Summary" in result["final_report"]
    assert result["execution_trace"]
    assert result["evidence_catalog"]


def test_iteration_guard_stops_at_configured_limit():
    from app.orchestrator.graph import enforce_iteration_limit, route_critic

    state = {
        "critic_review": {"overall_status": "REVISE", "missing_evidence": []},
        "iteration": 0,
        "max_iterations": 3,
    }
    state.update(enforce_iteration_limit(state))
    assert state["iteration"] == 1
    assert route_critic(state) == "revise"

    state = {
        "critic_review": {"overall_status": "REVISE", "missing_evidence": []},
        "iteration": 3,
        "max_iterations": 3,
    }
    update = enforce_iteration_limit(state)
    state.update(update)

    assert state["critic_review"]["overall_status"] == "INSUFFICIENT_EVIDENCE"
    assert route_critic(state) == "report"


def test_planner_uses_deterministic_tools_when_llm_returns_none(monkeypatch):
    from app.agents.planner import AnalysisPlannerAgent

    class NoToolsLLM:
        def call_tools(self, _messages, _tools):
            return []

    monkeypatch.setattr("app.agents.planner.MCP_ENABLED", False)
    agent = AnalysisPlannerAgent(NoToolsLLM())
    called_tools = []

    def record_tool(_state, _server, tool_name, _arguments, fallback=None):
        called_tools.append(tool_name)
        return {"tool": tool_name}

    agent.call_mcp_tool = record_tool
    state = {
        "user_question": "Analyze the dataset",
        "data_profile": {
            "numerical_columns": ["sales", "quantity"],
            "categorical_columns": ["region"],
            "datetime_columns": ["date"],
            "potential_target": "sales",
        },
        "cleaned_dataset_path": "authorized.csv",
        "tool_results": [],
        "errors": [],
        "iteration": 0,
    }

    agent.execute(state)

    assert called_tools == [
        "calculate_correlation",
        "group_analysis",
        "analyze_time_series",
    ]
    assert len(state["tool_results"]) == 3
    assert any("selected no tools" in error["error"] for error in state["errors"])
