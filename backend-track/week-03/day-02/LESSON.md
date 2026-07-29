# Day 10 — Teaching Lesson: Mongoose — Express Meets the Database

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered step
> builds on the one before it. Don't skip ahead: Step 5 assumes Step 4 already works.
>
> Yesterday you learned documents and queries by hand, in Compass, against a `library`
> database. Today the students API from Week 2 — currently a `let students = [...]`
> array that resets every time the server restarts — gets rewired to read and write
> real documents in your Atlas cluster instead. Same routes, same JSON shapes your
> Postman collection already expects — the array underneath is what changes.

## Objective
Connect the API to real storage — data that survives restarts.

## What you're building today
- A new Atlas database, `school`, with a `students` collection — created automatically
  the first time Mongoose saves a document into it.
- A Mongoose **schema** and **model** describing what a valid student document looks
  like, with real validation (`required`, `min`, `max`, `trim`).
- Every controller function rewritten to use Mongoose's async methods instead of array
  methods — `find()` instead of returning the array directly, `findByIdAndUpdate()`
  instead of `.find()` + mutate, and so on.

---

## Step 1 — Get a connection string for your application (not Compass this time)
Yesterday you copied a **Compass** connection string. Today you need the **driver**
connection string — same cluster, different tab in Atlas.

1. In Atlas, open your cluster and click **Connect** again.
2. This time choose **"Drivers"** (not Compass).
3. Select **Node.js** as the driver and confirm the version shown matches what
   `npm install mongoose` gives you (any recent version is fine).
4. Copy the connection string. It looks like:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. Paste it into your `.env` file as `DATABASE_URL`, replace `<username>`/`<password>`
   with your real Day 9 credentials, and add a database name right after the host —
   `school` — so Mongoose knows which database to use:
   ```
   DATABASE_URL=mongodb+srv://youruser:yourpassword@cluster0.xxxxx.mongodb.net/school?retryWrites=true&w=majority
   ```

**Checkpoint:** `.env` (copied from `.env.example`, same as Day 8) now has a
`DATABASE_URL` with your real username, password, and the `school` database name baked
in. Never commit this file — it's already in `.gitignore`.

---

## Step 2 — Installing and connecting Mongoose
**Definition:** Mongoose is a library that sits on top of the MongoDB driver and adds
schemas — a way to describe what shape your documents *should* have, with validation,
even though MongoDB itself doesn't require one.

```bash
cd exercises
npm install mongoose
```

```js
// config/db.js
import mongoose from "mongoose";

export async function connectDB() {
  try {
    await mongoose.connect(process.env.DATABASE_URL);
    console.log("MongoDB connected");
  } catch (error) {
    console.error("MongoDB connection failed:", error.message);
    process.exit(1);
  }
}
```
`mongoose.connect()` returns a promise — `await` it before the server starts accepting
requests, so the very first request never races an unfinished connection.

**Checkpoint:** run the server (`npm run dev`) and confirm `MongoDB connected` prints in
the terminal before `Server running at http://localhost:3000`. If you see a connection
error instead, re-check `DATABASE_URL` — a wrong password is the most common cause.

**See it land in Atlas:** the `school` database won't actually appear in Compass or the
Atlas UI yet — MongoDB only creates a database (and collection) the moment the first
document is saved into it. That happens in Step 5, once `createStudent` actually runs.

---

## Step 3 — Schemas: describing the shape of a document
**Definition:** a schema is a JavaScript object describing each field a document should
have, its type, and any rules on it. Mongoose checks every save against the schema
before it reaches the database.

```js
// models/Student.js
import mongoose from "mongoose";

const studentSchema = new mongoose.Schema({
  name: { type: String, required: true, trim: true },
  score: { type: Number, required: true, min: 0, max: 100 },
});

export default mongoose.model("Student", studentSchema);
```
- **`type`** — every field declares its type (`String`, `Number`, `Boolean`, `Date`,
  ...). A save with the wrong type either gets coerced or rejected.
- **`required: true`** — the field must be present, or the save is rejected with a
  `ValidationError`.
- **`trim: true`** — automatically strips leading/trailing whitespace from strings, so
  `"  Ada  "` gets stored as `"Ada"`.

**Checkpoint:** identify which two rules stop a student being saved with a negative
score, or a `100000`-point score. (`min: 0` and `max: 100`.)

---

## Step 4 — Models: turning a schema into something you can query
**Definition:** `mongoose.model("Student", studentSchema)` compiles a schema into a
**model** — an object with methods (`.find()`, `.create()`, ...) that talk to a specific
collection. Mongoose automatically pluralizes and lowercases the name you give it:
`"Student"` becomes the `students` collection.

```js
import Student from "../models/Student.js";

await Student.find();                          // all students
await Student.findById(id);                     // one, by _id
await Student.create({ name: "Ada", score: 91 }); // insert one, validated against the schema
await Student.findByIdAndUpdate(id, updates, { new: true, runValidators: true });
await Student.findByIdAndDelete(id);
```
- **`{ new: true }`** on an update tells Mongoose to return the *updated* document, not
  the one from before the change — without it you'd get the stale version back.
- **`{ runValidators: true }`** tells Mongoose to re-check the schema's rules on an
  update too — without it, updates can silently bypass validation that inserts don't.

**Checkpoint:** notice every one of these methods returns a promise — every single call
above needs an `await`, exactly like `fetch` did in Week 2.

---

## Step 5 — Worked example: connect, define the model, wire up two routes

This is solved live, in the session — the shape every remaining controller function
in today's assignment reuses.

### Problem statement
Wire up the connection, define the `Student` model, and rewrite `listStudents` and
`createStudent` to read and write real documents instead of the in-memory array.

### Thinking it through
1. The connection (Step 2) has to succeed before anything else works — it's called
   once, at startup, in `server.js`.
2. The model (Steps 3–4) replaces the `let students = [...]` array and `let nextId`
   counter from Day 8 entirely — MongoDB generates each document's `_id` for you, so
   there's no counter to maintain anymore.
3. Every controller function becomes `async`, and every Mongoose call inside it gets
   an `await`, wrapped in `try`/`catch` — a rejected Mongoose call (bad connection, a
   validation error) becomes a caught `error`, forwarded with `next(error)` to the same
   central error handler from Day 8. Nothing about that error handler changes today.

### Solution
See [`exercises/config/db.js`](./exercises/config/db.js),
[`exercises/models/Student.js`](./exercises/models/Student.js), and
[`exercises/controllers/students.js`](./exercises/controllers/students.js) —
`listStudents` and `createStudent` are fully solved and commented.

```js
// controllers/students.js
import Student from "../models/Student.js";

export async function listStudents(req, res, next) {
  try {
    const students = await Student.find();
    res.json({ students });
  } catch (error) {
    next(error);
  }
}

export async function createStudent(req, res, next) {
  try {
    const newStudent = await Student.create(req.body);
    res.status(201).json(newStudent);
  } catch (error) {
    next(error);
  }
}
```

Run it:
```bash
cd exercises
cp .env.example .env   # then fill in your real DATABASE_URL
npm run dev
```
Test with `curl`, same as every day since Day 7:
```bash
curl http://localhost:3000/students
curl -X POST http://localhost:3000/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Bruno","score":77}'
```

### What to notice
- `Student.create(req.body)` validates `req.body` against the schema automatically —
  if `name` is missing, this line itself throws, caught by the `catch` block, same as
  any other rejected promise.
- The response shape (`{ students }` for the list, the created object for `POST`)
  didn't change from Day 8 at all — only *where the data comes from* changed. Your
  existing Postman requests still work unchanged.
- One real difference you'll see in Postman: `_id` is now a long MongoDB `ObjectId`
  string (like `"665f1a2b3c4d5e6f7a8b9c0d"`), not the small sequential number
  (`1`, `2`, `3`) from the in-memory version.

---

## Your turn — the big assignment

Finish `exercises/models/Student.js` and `exercises/controllers/students.js`. Each TODO
comment matches a step below — do them in order, testing each in Postman before moving
to the next.

### Step 1 — finish the schema's validation rules
Add `min: 0, max: 100` to `score` and `trim: true` to `name` if you haven't already
copied them from Step 3 above. Confirm both are present before moving on — the rest of
today's testing depends on them actually rejecting bad input.

### Step 2 — `getStudent`
Use `Student.findById(req.params.id)`. Not found → build an `Error`, set
`err.statusCode = 404`, `err.message` to `"Student not found"`, and `next(err)` — same
error shape as Day 8, just a different data source underneath. Found → `res.json(student)`.
**Test:** a real `_id` from your last `POST` response → `200`. A made-up 24-character
hex string → `404` from your own check. A too-short string like `"123"` → `400` from
Mongoose's own `CastError` (see "Common mistakes" below) — you don't have to handle
this one specially, the central error handler already reports it as a 500 unless you
add the CastError check in the stretch goal.

### Step 3 — `updateStudent`
Use `Student.findByIdAndUpdate(req.params.id, req.body, { new: true, runValidators: true })`.
Not found (Mongoose returns `null`) → same 404 pattern as Step 2. Found → `res.json(updatedStudent)`.
**Test:**
```bash
curl -X PUT http://localhost:3000/students/<a real _id> \
  -H "Content-Type: application/json" \
  -d '{"name":"Kofi","score":75}'
```
Then try `{"score": 500}` — `runValidators: true` should make this fail with a
`ValidationError`, forwarded through `next(error)` same as any other caught error.

### Step 4 — `deleteStudent`
Use `Student.findByIdAndDelete(req.params.id)`. Not found → same 404 pattern. Found →
`res.status(204).end()`, no body — identical rule to Day 7/8.
**Test:** delete a real student, then `GET /students` to confirm it's gone, and try
deleting the same id again — should now 404.

### Step 5 — update the Postman collection
Re-run every saved request from Day 8's collection against the Mongoose-backed API.
`_id` values are different now (real ObjectIds, not `1`/`2`/`3`) — update any saved
request bodies/URLs that hardcoded the old numeric ids, save the collection, and
re-export it.

### Final checklist — every route should behave like this
| Route | Method | Expected result |
|---|---|---|
| `/students` | GET | `200` — `{ students: [...] }`, from Atlas |
| `/students` | POST (valid body) | `201` — the new student, with a real `_id` |
| `/students` | POST (missing name) | error from the central handler (`ValidationError`) |
| `/students/:id` | GET (real id) | `200` — that student |
| `/students/:id` | GET (well-formed but unknown id) | `404` — `{ error: "Student not found" }` |
| `/students/:id` | PUT (valid body) | `200` — the updated student |
| `/students/:id` | DELETE | `204` — no body |

### Common mistakes to watch for
- **Forgetting `await`** on any Mongoose call — you get a pending `Promise` back
  instead of your data, same failure shape as forgetting `await` on `fetch` in Week 2.
- **Forgetting `try`/`catch`** around a Mongoose call — an unhandled rejected promise
  inside an Express route crashes the process instead of reaching your error handler.
- **Forgetting `{ new: true }`** on an update — you'd send back the *old* document,
  which looks like your update silently did nothing.
- **Forgetting `{ runValidators: true }`** on an update — schema rules like `min`/`max`
  only apply to the *original* `create()`, not to later updates, unless you ask for it.
- **A malformed id string** (not a valid 24-character hex ObjectId) throws a Mongoose
  `CastError`, a different error shape than "not found" — the stretch goal below
  handles this explicitly; without it, your central error handler still catches it,
  just reports it as a generic `500` instead of a `400`.

### Stretch goal (optional, only if you finish early)
In the central error handler (`server.js`, from Day 8), add a check for
`error.name === "CastError"` *before* the generic fallback, and respond `400` with a
message like `"Invalid student id"` — a malformed id is a client mistake, not a server
failure, so it deserves a `4xx`, not a `500`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
