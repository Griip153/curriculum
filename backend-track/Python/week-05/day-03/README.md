# Day 19 — SQLAlchemy Relationships — Joining Data Automatically

## Objective
Stop manually looking up related rows — let the ORM fetch them for you, and control
exactly how much comes back.

## Concepts
`relationship()` and `back_populates`; one-to-many in the ORM; eager vs. lazy
loading; nested Pydantic response shapes; a second related table (`Course`) to
practice on.

## Watch before the session
- SQLAlchemy official docs — "Relationship Configuration" (basic one-to-many section)
- "SQLAlchemy Relationships Explained" — ArjanCodes or similar
- FastAPI official docs — "SQL Databases" tutorial, relationships section

## Task of the day
Add a `Course` model, make each `Student` belong to one `Course` (one-to-many), wire
`relationship()`/`back_populates` on both models, and build a
`GET /courses/{id}/students` route that returns a course with its enrolled students
nested inside, using nested Pydantic response shapes. Full step-by-step instructions
are in `LESSON.md`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
