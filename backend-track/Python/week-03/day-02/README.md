# Day 10 — SQLAlchemy — FastAPI Meets a Real Database

## Objective
Connect the API to real storage — data that survives restarts and scales past a
single Python list.

## Concepts
Getting a free cloud Postgres database (Neon); SQLAlchemy engine, session, and
declarative models; `Depends()` for a per-request database session; rewriting the
students service layer to use the ORM instead of a Python list.

## Watch before the session
- "SQLAlchemy 2.0 Tutorial" — Tech With Tim or ArjanCodes
- FastAPI official docs — "SQL (Relational) Databases" tutorial
- Neon docs — "Connect from any Postgres client" quickstart

## Task of the day
Create a free Neon Postgres database, connect FastAPI to it with SQLAlchemy, define a
`Student` model, and rewrite every controller function from Day 8 to read and write
real database rows instead of the in-memory list. Full step-by-step instructions are
in `LESSON.md`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
