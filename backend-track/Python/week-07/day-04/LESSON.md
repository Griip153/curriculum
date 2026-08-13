# Day 28 — Teaching Lesson: Deployment & API Documentation

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered
> step builds on the one before it. This is also the last teaching day before
> Week 8's final project — everything here should go straight onto that project too.

## Objective
Ship it — get your API running on the real internet, with documentation that's
genuinely useful to someone who isn't you.

## What you're doing today
- Deploying your Week 4/5/6 project to **Render**, a free-tier-friendly host.
- Wiring real production environment variables — the same `.env` keys you've used
  locally all along, now supplied by Render instead of a local file.
- Customising the automatic docs so `/docs` reads like real API documentation, not
  just a list of routes.

---

## Step 1 — Preparing your project for deployment

A few things every deployed Python project needs, that local development quietly
didn't force you to think about:

**A `requirements.txt` that's actually complete and current:**
```bash
pip freeze > requirements.txt
```
Do this now, from your activated venv, and check the file — if you've been adding
packages across Weeks 5-7 (`passlib`, `python-jose`, `slowapi`, `fastapi-mail`,
`pytest-cov`...), confirm they're all genuinely listed.

**A way to tell the server what port to run on.** Render (like most hosts) assigns a
port dynamically via an environment variable, rather than always using `8000`:
```python
# For local dev you've been running: uvicorn main:app --reload
# Render will run something like: uvicorn main:app --host 0.0.0.0 --port $PORT
```
You don't need to change any of your own code for this — it's purely how you tell
Render to *start* your app, covered in Step 3.

## Step 2 — A production database

Your Neon Postgres database (Day 10) already *is* a real, cloud-hosted database — you
don't need a separate "production" one for this track. Just make sure the
`DATABASE_URL` you'll give Render (Step 4) points to it, and consider creating a
**second, separate** Neon database for continued local development from today
forward, so your deployed API's data and your local testing data don't mix.

## Step 3 — Deploying to Render

1. Push your project to GitHub if it isn't already (it should be, from Week 4's
   kickoff).
2. Go to **render.com**, sign up, and click **New → Web Service**.
3. Connect your GitHub repo.
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Don't deploy yet — first, add your environment variables (Step 4).

**Reading the start command:** `--host 0.0.0.0` means "accept connections from
anywhere," not just `localhost` — required for a server the outside internet needs to
reach. `--port $PORT` reads the port Render assigns dynamically, mentioned in Step 1.

## Step 4 — Environment variables in production

In Render's dashboard, under your service's **Environment** tab, add every key
from your local `.env`:
```
DATABASE_URL=<your Neon connection string>
JWT_SECRET_KEY=<a fresh, different secret from your local one>
MAIL_USERNAME=<your Mailtrap or real provider username>
MAIL_PASSWORD=<...>
MAIL_FROM=<...>
MAIL_PORT=<...>
MAIL_SERVER=<...>
DEBUG=False
```
**Generate a fresh `JWT_SECRET_KEY` for production — never reuse your local dev
one.** This is the exact same principle from Day 17 applied across environments: a
leaked local secret shouldn't be able to forge tokens against your real, deployed
API.

**`DEBUG=False` in production, always.** Recall from Day 8 that `debug=settings.debug`
is passed to `FastAPI(...)` — FastAPI's debug mode can expose detailed internal
error information (stack traces) directly in responses, which is useful while
developing locally and a real information leak in production.

Now click **Deploy**. Render builds and starts your app; watch the logs for errors —
a missing environment variable or a typo'd `DATABASE_URL` are the most common first
deploy failures, and Render's logs will show you exactly which import or connection
failed.

**Checkpoint:** visit `https://your-app-name.onrender.com/health` — you should see
your `{"status": "ok", ...}` response, now served from the real internet.

## Step 5 — Customising the automatic docs

You've used `/docs` (Swagger UI) since Day 7 without customising it. Today, make it
read like real documentation:
```python
app = FastAPI(
    title="Students API",
    description="A backend for managing students, courses, and enrolments, "
                 "built as part of the Backend Track.",
    version="1.0.0",
    debug=settings.debug,
)
```
Add descriptions to your routers, so `/docs` groups routes clearly:
```python
app.include_router(
    students.router,
    prefix="/students",
    tags=["Students"],
)
app.include_router(
    courses.router,
    prefix="/courses",
    tags=["Courses"],
)
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)
```
And add a one-line description to individual routes where it's not obvious from the
path alone:
```python
@router.get("/stats", summary="Get enrolment statistics per course")
def course_stats(...):
    ...
```
FastAPI also gives you `/redoc` for free — a different, often more readable
documentation layout generated from the exact same code, no extra work required.
Visit both `/docs` and `/redoc` on your deployed URL and compare.

## Step 6 — A production checklist

| # | Check |
|---|---|
| 1 | `requirements.txt` is complete and current |
| 2 | `DEBUG=False` in production's environment variables |
| 3 | A fresh, different `JWT_SECRET_KEY` for production |
| 4 | `DATABASE_URL` points to your real Neon database |
| 5 | `.env` itself was never committed — only `.env.example` |
| 6 | `/health` responds correctly on the live URL |
| 7 | `/docs` has a real title, description, and tagged routers |
| 8 | CORS `allow_origins` includes your real frontend's domain (once you have one) |

---

## Worked example: the customised app metadata

### Problem statement
Apply Step 5's title/description/tags to the full Week 7 project.

### Solution
See [`exercises/main.py`](./exercises/main.py) — fully solved and commented, with
every router tagged clearly.

Run it locally first to confirm the docs render as expected before deploying:
```bash
cd exercises
uvicorn main:app --reload
```
Visit `/docs` and `/redoc` and compare how the same metadata renders differently in
each.

### What to notice
- None of this changes any route's *behaviour* — it's purely about how the automatic
  documentation presents what already exists, which is exactly why it's safe to do
  as a final pass, after everything else works.

---

## Your turn

1. Complete Step 5's customisation on your actual Week 4/5/6 project.
2. Deploy that project to Render, following Steps 1-4.
3. Confirm every item in Step 6's checklist, against the **live, deployed URL** — not
   just locally.
4. Update your project's `README.md` (started back on Week 4, Day 16) with the live
   URL and a link to `/docs`, so anyone can explore your API without running it
   locally at all.

---

## Common mistakes to watch for
- **An incomplete `requirements.txt`** — the #1 cause of a first deploy failing;
  regenerate it with `pip freeze` right before deploying, from the same venv you've
  actually been developing in.
- **Reusing your local `JWT_SECRET_KEY` in production** — always generate a fresh
  one.
- **Leaving `DEBUG=True` in production** — re-read Step 4's explanation of why this
  matters.
- **Forgetting the deployed app needs its *own* environment variables set** —
  Render doesn't read your local `.env` file at all; every value has to be entered
  in its dashboard directly.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
