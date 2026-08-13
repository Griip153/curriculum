# Day 17 — Teaching Lesson: Authentication I — Passwords & JWTs

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered
> step builds on the one before it.
>
> From today on, the students API gets **users** — every student record will
> eventually belong to whoever created it (Day 19), and every write will require
> being logged in (Day 18). Today is just the two building blocks: registering with a
> safely-stored password, and logging in to get a token.

## Objective
Let users register and log in safely — never store a password in readable form.

## What you're building today
- A `User` model: `id`, `email`, `hashed_password`.
- `POST /auth/register` — create an account, storing a **hash** of the password, never
  the password itself.
- `POST /auth/login` — verify the password, and if correct, return a signed **JWT**.

---

## Step 1 — Hashing vs. encryption: a critical distinction

**Definition:** Encryption is reversible — with the right key, you can turn encrypted
data back into the original. Hashing is **one-way** — a hash function turns input
into a fixed-length scrambled output that **cannot** be reversed back into the
original input, even by the person who built the system.

**This is why you hash passwords, never encrypt them.** If your database were ever
stolen, an attacker with encrypted passwords and the right key gets every real
password back. An attacker with *hashed* passwords gets nothing directly usable —
they'd have to guess a password, hash their guess, and check if it matches, one at a
time (this is why weak passwords are still risky even when hashed — they're easier to
guess).

## Step 2 — Hashing with `passlib`

```bash
pip install passlib bcrypt
pip freeze > requirements.txt
```
**Definition:** `bcrypt` is a specific, deliberately slow hashing algorithm designed
for passwords — slow is a *feature* here, since it makes large-scale guessing attacks
much more expensive. `passlib` is a Python library that wraps algorithms like bcrypt
behind one simple API.

```python
# security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```
```python
>>> hash_password("mysecret123")
'$2b$12$EixZaYVK1fsbw1ZfbX3OXe...'   # different every time you run it!
```
**Notice hashing the same password twice gives a different result each time** — bcrypt
mixes in a random **salt** automatically, which is exactly why you can't compare
hashes directly with `==`; you always compare with `verify_password(plain, hashed)`,
which knows how to extract and reuse the salt from the stored hash.

## Step 3 — The `User` model

```python
# models.py (add alongside Student)
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
```
**Definition:** `unique=True` is a database **constraint** — the database itself
rejects a second row with a duplicate `email`, which is exactly the `IntegrityError`
your Day 11 handler already knows how to turn into a clean `400`.

## Step 4 — Registering: `POST /auth/register`

```python
# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from database import get_db
from models import User
from security import hash_password

router = APIRouter()

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

@router.post("/register", status_code=201)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "email": user.email}
```
**Definition:** `EmailStr` is a Pydantic type (from the `pydantic[email]` extra —
`pip install pydantic[email]`) that validates the string actually looks like an
email address, the same category of tool as `Field(ge=0, le=100)` from Day 11, just
for a different shape of data.

**Notice the response never includes `hashed_password`** — even hashed, there's no
reason to ever send it back over the network. You'll formalise "never leak this
field" properly with response models in Week 6.

## Step 5 — What a JWT actually is

**Definition:** A JWT (JSON Web Token) is a signed, self-contained piece of text that
proves "the server issued this, and it hasn't been tampered with," without the server
needing to look anything up in a database to check it. It is **not encrypted** — the
data inside it (typically called **claims**) is readable by anyone who has the token,
just base64-encoded, not hidden. Never put a password or other secret *inside* a
JWT's payload.

A JWT has three dot-separated parts: `header.payload.signature`. The **signature** is
what makes it trustworthy — it's produced using a secret key only the server knows,
and lets the server later verify "yes, I really issued this, and nobody edited it in
between" without storing anything about the token itself.

## Step 6 — Issuing a JWT with `python-jose`

```bash
pip install "python-jose[cryptography]"
```
```python
# security.py (continued)
from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = settings.jwt_secret_key   # from .env — never hard-code this
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```
**Reading each piece:**
- **`data`** — the claims you want inside the token; conventionally at least a `sub`
  ("subject" — who this token is about, usually the user's id or email).
- **`exp`** — an expiration timestamp. A JWT that never expires is a serious security
  liability — if it ever leaks, it's valid forever. `jose` automatically rejects an
  expired token when you try to decode it.
- **`SECRET_KEY`** — must be a long, random string, kept in `.env`, **never**
  committed to Git and **never** the same value across environments. Generate one
  with `python3 -c "import secrets; print(secrets.token_hex(32))"`.

## Step 7 — Logging in: `POST /auth/login`

```python
class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
```
**A deliberate security detail:** the error message is identical whether the email
doesn't exist *or* the password is wrong — `"Incorrect email or password"`, never
`"No account with that email"`. If it named the specific problem, an attacker could
use your login endpoint to discover which emails have accounts at all.

`token_type: "bearer"` tells the client how to use it: the token gets sent in an
`Authorization: Bearer <token>` header on every future request — you'll build the
part that reads that header tomorrow (Day 18).

---

## Worked example: register + login, end to end

### Problem statement
Wire `routers/auth.py` (register and login) into `main.py`, add `jwt_secret_key` to
`Settings`/`.env`, and confirm a full register → login → get-a-token flow works in
`/docs`.

### Solution
See [`exercises/routers/auth.py`](./exercises/routers/auth.py),
[`exercises/security.py`](./exercises/security.py), and the updated
[`exercises/models.py`](./exercises/models.py) — all fully solved and commented.

Run it:
```bash
cd exercises
uvicorn main:app --reload
```

### What to notice
- `register` and `login` are genuinely different operations even though both touch
  passwords: register **creates** a hash; login **verifies** against an existing one.
  Never try to "reuse" one for the other.
- The token returned by `/auth/login` is just a string at this point — nothing in
  your API actually *checks* it yet. That's tomorrow's whole lesson
  (`Depends(get_current_user)`).

---

## Your turn

1. Test the full flow in `/docs`:
   - `POST /auth/register` with a new email/password → `201`.
   - `POST /auth/register` again with the **same** email → `400` (the `IntegrityError`
     path, or your explicit duplicate check — either is acceptable, but make sure one
     of them fires).
   - `POST /auth/login` with the right credentials → `200`, with an `access_token` in
     the response.
   - `POST /auth/login` with a wrong password → `401`.
2. Copy the `access_token` string from a successful login and decode it (without
   verifying) at **jwt.io**, pasting it into the "Encoded" box. Confirm you can read
   your `sub` and `exp` claims in the "Decoded" panel — and notice you did this
   *without* your `SECRET_KEY`, which is exactly why Step 5 said a JWT is signed, not
   encrypted.

---

## Common mistakes to watch for
- **Storing a plain-text password anywhere**, even temporarily in a log statement or
  print — hash it immediately, keep the plain-text version in memory for the
  shortest time possible.
- **Comparing hashes with `==`** instead of `verify_password(...)` — this will almost
  always fail, since bcrypt salts every hash differently (Step 2).
- **Putting sensitive data inside the JWT payload** — remember, it's readable by
  anyone holding the token (Step 5). A user id is fine; a password or a full profile
  is not.
- **A hard-coded `SECRET_KEY`** left in the code instead of `.env` — treat it exactly
  like `DATABASE_URL` from Day 10: real secret, never committed.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
