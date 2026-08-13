# Day 11 — Teaching Lesson: Validation & Error Handling Done Right

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered
> step builds on the one before it.
>
> Yesterday you finished full SQLAlchemy CRUD — bad *types* already get rejected by
> Pydantic before they ever reach the database. But two things still feel
> unpolished: a `score` of `-50` or a `name` of `""` currently sails straight through
> to the database, since Pydantic only checked *type*, not *reasonableness*. And a
> database-layer failure (like a broken connection) currently comes back as a scary,
> generic `500` instead of a clear message. Today you fix both — request data gets
> checked thoroughly *before* it reaches the database, and every failure, from every
> layer, comes back through the same shape: `{"error": "message"}`.

## Objective
Make your API fail clearly and safely — the mark of professional work.

## What you're building today
- Real validation rules on `StudentIn`: `name` must be non-empty and reasonably
  short; `score` must be between 0 and 100.
- The central error handler from Day 8, taught to recognise a database error and
  respond `400`/`500` appropriately with a clear message.
- Proof, in `/docs`, that five different kinds of bad request each fail with the
  right status code and the same `{"error": "..."}` shape.

---

## Step 1 — Why "it's an integer" isn't enough

**Definition:** Type validation (Day 7) checks *what kind* of value something is.
Constraint validation checks whether a value of the right type is *actually
reasonable* — a `score` of `-50` is a perfectly valid integer, but it's nonsense for
a student's score.

Two gaps type-only validation leaves open:
- **An out-of-range score.** `score: int` happily accepts `-50` or `9999` — nothing
  about "int" implies "between 0 and 100."
- **An empty or whitespace-only name.** `name: str` happily accepts `""` or `"   "` —
  nothing about "str" implies "not blank."

## 2. `Field()` — declaring constraints, not just types

**Definition:** `Field()` is Pydantic's way of attaching extra rules — minimum/
maximum values, string length, a default — directly onto a model's field
declaration.

```python
from pydantic import BaseModel, Field

class StudentIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    score: int = Field(..., ge=0, le=100)
```
**Reading each piece:**
- **`...`** (an ellipsis, used as the first argument) means "this field is required —
  no default."
- **`min_length` / `max_length`** — string length bounds.
- **`ge` / `le`** — "greater than or equal" / "less than or equal" — numeric bounds.
  (`gt`/`lt` exist too, for strict inequalities.)

Try `POST /students` with `{"name": "", "score": 150}` now — FastAPI responds `422`
automatically, with a message naming *exactly* which field failed and why, no code
of yours involved.

## 3. `@field_validator` — rules `Field()` can't express

**Definition:** Some rules are too specific for `Field()`'s built-in options — a
`@field_validator` is a method on your model, decorated to run automatically during
validation, that can contain arbitrary Python logic and either return a cleaned value
or raise an error.

```python
from pydantic import BaseModel, Field, field_validator

class StudentIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    score: int = Field(..., ge=0, le=100)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value):
        if not value.strip():
            raise ValueError("name must not be blank")
        return value.strip()   # you can also clean the value, not just check it
```
Notice this closes the "whitespace-only name" gap that `min_length=1` alone misses —
`"   "` has length 3, so `min_length=1` lets it through; the validator catches it
because it actually inspects the content, not just the length.

**Why this belongs in the Pydantic model, not the service layer:** the exact same
`if not name` check used to live in `services/students.py` (Day 8) as a manual
`ValueError`. Moving it here means the check happens automatically, on every route
that uses `StudentIn`, and produces FastAPI's structured `422` response instead of a
hand-rolled `400` — one consistent mechanism instead of two.

## 4. Handling database-layer errors

**Definition:** Even with perfect request validation, some failures only happen at
the database — a broken connection, a constraint the database enforces that Pydantic
doesn't know about, a duplicate value in a column marked `unique`. These surface as
SQLAlchemy exceptions, not Pydantic ones, and need their own handler.

```python
from sqlalchemy.exc import IntegrityError, OperationalError

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(status_code=400, content={"error": "A database constraint was violated."})

@app.exception_handler(OperationalError)
async def operational_error_handler(request: Request, exc: OperationalError):
    return JSONResponse(status_code=503, content={"error": "Database is temporarily unavailable."})
```
**Reading the distinction:** `IntegrityError` means the data itself was the problem
(e.g. violating a constraint) — that's the client's fault, `400`. `OperationalError`
means the database couldn't be reached at all — that's not the client's fault, `503
Service Unavailable` is the honest status code, telling them "try again," not "you
did something wrong."

## 5. One more shape to unify: Pydantic's own `422` body

FastAPI's default `422` response for a failed `StudentIn` validation looks like:
```json
{"detail": [{"loc": ["body", "score"], "msg": "...", "type": "..."}]}
```
That's genuinely useful for debugging, but it doesn't match your app's
`{"error": "..."}` shape from Day 8. You can unify it too, if you want every error in
your API to have exactly one shape:
```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]
    field = first_error["loc"][-1]
    message = first_error["msg"]
    return JSONResponse(status_code=422, content={"error": f"{field}: {message}"})
```
This is optional polish — both approaches are defensible. The point of this lesson is
that you now *choose*, deliberately, rather than having five inconsistent error
shapes by accident.

---

## Worked example: full validation, wired end to end

### Problem statement
Add the `Field()` and `@field_validator` rules from Steps 2-3 to `StudentIn`, and
register the `IntegrityError`/`OperationalError` handlers from Step 4 in `main.py`.

### Solution
See [`exercises/routers/students.py`](./exercises/routers/students.py) (the updated
`StudentIn`) and [`exercises/main.py`](./exercises/main.py) (the new handlers) — both
fully solved and commented.

Run it:
```bash
cd exercises
uvicorn main:app --reload
```

### What to notice
- `Field()` constraints and `@field_validator` logic both run *before* your route
  function is even called — by the time `create_student(student: StudentIn, ...)`
  executes, `student` is guaranteed valid. You'll never write a defensive `if score <
  0` inside a route body again.
- The database-layer handlers (Step 4) only ever fire for failures that *couldn't*
  have been caught earlier — this is the correct division of labour: catch what you
  can as early as possible (Pydantic), and handle what's left as gracefully as
  possible (the database layer), rather than trying to anticipate every database
  failure in application code.

---

## Your turn — prove it in `/docs`

Test each of these five requests against `POST /students` (or the matching route) in
`/docs`, and confirm the status code and general shape match:

| Request | Expected result |
|---|---|
| `{"name": "Bruno", "score": 77}` | `201` — created normally |
| `{"name": "", "score": 77}` | `422` — blank name rejected |
| `{"name": "Bruno", "score": 150}` | `422` — score out of range |
| `{"name": "   ", "score": 50}` | `422` — whitespace-only name caught by the validator |
| `GET /students/9999` (a non-existent id) | `404` — from Day 10's `HTTPException`, unaffected by today's changes |

Write one sentence in your daily report about *which layer* caught each failure
(Pydantic `Field`, your `@field_validator`, or the route's own `HTTPException`) — the
goal is to leave today able to say precisely where each kind of bad input gets
stopped.

---

## Common mistakes to watch for
- **Putting business rules in `@field_validator` that actually depend on the
  database** (like "this name must be unique") — Pydantic validators run before any
  database call and can't check that. Uniqueness belongs at the database/service
  layer, using a real query or a `UNIQUE` constraint.
- **Forgetting `@classmethod`** above a `@field_validator` — Pydantic requires it;
  omitting it raises a confusing error at import time, not at request time.
- **Catching `Exception` broadly** to "handle everything" — you lose the ability to
  respond differently to genuinely different problems (a `400` vs. a `503`), and you
  risk silently swallowing bugs you'd want to see crash loudly in development.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
