# Day 18 — Teaching Lesson: Protecting Routes & Ownership

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered
> step builds on the one before it.
>
> Yesterday you could log in and receive a token — but nothing in the API actually
> *checked* it. Today, every write to a student record requires being logged in, and
> only the student's owner (or an admin) can update or delete it.

## Objective
Actually enforce login — require a valid token, identify who's making the request,
and restrict writes to the record's owner.

## What you're building today
- A `created_by` column on `Student`, linking each record to the `User` who made it.
- `get_current_user` — a dependency that reads and verifies the token, and raises
  `401` if it's missing or invalid.
- Ownership and role checks on update/delete, raising `403` when a logged-in user
  tries to touch someone else's record.

---

## Step 1 — `401` vs. `403`: two different failures

**Definition:** `401 Unauthorized` means "I don't know who you are" — no valid
credentials were provided at all. `403 Forbidden` means "I know exactly who you are,
and you're not allowed to do this." Mixing these up is one of the most common REST
API mistakes — get the distinction right from today.

- No token at all, or an expired/invalid one → `401`.
- A valid token, but for a user who isn't the owner (and isn't an admin) → `403`.

## Step 2 — Reading the `Authorization` header with `OAuth2PasswordBearer`

**Definition:** `OAuth2PasswordBearer` is a FastAPI helper that knows how to extract a
bearer token from a request's `Authorization` header (`Authorization: Bearer
<token>`), and — critically — tells `/docs` to show an "Authorize" button so you can
test protected routes interactively, without hand-writing headers.

```python
# security.py (continued)
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
```
`tokenUrl` just tells `/docs` where to send a login request from its own "Authorize"
popup — it doesn't change how your `/auth/login` route itself works.

## Step 3 — Decoding the token and building `get_current_user`

```python
# security.py (continued)
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from database import get_db
from models import User

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_error = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_error
    except JWTError:
        raise credentials_error

    user = db.get(User, int(user_id))
    if user is None:
        raise credentials_error
    return user
```
**Reading each piece:**
- **`Depends(oauth2_scheme)`** — extracts the raw token string from the
  `Authorization` header. If it's missing entirely, FastAPI itself returns `401`
  before your function body even runs.
- **`jwt.decode(...)`** — verifies the signature (using the same `SECRET_KEY` that
  signed it in Step 6 of Day 17) and checks it hasn't expired. If either check fails,
  it raises `JWTError` — caught here and turned into a clean `401`.
- **`payload.get("sub")`** — recall from Day 17 that `sub` holds the user's id, as a
  string (JWT claims are commonly stored as strings — hence `int(user_id)` before the
  lookup).

**Using it in a route:**
```python
from fastapi import Depends
from security import get_current_user
from models import User

@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}
```
Any route that adds `current_user: User = Depends(get_current_user)` as a parameter
is now protected — no token, expired token, or tampered token, and the request never
reaches your function body at all.

## Step 4 — Linking students to their owner

```python
# models.py
from sqlalchemy import Column, ForeignKey, Integer, String

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
```
**Definition:** `ForeignKey("users.id")` is the SQLAlchemy version of Day 9's SQL
foreign key — it tells the database this column must reference a real row in
`users`. Set it automatically, from `current_user.id`, when a student is created —
never trust a client to supply it themselves.

```python
@router.post("/", status_code=201)
def create_student(
    student: StudentIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return students_service.create(db, student.name, student.score, current_user.id)
```

## Step 5 — Ownership checks: `403` when it's not yours

```python
@router.put("/{student_id}")
def update_student(
    student_id: int,
    student: StudentIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = students_service.get_by_id(db, student_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Student not found")

    if existing.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You do not own this student record")

    return students_service.update(db, student_id, student.name, student.score)
```
**Notice the order: check "does it exist?" (`404`) before "do you own it?"
(`403`).** Checking ownership first would leak information — a `403` on a
non-existent id would tell an attacker "this id exists, you just don't own it,"
which is more than they should learn.

## Step 6 — A simple role field for admin override

```python
# models.py
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")   # "user" or "admin"
```
```python
if existing.created_by != current_user.id and current_user.role != "admin":
    raise HTTPException(status_code=403, detail="You do not own this student record")
```
This is deliberately the simplest possible role system — one string column, checked
with a plain `if`. Real systems often grow more elaborate role/permission models, but
the underlying idea — "check some property of the current user before allowing the
action" — is exactly this, just with more properties to check.

---

## Worked example: protecting `create` end to end

### Problem statement
Add `created_by` to `Student`, wire `get_current_user` into `POST /students`, and
confirm creating a student without a token returns `401`, and with one returns `201`
with the correct `created_by`.

### Solution
See the fully solved [`exercises/models.py`](./exercises/models.py),
[`exercises/security.py`](./exercises/security.py), and
[`exercises/routers/students.py`](./exercises/routers/students.py) (the `create`
route only — update/delete are today's assignment).

Run it:
```bash
cd exercises
uvicorn main:app --reload
```
In `/docs`, click **Authorize** (top right), log in via `/auth/login` first to get a
token, paste it in, then try `POST /students/` — it should now require that
authorization to succeed.

### What to notice
- `Depends(get_current_user)` composes cleanly with `Depends(get_db)` — a route can
  depend on as many things as it needs; FastAPI resolves all of them before your
  function body runs.
- The client never sends `created_by` — it's derived entirely server-side from the
  verified token. This is a general security rule worth internalising early: **never
  trust the client to tell you who they are; only trust what you derived from a
  verified credential.**

---

## Your turn

1. Finish `update_student` and `delete_student` in
   `exercises/routers/students.py` (marked `# TODO`), following the ownership-check
   pattern from Step 5 (with the admin override from Step 6).
2. Add `role` to the `User` model and to `RegisterIn` (defaulting to `"user"` — don't
   let a client register themselves as `"admin"` directly; that's a manual database
   edit for now, or a separate admin-only endpoint if you want a stretch challenge).
3. Prove all of this in `/docs`:

| Scenario | Expected result |
|---|---|
| `POST /students/` with no Authorization header | `401` |
| `POST /students/` with a valid token | `201`, `created_by` set correctly |
| `PUT /students/{id}` as the owner | `200` |
| `PUT /students/{id}` as a different, non-admin user | `403` |
| `PUT /students/{id}` as an admin, not the owner | `200` (admin override) |
| `PUT /students/9999` (doesn't exist) as anyone | `404`, before any ownership check |

---

## Common mistakes to watch for
- **Checking ownership before existence** — always `404` first, as explained in
  Step 5.
- **Trusting a `created_by` or `role` sent in the request body** — both must come
  only from the verified token / an existing database row, never from client input.
- **Confusing `401` and `403`** — re-read Step 1's definitions any time you're
  unsure which applies.
- **Forgetting the `/docs` "Authorize" button needs a fresh token after it expires**
  (60 minutes, per Day 17's `ACCESS_TOKEN_EXPIRE_MINUTES`) — log in again if
  protected routes start failing unexpectedly during a long session.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
