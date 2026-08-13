# Day 24 — Teaching Lesson: File Uploads & Emails

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered
> step builds on the one before it.

## Objective
Handle two things almost every real API needs: accepting a file from a client, and
sending an email from the server.

## What you're building today
- `POST /students/{id}/photo` — upload a profile photo, validated by type and size,
  saved to disk.
- A welcome email sent automatically when `POST /auth/register` succeeds, sent to a
  free Mailtrap testing inbox — never a real address, while developing.

---

## Step 1 — `UploadFile` and `File()`

**Definition:** `UploadFile` is FastAPI's type for a file sent in a request —
distinct from a Pydantic model, because file data isn't ordinary JSON; it's sent as
`multipart/form-data`, a different request encoding designed for binary content.
`File(...)` marks a parameter as coming from that upload, the same role `Body`/
`Query` play for other kinds of input.

```python
from fastapi import UploadFile, File

@router.post("/{student_id}/photo")
async def upload_photo(student_id: int, photo: UploadFile = File(...)):
    return {"filename": photo.filename, "content_type": photo.content_type}
```
**Notice this route function is `async def`** — reading an uploaded file is an I/O
operation (Week 2, Day 5's territory), and `UploadFile`'s read methods are
awaitable, so the route needs to be async to use `await photo.read()` below.

## Step 2 — Validating type and size before saving anything

**Definition:** Never trust a client-supplied filename or `Content-Type` header
blindly — both can be set to anything by the client, so you validate against what
you actually expect, the same discipline as every validation lesson since Day 11.

```python
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}
MAX_FILE_SIZE = 2 * 1024 * 1024   # 2 MB

@router.post("/{student_id}/photo")
async def upload_photo(student_id: int, photo: UploadFile = File(...)):
    if photo.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG or PNG images are allowed")

    contents = await photo.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 2 MB)")

    ...
```
**Why check size *after* reading, not before:** `photo.file` (the underlying file
object) doesn't know its total size until you've read it — `Content-Length` from the
request header is a reasonable hint but shouldn't be fully trusted either (a client
could lie about it), so checking the actual bytes read is the reliable approach for
a file this small. (For very large uploads, you'd stream and check size
incrementally instead of reading everything into memory at once — a technique
outside today's scope, but worth knowing exists.)

## Step 3 — Saving the file

```python
import os
import uuid

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

extension = photo.filename.split(".")[-1]
unique_filename = f"{uuid.uuid4()}.{extension}"
file_path = os.path.join(UPLOAD_DIR, unique_filename)

with open(file_path, "wb") as f:
    f.write(contents)
```
**Definition:** `uuid.uuid4()` generates a random, essentially-unique identifier.
**Never save a file under the client-supplied filename directly** — two different
users could upload `photo.jpg` and overwrite each other, and a crafted filename
(`../../etc/passwd`) is a real security risk called **path traversal**. Generating
your own filename sidesteps both problems entirely.

Then store the path (or a public URL, if using cloud storage) on the student record:
```python
student = students_service.get_by_id(db, student_id)
if student is None:
    raise HTTPException(status_code=404, detail="Student not found")
student.photo_path = file_path
db.commit()
```
(This needs a new `photo_path: str | None` column on `Student` — add it the same way
`course_id` was added on Day 19.)

## Step 4 — Sending email with `fastapi-mail`

```bash
pip install fastapi-mail
```
**Definition:** `fastapi-mail` is a library for sending email from a FastAPI app,
configured once with your mail provider's credentials, then used anywhere in your
code with a simple async call.

**Get free testing credentials from Mailtrap** (mailtrap.io — free tier, no credit
card): sign up, create an inbox, and copy its SMTP credentials into `.env`. Every
email your app sends during development lands in that private Mailtrap inbox —
**never a real person's**, which is exactly why you always use a testing provider
like this while building, and only switch to a real provider for actual production
deployment.

```python
# email_service.py
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from config import settings

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

async def send_welcome_email(to_email: str) -> None:
    message = MessageSchema(
        subject="Welcome to the Students API!",
        recipients=[to_email],
        body="Thanks for registering. Your account is ready.",
        subtype=MessageType.plain,
    )
    fm = FastMail(mail_config)
    await fm.send_message(message)
```
Add the matching fields to `Settings` (Day 8's pattern) and to `.env`:
```
MAIL_USERNAME=your-mailtrap-username
MAIL_PASSWORD=your-mailtrap-password
MAIL_FROM=noreply@studentsapi.test
MAIL_PORT=2525
MAIL_SERVER=sandbox.smtp.mailtrap.io
```

## Step 5 — Calling it from `register`

```python
@router.post("/register", status_code=201, response_model=UserOut)
async def register(payload: RegisterIn, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    await send_welcome_email(user.email)

    return user
```
**Notice `register` is now `async def`**, since it `await`s `send_welcome_email` —
the same rule from Step 1 applies to any route that awaits anything inside it.

---

## Worked example: upload validation, fully wired

### Problem statement
Wire Steps 1-3 into a complete, working `upload_photo` route.

### Solution
See [`exercises/routers/students.py`](./exercises/routers/students.py) (the upload
route) — fully solved and commented.

Run it:
```bash
cd exercises
uvicorn main:app --reload
```
Test in `/docs` — the upload route renders a file picker automatically, since
FastAPI recognises `UploadFile` and generates the right form in the interactive docs
for you.

### What to notice
- `/docs` handles the `multipart/form-data` encoding transparently — you never wrote
  any code to parse that format yourself; `UploadFile` did it, the same "framework
  handles the tedious part" pattern from every FastAPI lesson since Day 7.
- Validation (Step 2) happens **before** any file gets written to disk — reject
  first, touch the filesystem only once you know the upload is acceptable.

---

## Your turn

1. Add `photo_path: str | None` to the `Student` model (Step 3) and finish wiring
   `upload_photo` to save it there.
2. Get a free Mailtrap inbox, fill in `.env`, and finish `send_welcome_email` (Step
   4) — it's stubbed in `exercises/email_service.py`.
3. Wire it into `register` (Step 5), and confirm: register a new user, then check
   your Mailtrap inbox — the welcome email should appear there within a few seconds.
4. Test the upload's validation directly: try uploading a `.txt` file (should get a
   `400`), and a real image (should succeed, and the returned student should show a
   `photo_path`).

---

## Common mistakes to watch for
- **Trusting the client-supplied filename for anything security-sensitive** — always
  generate your own (Step 3).
- **Skipping the content-type/size checks "just for testing"** — these are exactly
  the checks that matter most once a real, untrusted client is involved; build the
  habit now.
- **Accidentally emailing a real address during development** — always use a
  Mailtrap (or equivalent) sandbox inbox until you deliberately switch to a real
  provider for production, which is a Week 7/8 concern, not a Week 6 one.
- **Forgetting `async def`** on a route that `await`s anything — a very easy slip
  once you're mixing sync and async routes in the same project.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
