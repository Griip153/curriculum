# Day 19 — Teaching Lesson: SQLAlchemy Relationships

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered
> step builds on the one before it.
>
> Day 9 taught you `JOIN` by hand, in raw SQL. Today you teach SQLAlchemy to do that
> joining *for* you — accessing `course.students` or `student.course` directly as
> Python attributes, instead of writing a query every time you need related data.

## Objective
Stop manually looking up related rows — let the ORM fetch them for you.

## What you're building today
- A `Course` model.
- Each `Student` belongs to exactly one `Course` — a **one-to-many** relationship
  (one course, many students).
- `GET /courses/{id}/students` returning a course with its students nested inside,
  in one response.

---

## Step 1 — The `Course` model and the foreign key

```python
# models.py
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
```
Add the foreign key to `Student`, the same way `created_by` referenced `users.id`
yesterday:
```python
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
```
`nullable=True` here means a student *can* exist without a course assigned yet — a
deliberate, reasonable choice; make it `False` instead if your own project requires
every student to belong to a course from creation.

## Step 2 — `relationship()`: the Python-side link

**Definition:** `relationship()` doesn't create a database column — the foreign key
(Step 1) already did that. It tells SQLAlchemy, at the Python level, "these two
classes are related, and I want to access one from the other as a normal attribute,"
generating the necessary `JOIN` queries behind the scenes when you actually use it.

```python
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

    students = relationship("Student", back_populates="course")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)

    course = relationship("Course", back_populates="students")
```
**Definition:** `back_populates` links the two `relationship()` declarations
together, so setting one side automatically keeps the other side consistent *within
the same Python session* — assigning `student.course = some_course` also makes
`some_course.students` include that student, without a second database query.

**Reading the two directions:**
- `Course.students` — a **list**, since one course has many students (the "many"
  side).
- `Student.course` — a **single object** (or `None`), since one student has (at most)
  one course (the "one" side, from the student's perspective — confusingly named
  relative to the table names, but this is the standard pattern).

## Step 3 — Using it: no manual `JOIN` needed

```python
course = db.get(Course, 1)
for student in course.students:      # SQLAlchemy runs the JOIN for you
    print(student.name)

student = db.get(Student, 1)
print(student.course.title)           # the other direction, same idea
```
Compare this to Day 9's raw SQL:
```sql
SELECT * FROM students WHERE course_id = 1;
```
`course.students` produces (roughly) that exact query, automatically, the moment you
access it — this is the entire value relationships add: expressing a `JOIN` as a
Python attribute access instead of hand-writing SQL every time you need related data.

## Step 4 — Eager vs. lazy loading (a first look)

**Definition:** By default, SQLAlchemy relationships are **lazy** — the related data
isn't fetched until you actually access the attribute (`course.students`), which
means it runs as a *separate* query, after the first one. **Eager loading** fetches
related data upfront, in the same query (or an immediately-following one), which is
often more efficient when you already know you'll need it.

```python
from sqlalchemy.orm import joinedload

course = db.query(Course).options(joinedload(Course.students)).filter(Course.id == 1).first()
```
You don't need to master the performance tuning behind this choice today — just
recognise the term `joinedload` for when you profile a slow endpoint later and
discover it's making many small queries instead of one bigger one (a pattern often
called the "N+1 query problem").

## Step 5 — Nested Pydantic response shapes

**Definition:** A **response model** describes the shape of what a route sends back —
you'll formalize this properly on Week 6, Day 3, but today's task needs a first,
practical version: a Pydantic model that nests another Pydantic model inside it, to
match a nested relationship.

```python
from pydantic import BaseModel

class StudentOut(BaseModel):
    id: int
    name: str
    score: int

    class Config:
        from_attributes = True   # lets Pydantic read straight from a SQLAlchemy object

class CourseWithStudentsOut(BaseModel):
    id: int
    title: str
    students: list[StudentOut]

    class Config:
        from_attributes = True
```
**`from_attributes = True`** is the one new setting here — without it, Pydantic
expects a plain dictionary; with it, Pydantic can read attributes directly off a
SQLAlchemy model object (`course.title`, `course.students`), which is exactly what a
database query returns.

---

## Worked example: `GET /courses/{id}/students`

### Problem statement
Given the models and relationship from Steps 1-2, write a route that returns a course
and its enrolled students in one nested JSON response.

### Solution
See [`exercises/models.py`](./exercises/models.py) and
[`exercises/routers/courses.py`](./exercises/routers/courses.py) — both fully solved
and commented.

```python
# routers/courses.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Course
from schemas import CourseWithStudentsOut

router = APIRouter()

@router.get("/{course_id}/students", response_model=CourseWithStudentsOut)
def get_course_with_students(course_id: int, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
```
**Notice the route just `return course` — a raw SQLAlchemy object**, not a
dictionary. `response_model=CourseWithStudentsOut` tells FastAPI to run that object
through the Pydantic model on the way out, which is what makes `from_attributes =
True` necessary — it's Pydantic reading `course.id`, `course.title`, and
`course.students` (triggering the lazy-loaded relationship from Step 4) directly off
the SQLAlchemy object.

Run it:
```bash
cd exercises
uvicorn main:app --reload
```

### What to notice
- You never manually looped over students and built a list of dictionaries — the
  nested Pydantic shape (Step 5) plus `response_model` did that conversion
  automatically, including the nested `JOIN` from the relationship.
- `response_model` is also a **filter**: even if `Student` gained new columns later
  that aren't in `StudentOut`, they wouldn't leak into this response. You'll build on
  this idea directly on Week 6, Day 3.

---

## Your turn

1. Add a `POST /courses/` route to create a course (a plain `CourseIn` Pydantic
   model with just `title`, same pattern as `StudentIn`).
2. Add a `course_id: int | None = None` field to `StudentIn` and thread it through
   `services/students.py`'s `create` function, so a student can be assigned to a
   course when created.
3. Build a second nested response: add a `StudentWithCourseOut` schema
   (`id`, `name`, `score`, and a nested `course: CourseOut | None`), and use it as the
   `response_model` on `GET /students/{id}`, so fetching one student also shows which
   course they belong to (or `None` if unassigned).
4. Confirm in `/docs`: create a course, create a student assigned to it, then hit
   both `GET /courses/{id}/students` and `GET /students/{id}` and see the
   relationship reflected correctly in both directions.

---

## Common mistakes to watch for
- **Forgetting `back_populates` on one side** — the relationship still half-works,
  but the two directions can drift out of sync within the same session; always
  declare both sides together.
- **Forgetting `from_attributes = True`** — Pydantic raises a validation error trying
  to read a SQLAlchemy object as if it were a plain dictionary.
- **A course-less student breaking `StudentWithCourseOut`** — make sure the nested
  `course` field is typed `CourseOut | None`, matching `course_id`'s `nullable=True`
  from Step 1; forgetting the `| None` will make Pydantic reject any student with no
  course.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
