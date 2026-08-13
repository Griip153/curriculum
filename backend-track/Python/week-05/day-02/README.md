# Day 18 — Authentication II — Protecting Routes & Ownership

## Objective
Actually enforce login — require a valid token, identify who's making the request,
and restrict writes to the record's owner.

## Concepts
`Depends(get_current_user)`; reading the `Authorization` header; `401` vs `403`;
ownership checks; a simple role field for admin-only routes.

## Watch before the session
- FastAPI official docs — "Get Current User" tutorial section
- "OAuth2 with FastAPI" — Tech With Tim
- "401 vs 403 — What's the Difference?" — any short explainer video

## Task of the day
Add a `created_by` column to `Student`, a `get_current_user` dependency, protect
create/update/delete so only a logged-in user can call them, restrict update/delete
to the student's owner (or an admin), and prove `401`/`403`/`200` all fire correctly.
Full step-by-step instructions are in `LESSON.md`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
