# Day 27 — Teaching Lesson: SQL Aggregation & Indexes

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered
> step builds on the one before it.
>
> Day 9 briefly used `COUNT(*)` on the whole table. Today formalises grouped
> aggregation — summarising *per group*, not just overall — and introduces indexes,
> the single most impactful tool for keeping queries fast as your tables grow.

## Objective
Answer "summary" questions efficiently, and understand why some queries are fast.

## 1. `GROUP BY` — summarising per group, not overall

**Definition:** `GROUP BY` collapses rows sharing the same value in a column into one
row per distinct value, letting aggregate functions (`COUNT`, `AVG`, `SUM`) compute
a result *for each group* rather than for the whole table at once.

```sql
SELECT course_id, COUNT(*) AS student_count
FROM students
GROUP BY course_id;
```
This returns one row per `course_id`, each with how many students belong to it — not
one number for the whole table (that would just be Day 9's plain `COUNT(*)`).

```sql
SELECT course_id, AVG(score) AS average_score
FROM students
GROUP BY course_id;
```
**The rule that catches everyone once:** in a query with `GROUP BY`, every column in
your `SELECT` list must either be in the `GROUP BY` clause itself, or wrapped in an
aggregate function. `SELECT name, course_id, COUNT(*) FROM students GROUP BY
course_id` is invalid — `name` isn't grouped and isn't aggregated, so SQL can't know
which student's name to show for a group containing several.

## 2. `HAVING` — filtering *after* grouping

**Definition:** `WHERE` filters individual rows *before* grouping happens; `HAVING`
filters *groups*, after aggregation, based on the aggregated value itself.

```sql
SELECT course_id, COUNT(*) AS student_count
FROM students
GROUP BY course_id
HAVING COUNT(*) >= 5;
```
This finds only courses with 5 or more students. You can't write `WHERE COUNT(*) >=
5` — `WHERE` runs before `COUNT(*)` has even been computed; `HAVING` is specifically
for filtering on the result of the aggregation.

## 3. Doing this in SQLAlchemy with `func`

```python
from sqlalchemy import func

results = (
    db.query(Student.course_id, func.count(Student.id).label("student_count"))
    .group_by(Student.course_id)
    .all()
)
# results is a list of (course_id, student_count) tuples
```
**Definition:** `func` is SQLAlchemy's namespace for SQL functions —
`func.count(...)`, `func.avg(...)`, `func.sum(...)` map directly onto their SQL
equivalents. `.label("student_count")` names the computed column, which is what
lets you refer to it clearly afterward instead of an unlabelled generic name.

Adding `HAVING`:
```python
from sqlalchemy import func

results = (
    db.query(Student.course_id, func.count(Student.id).label("student_count"))
    .group_by(Student.course_id)
    .having(func.count(Student.id) >= 5)
    .all()
)
```

**Joining the grouped result back to `Course` for the title**, using Day 19's
relationship knowledge:
```python
results = (
    db.query(
        Course.id,
        Course.title,
        func.count(Student.id).label("student_count"),
        func.avg(Student.score).label("average_score"),
    )
    .join(Student, Student.course_id == Course.id, isouter=True)
    .group_by(Course.id)
    .all()
)
```
**`isouter=True`** makes this a **LEFT JOIN** — a course with *zero* students still
appears in the results (with `student_count` of `0`), rather than disappearing
entirely, which a regular (**INNER**) join would do. Use `isouter=True` whenever you
want "every row from the left table, matched data from the right table if it exists."

## 4. Indexes — why some queries are fast

**Definition:** An index is a separate, sorted data structure the database
maintains alongside a table, letting it find matching rows without scanning every
single row — the same idea as a book's index letting you jump to a page instead of
reading cover to cover to find one topic.

You've actually been creating indexes since Day 10 without dwelling on it —
`Column(Integer, primary_key=True, index=True)` and `Column(String, unique=True, ...,
index=True)` both create one automatically. Today, add one deliberately, on a column
you filter by often but that isn't already a primary or unique key:
```python
# models.py
class Student(Base):
    __tablename__ = "students"
    ...
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True, index=True)
```
**Why `course_id` specifically:** you filter and join on it constantly (Day 19's
`course.students`, today's `GROUP BY course_id`) — exactly the kind of column that
benefits most from an index. **Don't index every column reflexively** — an index
speeds up *reads* on that column, but slightly slows down every *write* (the index
itself has to be updated too), and takes extra storage. Index columns you actually
filter, sort, or join on frequently; leave the rest alone.

## 5. `EXPLAIN` — seeing whether an index is actually used

**Definition:** `EXPLAIN` (prefixing any query) asks the database to show its
**query plan** — how it intends to execute the query — instead of running it.
This is how you *confirm* an index is actually helping, rather than just assuming it
is.

```sql
EXPLAIN SELECT * FROM students WHERE course_id = 1;
```
Look for the word **"scan"** in the output. A **full table scan** (SQLite:
`SCAN students`; Postgres: `Seq Scan`) means the database is checking every row —
no index is being used. An **index-based lookup** (SQLite: `SEARCH students USING
INDEX ...`; Postgres: `Index Scan using ...`) confirms the index is doing its job.

Run this both **before** and **after** adding the index in Step 4, and compare — this
before/after comparison is the actual point of today's exercise, not just adding the
index and assuming it worked.

---

## Worked example: `GET /courses/stats`

### Problem statement
Return every course with its student count and average score, using `GROUP BY` and a
left join so courses with zero students still appear.

### Solution
See [`exercises/routers/courses.py`](./exercises/routers/courses.py) — fully solved
and commented.

```python
from sqlalchemy import func

@router.get("/stats")
def course_stats(db: Session = Depends(get_db)):
    results = (
        db.query(
            Course.id,
            Course.title,
            func.count(Student.id).label("student_count"),
            func.avg(Student.score).label("average_score"),
        )
        .join(Student, Student.course_id == Course.id, isouter=True)
        .group_by(Course.id)
        .all()
    )
    return [
        {
            "id": r.id,
            "title": r.title,
            "student_count": r.student_count,
            "average_score": round(r.average_score, 1) if r.average_score is not None else None,
        }
        for r in results
    ]
```
Run it:
```bash
cd exercises
uvicorn main:app --reload
```

### What to notice
- `r.average_score` can be `None` — a course with zero students has no scores to
  average, and SQL's `AVG` of nothing is `NULL`, not `0`. The `if ... is not None
  else None` guard handles this correctly, distinct from actually being `0`.
- `.label(...)` names carry through to the result tuples' attribute names (`r.id`,
  `r.student_count`) — this is what makes the dictionary-building comprehension at
  the bottom readable.

---

## Your turn

1. Add `index=True` to `course_id` (Step 4).
2. Using DB Browser for SQLite (or Neon's SQL console for Postgres), run
   `EXPLAIN SELECT * FROM students WHERE course_id = 1;` **before** the index exists,
   note the plan, then create the table fresh with the index added and run it again.
   Confirm the plan changes from a scan to an index-based lookup.
3. Add a `HAVING` variant: `GET /courses/stats?min_students=5` — same query as the
   worked example, but only returning courses with at least `min_students` enrolled
   (Section 2-3's `.having(...)`).
4. Write one pytest test for `course_stats`: create a course, add 2 students to it
   with known scores, call the endpoint, and assert `student_count` and
   `average_score` match what you'd compute by hand.

---

## Common mistakes to watch for
- **Selecting a non-grouped, non-aggregated column** — SQL will reject the query
  outright (Section 1); if you hit this, check every column in your `SELECT` is
  either grouped or wrapped in an aggregate function.
- **Using `WHERE` where `HAVING` is needed**, or vice versa — `WHERE` filters rows
  before grouping; `HAVING` filters groups after.
- **Forgetting `isouter=True`** when you want to include groups with zero matches —
  a regular join silently drops them.
- **Indexing every column "just in case"** — re-read Step 4's caution; indexes have
  a real cost on writes, so add them deliberately, where you actually filter/sort/join.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
