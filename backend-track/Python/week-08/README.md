# Week 8 — Project Week & Showcase (Final Project)

The capstone: one more complete CRUD API, built and shipped using everything from
the entire track — FastAPI, SQLAlchemy + Postgres, authentication and ownership,
full type hints, tested, secured, and deployed to the real internet.

**Ideas:** the same categories as Week 4, but push for more depth this time — a
njangi/tontine group ledger with member roles and contribution history, a clinic
appointment system with doctors/patients/appointments, a small marketplace with
sellers/products/orders, a church contributions and events API.

**Requirements — this is the full checklist from every week, in one project:**
- Postgres (Neon) database with **at least 3 related tables**, using
  `relationship()`/`back_populates` correctly (Week 5, Day 19).
- Full CRUD on at least two resources, with clean REST routes and a thin
  router/service split (Week 2, Days 7-8).
- Registration, login, JWT auth, and ownership + at least one role-based restriction
  (Week 5, Days 17-18).
- Real validation throughout: `Field()`/`@field_validator`, consistent error shapes
  (Week 3, Day 11).
- Pagination, sorting, and search on at least one list endpoint (Week 5, Day 20).
- Full type hints across your service layer, checked clean with `mypy` (Week 6, Days
  21-23).
- At least one `GROUP BY`/aggregation endpoint with a sensible index behind it (Week
  7, Day 3).
- CORS configured, and at least one rate-limited route (Week 7, Day 1).
- **At least 15 passing `pytest` tests**, including a real ownership pair (two
  distinct users, Week 7, Day 2) and at least one parametrized test.
- Deployed to Render (or equivalent) with production environment variables and
  customised `/docs` metadata (Week 7, Day 4).
- A complete `README.md`: what the API does, every endpoint documented, the live URL,
  and how to run it locally.
- All daily-report PRs merged.

## Day 29 — Project Kickoff & Planning
Choose the project, design your (at least 3) tables and every relationship between
them on paper, sketch the full endpoint list including auth and the aggregation
route, create the repo, and get the plan approved.

## Day 30 — Build Day 1
Models, migrations/`create_all`, Neon connection, and core CRUD on your two main
resources working end to end in `/docs`. Push your code.

## Day 31 — Build Day 2
Auth (register/login/JWT), ownership and role checks, and the relationships between
your tables wired and tested manually in `/docs`. Push your code.

## Day 32 — Polish & Ship
Finish validation, pagination/search, the aggregation endpoint, the pytest suite
(15+ passing), `mypy` clean, deploy to Render, finish the README, and present your
API live: a full CRUD + auth walkthrough in `/docs` against the deployed URL, then
`pytest -v` and `mypy` shown green.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
