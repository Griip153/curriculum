# Day 4 — Modern Python — Comprehensions, Modules, Files & JSON

## Objective
Learn the syntax and standard-library tools every real Python backend project
assumes you already know.

## Concepts
f-strings; list/dict comprehensions (deeper practice); tuple unpacking; modules and
`import`; the `json` module (`json.dumps` / `json.loads`); reading and writing files
with `open()`.

## Watch before the session
- Corey Schafer — "String Formatting" and "Modules and Packages" videos
- Programming with Mosh — comprehensions and file handling sections
- "Working with JSON in Python" — Tech With Tim

## Task of the day
Upgrade yesterday's student-records program: split it into a separate module
(`students.py`) that your main script imports, and save/load the students list
to/from a JSON file on disk so the data survives between runs.

**A concrete starting point**, if you'd like one:
```python
# students.py
import json

FILE_PATH = "students.json"

def load_students():
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_students(students):
    with open(FILE_PATH, "w") as f:
        json.dump(students, f, indent=2)
```
```python
# main.py
from students import load_students, save_students

students = load_students()
students.append({"name": "Bruno", "score": 77})
save_students(students)
print(students)
```
Run `python3 main.py` twice in a row — the second run should already include Bruno,
loaded back from `students.json`. That's the whole point of today: data that
survives a restart, using nothing but the standard library.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*