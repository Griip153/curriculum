# Day 8 — Teaching Lesson: REST Design & Project Structure

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered step
> builds on the one before it. Don't skip ahead: Step 6 assumes Step 5 already works.
>
> Yesterday you built full CRUD, but every route's logic lived directly inside
> `routes/students.js`, and the port was hardcoded as `const PORT = 3000`. Today you
> don't add new endpoints — you make the *project itself* look like something a
> professional team would ship: proper REST naming, routes that only route, a real
> place for config, and one consistent way of handling errors instead of a `404` here
> and a raw crash there.
>
> One more change: today's `exercises/` uses **ES Modules** (`import`/`export`)
> instead of the CommonJS (`require`/`module.exports`) you've used since Day 6 —
> `package.json` has `"type": "module"` set, which is what tells Node to read every
> `.js` file in this folder as ESM. Remember the one rule from Day 6: never mix
> `require` and `import` in the same file — this folder is `import` throughout, no
> exceptions.

## Objective
Structure an API like a professional team — controllers, routes, and errors that make
sense.

## What you're building today
The same students API, restructured, not rewritten:
- routes/students.js becomes **thin** — no logic, just "this URL calls this function"
- controllers/students.js becomes **where the logic actually lives**
- a global **404 handler** for any URL that matches no route at all
- a global **error-handling middleware** — one place that turns a thrown error into a
  proper JSON response, instead of every route handling its own errors differently
- `PORT` (and any other config) moves out of the code and into a `.env` file

---

## Step 1 — REST principles: naming resources like nouns, not verbs
**Definition:** REST ("REpresentational State Transfer") is a convention for API URLs —
the URL names a **resource** (a noun, usually plural), and the **HTTP method** says what
to do with it. The verb goes in the method, never in the path.

```
Bad:                          Good:
GET  /getAllStudents          GET    /students
POST /createNewStudent        POST   /students
GET  /getStudentById/5        GET    /students/5
POST /deleteStudent/5         DELETE /students/5
```
You've actually been doing this correctly since Day 7 without naming it — `router.get("/")`,
`router.post("/")`, `router.get("/:id")` are already REST-shaped. Today just puts a name
to the pattern, and extends it: nested resources (if you ever added, say, a student's
grades) would read `GET /students/5/grades`, not `GET /getGradesForStudent/5`.

**Checkpoint:** look back at Day 7's four routes — confirm none of them have a verb
anywhere in the URL path itself.

---

## Step 2 — Why split routes from controllers
**Definition:** a **route** answers "which URL, which method, which function handles
it?" A **controller** answers "what actually happens when that function runs?" Keeping
them in the same file (like yesterday) works fine for four routes — it stops working
once a real API has forty.

```js
// Yesterday — route AND logic tangled together
router.get("/", (req, res) => {
  res.json({ students });
});
```
```js
// Today — route just points at a named function
router.get("/", studentsController.listStudents);

// controllers/students.js
export function listStudents(req, res) {
  res.json({ students });
}
```
**Why this matters:** the route file becomes a one-glance table of contents for your
whole API's URL surface. The controller file is where you'd actually add validation,
call a database, etc. — none of that clutters the routing.

**Checkpoint:** open `exercises/routes/students.js` — `GET /` and `POST /` are already
split this way. Notice the route file doesn't contain a single line of student-array
logic anymore.

---

## Step 3 — dotenv and environment variables
**Definition:** an environment variable is a setting that lives *outside* your code —
different per machine (your laptop vs. a real server) without ever editing a file.
`dotenv` is a package that reads a local `.env` file and copies its values into
`process.env` for you, so you write `process.env.PORT` instead of hardcoding `3000`.

```bash
cd exercises
npm install dotenv
```
```js
// very first line of server.js — before anything else runs
import "dotenv/config";

const PORT = process.env.PORT || 3000;
```
`import "dotenv/config"` is a **side-effect import** — it runs `dotenv`'s setup code
immediately (loading `.env` into `process.env`) without needing to name or call
anything yourself. It's the ESM equivalent of yesterday's `require("dotenv").config()`.
- **`.env`** — the real file, holding real values for *your* machine. **Never commit
  it** — it's already in `.gitignore`.
- **`.env.example`** — a committed template listing the variable *names* (no real
  secrets), so a teammate knows what to create. Already in `exercises/.env.example`.

**Checkpoint:** copy the example and confirm it's picked up:
```bash
cp .env.example .env
```
Change the value inside `.env` to `PORT=4000`, run the server, and confirm the console
now says `http://localhost:4000` instead of `3000`.

---

## Step 4 — Central error-handling middleware
**Definition:** Express treats any middleware function with **exactly four parameters**
`(err, req, res, next)` as an error handler — a different signature than every other
middleware you've written (three params: `req, res, next`). Express skips straight to
it whenever something calls `next(err)` or a route throws.

```js
app.use((err, req, res, next) => {
  console.error(err);
  res.status(err.statusCode || 500).json({ error: err.message || "Something went wrong" });
});
```
- It must be registered with `app.use()` **after every other route** — Express error
  handlers only catch what happens "above" them in the file.
- A controller reports an error by building one and calling `next(err)` — it does
  **not** call `res.status(...).json(...)` itself:
```js
function getStudent(req, res, next) {
  const student = students.find((s) => s.id === Number(req.params.id));
  if (!student) {
    const err = new Error("Student not found");
    err.statusCode = 404;
    return next(err);   // hands off to the error handler above — response shape lives in ONE place
  }
  res.json(student);
}
```
**Why this matters:** yesterday, every route repeated its own `res.status(404).json({
error: ... })`. If you ever want to change that shape (add a `success: false` field,
say), you'd have to find and edit every single route. With one central handler, you
change it in exactly one place.

---

## Step 5 — 404 handling for unmatched routes
**Definition:** the error handler in Step 4 only fires when something explicitly calls
`next(err)`. It does **nothing** for a URL that matches *no route at all* — e.g.
`GET /nonsense`. That needs its own middleware, registered **after every route** but
**before** the error handler:

```js
app.use((req, res) => {
  res.status(404).json({ error: `Route ${req.method} ${req.originalUrl} not found` });
});
```
Order matters here more than anywhere else today:
```
app.use("/students", studentsRouter);   // 1. real routes first
app.use(the 404 handler);               // 2. catches anything unmatched above
app.use(the error handler);             // 3. catches anything that called next(err)
```
If you swap 2 and 3, or put either one before your routes, they'll swallow requests
that should have reached your real routes instead.

---

## Step 6 — Worked example: wiring one controller function end to end

This is the part solved live, in the session — the shape every remaining TODO reuses.

### Problem statement
Take yesterday's inline `GET /` and `POST /` route handlers and turn them into
`listStudents` and `createStudent` in a new `controllers/students.js`, called from a
now-thin `routes/students.js`.

### Thinking it through
1. The logic itself doesn't change *at all* — only where it lives. Cut the function
   body out of the route, paste it into the controller file as a named function.
2. A controller function keeps the exact same `(req, res)` signature a route handler
   already had — that's *why* `router.get("/", studentsController.listStudents)` works
   with no wrapper: Express calls whatever function you hand it, and doesn't care
   which file it came from.
3. `controllers/students.js` needs `export function listStudents(...) {...}` (a
   **named export**, one per function) so `routes/students.js` can
   `import * as studentsController from "../controllers/students.js"` and read
   `studentsController.listStudents` off the resulting object. Note the `.js` on the
   end of that path — ESM import paths for your own files must include the
   extension; Node won't guess it for you the way `require()` did.

### Solution
See [`exercises/controllers/students.js`](./exercises/controllers/students.js) and
[`exercises/routes/students.js`](./exercises/routes/students.js) — both fully solved
and commented for `listStudents`/`createStudent`.

```js
// controllers/students.js
let students = [
  { id: 1, name: "Ada", score: 91 },
  { id: 2, name: "Kofi", score: 68 },
  { id: 3, name: "Zara", score: 84 },
];
let nextId = 4;

export function listStudents(req, res) {
  res.json({ students });
}

export function createStudent(req, res) {
  const { name, score } = req.body;
  const newStudent = { id: nextId++, name, score };
  students.push(newStudent);
  res.status(201).json(newStudent);
}
// ...the rest you're about to write, each as its own `export function`
```
```js
// routes/students.js
import express from "express";
import * as studentsController from "../controllers/students.js";

const router = express.Router();

router.get("/", studentsController.listStudents);
router.post("/", studentsController.createStudent);

export default router;
```

### What to notice
- `students` and `nextId` moved into the controller file, not the route file — the
  data a resource owns lives next to the logic that manipulates it.
- Nothing about `listStudents`'s *body* changed from yesterday's route handler — this
  step is purely about *where code lives*, not what it does.

### Common mistakes to watch for (today's whole session)
- **Registering the 404 handler or error handler before your real routes** — see Step
  5's ordering diagram; either one placed too early swallows requests it shouldn't.
- **An error handler with three parameters instead of four** — Express silently treats
  it as regular middleware, not an error handler, and it never fires on `next(err)`.
- **Calling `res.json(...)` yourself AND `next(err)`** for the same request — pick one;
  a controller either responds or hands off to the error handler, never both.
- **Forgetting `import "dotenv/config"` at the very top of `server.js`**, or putting it
  after something already reads `process.env` — it must run first.
- **Leaving off the `.js` extension** on a relative import (`"./routes/students"`
  instead of `"./routes/students.js"`) — CommonJS's `require()` would forgive this;
  ESM's `import` throws `ERR_MODULE_NOT_FOUND`.

---

## Your turn — the big assignment

Extend `exercises/controllers/students.js` and `exercises/routes/students.js`, then
finish `exercises/server.js`. Each TODO comment matches a step below — do them in order.

### Step 1 — `getStudent`
In `controllers/students.js`, write `getStudent(req, res, next)`: find the student by
`Number(req.params.id)`. Not found → build an `Error`, set `err.statusCode = 404`,
`err.message` to something like `"Student not found"`, and `return next(err)`. Found →
`res.json(student)`. Then uncomment its route in `routes/students.js`.
**Test:** `/students/2` → Kofi. `/students/99` → your error handler's JSON, status 404.

### Step 2 — `updateStudent`
Same not-found handling as Step 1. If found, overwrite `name`/`score` from `req.body`
and respond `200` with the updated student. Uncomment its route.
**Test:**
```bash
curl -X PUT http://localhost:3000/students/2 \
  -H "Content-Type: application/json" \
  -d '{"name":"Kofi","score":75}'
```

### Step 3 — `deleteStudent`
Same not-found handling. Use `.findIndex()` to get the position, `.splice(index, 1)` to
remove it, then respond `204` with no body (`res.status(204).end()` — no `.json()`
call). Uncomment its route.
**Test:** `DELETE /students/3`, then `GET /students` — Zara should be gone.

### Step 4 — the central error-handling middleware
In `server.js`, uncomment the four-argument `app.use((err, req, res, next) => {...})`
block at the bottom of the file. Confirm it's the **very last** `app.use()` call.
**Test:** `GET /students/99` should now return the JSON from *this* handler (status
`404`, from the `err.statusCode` you set in Step 1), not a raw stack trace in the
terminal.

### Step 5 — the global 404 handler
Uncomment the `app.use((req, res) => {...})` block — it must sit **after** the students
router but **before** the error-handling middleware from Step 4.
**Test:** `GET /nonsense-route` → `404` with `{ error: "Route GET /nonsense-route not
found" }`.

### Step 6 — move `PORT` into `.env`
Follow Step 3 above: `npm install dotenv`, `cp .env.example .env`, confirm
`import "dotenv/config"` is the first line of `server.js` and `PORT` reads from
`process.env.PORT`.
**Test:** change the value in `.env`, restart the server, confirm the console prints
the new port.

### Final checklist — every route should behave like this
| Route | Method | Expected result |
|---|---|---|
| `/health` | GET | `200` — `{ status: "ok" }` |
| `/students` | GET | `200` — `{ students: [...] }` |
| `/students/2` | GET | `200` — Kofi's record |
| `/students/99` | GET | `404` — from the central error handler |
| `/students` | POST (valid body) | `201` — the new student, with an `id` |
| `/students/2` | PUT (valid body) | `200` — the updated student |
| `/students/2` | DELETE | `204` — no body |
| `/nonsense-route` | GET | `404` — `{ error: "Route GET /nonsense-route not found" }` |

### Stretch goal (optional, only if you finish early)
Reintroduce yesterday's `validateStudent` middleware, but have it call
`next(err)` (with `err.statusCode = 400`) instead of responding directly — so
*every* error in the whole app, validation included, flows through the one central
handler from Step 4.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
