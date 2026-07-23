# Day 7 — Teaching Lesson: Express I — Routes & Middleware

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered step
> builds on the one before it. Don't skip ahead: Step 6 assumes Step 5 already works.
>
> Yesterday you built a raw HTTP server by hand: manual routing with `if`/`else`,
> manual JSON headers, manual body-parsing. Today you rebuild the *same idea* — a
> students API — with Express, and feel directly how much of that Express does for
> you. Keep yesterday's `server.js` open in another tab if you want to compare.

## Objective
Meet the framework — and middleware, the idea everything else in Express is built on.

## What you're building today
The students API from yesterday, properly this time:
- full CRUD — list (with optional filtering), get one, create, update, delete
- a custom middleware that logs every request
- a validation middleware that rejects bad input before it reaches your route
- the students routes organised into their own file with `express.Router()`

---

## Step 1 — Installing and starting Express
**Definition:** Express is a framework — a library that sits on top of Node's `http`
module and handles routing, headers, and parsing for you, so you write far less
boilerplate per route than you did yesterday.

```bash
cd exercises
npm install express
```
That downloads Express into `node_modules/` and adds it to `package.json`'s
`dependencies` automatically — the same mechanic from yesterday's `npm install
--save-dev nodemon`, just without `--save-dev`, because your app needs Express to
*run*, not just while developing.

The smallest possible Express app:
```js
const express = require("express");
const app = express();

app.listen(3000, () => {
  console.log("Server running at http://localhost:3000");
});
```
Run it (`node server.js`) — it starts, but there are no routes yet, so every URL
currently 404s with Express's own default page. That's expected; Step 2 adds a route.

**Checkpoint:** run the snippet above and confirm you see "Server running..." in the
terminal, with no errors.

---

## Step 2 — Your first route: `GET /health`
Compare these two, side by side — yesterday's raw version, and today's Express
version, doing the exact same job:

```js
// Yesterday — raw http
if (req.method === "GET" && req.url === "/health") {
  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ status: "ok" }));
}
```
```js
// Today — Express
app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});
```
**Definition:** `app.get(path, handler)` registers a handler that only runs for `GET`
requests to that exact path — Express does the `req.method`/`req.url` checking for
you. `res.json(data)` replaces `writeHead` + `JSON.stringify` + `end()` with one call,
and sets the `Content-Type` header for you too.

There's a matching method for every HTTP verb: `app.get`, `app.post`, `app.put`,
`app.delete`. You'll use all four today.

**Checkpoint:** add the `/health` route to your `server.js`, restart, and visit
`http://localhost:3000/health` — same response as yesterday, a fraction of the code.

---

## Step 3 — Route params: one student by id
**Definition:** a route param is a placeholder in the URL path itself, written with a
colon. Express extracts it into `req.params` for you.

```js
app.get("/students/:id", (req, res) => {
  console.log(req.params.id);   // the id from the URL, e.g. "2" — as a STRING
});
```
Compare to yesterday, where you had to `req.url.split("/")` and pick out the piece by
hand. Express parses it for you — but **`req.params.id` is always a string**, even
when the URL only contains digits. `Number(req.params.id)` before comparing it to a
student's numeric `id`, same gotcha as yesterday.

---

## Step 4 — Query strings: filtering a list
**Definition:** a query string is the `?key=value` part of a URL, used for optional
extras like filters or sorting — not part of the route path itself. Express parses it
into `req.query`.

```js
// GET /students?minScore=80
app.get("/students", (req, res) => {
  console.log(req.query.minScore);   // "80" — also a string, same rule as params
});
```
You'll use this in the big assignment below to let `GET /students?minScore=80` return
only students scoring 80 or above.

---

## Step 5 — Middleware: the idea everything else is built on
**Definition:** middleware is a function that runs *between* the request arriving and
your route's handler responding — it can inspect or modify the request, and then must
call `next()` to pass control forward. If it never calls `next()` (and never sends a
response itself), the request hangs forever — the same failure shape as forgetting
`res.end()` yesterday, just one level up.

```js
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} ${req.method} ${req.url}`);
  next();   // without this, EVERY request hangs — nothing after this middleware ever runs
});
```
- **`app.use(fn)`** registers middleware that runs on *every* request, in the exact
  order you `app.use()` them — order matters.
- A middleware function always has the shape `(req, res, next)` — three parameters,
  always in that order.

This one — logging every request — is solved for you in `server.js`, and is the
worked example below.

---

## Step 6 — `express.json()`: parsing request bodies
**Definition:** `express.json()` is a piece of middleware, built into Express, that
reads an incoming JSON body and parses it into `req.body` for you.

```js
app.use(express.json());

app.post("/students", (req, res) => {
  console.log(req.body);   // { name: "Bruno", score: 77 } — already parsed, no req.on()
});
```
Compare to yesterday's `POST /students`, where you manually collected `req.on("data",
...)` chunks and called `JSON.parse(body)` yourself once `req.on("end", ...)` fired.
`express.json()` is that entire dance, done once, for every route.

**One placement rule:** `app.use(express.json())` must come *before* any route that
reads `req.body` — middleware only affects routes registered after it.

---

## Step 7 — Worked example: list, create, and wire it all together

This is the part solved live, in the session — the shape every remaining route in
today's assignment reuses.

### Problem statement
Build the skeleton of the students API: a logger middleware, `express.json()`, `GET
/health`, and a students router (in its own file) with `GET /students` (list) and
`POST /students` (create) working end to end.

### Thinking it through
1. Middleware order matters (Step 5) — the logger and `express.json()` need to be
   registered with `app.use()` *before* any route, so they run on every request.
2. "Organising routes" (today's last concept) means the students routes shouldn't all
   live directly on `app` in `server.js` — they belong in their own file, using
   `express.Router()`, which behaves just like a mini version of `app` but only for
   paths under one prefix.
3. A router file exports itself (`module.exports = router`) so `server.js` can
   `require()` it and mount it with `app.use("/students", studentsRouter)` — from
   that point on, a route written inside the router as `router.get("/")` really means
   `GET /students`, because Express prepends the mount path automatically.
4. `POST /students` needs `req.body` (Step 6) — a new student gets an `id` assigned by
   the server, never trusted from the client, then gets pushed into the in-memory
   array and returned with status `201` (the correct code for "a new resource was
   created," not the default `200`).

### Solution
See [`exercises/server.js`](./exercises/server.js) and
[`exercises/routes/students.js`](./exercises/routes/students.js) — both fully solved
and commented for the pieces below.

```js
// server.js
const express = require("express");
const studentsRouter = require("./routes/students");

const app = express();
const PORT = 3000;

app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} ${req.method} ${req.url}`);
  next();
});

app.use(express.json());

app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

app.use("/students", studentsRouter);

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
```
```js
// routes/students.js
const express = require("express");
const router = express.Router();

let students = [
  { id: 1, name: "Ada", score: 91 },
  { id: 2, name: "Kofi", score: 68 },
  { id: 3, name: "Zara", score: 84 },
];
let nextId = 4;

router.get("/", (req, res) => {
  res.json({ students });
});

router.post("/", (req, res) => {
  const { name, score } = req.body;
  const newStudent = { id: nextId++, name, score };
  students.push(newStudent);
  res.status(201).json(newStudent);
});

module.exports = router;
```

Run it:
```bash
cd exercises
npm start
```
Test with `curl`:
```bash
curl http://localhost:3000/health
curl http://localhost:3000/students
curl -X POST http://localhost:3000/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Bruno","score":77}'
```

### What to notice
- `students` and `nextId` live at the top of `routes/students.js`, outside any route —
  same reason `startedAt` lived outside the handler yesterday: state that needs to
  persist across requests has to live outside the function that runs per-request.
- `res.status(201).json(newStudent)` chains two calls — `status()` returns `res`
  itself, which is why you can immediately call `.json()` on the result.
- Nothing in `routes/students.js` mentions the path `/students` — that prefix comes
  entirely from how it's mounted in `server.js` (`app.use("/students", ...)`). This is
  what makes the router reusable: you could mount the same router at a different
  prefix without touching a line inside it.

### Common mistakes to watch for (today's whole session)
- **Forgetting `next()` in a middleware** — the request hangs, same failure shape as
  forgetting `res.end()` yesterday.
- **Registering `express.json()` (or the logger) *after* the routes that need it** —
  middleware only applies to routes registered after it, in order.
- **Treating `req.params.id` or `req.query.minScore` as a number without converting**
  — both always arrive as strings.
- **Sending two responses to one request** — same rule as yesterday: every branch
  should `return` right after it responds, or execution can fall through into another
  `res.json()`/`res.status()` call, which throws.

---

## Your turn — the big assignment

Extend `exercises/routes/students.js` one step at a time, in order. Each TODO comment
in the file matches a step below.

### Step 1 — filter the list: `GET /students?minScore=`
In the existing `router.get("/", ...)` handler, check `req.query.minScore`. If it's
present, only include students whose `score` is greater than or equal to it (remember:
`req.query.minScore` is a string — convert with `Number()` before comparing).
**Test:** `/students` → all 3. `/students?minScore=80` → only Ada and Zara.

### Step 2 — `GET /students/:id`: one student
Use `req.params.id` (Step 3 above) to find the matching student. Found → `200` with
that student. Not found → `404` with `{ error: "Student not found" }`.
**Test:** `/students/2` → Kofi. `/students/99` → the 404.

### Step 3 — `PUT /students/:id`: update
Find the student the same way as Step 2. Not found → same `404`. Found → overwrite its
`name` and `score` from `req.body`, then respond `200` with the updated student.
**Test:**
```bash
curl -X PUT http://localhost:3000/students/2 \
  -H "Content-Type: application/json" \
  -d '{"name":"Kofi","score":75}'
```
Then `GET /students/2` again to confirm the change stuck.

### Step 4 — `DELETE /students/:id`: remove
Use `.findIndex()` this time (not `.find()`) — you need the *position* in the array to
remove it with `.splice(index, 1)`. Not found → `404`. Found → remove it and respond
with **status `204` and no body at all** — no `res.json(...)` call, just
`res.status(204).end()`. `204 No Content` is the correct status for "it worked, and
there's nothing to send back."
**Test:** `DELETE /students/3`, then `GET /students` — Zara should be gone.

### Step 5 — validation middleware: reject bad input
Write a function:
```js
function validateStudent(req, res, next) {
  const { name, score } = req.body;
  if (typeof name !== "string" || name.trim() === "" || typeof score !== "number") {
    return res.status(400).json({ error: "name (string) and score (number) are required" });
  }
  next();
}
```
Apply it to **both** the POST route and the PUT route you wrote in Step 3, as a second
argument before the handler:
```js
router.post("/", validateStudent, (req, res) => { /* ... */ });
router.put("/:id", validateStudent, (req, res) => { /* ... */ });
```
This is route-specific middleware — unlike the logger (which runs on every request via
`app.use`), this only runs for the two routes you attach it to.
**Test:** `POST /students` with `{"name":"","score":"not a number"}` → `400` with your
error message, and nothing gets added to the array.

### Step 6 — confirm the router organisation
This part is already wired up in the solved code — `routes/students.js` exports a
`Router`, and `server.js` mounts it at `/students`. Re-read Step 7's "What to notice"
above and confirm you understand *why* none of your routes in `students.js` mention
the word `/students` anywhere in their path strings.

### Step 7 — test everything in Postman
Open Postman, create a collection called "Students API," and add one request per
route below, checking the status code each time. Save the collection, export it as
JSON, and push the export alongside your code.

### Final checklist — every route should behave like this
| Route | Method | Expected result |
|---|---|---|
| `/health` | GET | `200` — `{ status: "ok" }` |
| `/students` | GET | `200` — `{ students: [...] }` |
| `/students?minScore=80` | GET | `200` — only students scoring 80+ |
| `/students/2` | GET | `200` — Kofi's record |
| `/students/99` | GET | `404` — `{ error: "Student not found" }` |
| `/students` | POST (valid body) | `201` — the new student, with an `id` |
| `/students` | POST (bad body) | `400` — validation error message |
| `/students/2` | PUT (valid body) | `200` — the updated student |
| `/students/2` | DELETE | `204` — no body |
| `/students/99` | DELETE | `404` — `{ error: "Student not found" }` |

### Stretch goal (optional, only if you finish early)
Add a second query filter, `?sort=score`, that returns the list sorted by score
descending — combine it with `?minScore=` so both can be used at once
(`/students?minScore=70&sort=score`). Not required — Day 8 formalises the whole "REST
design" side of this, so don't over-engineer it today.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
