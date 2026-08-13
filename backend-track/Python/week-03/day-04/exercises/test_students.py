# Day 12 - SOLVED: 4 tests worked together in the session
# (test_health_check, test_create_student, test_get_student_not_found,
# test_create_student_invalid_score). Exercises 5-8 are the "Your turn"
# assignment - marked with # TODO, each with the assertions to write.
#
# Run: pytest -v

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_student():
    response = client.post("/students/", json={"name": "Ada", "score": 91})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Ada"
    assert data["score"] == 91
    assert "id" in data


def test_get_student_not_found():
    response = client.get("/students/9999")
    assert response.status_code == 404


def test_create_student_invalid_score():
    response = client.post("/students/", json={"name": "Ada", "score": 500})
    assert response.status_code == 422


# TODO 5: test_list_students
#   - create a student via client.post(...)
#   - GET /students/
#   - assert status_code == 200 and len(response.json()["students"]) == 1


# TODO 6: test_update_student
#   - create a student, capture its id from the response JSON
#   - PUT /students/{id} with a new name/score
#   - assert status_code == 200 and the response reflects the new values


# TODO 7: test_update_student_not_found
#   - PUT /students/9999 with any valid body
#   - assert status_code == 404


# TODO 8: test_delete_student
#   - create a student, capture its id
#   - DELETE /students/{id}, assert status_code == 204
#   - GET /students/{id} again, assert status_code == 404 (confirms it's gone)


# STRETCH: test_list_students_min_score_filter
#   - create two students with different scores (e.g. 60 and 90)
#   - GET /students/?min_score=80
#   - assert only the higher-scoring one comes back
