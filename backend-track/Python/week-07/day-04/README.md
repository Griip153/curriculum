# Day 28 — Deployment & API Documentation

## Objective
Ship it — get your API running on the real internet, and make its documentation
genuinely useful to someone who isn't you.

## Concepts
Deploying to Render (or Railway); environment variables in production; the
automatic `/docs` and `/redoc` pages; customising OpenAPI metadata (title,
description, tags); a production checklist.

## Watch before the session
- "Deploy FastAPI to Render" — Tech With Tim or the Render docs quickstart
- FastAPI official docs — "Metadata and Docs URLs" page
- "12 Factor App" — skim factors III (config) and X (dev/prod parity)

## Task of the day
Deploy the Week 4/5/6 project to Render with real environment variables (a
production `DATABASE_URL`, `JWT_SECRET_KEY`, and mail credentials), customise your
OpenAPI title/description/tags, and confirm `/docs` works against the live URL. Full
step-by-step instructions are in `LESSON.md`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
