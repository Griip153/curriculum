# Day 11 — Teaching Lesson: Validation & Error Handling Done Right

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered step
> builds on the one before it. Don't skip ahead: Step 5 assumes Step 4 already works.
>
> Yesterday you finished full Mongoose CRUD with schema rules (`required`, `min`, `max`,
> `trim`) — bad data already gets rejected before it's saved. But two things still feel
> unpolished: a malformed `:id` in the URL (like `/students/123`) throws a raw Mongoose
> `CastError` that your central error handler reports as a generic `500`, and a
> `ValidationError` from a bad `POST` body comes back as a scary nested object instead of
> one clear message. Today you fix both — request data gets checked *before* it ever
> reaches Mongoose, and every failure, from every layer, comes back through the same
> error handler as one clean `{ error: "message" }`.

## Objective
Make your API fail clearly and safely — the mark of professional work.

## What you're building today
- A `validators/students.js` file — `express-validator` rule chains for the write
  routes (`POST /students`, `PUT /students/:id`), plus one shared middleware that turns
  any validation failure into a `next(err)` call.
- The central error handler from Day 8, taught to recognize two specific Mongoose error
  types — `ValidationError` and `CastError` — and respond `400` with a clear message
  instead of falling through to a generic `500`.
- Proof, in Postman, that five different kinds of bad request each fail with the right
  status code and the same `{ error: "..." }` shape.

---

## Step 1 — Why schema validation alone isn't enough
**Definition:** schema validation (Day 10) checks data *at the database layer*, right
before a save. Request validation checks it *at the door*, before a single line of your
controller or a single Mongoose call runs.

Two gaps schema validation leaves open:
- **A malformed id.** `Student.findById("123")` doesn't fail because `123` is a bad
  *student* — it fails because `"123"` isn't a valid MongoDB `ObjectId` at all. Mongoose
  throws a `CastError` for this, a completely different problem than "validation failed
  on save," and your Day 10 error handler doesn't tell them apart — both come back `500`.
- **Confusing failure messages.** A `ValidationError` from a broken `min`/`max`/`required`
  rule carries a nested `err.errors` object, one entry per broken field, each with its
  own message buried a few levels deep — not something you'd want to hand a frontend
  developer as-is.

**Checkpoint:** in Postman, hit `GET /students/123` against your finished Day 10 API
right now. Confirm you get a `500` with a generic message — that's the gap this lesson
closes.

---

## Step 2 — Installing express-validator
**Definition:** `express-validator` is a middleware library for declaring validation
rules per route — each rule is a small chain like `body("score").isFloat({ min: 0, max:
100 })`, run *before* your controller, so bad input never reaches it at all.

```bash
cd exercises
npm install express-validator
```

**Checkpoint:** confirm `express-validator` now appears under `dependencies` in
`package.json`.

---

## Step 3 — Writing a validation rule chain
```js
import { body } from "express-validator";

export const createStudentValidator = [
  body("name").trim().notEmpty().withMessage("name is required"),
  body("score")
    .notEmpty().withMessage("score is required")
    .isFloat({ min: 0, max: 100 }).withMessage("score must be a number between 0 and 100"),
];
```
- Each `body(field)` starts a chain for one field of the request body; chain multiple
  checks with `.method().method()...`.
- `.withMessage(...)` attaches the message reported if *that specific* check fails.
- This is an **array of middleware** — Express runs each one in order when you pass the
  whole array as a route handler argument, same as any middleware list.

**Checkpoint:** notice this doesn't reject anything by itself yet — it only *collects*
problems onto the request. Step 4 is what actually stops a bad request.

---

## Step 4 — Worked example: wiring `createStudentValidator` end to end

This is solved live, in the session — the shape today's one remaining TODO reuses.

### Problem statement
Validate `POST /students` before it reaches `createStudent`, and respond `400` with one
clear message the moment any rule fails.

### Thinking it through
1. `express-validator`'s checks don't throw — they attach their findings to the request,
   readable via `validationResult(req)`. Something has to actually read that and decide
   what to do.
2. That "something" is its own middleware, run *after* the validator chain, *before* the
   controller — if it finds problems, it builds an `Error`, sets `err.statusCode = 400`,
   and calls `next(err)`, handing off to the exact same central error handler from Day 8.
   If there are no problems, it just calls `next()` and the controller runs normally.
3. Because it's a normal middleware function, one shared `handleValidationErrors` works
   for every route — you don't write this check once per route, only the *rule chain*
   changes per route.

### Solution
See [`exercises/validators/students.js`](./exercises/validators/students.js) and
[`exercises/routes/students.js`](./exercises/routes/students.js) —
`createStudentValidator` and `handleValidationErrors` are fully solved, wired onto
`POST /students`.

```js
// validators/students.js
import { body, validationResult } from "express-validator";

export const createStudentValidator = [
  body("name").trim().notEmpty().withMessage("name is required"),
  body("score")
    .notEmpty().withMessage("score is required")
    .isFloat({ min: 0, max: 100 }).withMessage("score must be a number between 0 and 100"),
];

export function handleValidationErrors(req, res, next) {
  const errors = validationResult(req);
  if (errors.isEmpty()) return next();

  const err = new Error(errors.array()[0].msg);
  err.statusCode = 400;
  next(err);
}
```
```js
// routes/students.js
router.post(
  "/",
  createStudentValidator,
  handleValidationErrors,
  studentsController.createStudent
);
```

Test it:
```bash
curl -X POST http://localhost:3000/students \
  -H "Content-Type: application/json" \
  -d '{"score": 500}'
```

### What to notice
- The response is now `{ "error": "name is required" }` — one message, no nested
  Mongoose error object — even though `score` is *also* invalid. `validationResult`
  collects every failure; `.array()[0]` reports just the first, which is enough for a
  human to fix and resubmit.
- `createStudent` itself didn't change at all — by the time it runs, `req.body` is
  already known-good. The controller stays exactly as simple as Day 10 left it.
- This request never touched Mongoose or Atlas — it failed at the door, which is
  cheaper and faster than a rejected database write.

---

## Your turn — the big assignment

### Step 1 — `updateStudentValidator`
In `validators/students.js`, write `updateStudentValidator`: same two fields as
`createStudentValidator`, but add `.optional()` as the *first* link in each chain — a
`PUT` here might only send `{ "score": 75 }`, and a missing `name` shouldn't be treated
as an error on an update the way it is on a create. Wire it onto `PUT /students/:id` in
`routes/students.js`, the same way Step 4's worked example wired the create validator.
**Test:** `PUT /students/<real id>` with `{"score": 500}` → `400`,
`"score must be a number between 0 and 100"`. With `{"score": 80}` alone (no `name`) →
`200`, updates just the score.

### Step 2 — Handle Mongoose's `ValidationError` in the central error handler
In `server.js`'s error-handling middleware, **before** the generic fallback, add:
```js
if (err.name === "ValidationError") {
  const firstError = Object.values(err.errors)[0].message;
  return res.status(400).json({ error: firstError });
}
```
This only fires for validation failures that somehow still reach Mongoose directly
(e.g. a `runValidators` failure on update) — express-validator already caught the
common cases at the door in Steps 3–4, but the schema is still the last line of defense.
**Test:** temporarily comment out `updateStudentValidator` on the route, send a bad
`PUT`, confirm you still get a clean `400` instead of a `500` — then uncomment it again.

### Step 3 — Handle Mongoose's `CastError` in the central error handler
Right after the `ValidationError` check, add:
```js
if (err.name === "CastError") {
  return res.status(400).json({ error: "Invalid student id" });
}
```
**Test:** `GET /students/123` (too short to be a real `ObjectId`) → `400`,
`{ "error": "Invalid student id" }`, not a `500`.

### Step 4 — Prove it: five deliberately bad requests in Postman
Save all five in your collection, confirm each returns the status/shape below, then
export the collection.

### Final checklist — every failure should behave like this
| Request | Expected result |
|---|---|
| `POST /students` with no `name` | `400` — `{ error: "name is required" }` |
| `POST /students` with `score: 500` | `400` — `{ error: "score must be a number between 0 and 100" }` |
| `PUT /students/:id` with `score: -5` | `400` — same message shape as above |
| `GET /students/123` (malformed id) | `400` — `{ error: "Invalid student id" }` |
| `GET /students/<well-formed but unknown id>` | `404` — `{ error: "Student not found" }` (unchanged from Day 10) |

### Common mistakes to watch for
- **Forgetting `.optional()` on the update validator** — every `PUT` that doesn't
  resend every field gets rejected as if a required field were missing.
- **Putting the `ValidationError`/`CastError` checks *after* the generic fallback** —
  the generic `res.status(err.statusCode || 500)...` line always runs and sends a
  response; anything after it that also tries to respond throws
  `ERR_HTTP_HEADERS_SENT`. Both new checks must come first and each `return` immediately.
- **Validating in the controller instead of a route-level middleware** — it works, but
  duplicates the same `if` checks in every controller function instead of declaring
  the rule once per route.
- **Forgetting `handleValidationErrors` after the rule chain** — without it,
  `express-validator` still *collects* errors onto the request, but nothing ever reads
  them or stops the controller from running with bad data.

### Stretch goal (optional, only if you finish early)
Add a custom rule rejecting a `name` that's purely numeric (e.g. `"12345"`) —
`.custom(value => isNaN(Number(value)))` — with its own `.withMessage(...)`. Confirm it
fires on `POST` but is skipped entirely on a `PUT` that doesn't send `name` at all.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
