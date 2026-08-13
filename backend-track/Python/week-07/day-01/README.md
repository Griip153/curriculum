# Day 25 — Security Hardening

## Objective
Close the gaps that don't show up until an attacker (or just a heavy user) finds
them.

## Concepts
CORS and `CORSMiddleware`; rate limiting with `slowapi`; input sanitisation
recap; secrets management recap; a practical security checklist.

## Watch before the session
- "CORS Explained" — Fireship or Web Dev Simplified
- "Rate Limiting APIs" — any short backend-focused explainer
- OWASP API Security Top 10 — skim the list (owasp.org)

## Task of the day
Add `CORSMiddleware` configured for a real frontend origin, add rate limiting to the
login route with `slowapi`, and walk through a security checklist against the whole
project, fixing anything that fails it. Full step-by-step instructions are in
`LESSON.md`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
