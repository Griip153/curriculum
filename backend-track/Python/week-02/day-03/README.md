# Day 7 — FastAPI I — Path Operations & Middleware

## Objective
Meet the framework — and middleware, the idea everything else in FastAPI is built on.

## Concepts
FastAPI setup with `uvicorn`; path operations (GET/POST/PUT/DELETE); path parameters
and query parameters; request bodies with Pydantic models; middleware; automatic
interactive docs; organising routes with `APIRouter`.

## Watch before the session
- "FastAPI Course for Beginners" — freeCodeCamp (first hour)
- "FastAPI Crash Course" — Tech With Tim
- FastAPI official docs — "First Steps" and "Path Parameters" pages

## Task of the day
Rebuild yesterday's raw-Python students server as a proper FastAPI app: full CRUD
(list with optional filtering, get one, create, update, delete) on an in-memory list,
a custom logging middleware, request validation via Pydantic, and the students routes
organised into their own `APIRouter`. Test every route in the automatic `/docs` page,
with correct status codes. Full step-by-step instructions are in `LESSON.md`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*