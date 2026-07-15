# Day 24 — Testing Your API

## Objective
Prove the API works — automatically, every time, before anyone finds the bug for you.

## Concepts
DRF’s APITestCase / APIClient; testing auth-protected endpoints; testing permissions ("user B cannot delete user A’s record"); running tests in CI (concept).

## Watch before the session
- BugBytes — testing DRF videos
- Dennis Ivy — Django testing content
- DRF docs — testing page

## Task of the day
Write at least 10 API tests: happy paths, a 401 without a token, a 403 for the wrong owner, and a validation failure. All green.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
