# Day 20 — Teaching Lesson: Filtering, Sorting, Pagination & Search

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered
> step builds on the one before it.
>
> `GET /students` has returned "everyone" since Day 7. That's fine with 5 students —
> it's a real problem with 50,000. Today you fix that permanently, and finish Week 5
> with a list endpoint that behaves the way any production API's does.

## Objective
Make a list endpoint behave the way a real API must at scale.

## What you're building today
`GET /students`, upgraded to support, all at once:
- **pagination** (`skip`/`limit`) — never return the whole table in one response
- **sorting** (`sort_by`, `order`) — by any reasonable field, ascending or descending
- **search** (`search`) — a partial, case-insensitive match on `name`

---

## Step 1 — Why "return everyone" doesn't scale

With 5 students, `db.query(Student).all()` is instant. With 500,000, it's a query
that returns an enormous response, uses a large amount of memory building it, and is
slow for both the database and the client parsing it — and almost never what a real
client actually wants. **Pagination** means the client asks for one *page* of results
at a time.

## Step 2 — `skip` and `limit` with SQLAlchemy

**Definition:** `.offset(n)` skips the first `n` matching rows; `.limit(n)` caps how
many rows come back. Together, `skip`/`limit` let a client request "give me rows 20
through 29" — the next "page" after the first 20.

```python
@router.get("/")
def list_students(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    query = db.query(Student)
    total = query.count()
    students = query.offset(skip).limit(limit).all()
    return {"total": total, "skip": skip, "limit": limit, "students": students}
```
**Notice `total` is computed with `.count()` on the query *before* `.offset()`/
`.limit()` are applied** — the client needs to know how many results exist *overall*
to build "page 3 of 12," not just how many came back in this one response.

**Always cap `limit`**, so a client can't request an unreasonably huge page and
defeat the whole point:
```python
limit: int = Field(20, le=100)   # via Query(), shown in Step 3
```

## Step 3 — Validating query parameters with `Query()`

**Definition:** `Query()` is `Field()`'s counterpart for query parameters
specifically — the same idea from Day 11, applied to `skip`/`limit` instead of a
request body.

```python
from fastapi import Query

@router.get("/")
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    ...
```
Now `GET /students?limit=99999` is automatically rejected with a `422`, the same
category of protection Day 11 gave request bodies — this time for the URL's query
string.

## Step 4 — Sorting: `sort_by` and `order`

**Definition:** Sorting by a *client-chosen* field needs care — you can't just
interpolate whatever string the client sends into SQL (recall Day 9's SQL injection
warning). Instead, map an allow-list of known field names to actual SQLAlchemy
columns.

```python
ALLOWED_SORT_FIELDS = {"name": Student.name, "score": Student.score, "id": Student.id}

@router.get("/")
def list_students(
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
):
    column = ALLOWED_SORT_FIELDS.get(sort_by, Student.id)
    query = db.query(Student)
    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())
    ...
```
**Why the allow-list matters:** an unrecognised `sort_by` value silently falls back
to sorting by `id`, rather than crashing or (far worse) being used to construct a raw
SQL fragment. This is the same principle as Day 9's `?` placeholders — never let
client input become part of the *structure* of your query; only ever let it become a
*value* you compare against, or here, a controlled lookup into a small trusted set.

## Step 5 — Search with `LIKE`

**Definition:** SQL's `LIKE` operator does pattern matching; `%` matches any sequence
of characters. `ILIKE` (Postgres-specific; SQLite's `LIKE` is already
case-insensitive by default) does the same thing, ignoring case.

```python
if search:
    query = query.filter(Student.name.ilike(f"%{search}%"))
```
**Notice this still goes through SQLAlchemy's `.ilike()` method with an f-string
building the *pattern*, not the *query structure*** — SQLAlchemy still parameterises
the actual value safely underneath; you are not hand-building a raw SQL string the
way Day 9 warned against. `%{search}%` matches "search" appearing anywhere in the
name — "ada" would match both "Ada" and "Nadia."

## Step 6 — Combining everything, in one clean function

The order operations get applied in matters: filter first (search, `min_score`),
*then* sort, *then* paginate. Sorting or paginating before filtering would give the
wrong results — you'd be sorting/paginating a set of rows that includes ones you
meant to exclude.

```python
@router.get("/")
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = "id",
    order: str = "asc",
    search: str | None = None,
    min_score: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Student)

    if search:
        query = query.filter(Student.name.ilike(f"%{search}%"))
    if min_score is not None:
        query = query.filter(Student.score >= min_score)

    total = query.count()

    column = ALLOWED_SORT_FIELDS.get(sort_by, Student.id)
    query = query.order_by(column.desc() if order == "desc" else column.asc())

    students = query.offset(skip).limit(limit).all()

    return {"total": total, "skip": skip, "limit": limit, "students": students}
```

---

## Worked example: the full route, solved

### Problem statement
Combine Steps 2-6 into the final `list_students` route.

### Solution
See [`exercises/routers/students.py`](./exercises/routers/students.py) — fully
solved and commented.

Run it:
```bash
cd exercises
uvicorn main:app --reload
```
Try a few combined requests directly:
```
GET /students/?limit=5
GET /students/?search=a&sort_by=score&order=desc
GET /students/?skip=5&limit=5&sort_by=name
```

### What to notice
- `total` is computed once, before pagination, so the client can compute how many
  pages exist (`total / limit`, rounded up) without a second request.
- Every added filter (`search`, `min_score`) is applied *before* `total` is counted —
  `total` reflects "how many results match your filters," not "how many rows exist in
  the whole table."
- This single route now safely handles arbitrary client input across five different
  query parameters, each validated or allow-listed appropriately — this is what a
  genuinely production-shaped list endpoint looks like.

---

## Your turn

1. Confirm the worked route above is running, and test all five query parameters
   together in one request.
2. Add one more allowed sort field of your choice (e.g. if your project has a
   `created_at` column) to `ALLOWED_SORT_FIELDS`.
3. Write two new tests in your pytest suite (building on Week 3, Day 12's patterns):
   - `test_list_students_pagination` — create 5 students, request `limit=2`, assert
     exactly 2 come back and `total` equals 5.
   - `test_list_students_search` — create students named "Ada" and "Kofi", search for
     `"ad"`, assert only Ada comes back.

This is the last day of Week 5 — before moving to Week 6, make sure every route
across the whole project (students, courses, auth) still passes its tests with
`pytest -v`.

---

## Common mistakes to watch for
- **Sorting by a raw client-supplied field name without an allow-list** — always map
  through a trusted dictionary, as in Step 4.
- **Computing `total` after `.offset()`/`.limit()` are applied** — this gives you
  "how many results are on this page" (always ≤ `limit`), not the actual total the
  client needs for pagination.
- **No upper bound on `limit`** — always cap it (`le=100` or similar); an unbounded
  `limit` defeats the entire purpose of pagination.
- **Case-sensitive search surprising users** — `.ilike()` (or SQLite's default
  case-insensitive `LIKE`) avoids "Ada" not matching a search for "ada."

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
