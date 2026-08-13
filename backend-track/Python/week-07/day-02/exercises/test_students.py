# Day 26 - SOLVED: the ownership pair (test_update_student_forbidden_for_non_owner,
# test_update_student_allowed_for_owner), worked together in the session.
# "Your turn" items 1-2 (the DELETE matrix, the parametrized score boundary
# test) are marked with # TODO below.
#
# Run: pytest -v
# Coverage: pytest --cov=services --cov=routers --cov-report=term-missing

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_update_student_forbidden_for_non_owner(user_a_headers, user_b_headers):
    created = client.post(
        "/students/", json={"name": "Ada", "score": 91}, headers=user_a_headers
    ).json()

    response = client.put(
        f"/students/{created['id']}",
        json={"name": "Ada", "score": 100},
        headers=user_b_headers,
    )
    assert response.status_code == 403


def test_update_student_allowed_for_owner(user_a_headers):
    created = client.post(
        "/students/", json={"name": "Ada", "score": 91}, headers=user_a_headers
    ).json()

    response = client.put(
        f"/students/{created['id']}",
        json={"name": "Ada", "score": 100},
        headers=user_a_headers,
    )
    assert response.status_code == 200


# TODO 1: the full DELETE /students/{id} matrix (see LESSON.md Section 3):
#   - test_delete_student_no_token -> 401 (no headers passed at all)
#   - test_delete_student_forbidden_for_non_owner -> 403 (user_a creates, user_b deletes)
#   - test_delete_student_allowed_for_owner -> 204 (user_a creates, user_a deletes)
#   - test_delete_student_not_found -> 404 (any valid headers, id=9999)
#   Admin case is optional/stretch - it needs a database-level promotion to
#   UserRole.ADMIN since there's no public endpoint for it by design.


# TODO 2: a parametrized test for score boundaries, following the exact
# @pytest.mark.parametrize pattern in LESSON.md Section 5:
#   score=-1 -> 422, score=101 -> 422, score=0 -> 201, score=100 -> 201,
#   score=50 -> 201. Remember to import pytest at the top of this file.
