# Day 8 — REST Design & Project Structure

## Objective
Structure an API like a professional team — routers, a service layer, and errors
that make sense.

## Concepts
REST principles (resources, nouns, methods); routes vs. a service/CRUD layer; global
exception handlers; 404 handling; `pydantic-settings` and environment variables.

## Watch before the session
- "REST API Design Best Practices" — freeCodeCamp or ArjanCodes
- FastAPI official docs — "Handling Errors" and "Settings and Environment Variables"
  pages
- "What is REST API?" — Fireship (the concepts transfer directly from Node examples)

## Task of the day
Refactor the students API into `routers/` and `services/`, add a global exception
handler and a catch-all 404 handler, and move configuration into a `.env` file read
by `pydantic-settings`. Full step-by-step instructions are in `LESSON.md`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
