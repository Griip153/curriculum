# Day 8 — Teaching Lesson: REST Design & Project Structure

> Companion to `README.md`. This is a **step-by-step walkthrough**. Today you take
> yesterday's working-but-messy students API and make it look like something a
> professional team would actually ship: clean URLs, a real folder structure, and
> errors that behave consistently everywhere, not just where you remembered to write
> a `try`/`except`.

## Objective
Structure an API like a professional team — routers, a service layer, and errors
that make sense.

## 1. REST — designing URLs that make sense

**Definition:** REST (REpresentational State Transfer) is a set of conventions for
designing web APIs around **resources** (nouns — "students," "orders") and standard
HTTP **methods** (verbs — GET, POST, PUT, DELETE) instead of inventing a new URL
shape for every action.

**The core rule: URLs are nouns, methods are verbs.**
```
BAD:  GET /getAllStudents
BAD:  POST /createNewStudent
BAD:  GET /deleteStudent?id=3

GOOD: GET    /students          -> list students
GOOD: GET    /students/3        -> get one student
GOOD: POST   /students          -> create a student
GOOD: PUT    /students/3        -> update a student
GOOD: DELETE /students/3        -> delete a student
```
The action is expressed by the **method**, not stuffed into the path. This is exactly
what you built yesterday — today formalises *why* that shape is the industry
standard, so you recognise and design it correctly by default from now on.

**A note on `PUT` vs `PATCH`:** `PUT` conventionally means "replace the entire
resource with this data." `PATCH` means "update only these specific fields." Your
students API uses `PUT` throughout this track for simplicity — just know the
distinction exists, since you'll see both in real APIs.

## 2. Routes vs. a service layer

**Definition:** A route function's job should be limited to three things: read the
request, call some other function that does the actual work, and shape the response.
The "actual work" — the business logic — belongs in a separate layer, often called
**services** (or sometimes **CRUD** functions), so it can be tested and reused
without needing a fake HTTP request to trigger it.

Yesterday, `routers/students.py` mixed both together — the route function directly
manipulated `students_db`. Today, split it:
```python
# services/students.py — the logic, no FastAPI imports at all
def get_all(min_score=None):
    if min_score is None:
        return students_db
    return [s for s in students_db if s["score"] >= min_score]

def get_by_id(student_id):
    return next((s for s in students_db if s["id"] == student_id), None)
```
```python
# routers/students.py — thin, just wires HTTP to the service layer
from services import students as students_service

@router.get("/")
def list_students(min_score: int | None = None):
    return {"students": students_service.get_all(min_score)}
```
**Why this matters, concretely:** `students_service.get_all(80)` can be called and
tested directly, in a plain Python script or a test file, with no server running at
all. That becomes very valuable starting Week 3, Day 4 (testing) — code that doesn't
need a fake HTTP request to test is dramatically easier to test well.

## 3. Global exception handling

**Definition:** A global exception handler is a function, registered once at the app
level, that catches a specific type of error from *anywhere* in your application and
turns it into a consistent, well-shaped response — instead of every route needing its
own repeated `try`/`except`.

You already know `HTTPException` from Day 7 (`raise HTTPException(status_code=404,
...)`) — FastAPI has a built-in handler for that one already. Today's new tool is
`@app.exception_handler(...)`, for catching your *own* custom exception types, or
built-in Python ones you want to handle uniformly:
```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)},
    )
```
Now, **any** route in your entire app that raises a plain `ValueError` automatically
gets converted into a clean `400` response with that message — you never write
`try`/`except ValueError` in a route again. This is the FastAPI-native version of the
"one central error handler" idea from Express-style Node backends.

## 4. Catch-all 404 handling

**Definition:** By default, FastAPI already returns a `404` for any URL that doesn't
match a registered route — you get this for free, unlike yesterday's raw server where
you wrote the `else: 404` branch by hand. Today's job is just making sure that
default response is *shaped* the way the rest of your API is — for consistency, you
can override it:
```python
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def not_found_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )
```
This intercepts FastAPI's built-in 404s (and every other `HTTPException`, including
the ones you raise yourself) and guarantees they all come back shaped as
`{"error": "..."}`, consistently, everywhere in your app.

## 5. Environment variables with `pydantic-settings`

**Definition:** An environment variable is a named value provided to your program by
the operating system (or a `.env` file), rather than hard-coded — used for anything
that changes between environments or that must never be committed to Git (database
URLs, secret keys, API tokens). `pydantic-settings` is a library that reads
environment variables into a validated, type-hinted Python object.

```bash
pip install pydantic-settings python-dotenv
```
```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Students API"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```
```
# .env  (never commit this file — it's in .gitignore)
DEBUG=True
```
```python
# main.py
from config import settings

app = FastAPI(title=settings.app_name)
```
**Why this matters:** `Settings` validates that `debug` really is `True`/`False` and
not some typo'd string, the same way Pydantic validates request bodies. Nothing
sensitive lives directly in your code — a teammate, or a production server, supplies
their own `.env` with their own values, and your code doesn't change at all.

Create a `.env.example` (committed to Git, with placeholder values) alongside the
real `.env` (never committed) — this is how a teammate knows what variables exist
without ever seeing your real secrets.

---

## Worked example: wiring it all together

### Problem statement
Take yesterday's `routers/students.py` and split it into `routers/students.py` (thin,
HTTP-only) and `services/students.py` (the actual logic), then register both a
`ValueError` handler and a shaped 404/HTTPException handler in `main.py`, and load
`app_name` from a `.env` file.

### Solution
See the fully solved, commented project in `exercises/` — `main.py`,
`config.py`, `services/students.py`, and `routers/students.py`.

Run it:
```bash
cd exercises
uvicorn main:app --reload
```

### What to notice
- `services/students.py` never imports anything from `fastapi` — it's plain Python,
  which is exactly what makes it independently testable later.
- Both exception handlers live in `main.py`, registered once, and apply to
  **every** router mounted on `app` — you don't repeat this setup per router.
- `.env` holds `DEBUG=True` for local development; a real deployment (Week 7, Day 4)
  will supply its own `.env` with `DEBUG=False` and real secrets, and none of your
  Python code changes.

### Common mistakes to watch for
- **Putting business logic back in the route function "just this once"** — it always
  grows. Keep the boundary strict from day one.
- **Committing a real `.env` file** — always double check `.gitignore` includes it
  before your first `git add .` on any new project.
- **Registering an exception handler for a type that's too broad**, like `Exception`
  itself, without being deliberate about it — it can accidentally swallow errors you
  actually wanted to see crash loudly during development. Start narrow (specific
  exception types) and widen only if you have a good reason to.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
