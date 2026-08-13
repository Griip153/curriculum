# Day 10 — Teaching Lesson: SQLAlchemy — FastAPI Meets a Real Database

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered
> step builds on the one before it. Don't skip ahead: Step 5 assumes Step 4 already
> works.
>
> Yesterday you learned tables and queries by hand, against a local `library.db`
> file. Today the students API from Week 2 — currently a Python list that resets
> every time the server restarts — gets rewired to read and write real rows in a
> cloud Postgres database instead. Same routes, same JSON shapes your `/docs` page
> already expects — the storage underneath is what changes.

## Objective
Connect the API to real storage — data that survives restarts.

## What you're building today
- A free Postgres database on **Neon** (cloud-hosted, no local install).
- A SQLAlchemy **model** describing what a student row looks like.
- Every service function from Day 8 rewritten to use SQLAlchemy's session instead of
  a Python list — `session.query(...)` instead of list comprehensions, and so on.

---

## Step 1 — Get a free Postgres database on Neon

1. Go to **neon.tech** and sign up for a free account.
2. Create a new project — Neon creates a default database for you automatically.
3. On your project's dashboard, find the **connection string** — it looks like:
   ```
   postgresql://username:password@ep-xxxx.region.aws.neon.tech/dbname?sslmode=require
   ```
4. Copy it into your `.env` file (created on Day 8) as `DATABASE_URL`:
   ```
   DATABASE_URL=postgresql://username:password@ep-xxxx.region.aws.neon.tech/dbname?sslmode=require
   ```

**Checkpoint:** `.env` (never committed — check `.gitignore`) now has a
`DATABASE_URL` with your real Neon credentials in it.

> **Note:** if you'd rather practice locally first with zero network dependency, you
> can set `DATABASE_URL=sqlite:///./students.db` instead — everything in this lesson
> works identically against SQLite. Switch to your real Neon URL whenever you're
> ready; that's the entire point of keeping the URL in `.env` instead of hard-coded.

## Step 2 — Installing and connecting SQLAlchemy

**Definition:** SQLAlchemy is a library that lets you work with a relational database
using Python objects and method calls instead of writing raw SQL strings by hand —
this pattern is called an **ORM** (Object-Relational Mapper): it *maps* database rows
to Python objects, and back.

```bash
pip install sqlalchemy psycopg2-binary
pip freeze > requirements.txt
```
**Definition:** `psycopg2-binary` is the actual **driver** — the low-level library
that speaks Postgres's network protocol. SQLAlchemy sits on top of it and gives you a
much nicer API; you'll almost never touch `psycopg2` directly.

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```
**Reading each piece:**
- **`create_engine(url)`** — the engine manages the actual connection(s) to the
  database. You create it once, when your app starts.
- **`sessionmaker(...)`** — a factory that produces **sessions**. A session is a
  single "conversation" with the database — you'll open one per request (Step 4).
- **`declarative_base()`** — returns a base class. Every model you define (Step 3)
  inherits from it, which is how SQLAlchemy knows a given Python class corresponds to
  a database table.

Add `database_url: str` to your `Settings` class from Day 8, so it's read from
`.env` the same way `app_name` and `debug` already are.

**Checkpoint:** `database.py` imports without errors — this just sets up the
machinery, it doesn't actually connect yet.

## Step 3 — Defining a model

**Definition:** A SQLAlchemy model is a Python class where each **class attribute**
corresponds to a **column** in a database table. It's the ORM equivalent of
yesterday's `CREATE TABLE` statement — but written as Python, and reusable for
building queries, not just table creation.

```python
# models.py
from sqlalchemy import Column, Integer, String
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
```
Compare directly to yesterday's SQL:
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    score INTEGER NOT NULL
);
```
Same shape, same constraints (`nullable=False` is `NOT NULL`), described as a Python
class instead of a SQL string.

**Creating the table from your model**, once, at app startup:
```python
# main.py
from database import Base, engine
import models

Base.metadata.create_all(bind=engine)
```
This inspects every model that inherits from `Base` and creates the matching table if
it doesn't already exist — you never hand-write `CREATE TABLE` again from here on.

**Checkpoint:** run your app once, then check Neon's dashboard (or open `students.db`
in DB Browser if you're using SQLite) — a `students` table now exists, empty.

## Step 4 — A database session per request, with `Depends()`

**Definition:** `Depends()` is FastAPI's **dependency injection** system — a way to
say "before running this route, run this other function first, and give me its
result as a parameter." It's used constantly for exactly this pattern: opening a
resource before the route runs, and guaranteeing it's closed afterward.

```python
# database.py (continued)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
**Definition:** `yield` inside a function like this makes it a **generator** — the
code before `yield` runs first (open a session), the value after `yield` is handed to
whoever's using it (the route), and the code after `yield` (`db.close()`) runs
afterward, no matter what — even if the route raised an error. This guarantees every
request cleanly closes its own database session.

Using it in a route:
```python
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

@router.get("/")
def list_students(db: Session = Depends(get_db)):
    ...
```
FastAPI sees `Depends(get_db)`, runs `get_db()` for you, and hands you the session as
`db` — a fresh one, scoped to this one request, automatically cleaned up when the
request finishes.

## Step 5 — Querying with the session: the CRUD operations

**Definition:** A `Session` object is how you talk to the database through your
models — `.query()` to read, `.add()`/`.commit()` to write.

```python
# Read all
db.query(Student).all()

# Read one, by primary key — the fast, indexed lookup
db.query(Student).get(student_id)     # older SQLAlchemy style
db.get(Student, student_id)            # SQLAlchemy 2.0 style — prefer this

# Filter
db.query(Student).filter(Student.score >= 80).all()

# Create
new_student = Student(name="Bruno", score=77)
db.add(new_student)
db.commit()
db.refresh(new_student)   # reload it from the DB, so new_student.id is populated

# Update
student = db.get(Student, 2)
student.score = 75
db.commit()

# Delete
student = db.get(Student, 3)
db.delete(student)
db.commit()
```
**One rule that catches everyone once:** changes made through the session (`.add()`,
setting an attribute like `student.score = 75`, `.delete()`) don't actually reach the
database until you call **`db.commit()`**. Forgetting it is the SQLAlchemy version of
Day 9's "forgetting `conn.commit()`."

---

## Worked example: rewiring `get_all` and `create`

### Problem statement
Rewrite `services/students.py`'s `get_all` and `create` functions (from Day 8) to use
SQLAlchemy instead of a plain Python list.

### Thinking it through
1. Every service function now needs a `db: Session` — pass it in as a parameter,
   supplied by the router via `Depends(get_db)` (Step 4).
2. `get_all` becomes a `.query(Student)`, with `.filter(...)` only applied when
   `min_score` is given (Step 5).
3. `create` becomes building a `Student(...)` object, `db.add()`, `db.commit()`,
   `db.refresh()` (Step 5) — the validation (`if not name`) stays exactly as it was;
   only the storage mechanism changed.

### Solution
See [`exercises/services/students.py`](./exercises/services/students.py) and
[`exercises/models.py`](./exercises/models.py) for the complete, working version.

```python
# services/students.py
from sqlalchemy.orm import Session
from models import Student

def get_all(db: Session, min_score: int | None = None):
    query = db.query(Student)
    if min_score is not None:
        query = query.filter(Student.score >= min_score)
    return query.all()

def create(db: Session, name: str, score: int):
    if not name or not name.strip():
        raise ValueError("name must not be empty")
    new_student = Student(name=name, score=score)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student
```

Run it:
```bash
cd exercises
uvicorn main:app --reload
```
Test with `/docs` exactly like Day 7/8 — the routes and JSON shapes are unchanged;
only what happens underneath is different. Restart the server and confirm your
students are still there — that's today's whole win.

### What to notice
- The **router** doesn't change at all beyond adding `db: Session = Depends(get_db)`
  as a parameter and passing `db` through to the service call — this is exactly why
  Day 8's "thin router, real logic in services" split paid off today.
- `query.filter(...)` only runs when needed, and reassigns `query` — SQLAlchemy
  queries are **chainable**, building up the final SQL statement piece by piece,
  similar to yesterday's SQL clauses stacking together.
- `raise ValueError(...)` still works exactly as it did on Day 8 — your global
  exception handler in `main.py` catches it the same way, completely unaware the
  storage layer underneath changed.

---

## Your turn — finish the rewrite

Using the same approach as `get_all` and `create` above, rewrite the remaining three
service functions in `exercises/services/students.py`, each marked with a `# TODO`:

| Function | What changes |
|---|---|
| `get_by_id(db, student_id)` | `db.get(Student, student_id)` instead of the old comprehension |
| `update(db, student_id, name, score)` | look up with `db.get`, set attributes directly, `db.commit()` |
| `delete(db, student_id)` | look up with `db.get`, `db.delete(student)`, `db.commit()` |

Then update every route in `exercises/routers/students.py` (also marked with
`# TODO`) to accept `db: Session = Depends(get_db)` and pass it through to the
matching service call.

**Test everything** in `/docs`, exactly as you did on Day 7 — same checklist, same
expected status codes, just backed by Postgres now instead of a list.

---

## Common mistakes to watch for
- **Forgetting `db.commit()`** after a create/update/delete — the change happens in
  the session's memory but never reaches the database.
- **Forgetting `db.refresh(new_student)`** after creating a row — without it,
  `new_student.id` stays `None`, since the database (not your Python code) assigns
  the real id.
- **Opening a session manually instead of via `Depends(get_db)`** — you'd lose the
  automatic cleanup `yield`/`finally` gives you, and risk leaking open connections
  under load.
- **A `DATABASE_URL` typo or unreachable Neon project** — SQLAlchemy's error message
  when it can't connect can look intimidating; read the last line of the traceback
  first, it usually names the real problem (wrong password, wrong host, etc.).

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
