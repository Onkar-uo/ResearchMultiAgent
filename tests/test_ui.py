from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_streamlit_upload_form_renders():
    app_path = Path(__file__).parents[1] / "app" / "ui" / "streamlit_app.py"
    app_test = AppTest.from_file(str(app_path)).run(timeout=30)

    assert not app_test.exception
    assert any("AI Data Science Team" in title.value for title in app_test.title)
    assert app_test.file_uploader
    assert app_test.text_area
