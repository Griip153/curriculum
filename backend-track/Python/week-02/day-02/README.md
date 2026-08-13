# Day 6 — Python In Depth: Packages, Modules & Raw HTTP

## Objective
Understand the platform itself — `pip`, packages, modules — and build a raw HTTP
server once by hand, so you feel exactly what FastAPI saves you starting tomorrow.

## Concepts
`pip` and `requirements.txt`; the standard library vs third-party packages; modules
and packages (`__init__.py`); the built-in `http.server` module; the `os` and
`platform` modules; building a raw JSON API with no framework at all.

## Watch before the session
- "Python Modules and Packages" — Corey Schafer
- "Build a Web Server From Scratch in Python" — Tech With Tim (or similar)
- Real Python — "Python's `http.server`" article

## Task of the day
Build a raw HTTP server (no framework) with several JSON routes: a health check, a
list-all-students route, a get-one-student-by-id route, and a create-student route —
with the student list saved to a JSON file on disk so it survives a restart. Add one
more route that reports info about your machine using the `platform` module. Push
with a proper `.gitignore` (`venv/` and the generated data file!). Full step-by-step
instructions are in `LESSON.md`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*