from io import BytesIO

from web.app import create_app


def test_upload_answers_endpoint_returns_upload_metadata():
    app = create_app()
    client = app.test_client()

    csv_bytes = b"student_id,question_id,answer_text\nS1,Q1,test\n"
    response = client.post(
        "/upload/answers",
        data={"file": (BytesIO(csv_bytes), "answers.csv")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert "upload_id" in payload
    assert payload["n_students"] == 1
    assert payload["n_questions"] == 1


def test_run_analyze_requires_valid_mode():
    app = create_app()
    client = app.test_client()

    response = client.post("/run/analyze", json={"upload_id": "x", "mode": "invalid"})
    assert response.status_code == 400
