# Day 7 — Teaching Lesson: FastAPI I — Path Operations & Middleware

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered
> step builds on the one before it. Don't skip ahead: Step 6 assumes Step 5 already
> works.
>
> Yesterday you built a raw HTTP server by hand: manual routing with `if`/`elif`,
> manual JSON headers, manual body-parsing. Today you rebuild the *same idea* — a
> students API — with FastAPI, and feel directly how much of that FastAPI does for
> you. Keep yesterday's `server.py` open in another tab if you want to compare.

## Objective
Meet the framework — and middleware, the idea everything else in FastAPI is built on.

## What you're building today
The students API from yesterday, properly this time:
- full CRUD — list (with optional filtering), get one, create, update, delete
- a custom middleware that logs every request
- validation of incoming data, for free, from Pydantic
- the students routes organised into their own file with `APIRouter`

---

## Step 1 — Installing and starting FastAPI

**Definition:** FastAPI is a framework — a library that sits on top of Python's async
tools and handles routing, validation, and JSON conversion for you, so you write far
less boilerplate per route than you did yesterday. `uvicorn` is the **server** that
actually runs a FastAPI application — FastAPI describes *what* to do with a request;
`uvicorn` is the program that listens on a port and hands requests to it.

```bash
cd exercises
pip install fastapi uvicorn
pip freeze > requirements.txt
```

The smallest possible FastAPI app:
```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}
```
Run it with `uvicorn`, not `python3 main.py`:
```bash
uvicorn main:app --reload
```
**Definition:** `main:app` means "in the file `main.py`, use the object called
`app`." `--reload` tells uvicorn to restart the server automatically whenever you
save a file — yesterday's manual "stop and restart" habit, done for you from here on.

**Checkpoint:** visit `http://localhost:8000/health` — you should see
`{"status":"ok"}`. Then visit `http://localhost:8000/docs` — FastAPI generates a
full, interactive API explorer automatically, from your code. Nothing like this
existed yesterday; you get it for free from this point forward.

---

## Step 2 — Comparing yesterday's route to today's

```python
# Yesterday — raw http.server
if self.path == "/health":
    self._send_json(200, {"status": "ok"})
```
```python
# Today — FastAPI
@app.get("/health")
def health_check():
    return {"status": "ok"}
```
**Definition:** `@app.get("/health")` is a **decorator** — a line starting with `@`
that wraps the function below it with extra behaviour. Here, it registers
`health_check` to run whenever a `GET` request hits `/health`. FastAPI handles the
method check, JSON conversion (`json.dumps` equivalent), headers, and status code (a
default `200`) — all the things you wrote by hand yesterday, from one `return`
statement.

There's a matching decorator for every HTTP verb: `@app.get`, `@app.post`,
`@app.put`, `@app.delete`. You'll use all four today.

---

## Step 3 — Path parameters: one student by id

**Definition:** A path parameter is a placeholder in the URL path itself, written in
curly braces. FastAPI extracts it into a function argument for you — and, if you add
a **type hint**, converts and validates it automatically.

```python
@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {"id": student_id}
```
Compare this to yesterday, where you had to `self.path.split("/")` and manually
`int(...)` the result, catching the error yourself. Here, `student_id: int` tells
FastAPI: "this must be a whole number." Visit `/students/abc` and FastAPI
automatically responds `422 Unprocessable Entity` with a clear error message — you
wrote **zero** validation code for that.

This is your first real look at Python **type hints** (you'll go much deeper on them
in Week 6) — FastAPI reads them and uses them to validate, convert, and document your
API automatically.

---

## Step 4 — Query parameters: filtering a list

**Definition:** A query parameter is the `?key=value` part of a URL, used for
optional extras like filters or sorting — not part of the route path itself. In
FastAPI, any function parameter that *isn't* named in the path is automatically
treated as a query parameter.

```python
# GET /students?min_score=80
@app.get("/students")
def list_students(min_score: int | None = None):
    ...
```
**Definition:** `int | None = None` means "an integer, or nothing at all, defaulting
to nothing" — this makes the parameter **optional**. If the request doesn't include
`?min_score=`, FastAPI passes `None`; if it does, FastAPI has already converted it to
an `int` for you.

You'll use this in the big assignment below to let `GET /students?min_score=80`
return only students scoring 80 or above.

---

## Step 5 — Request bodies with Pydantic models

**Definition:** Pydantic is the data-validation library FastAPI is built on top of. A
Pydantic **model** is a class that describes the exact shape a piece of data should
have — field names, types, and whether each is required — and Pydantic validates
incoming data against it automatically.

```python
from pydantic import BaseModel

class StudentIn(BaseModel):
    name: str
    score: int

@app.post("/students")
def create_student(student: StudentIn):
    return student
```
Send a `POST /students` request with a JSON body like `{"name": "Bruno", "score":
77}`, and FastAPI automatically: reads the raw body, parses it as JSON, checks it
against `StudentIn` (rejecting anything missing or the wrong type with a `422` and a
detailed error message), and hands you back a real Python object with `student.name`
and `student.score` already validated and type-correct.

Compare this to yesterday's manual `Content-Length` read, `json.loads`, and complete
lack of validation. This one class replaces all of it.

---

## Step 6 — Middleware: the idea everything else is built on

**Definition:** Middleware is a function that runs *between* the request arriving and
your route's handler responding — it can inspect or modify the request, and then must
call the next step to pass control forward. If it never does (and never returns a
response itself), the request hangs forever — the same failure shape as forgetting
`self.wfile.write()` yesterday, just one level up.

```python
import time
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)   # pass control to the next step
    duration = time.time() - start_time
    print(f"{request.method} {request.url.path} — {response.status_code} ({duration:.3f}s)")
    return response
```
- **`@app.middleware("http")`** registers middleware that runs on *every* HTTP
  request, in the order you register them — order matters, same as yesterday's
  manual "check this if, then that elif" order.
- **`call_next(request)`** is how you pass control forward to the next middleware, or
  to the route handler itself if there are no more. **You must `await` it and return
  its result** — skipping either breaks every route.

This one — logging every request — is solved for you in `main.py`, and is the worked
example below.

---

## Step 7 — Worked example: list, create, and wire it all together

This is the part solved live, in the session — the shape every remaining route in
today's assignment reuses.

### Problem statement
Build the skeleton of the students API: a logging middleware, `GET /health`, and a
students router (in its own file) with `GET /students` (list) and `POST /students`
(create) working end to end.

### Thinking it through
1. The middleware (Step 6) needs to be registered once, in `main.py`, so it runs on
   every request regardless of which router handles it.
2. "Organising routes" (today's last concept) means the students routes shouldn't all
   live directly on `app` in `main.py` — they belong in their own file, using
   `APIRouter`, which behaves like a mini version of `app` but only for paths under
   one prefix.
3. A router file creates a `router = APIRouter()` object; `main.py` imports it and
   mounts it with `app.include_router(students_router, prefix="/students")` — from
   that point on, a route written inside the router as `@router.get("/")` really
   means `GET /students`, because FastAPI prepends the mount prefix automatically.
4. `POST /students` needs a Pydantic body (Step 5) — a new student gets an `id`
   assigned by the server, never trusted from the client, then gets appended to the
   in-memory list and returned with status `201` (the correct code for "a new
   resource was created," not the default `200`).

### Solution
See [`exercises/main.py`](./exercises/main.py) and
[`exercises/routers/students.py`](./exercises/routers/students.py) — both fully
solved and commented for the pieces below.

```python
# main.py
import time
from fastapi import FastAPI, Request
from routers import students

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    print(f"{request.method} {request.url.path} — {response.status_code} ({duration:.3f}s)")
    return response

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(students.router, prefix="/students", tags=["students"])
```
```python
# routers/students.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class StudentIn(BaseModel):
    name: str
    score: int

students_db = [
    {"id": 1, "name": "Ada", "score": 91},
    {"id": 2, "name": "Kofi", "score": 68},
    {"id": 3, "name": "Zara", "score": 84},
]
next_id = 4

@router.get("/")
def list_students():
    return {"students": students_db}

@router.post("/", status_code=201)
def create_student(student: StudentIn):
    global next_id
    new_student = {"id": next_id, "name": student.name, "score": student.score}
    students_db.append(new_student)
    next_id += 1
    return new_student
```

Run it:
```bash
cd exercises
uvicorn main:app --reload
```
Test with `curl`, or just use `/docs`:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/students
curl -X POST http://localhost:8000/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Bruno","score":77}'
```

### What to notice
- `students_db` and `next_id` live at the top of `routers/students.py`, outside any
  route — same reason `students`/`nextId` lived outside the handler in yesterday's
  raw server: state that needs to persist across requests has to live somewhere that
  isn't recreated on every function call. (This in-memory list still resets on
  restart — Week 3 fixes that permanently, with a real database.)
- `@router.post("/", status_code=201)` — the status code for a successful creation is
  set right in the decorator, rather than a separate method call.
- Nothing in `routers/students.py` mentions the path `/students` — that prefix comes
  entirely from how it's mounted in `main.py`
  (`app.include_router(students.router, prefix="/students")`). This is what makes the
  router reusable: you could mount the same router at a different prefix without
  touching a line inside it.

### Common mistakes to watch for (today's whole session)
- **Forgetting to `await call_next(request)` or forgetting to `return response`** in
  a middleware — either one breaks every route in the app.
- **Not adding type hints to path/query parameters** — without `student_id: int`,
  FastAPI treats it as a plain string and you lose the automatic validation.
- **Confusing a Pydantic model's *class* with an *instance*** — `StudentIn` is the
  shape; `student` (the function parameter) is one real validated object matching
  that shape.
- **Global mutable state without `global`** — reassigning `next_id` inside a function
  without the `global next_id` line raises an `UnboundLocalError`. (Note: `.append()`
  on `students_db` doesn't need `global` — you're modifying the list's contents, not
  reassigning the variable itself. Only reassignment needs `global`.)

---

## Your turn — the big assignment

Extend `exercises/routers/students.py` one step at a time, in order.

### Step 1 — filter the list: `GET /students?min_score=`
In the existing `list_students` handler, add a `min_score: int | None = None`
parameter (Step 4). If it's given, only include students whose `score` is greater
than or equal to it.
**Test:** `/students` → all 3. `/students?min_score=80` → only Ada and Zara.

### Step 2 — `GET /students/{student_id}`: one student
Use a path parameter (Step 3) to find the matching student. Found → `200` with that
student. Not found → raise `HTTPException(status_code=404, detail="Student not
found")` — FastAPI's built-in way to return an error response, which you'll import
with `from fastapi import HTTPException`.
**Test:** `/students/2` → Kofi. `/students/99` → the 404.

### Step 3 — `PUT /students/{student_id}`: update
Find the student the same way as Step 2. Not found → same 404. Found → overwrite its
`name` and `score` from the request body (a `StudentIn`, same as create), then
respond with the updated student.
**Test:** in `/docs`, try the PUT route with a body like `{"name": "Kofi", "score":
75}` against id `2`. Then `GET /students/2` again to confirm the change stuck.

### Step 4 — `DELETE /students/{student_id}`: remove
Find the student's *position* in the list (a plain loop with `enumerate`, or a
comprehension that finds the index) so you can remove it. Not found → `404`. Found →
remove it and respond with **status `204` and no body at all** — set
`status_code=204` in the decorator and `return None`(or nothing) from the function.
`204 No Content` is the correct status for "it worked, and there's nothing to send
back."
**Test:** `DELETE /students/3`, then `GET /students` — Zara should be gone.

### Step 5 — confirm validation is already working
This part needs no new code — Pydantic is already validating every `POST` and `PUT`
body against `StudentIn`. Prove it: in `/docs`, try `POST /students` with
`{"name": "", "score": "not a number"}` and confirm you get a `422` with a detailed
error message, and nothing gets added to the list.

### Step 6 — confirm the router organisation
This part is already wired up in the solved code — `routers/students.py` exports a
`router`, and `main.py` mounts it at `/students`. Re-read Step 7's "What to notice"
above and confirm you understand *why* none of your routes in `students.py` mention
the word `/students` anywhere in their path strings.

### Step 7 — test everything in `/docs`
Open `http://localhost:8000/docs` and try every route below directly in the browser —
no Postman needed today, though you're welcome to use it if you prefer. Confirm each
status code matches the table.

### Final checklist — every route should behave like this
| Route | Method | Expected result |
|---|---|---|
| `/health` | GET | `200` — `{"status": "ok"}` |
| `/students` | GET | `200` — `{"students": [...]}` |
| `/students?min_score=80` | GET | `200` — only students scoring 80+ |
| `/students/2` | GET | `200` — Kofi's record |
| `/students/99` | GET | `404` — `{"detail": "Student not found"}` |
| `/students` | POST (valid body) | `201` — the new student, with an `id` |
| `/students` | POST (bad body) | `422` — Pydantic's validation error |
| `/students/2` | PUT (valid body) | `200` — the updated student |
| `/students/2` | DELETE | `204` — no body |
| `/students/99` | DELETE | `404` — `{"detail": "Student not found"}` |

### Stretch goal (optional, only if you finish early)
Add a second query parameter, `sort: str | None = None`, so that
`/students?sort=score` returns the list sorted by score descending — combine it with
`min_score` so both can be used at once (`/students?min_score=70&sort=score`). Not
required — Day 8 formalises the whole "REST design" side of this, so don't
over-engineer it today.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*