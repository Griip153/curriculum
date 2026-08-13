# Day 25 — Teaching Lesson: Security Hardening

> Companion to `README.md`. This is a **step-by-step walkthrough**, and also a
> checkpoint on everything since Day 9 — several of today's "checks" just confirm
> earlier lessons stuck, rather than teaching something entirely new.

## Objective
Close the gaps that don't show up until an attacker (or a heavy user) finds them.

## 1. CORS — why a browser blocks your own API by default

**Definition:** CORS (Cross-Origin Resource Sharing) is a **browser** security rule
that blocks a web page running on one origin (domain + port) from calling an API on a
*different* origin, unless that API explicitly says it's allowed. It only applies to
requests made *from a browser* — tools like `curl` or Postman are never affected by
it, which is why your API has worked fine in `/docs` and `curl` all along despite
never configuring this.

If you build a frontend later (React, running on `http://localhost:3000`) that calls
your API (`http://localhost:8000`), the browser will block it by default — those are
different origins. `CORSMiddleware` is how you explicitly allow it:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
**Never use `allow_origins=["*"]` alongside `allow_credentials=True`** — browsers
actively reject that combination, and even where they didn't, it would mean "any
website on the internet can make authenticated requests to my API on a logged-in
user's behalf," which defeats the entire purpose of the restriction. List your real
frontend origins explicitly, including your eventual production domain once you
deploy (Day 4 this week).

## 2. Rate limiting — protecting against abuse and brute force

**Definition:** Rate limiting caps how many requests a single client (usually
identified by IP address) can make in a given time window, protecting your API from
being overwhelmed and, specifically for `/auth/login`, from an attacker trying
thousands of passwords per second against one account (a **brute-force attack**).

```bash
pip install slowapi
```
```python
# main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```
```python
# routers/auth.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, payload: LoginIn, db: Session = Depends(get_db)):
    ...
```
**Reading each piece:**
- **`get_remote_address`** — identifies a client by IP address; this is
  `slowapi`'s default and is fine for this track's purposes.
- **`@limiter.limit("5/minute")`** — a decorator, applied *below* the route
  decorator, capping this specific route to 5 requests per minute per client. Exceed
  it, and `slowapi` automatically responds `429 Too Many Requests` — you write zero
  code for that response yourself.
- **The route now needs `request: Request` as a parameter** — `slowapi` reads the
  client's address from it, so it must be present even though your function body
  doesn't otherwise use it directly.

**Why `/auth/login` specifically, today:** it's the single most valuable place to
start — it's the route most attractive to brute-force, and unlike most of your other
routes, it's reachable by someone with *zero* prior access (no token needed to even
attempt it).

## 3. Recap: input sanitisation — where you've already handled this

Nothing new to write here — this is a deliberate checkpoint. Confirm, by re-reading
your own code, that:
- Every SQL you've written goes through SQLAlchemy's query builder or `?`
  placeholders (Day 9-10) — never raw string interpolation of client input into SQL.
- Every request body is validated through a Pydantic model with real constraints
  (Day 11) — never read directly off a raw, unchecked dict.
- File uploads are validated by content type and size, and saved under
  server-generated filenames, never client-supplied ones (Day 24).

If any of these have quietly drifted since they were introduced — go fix it before
moving on. This is exactly the kind of gap that's invisible until a real attacker (or
a fuzzing tool) finds it for you.

## 4. Recap: secrets management — where you've already handled this

Also a checkpoint, not new material. Confirm:
- `SECRET_KEY`, `DATABASE_URL`, and your Mailtrap credentials all live in `.env`
  (Day 8, Day 10, Day 17, Day 24) — never hard-coded in a `.py` file.
- `.gitignore` includes `.env` in every project you've built — check this
  literally, right now, with `git status` after touching `.env`; it should show
  nothing changed.
- `.env.example` exists with placeholder values, so a teammate (or your future self,
  on a new machine) knows what's needed without ever seeing a real secret.

## 5. A practical security checklist

Walk through this against your Week 4/5/6 project, right now, one line at a time:

| # | Check | Where it was introduced |
|---|---|---|
| 1 | Passwords are hashed with bcrypt, never stored plain | Day 17 |
| 2 | JWTs are signed with a secret from `.env`, and expire | Day 17 |
| 3 | Every write route requires a valid token | Day 18 |
| 4 | Update/delete check ownership (or admin) before proceeding | Day 18 |
| 5 | Every request body has real validation constraints, not just types | Day 11 |
| 6 | All SQL goes through SQLAlchemy/parameterised queries | Day 9-10 |
| 7 | File uploads validate type, size, and use generated filenames | Day 24 |
| 8 | `.env` is gitignored in every project | today |
| 9 | CORS is configured with explicit origins, not `*` with credentials | today |
| 10 | `/auth/login` is rate-limited | today |

---

## Worked example: CORS + rate limiting, wired together

### Problem statement
Add `CORSMiddleware` (allowing `http://localhost:3000`, a placeholder future
frontend) and rate-limit `/auth/login` to 5 requests per minute.

### Solution
See [`exercises/main.py`](./exercises/main.py) and
[`exercises/routers/auth.py`](./exercises/routers/auth.py) — both fully solved and
commented.

Run it:
```bash
cd exercises
uvicorn main:app --reload
```
Test the rate limit directly — hit `POST /auth/login` 6 times quickly (a bad
password is fine, you're testing the limit, not a successful login) and confirm the
6th attempt returns `429`.

### What to notice
- CORS only ever matters to a browser — testing it with `curl` or `/docs` won't show
  you anything different; you'd need an actual browser-based frontend (or a tool
  that specifically simulates CORS preflight requests) to observe it directly. Trust
  the configuration and move on; you'll see it in action for real once you build a
  frontend.
- The rate limiter's `429` response is completely automatic — you never wrote an
  `except` block or an `if` check for "too many requests"; `slowapi`'s middleware
  handles the whole thing.

---

## Your turn

1. Confirm the worked example runs, and manually trigger the `429` on `/auth/login`
   as described above.
2. Add a second rate limit: `5/minute` on `POST /auth/register` too — same reasoning,
   a different endpoint attackers could otherwise hammer.
3. Walk through **the full checklist in Section 5** against your actual Week 4/5/6
   project (not just this lesson's exercise folder), line by line, and fix anything
   that fails. Write one sentence per failed item in your daily report describing
   what you changed.

---

## Common mistakes to watch for
- **`allow_origins=["*"]` with `allow_credentials=True`** — browsers reject this
  combination outright; list real origins.
- **Rate limiting by IP alone in an environment with shared IPs** (e.g. many users
  behind one corporate NAT) — a known, accepted limitation of IP-based rate limiting;
  worth being aware of, not something to solve today.
- **Treating today's checklist as a one-time task** — revisit it any time you add a
  new route, especially one that writes data or handles credentials.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
