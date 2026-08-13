# Day 11 — Validation & Error Handling Done Right

## Objective
Make your API fail clearly and safely — the mark of professional work.

## Concepts
Pydantic field validators (`Field`, `@field_validator`); the difference between
request validation and database constraints; handling SQLAlchemy errors cleanly;
consistent error response shapes across every failure mode.

## Watch before the session
- FastAPI official docs — "Body — Fields" and "Handling Errors" pages
- Pydantic official docs — "Validators" page
- "Pydantic Validators Deep Dive" — ArjanCodes or similar

## Task of the day
Add real validation rules to `StudentIn` (name length, score range), and teach your
central error handler to recognise SQLAlchemy errors and respond with a clear `400`
instead of a generic `500`. Prove, in `/docs`, that five different kinds of bad
request each fail with the right status code and the same error shape. Full
step-by-step instructions are in `LESSON.md`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
