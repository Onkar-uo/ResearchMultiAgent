from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_returns_api_information():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"
    assert response.json()["health"] == "/health"


def test_favicon_does_not_return_not_found():
    response = client.get("/favicon.ico")

    assert response.status_code == 204


def test_analyze_rejects_paths_outside_configured_data_directories(tmp_path):
    dataset_path = tmp_path / "outside.csv"
    dataset_path.write_text("sales\n1\n", encoding="utf-8")
    response = client.post(
        "/analyze",
        json={"dataset_path": str(dataset_path), "user_question": "Analyze"},
    )

    assert response.status_code == 400
    assert "outside" in response.json()["detail"]
