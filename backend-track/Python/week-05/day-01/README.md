# Day 17 — Authentication I — Passwords & JWTs

## Objective
Let users register and log in safely — never store a password in readable form.

## Concepts
Hashing vs. encryption; `passlib`/`bcrypt` for password hashing; what a JWT is and
what it isn't; issuing an access token on login; `python-jose` for encoding/decoding.

## Watch before the session
- "JWT Authentication Explained" — Web Dev Simplified or Fireship
- FastAPI official docs — "Security" section, "OAuth2 with Password" tutorial
- "How Password Hashing Works" — Computerphile

## Task of the day
Add a `User` model, a `POST /auth/register` route that hashes the password before
storing it, and a `POST /auth/login` route that verifies the password and returns a
signed JWT access token. Full step-by-step instructions are in `LESSON.md`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
