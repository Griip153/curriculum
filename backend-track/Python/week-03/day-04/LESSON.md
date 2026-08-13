# Day 12 — Teaching Lesson: Testing Your API

> Companion to `README.md`. This is a **step-by-step walkthrough**. Today has no new
> API features — it's entirely about proving, automatically, that everything you've
> built since Day 7 actually works, and keeps working as you keep changing it.

## Objective
Prove your endpoints work automatically — before a user finds the bug for you.

## 1. Why tests exist

**Definition:** An automated test is a small program that calls your code and checks
the result against what you expect, failing loudly if it doesn't match. The
alternative — manually clicking through `/docs` after every change, like you've been
doing since Day 7 — works, but it's slow, easy to forget a case, and gets worse every
week as your API grows.

The payoff isn't really about today — it's about every day *after* today. Once you
have tests, you can change `services/students.py` next week with confidence: run the
tests, and know immediately if you broke something, instead of finding out from a
user.

## 2. Installing pytest and httpx's test client

```bash
pip install pytest
pip freeze > requirements.txt
```
**Definition:** `pytest` is the standard Python testing framework — it finds every
function starting with `test_` in any file starting with `test_`, runs each one, and
reports which passed or failed.

FastAPI ships its own test tool built on top of `httpx`, so no extra install is
needed for it:
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
```
**Definition:** `TestClient` lets you call your FastAPI app's routes directly in
Python — no running server, no real network — while behaving exactly like a real
HTTP client would (`client.get(...)`, `client.post(...)`, checking
`.status_code` and `.json()`).

## 3. Your first test

```python
# test_students.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```
**Definition:** `assert` is a statement that does nothing if the condition is true,
and raises an `AssertionError` (which `pytest` reports as a failure) if it's false. A
test is, at its core, just a sequence of `assert` statements checking what you expect
to be true.

Run it:
```bash
pytest
```
`pytest` finds `test_students.py`, runs `test_health_check`, and reports `1 passed`
(green) or shows exactly which `assert` failed (red), with the actual vs. expected
values.

## 4. A separate test database — the single most important idea today

**Definition:** Tests should never run against your real development or production
database. If they did, running your test suite would create, modify, and delete real
data every time — tests need their own, disposable database, reset between runs.

```python
# conftest.py — pytest automatically loads this file before any test
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)   # fresh tables before each test
    yield
    Base.metadata.drop_all(bind=engine)     # wipe them after each test
```
**Reading the two new ideas here:**
- **`app.dependency_overrides[get_db] = override_get_db`** — this is FastAPI's
  built-in mechanism for swapping out a dependency during tests. Every route that
  normally gets a real database session via `Depends(get_db)` now transparently gets
  a *test* database session instead — no route code changes at all.
- **`@pytest.fixture(autouse=True)`** — a **fixture** is a function that sets
  something up before a test and (via `yield`) tears it down after. `autouse=True`
  means it runs automatically before and after *every single test* in this file, with
  no need to mention it by name. This guarantees each test starts from a clean,
  empty database — tests should never depend on the order they run in, or on data
  left behind by a previous test.

## 5. Testing the happy paths: create, list, get, update, delete

```python
def test_create_student():
    response = client.post("/students/", json={"name": "Ada", "score": 91})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Ada"
    assert data["score"] == 91
    assert "id" in data

def test_list_students():
    client.post("/students/", json={"name": "Ada", "score": 91})
    response = client.get("/students/")
    assert response.status_code == 200
    assert len(response.json()["students"]) == 1

def test_get_student():
    created = client.post("/students/", json={"name": "Ada", "score": 91}).json()
    response = client.get(f"/students/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Ada"
```
**Notice the shape:** each test is short, checks one behaviour, and sets up whatever
data it needs itself (creating a student before testing "get" or "list") — it never
assumes another test ran first, because the database is wiped between every single
test (Step 4).

## 6. Testing the failure paths

This is the part beginners skip, and it's the part that matters most — a test suite
that only checks happy paths gives you false confidence.

```python
def test_get_student_not_found():
    response = client.get("/students/9999")
    assert response.status_code == 404

def test_create_student_invalid_score():
    response = client.post("/students/", json={"name": "Ada", "score": 500})
    assert response.status_code == 422

def test_create_student_blank_name():
    response = client.post("/students/", json={"name": "   ", "score": 50})
    assert response.status_code == 422
```
These three tests directly verify the work you did on Day 11 — they'll fail loudly if
you (or a future teammate) accidentally weaken the validation later. This is exactly
what "before a user finds the bug for you" means in practice.

---

## Worked example: 4 tests, fully wired

### Problem statement
Write `conftest.py` (Step 4) and four tests: `test_health_check`,
`test_create_student`, `test_get_student_not_found`, and
`test_create_student_invalid_score`.

### Solution
See [`exercises/conftest.py`](./exercises/conftest.py) and
[`exercises/test_students.py`](./exercises/test_students.py) — both fully solved and
commented, copied forward from Day 11's completed project.

Run the whole suite:
```bash
cd exercises
pytest -v
```
The `-v` flag ("verbose") prints each test's name and result individually, instead of
just a summary — worth using while you're still building the habit.

### What to notice
- Every test file, and `conftest.py` itself, lives in the *same* `exercises/` folder
  as `main.py` — pytest discovers them by filename convention (`test_*.py`), no
  registration needed.
- `test.db` (or whatever your `TEST_DATABASE_URL` points to) gets created and
  destroyed by the fixture — you can safely delete it at any time; it holds nothing
  real.
- None of today's tests talk to your actual Neon/Postgres database at all — that's
  the entire point of Step 4.

---

## Your turn — reach 8+ tests

Add these to `exercises/test_students.py`, using the same pattern as the worked
examples:

| # | Test | Checks |
|---|---|---|
| 5 | `test_list_students` | listing returns everything you created |
| 6 | `test_update_student` | a `PUT` changes the stored values |
| 7 | `test_update_student_not_found` | `PUT` on a missing id returns `404` |
| 8 | `test_delete_student` | a `DELETE` removes it — confirm with a follow-up `GET` returning `404` |

**Stretch goal:** add a test for the `min_score` query filter from Day 7 — create two
students with different scores, request `/students/?min_score=80`, and assert only
the higher-scoring one comes back.

---

## Common mistakes to watch for
- **Tests that depend on each other's order or leftover data** — always create the
  exact data a test needs, inside that test, and rely on the `autouse` fixture to
  wipe the database between tests. If you ever find yourself thinking "this test only
  passes if it runs after that other one," something's wrong.
- **Forgetting `app.dependency_overrides[get_db] = override_get_db`** — without it,
  your tests silently run against your real database, which is exactly what today is
  about avoiding.
- **Only testing happy paths** — Section 6 exists because this is the single most
  common gap in beginner test suites, and the one that catches the fewest real bugs.
- **Committing `test.db`** — add it to `.gitignore` alongside your other generated
  database files.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
