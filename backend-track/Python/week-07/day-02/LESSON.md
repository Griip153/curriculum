# Day 26 — Teaching Lesson: Advanced Testing

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered
> step builds on the one before it.
>
> Week 3, Day 12 gave you the basics: `TestClient`, a test database, happy-path and
> failure-path tests. Since then, you've added authentication, ownership checks, and
> file uploads — today your test suite catches up to all of it, and you measure how
> thoroughly with `pytest-cov`.

## Objective
Reusable fixtures, testing protected/forbidden routes properly, and measuring
coverage.

## 1. A reusable authentication fixture

You may have already written something like this ad hoc (Week 5, Day 20's
`auth_headers` fixture). Today, formalise it properly, and add a *second* user so you
can actually test ownership failures — something one user alone can never exercise.

```python
# conftest.py (continued)
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def user_a_headers():
    client.post("/auth/register", json={"email": "a@example.com", "password": "password123"})
    response = client.post("/auth/login", json={"email": "a@example.com", "password": "password123"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def user_b_headers():
    client.post("/auth/register", json={"email": "b@example.com", "password": "password123"})
    response = client.post("/auth/login", json={"email": "b@example.com", "password": "password123"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```
**Definition:** A **fixture that depends on nothing else** (like these two) can be
requested by *any* test simply by naming it as a parameter — `pytest` resolves and
injects it automatically, the same dependency-injection idea `Depends()` gave you in
FastAPI itself (Day 18), just at the test level instead of the request level.

## 2. Testing ownership properly: two real users, not one

This is the test Week 5/6 never actually wrote — proving `403` fires for the right
reason, not just trusting the code:
```python
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
```
**Notice this genuinely exercises the ownership check's logic** — user A creates it,
user B is blocked, user A themselves succeeds. A single-user test suite literally
cannot distinguish "the ownership check works" from "the ownership check is missing
entirely, and everything just happens to succeed because there's only ever one
user" — this is exactly why the gap matters.

## 3. A complete auth matrix, systematically

Rather than testing scenarios one at a time as they occur to you, build the full
matrix deliberately for each protected route:

| Scenario | Expected |
|---|---|
| No token | `401` |
| Valid token, not the owner, not admin | `403` |
| Valid token, is the owner | `200`/`204` |
| Valid token, is admin, not the owner | `200`/`204` |
| Valid token, resource doesn't exist | `404` |

Writing this table out *before* writing the tests (as you're doing right now,
reading it) is the actual skill today — the code itself is short once you know
exactly what to check.

## 4. `pytest-cov` — measuring what your tests actually exercise

```bash
pip install pytest-cov
pytest --cov=services --cov=routers --cov-report=term-missing
```
**Definition:** Test coverage measures what percentage of your code's lines actually
ran during your test suite. `--cov-report=term-missing` additionally lists the
*specific line numbers* that were never executed by any test — the most actionable
part of the report.

```
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
services/students.py        42      3    93%   58-60
routers/students.py         38      5    87%   71-75
------------------------------------------------------
TOTAL                       80      8    90%
```
**A crucial caveat, worth understanding precisely:** 100% coverage means every line
*ran* — it does **not** mean every line was tested *correctly*. A test with no
`assert` statements at all would still count toward coverage while checking nothing.
Coverage tells you where you have *zero* tests (a real gap, worth acting on
immediately); it can't tell you where your existing tests are weak. Use it to find
untested code, not as a substitute for thinking about what each test actually
verifies.

## 5. Parametrized tests — one test, many inputs

**Definition:** `@pytest.mark.parametrize` runs the same test function once per
listed set of inputs, avoiding near-identical copy-pasted tests that differ only in
their values.

```python
import pytest

@pytest.mark.parametrize("score,expected_status", [
    (-1, 422),
    (101, 422),
    (0, 201),
    (100, 201),
    (50, 201),
])
def test_create_student_score_boundaries(score, expected_status, user_a_headers):
    response = client.post(
        "/students/", json={"name": "Ada", "score": score}, headers=user_a_headers
    )
    assert response.status_code == expected_status
```
This single function runs 5 times, once per tuple, and `pytest -v` reports each one
individually — this is the clean way to test boundary conditions (Day 11's `ge=0,
le=100`) thoroughly, without writing five nearly-identical functions by hand.

---

## Worked example: the ownership pair, fully wired

### Problem statement
Add `user_a_headers`/`user_b_headers` fixtures and the two ownership tests from
Section 2.

### Solution
See [`exercises/conftest.py`](./exercises/conftest.py) and
[`exercises/test_students.py`](./exercises/test_students.py) — both fully solved and
commented.

Run it:
```bash
cd exercises
pytest -v
```

### What to notice
- Both fixtures register a **different** email — reusing the same one would collide
  with Day 17's unique-email constraint (`IntegrityError` → your Day 11 handler's
  `400`), which is itself worth knowing as you design test data.
- Nothing about `main.py` or your route code changed today — this whole lesson is
  entirely about the *test* side getting more rigorous, proving behaviour that was
  already there (or catching it if it wasn't).

---

## Your turn

1. Using Section 3's matrix, write the complete set of tests for
   `DELETE /students/{id}`: no-token `401`, non-owner `403`, owner `204`, admin
   `204`, missing-id `404`. (You'll need an admin user for the admin case — register
   one normally, then manually promote it to `UserRole.ADMIN` in your test database
   setup, since there's no public "become an admin" endpoint by design.)
2. Add the parametrized boundary test from Section 5 for `score`.
3. Run `pytest --cov=services --cov=routers --cov-report=term-missing` against your
   real Week 4/5/6 project (not just this lesson's exercise folder) and get to at
   least **80% coverage** on `services/`. Read the "Missing" column for anything
   below that, and add tests for the specific gaps it names — don't just add tests
   at random hoping the number goes up.

---

## Common mistakes to watch for
- **Testing ownership with only one user** — Section 2 explained exactly why this
  gives false confidence; always use two distinct users for a `403` test.
- **Chasing 100% coverage as a goal in itself** — 80-90% with genuinely meaningful
  assertions is far more valuable than 100% achieved by padding tests with no real
  checks. Coverage is a tool for finding gaps, not a target to game.
- **Parametrized test cases that don't actually differ meaningfully** — each case in
  a `@pytest.mark.parametrize` list should test something the others don't (a
  boundary, an edge case), not just be filler.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
