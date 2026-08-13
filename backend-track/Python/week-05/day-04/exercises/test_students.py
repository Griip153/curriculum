# Day 20 - "Your turn" items 3: pagination and search tests, plus a couple of
# already-solved tests carried forward to show the pattern with auth_headers.
#
# Run: pytest -v

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200


def test_create_student_requires_auth():
    response = client.post("/students/", json={"name": "Ada", "score": 91})
    assert response.status_code == 401


def test_create_student_with_auth(auth_headers):
    response = client.post(
        "/students/", json={"name": "Ada", "score": 91}, headers=auth_headers
    )
    assert response.status_code == 201


# TODO: test_list_students_pagination
#   - create 5 students via client.post(..., headers=auth_headers)
#   - GET /students/?limit=2
#   - assert response.json()["total"] == 5
#   - assert len(response.json()["students"]) == 2


# TODO: test_list_students_search
#   - create a student named "Ada" and one named "Kofi" (headers=auth_headers)
#   - GET /students/?search=ad
#   - assert only "Ada" appears in the results
