# Day 27 — SQL Aggregation & Indexes

## Objective
Answer "summary" questions efficiently — counts, averages, grouped totals — and
understand why some queries are fast and others aren't.

## Concepts
`GROUP BY` and `HAVING`; SQLAlchemy's `func` (`count`, `avg`, `sum`); indexes and why
they matter; reading a query plan with `EXPLAIN`.

## Watch before the session
- "SQL GROUP BY and Aggregate Functions" — freeCodeCamp
- "Database Indexing Explained" — Hussein Nasser or similar
- SQLAlchemy docs — "Using SQL Functions" page

## Task of the day
Add `GET /courses/stats` returning each course's student count and average score
using `GROUP BY`, add an index to a frequently-filtered column, and use `EXPLAIN` to
confirm the index is actually used. Full step-by-step instructions are in
`LESSON.md`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
