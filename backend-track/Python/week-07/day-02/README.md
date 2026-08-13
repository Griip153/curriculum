# Day 26 — Advanced Testing

## Objective
Level up your test suite: reusable fixtures, testing protected and forbidden routes
properly, and measuring how much of your code your tests actually exercise.

## Concepts
`pytest` fixtures beyond `autouse`; a reusable `authenticated_client` fixture;
testing `401`/`403`/`404` deliberately for every protected route; `pytest-cov` for
coverage reports; parametrized tests.

## Watch before the session
- "Pytest Fixtures Explained" — ArjanCodes or Tech With Tim
- "Test Coverage with pytest-cov" — any short explainer
- pytest official docs — "How to parametrize fixtures and test functions"

## Task of the day
Refactor your test suite's authentication setup into a shared, reusable fixture,
write a full matrix of `401`/`403`/`200` tests across every protected route, and run
`pytest-cov` to reach at least 80% coverage on your service layer. Full step-by-step
instructions are in `LESSON.md`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
