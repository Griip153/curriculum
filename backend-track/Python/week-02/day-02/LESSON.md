# Day 6 — Teaching Lesson: Python In Depth — Packages, Modules & Raw HTTP

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered
> step builds on the one before it. Don't skip ahead.
>
> By the end you'll have built a real (if small) backend server by hand, with no
> framework — which is exactly why tomorrow's FastAPI lesson will feel like a relief
> instead of more new syntax.

## Objective
Understand the platform itself — `pip`, packages, modules — by building one thing
FastAPI normally does for you: a raw HTTP server.

## What you're building today
A small server that can:
- report that it's alive (`/health`)
- list students, look one up by id, and add a new one (`/students`)
- remember those students even after you restart the server (a JSON file on disk)
- report a bit about the computer it's running on (`/system-info`)

That's a lot of new ideas, so we go one small piece at a time.

---

## Step 1 — `pip`, packages, and `requirements.txt`

**Definition:** `pip` is Python's package manager — a tool that downloads other
people's code (a **package**) for you to use in your project. `requirements.txt` is
your project's shopping list: a plain text file listing every package your project
needs, so anyone (including future you) can reinstall the exact same setup.

Make sure your virtual environment from Day 5 is active (you should see `(venv)` in
your prompt — if not, run `source venv/bin/activate`). Then, whenever you install
something, save it to the list:
```bash
pip freeze > requirements.txt
```
And to reinstall everything on a fresh machine (or after cloning the repo):
```bash
pip install -r requirements.txt
```
Today's server needs **no third-party packages at all** — everything we're using
lives in Python's **standard library** (the tools that ship with Python itself). This
is deliberate: it's the clearest way to see exactly what a framework like FastAPI
adds on top.

**Checkpoint:** your venv is active, and you understand `requirements.txt` is a list,
not magic — it's just `pip install`, remembered.

---

## Step 2 — Modules and packages, properly

**Definition:** A module is just a `.py` file that can be imported into another file.
A **package** (the "importable folder" kind, not the pip kind — confusing, but both
words are standard) is a folder of modules with an `__init__.py` file inside it,
which lets you `import` the folder like a single unit.

You already did this informally on Day 4 (`from students import load_students`).
Today's project has a proper `data.py` module, imported into `server.py`:
```python
# data.py
def load_students():
    ...

# server.py
from data import load_students
```
No `__init__.py` needed yet — that only matters once you group multiple modules into
a sub-folder, which you'll do properly once we reach FastAPI project structure
(Day 8).

---

## Step 3 — The smallest possible raw HTTP server

**Definition:** `http.server` is a module in Python's standard library that lets you
build an HTTP server without installing anything. `BaseHTTPRequestHandler` is a class
you extend to define what happens for each incoming request.

```python
# server.py
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status": "ok"}')

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), Handler)
    print("Server running at http://localhost:8000")
    server.serve_forever()
```
**What each piece does:**
- `do_GET(self)` runs automatically for every incoming `GET` request, no matter the
  URL — right now, our server answers the same thing everywhere.
- `self.send_response(200)` sends the status code.
- `self.send_header(...)` / `self.end_headers()` sends headers, then signals headers
  are finished.
- `self.wfile.write(...)` writes the response body — note it needs **bytes**, not a
  plain string, hence the `b'...'` prefix.
- `if __name__ == "__main__":` means "only run this when the file is executed
  directly, not when it's imported by another file" — a Python convention you'll see
  in almost every script from now on.

Run it:
```bash
python3 server.py
```
Visit `http://localhost:8000` in a browser, or in a second terminal:
```bash
curl http://localhost:8000
```

**Checkpoint:** you see `{"status": "ok"}` printed back, no matter what URL path you
visit — that's expected, we haven't checked the path yet.

---

## Step 4 — Routing by hand: checking `self.path`

**Definition:** Routing is the process of matching an incoming request's method and
URL path to the correct piece of code to handle it. A framework does this for you
automatically — right now, you do it with plain `if`/`elif` on `self.path`.

```python
def do_GET(self):
    if self.path == "/health":
        self._send_json(200, {"status": "ok"})
    else:
        self._send_json(404, {"error": "Not found"})
```
Refactor the repeated "send JSON" logic from Step 3 into one helper method, so you're
not retyping `send_response`/`send_header`/`end_headers`/`wfile.write` every time:
```python
import json

def _send_json(self, status_code, data):
    body = json.dumps(data).encode("utf-8")
    self.send_response(status_code)
    self.send_header("Content-Type", "application/json")
    self.end_headers()
    self.wfile.write(body)
```
**Definition:** `json.dumps(data)` converts a Python dictionary into a JSON-formatted
string. `.encode("utf-8")` turns that string into bytes, which is what `wfile.write`
requires. You met `json.dumps`/`json.loads` briefly on Day 4 — today's the day you
see exactly why a server needs them on every single response.

**Checkpoint:** `/health` returns `{"status": "ok"}` with status `200`; any other path
returns `{"error": "Not found"}` with status `404`.

---

## Step 5 — Persisting students to a JSON file

**Definition:** Persisting data means saving it somewhere that survives the program
ending — here, a `.json` file on disk, read on startup and rewritten whenever it
changes. Without this, every restart would reset your students back to empty.

```python
# data.py
import json
import os

FILE_PATH = "students.json"

def load_students():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_students(students):
    with open(FILE_PATH, "w") as f:
        json.dump(students, f, indent=2)
```
This is the same pattern from Day 4's task — the only thing new here is that a
*server* is what's calling it, on every request that changes the data, instead of a
one-off script.

**Checkpoint:** run any script that calls `save_students([...])`, confirm
`students.json` appears in your folder with that data inside, formatted and
readable.

---

## Step 6 — `GET /students` and `POST /students`

Reading the request body for a `POST` needs one more piece — the raw HTTP server
doesn't parse it for you the way FastAPI will tomorrow:
```python
def do_GET(self):
    if self.path == "/health":
        self._send_json(200, {"status": "ok"})
    elif self.path == "/students":
        students = load_students()
        self._send_json(200, {"students": students})
    else:
        self._send_json(404, {"error": "Not found"})

def do_POST(self):
    if self.path == "/students":
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        new_student = json.loads(body)

        students = load_students()
        new_student["id"] = len(students) + 1
        students.append(new_student)
        save_students(students)

        self._send_json(201, new_student)
    else:
        self._send_json(404, {"error": "Not found"})
```
**Definition:** `Content-Length` is a header telling the server how many bytes of body
to expect. Without reading exactly that many bytes with `self.rfile.read(...)`, the
server wouldn't know where the request body ends. This is precisely the manual work a
framework's body-parser does for you automatically — worth seeing once, by hand.

**Checkpoint:**
```bash
curl -X POST http://localhost:8000/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Bruno", "score": 77}'

curl http://localhost:8000/students
```
The second command should show Bruno, with an `id` the server assigned.

---

## Step 7 — `GET /students/<id>`: routing with a dynamic path

Raw `http.server` has no built-in idea of "path parameters" — you split the string
yourself:
```python
elif self.path.startswith("/students/"):
    student_id = int(self.path.split("/")[-1])
    students = load_students()
    match = next((s for s in students if s["id"] == student_id), None)
    if match:
        self._send_json(200, match)
    else:
        self._send_json(404, {"error": "Student not found"})
```
**Definition:** `next((... for ... in ...), None)` walks a generator expression and
returns the first match, or `None` if nothing matched — the same idea as `.find()` in
some other languages, using tools you already know from Day 3's comprehensions.

Notice how much manual string-splitting and type-converting this takes compared to
Step 6's simpler routes — remember this feeling for tomorrow.

---

## Step 8 — `/system-info` with the `platform` module

**Definition:** `platform` is a standard-library module that reports information
about the machine Python is running on — operating system, Python version, processor
architecture.

```python
import platform

elif self.path == "/system-info":
    info = {
        "system": platform.system(),
        "python_version": platform.python_version(),
        "machine": platform.machine(),
    }
    self._send_json(200, info)
```

---

## Full solution

See [`exercises/server.py`](./exercises/server.py) and
[`exercises/data.py`](./exercises/data.py) for the complete, working, commented
version of everything above, wired together into one file.

Run it:
```bash
cd exercises
python3 server.py
```

### Common mistakes to watch for
- **Forgetting `.encode("utf-8")`** before `wfile.write()` — it needs bytes, a plain
  string raises a `TypeError`.
- **Not reading exactly `Content-Length` bytes** — reading too few leaves data
  unread and confuses the next request; there is no automatic body-parser here to
  save you, unlike tomorrow.
- **Forgetting `if __name__ == "__main__":`** — without it, importing this file from
  another script would immediately start a server as a side effect, which is almost
  never what you want.
- **`.gitignore` missing `venv/` and `students.json`** — neither belongs in Git: one
  is a local environment, the other is generated data that will differ per machine.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*