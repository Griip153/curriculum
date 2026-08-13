# Week 4 — Project Week & Showcase

Build a complete CRUD API of your own, using everything from Weeks 1-3: FastAPI
routes organised into routers, a service layer, SQLAlchemy models backed by a real
Postgres (Neon) database, Pydantic validation, consistent error handling, and a
pytest test suite.

**Ideas:** a church contributions API, a shop inventory API, a njangi group ledger, a
student results API, a small clinic appointments API.

**Requirements:**
- Postgres (Neon) database with **at least 2 related tables** (a foreign key between
  them — e.g. an inventory API with `products` and `categories`, or a ledger API with
  `members` and `contributions`).
- Full CRUD on the main resource (list, get one, create, update, delete).
- Validation and error handling matching Week 3's standard: `Field()`/
  `@field_validator` constraints, and the same consistent `{"error": "..."}` shape on
  every failure.
- **At least 8 passing `pytest` tests**, covering happy paths and failure paths, run
  against an isolated test database (Day 12's pattern).
- A Postman collection (or an equivalent `/docs`-based walkthrough) committed to the
  repo.
- A `README.md` documenting every endpoint: method, path, expected body, expected
  response, and status codes.
- All daily-report PRs merged.

## Day 13 — Project Kickoff & Planning
Choose the project, design your two (or more) tables and their relationship on
paper — which table holds the foreign key, and why — sketch every endpoint you'll
need, create the repo in the organisation, and get the plan approved.

## Day 14 — Build Day 1
Models, Neon connection, and core CRUD on the main resource working end to end in
`/docs` by the end of the day. Push your code.

## Day 15 — Build Day 2
Wire the second table and its relationship, add validation and error handling, and
write your first tests. Push your code.

## Day 16 — Polish, Test, and Showcase
Finish the pytest suite (8+ passing), write the endpoint documentation in your
README, export the Postman collection, and present your API live: walk through one
full CRUD flow in `/docs`, then run `pytest -v` on stream to show it green.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
