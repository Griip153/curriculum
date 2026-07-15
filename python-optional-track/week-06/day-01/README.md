# Day 21 — Authentication & Permissions (heavy day)

## Objective
Protect your API — who can read, who can write, and how users prove who they are.

## Concepts
Django users; token authentication and JWT (SimpleJWT); registration and login endpoints; permission classes; object-level permissions (only the owner can edit).

## Watch before the session
- Dennis Ivy — DRF authentication videos
- BugBytes — SimpleJWT videos
- DRF docs — authentication & permissions pages

## Task of the day
Add JWT auth: register, login, refresh. Anyone can read; only authenticated users create; only the record’s owner can update or delete.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
