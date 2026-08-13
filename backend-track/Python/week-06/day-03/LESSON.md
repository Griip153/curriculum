# Day 23 — Teaching Lesson: FastAPI + Full Typing

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered
> step builds on the one before it.
>
> Days 21-22 were about typing plain Python. Today those same tools go directly into
> the project that's been running since Week 2 — every route gets a declared
> response shape, every service function gets full hints, and the plain
> `role: str = "user"` from Week 5 becomes a real `Enum`.

## Objective
Fully typed routes, strict response shapes, and typed dependencies throughout.

## What you're building today
- `response_model` on every route that returns data.
- `UserRole(str, Enum)` replacing the plain string `role` field.
- Complete type hints on every function in `services/students.py`.

---

## Step 1 — `response_model` as a contract, revisited

You used `response_model` briefly on Week 5, Day 19 for the nested course/students
shape. Today, formalise it everywhere: **every route that returns data declares
exactly what it returns**, and FastAPI enforces that shape on the way out — not just
documenting it, but actually filtering the response to match.

```python
from schemas import StudentOut

@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = students_service.get_by_id(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student   # a raw SQLAlchemy object — FastAPI shapes it via StudentOut
```
**Why this is a security feature, not just documentation:** imagine `Student` later
gained a sensitive column your Pydantic `StudentOut` schema doesn't list.
`response_model=StudentOut` guarantees that new column **never appears in the
response**, even if a developer forgets to update the route — the schema is the
single source of truth for "what's allowed to leave this route," enforced
automatically, every time.

## Step 2 — List responses need their own schema

```python
class StudentListOut(BaseModel):
    total: int
    skip: int
    limit: int
    students: list[StudentOut]

    class Config:
        from_attributes = True

@router.get("/", response_model=StudentListOut)
def list_students(...):
    ...
```
This is the typed version of the dictionary Week 5, Day 20's `list_students` already
returned (`{"total": ..., "students": [...]}`) — same shape, now declared explicitly
and enforced by FastAPI, instead of just implicitly correct because you wrote it
carefully.

## Step 3 — `UserRole` as a real `Enum`

Recall Week 5, Day 18's plain string field: `role = Column(String, default="user")`.
Today, following Day 22's `Enum` pattern, make it a real, closed set:
```python
# models.py
from enum import Enum as PyEnum
from sqlalchemy import Enum as SAEnum

class UserRole(str, PyEnum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(SAEnum(UserRole), default=UserRole.USER, nullable=False)
```
**Two different `Enum`s, deliberately distinguished by import alias:** Python's
built-in `enum.Enum` (aliased `PyEnum` here) defines the actual set of values;
SQLAlchemy's own `sqlalchemy.Enum` (aliased `SAEnum`) is a **column type** that
tells the database to enforce the same restriction at the storage layer too — the
database itself will now reject an invalid role value, the same category of
protection Day 9's `NOT NULL` constraint gave you for blank names.

Update the ownership check from Week 5, Day 18 to compare against the `Enum` member
instead of a raw string:
```python
if existing.created_by != current_user.id and current_user.role != UserRole.ADMIN:
    raise HTTPException(status_code=403, detail="You do not own this student record")
```

## Step 4 — Fully typing the service layer

Every function in `services/students.py` gets complete hints, following Day 21's
patterns directly:
```python
from sqlalchemy.orm import Session
from models import Student

def get_all(
    db: Session,
    min_score: int | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 20,
) -> tuple[list[Student], int]:
    ...

def get_by_id(db: Session, student_id: int) -> Student | None:
    return db.get(Student, student_id)

def create(db: Session, name: str, score: int, created_by: int, course_id: int | None = None) -> Student:
    ...
```
**Notice `get_by_id` returning `Student | None`** — exactly Day 21's Section 4
pattern, and it's what makes the `if student is None:` check in every route not just
a habit, but something `mypy` will actually flag as missing if you ever forget it in
new code.

---

## Worked example: `response_model` + typed dependency, together

### Problem statement
Add `response_model=StudentOut` to `get_student`, and add a small typed dependency
`require_admin` that only lets admins through, reusing `get_current_user`.

### Solution
See [`exercises/schemas.py`](./exercises/schemas.py) and
[`exercises/security.py`](./exercises/security.py) — both fully solved and
commented.

```python
# security.py (continued)
from models import User, UserRole

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
```
```python
@router.delete("/{course_id}", status_code=204)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    ...
```
### What to notice
- `require_admin` **wraps** `get_current_user` — it depends on it via its own
  `Depends()`, meaning FastAPI resolves `get_current_user` first (checking the
  token), then runs `require_admin`'s own check on top. This is dependency chaining:
  small, typed, composable checks stacked together, rather than one large function
  doing everything.
- Any route using `Depends(require_admin)` instead of `Depends(get_current_user)`
  automatically gets *both* checks — logged in, *and* an admin — with zero repeated
  code.

---

## Your turn

1. Add `response_model` to every remaining route across `students.py`,
   `courses.py`, and `auth.py` — build the matching `*Out` schemas in
   `schemas.py` where they don't exist yet.
2. Convert `User.role` to the real `UserRole` Enum (Step 3), and update every
   comparison against `"admin"` to compare against `UserRole.ADMIN` instead.
3. Fully type every function in `services/students.py` (Step 4).
4. Run `mypy` across the whole project and resolve every error:
   ```bash
   mypy exercises/
   ```
5. Re-run your Week 5 pytest suite — confirm everything still passes. Typing
   shouldn't change behaviour; it should only catch mistakes and clarify intent.

---

## Common mistakes to watch for
- **Building a `response_model` that's missing a field the route actually needs to
  return** — FastAPI silently drops anything not listed in the schema; a missing
  field in a response isn't always an error, it might just mean the schema is
  incomplete. Double check against `/docs`'s example response after adding one.
- **Forgetting `from_attributes = True`** on any `*Out` schema built from a
  SQLAlchemy object — the same gap from Week 5, Day 19.
- **Comparing a `UserRole` Enum member to a raw string** (`current_user.role ==
  "admin"`) after switching to the real Enum — this technically still works, since
  `UserRole` inherits from `str`, but prefer comparing to `UserRole.ADMIN` explicitly
  so `mypy` can catch a typo'd string elsewhere in the codebase.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
