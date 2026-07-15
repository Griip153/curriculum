# Day 24 — Authentication II — Protecting Routes & Ownership

## Objective
Decide who can do what — authentication is who you are, authorization is what you may do.

## Concepts
Auth middleware reading the Authorization header; protecting write routes; attaching req.user; ownership checks (only the creator can edit/delete); simple roles (admin vs user).

## Watch before the session
- Web Dev Simplified — JWT middleware videos
- Traversy Media — Node.js auth videos
- Dev Ed — Node authentication content

## Task of the day
Protect the students API: anyone reads, only logged-in users create, only the record’s creator (or an admin) can update/delete. Prove all three cases in Postman.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
