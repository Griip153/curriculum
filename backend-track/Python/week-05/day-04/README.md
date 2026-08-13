# Day 20 — Filtering, Sorting, Pagination & Search

## Objective
Make a list endpoint behave the way a real API must at scale — never return
"everything" unconditionally.

## Concepts
Pagination (`skip`/`limit` or `page`/`page_size`); sorting by a chosen field and
direction; text search with SQL `LIKE`; combining several query parameters cleanly;
sensible defaults and upper bounds.

## Watch before the session
- "API Pagination Explained" — any short backend-focused explainer
- FastAPI official docs — "Query Parameters" (defaults, validation) page
- SQLAlchemy docs — `.offset()`/`.limit()`/`.order_by()`

## Task of the day
Upgrade `GET /students` to support `skip`, `limit` (capped at a sensible maximum),
`sort_by` + `order`, and a `search` term matched against student names — all
combinable in one request. Full step-by-step instructions are in `LESSON.md`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
