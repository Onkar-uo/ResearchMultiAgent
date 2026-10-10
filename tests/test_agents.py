from app.agents.profiler import DataProfilerAgent
from app.agents.cleaner import DataCleaningAgent
from scripts.generate_demo_dataset import generate_demo_dataset


def test_agent_flow(tmp_path):
    dataset_path = tmp_path / "sales.csv"
    generate_demo_dataset(dataset_path)
    state = {"dataset_path": str(dataset_path), "session_id": "agent-test", "data_profile": {}, "cleaning_report": {}, "errors": [], "execution_trace": [], "iteration": 0, "max_iterations": 3}
    profiler = DataProfilerAgent()
    cleaner = DataCleaningAgent()

    after_profiler = profiler.run(state.copy())
    after_cleaner = cleaner.run(after_profiler)
    assert after_profiler["data_profile"]["row_count"] > 0
    assert after_cleaner["cleaning_report"]["cleaned_dataset_path"]
