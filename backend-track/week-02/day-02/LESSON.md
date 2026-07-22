# Day 6 — Teaching Lesson: Node.js In Depth

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered step
> builds on the one before it, with a tiny bit of code to run and check before moving
> on. Don't skip ahead: Step 5 assumes Step 4 already works.
>
> By the end you'll have built a real (if small) backend server by hand, with no
> framework — which is exactly why tomorrow's Express lesson will feel like a relief
> instead of more new syntax.

## Objective
Understand the platform itself — npm, modules, and what Node gives you beyond the
language — by building one thing Express normally does for you: a raw HTTP server.

## What you're building today
A small server that can:
- report that it's alive (`/health`)
- list students, look one up by id, and add a new one (`/students`)
- remember those students even after you restart the server (a JSON file on disk)
- report a bit about the computer it's running on (`/system-info`)

That's a lot of new ideas, so we go **one small piece at a time**. If something feels
confusing, re-read the step just before it — everything here is cumulative.

---

## Step 1 — What is npm, and what is `package.json`?
**Definition:** npm is Node's package manager — a tool that downloads other people's
code for you to use, and can run little "shortcut commands" for your project. Think of
`package.json` as your project's **ID card**: it says what the project is called, what
commands it supports, and which extra packages it needs to run.

Try it — inside `exercises/`, this file already exists, but here's how you'd create one
from scratch on a new project:
```bash
npm init -y
```
That writes a starter `package.json` for you. Open the one already in `exercises/` and
look at it now — it's short, just a name and a `"start"` script.

### Scripts — shortcut commands
```json
"scripts": {
  "start": "node server.js"
}
```
Instead of typing `node server.js` every time, you type:
```bash
npm start
```
`start` (and `test`) are special — they work without the word `run`. Every *other*
script name needs `npm run <name>`, e.g. `npm run dev`. You'll add a `dev` script
yourself in Step 6.

### Two kinds of dependencies
- **`dependencies`** — code your app needs to actually *run* (you'll add `express`
  tomorrow). Installed with `npm install <package>`.
- **`devDependencies`** — tools you only need while *developing*, like `nodemon`
  (restarts your server automatically when you save a file). Installed with
  `npm install --save-dev <package>`.

**Why this matters:** whichever list a package is in, npm writes it into
`package.json` for you. That file (plus `package-lock.json`, which npm also writes) is
the *complete record* of what your project needs — which is why the actual downloaded
code, `node_modules/`, never needs to be committed to git. Anyone can regenerate it
with one command: `npm install`.

**Checkpoint:** open `exercises/package.json` right now and find the `"scripts"`
block. That's the only part you'll be editing today.

---

## Step 2 — CommonJS vs ES Modules (two ways to split code into files)
**Definition:** these are two different systems Node uses for sharing code between
files. You already met one of them last week.

| | Import syntax | Export syntax | Default for |
|---|---|---|---|
| **CommonJS** | `require("./math")` | `module.exports = {...}` | plain `.js` files |
| **ES Modules (ESM)** | `import { double } from "./math.mjs"` | `export function double() {}` | `.mjs` files (what you used last week) |

```js
// CommonJS — math.js
function double(n) { return n * 2; }
module.exports = { double };

// app.js
const { double } = require("./math");
```

Today's server file is plain **CommonJS** (`server.js`, using `require`) — that's the
default the moment a file just ends in `.js` with no special config. It's still the
style you'll see in the majority of real-world Node code, so you need to be
comfortable in both, not just the `import`/`export` syntax from last week.

**One rule to remember:** never mix `require` and `import` in the *same file* — Node
will throw a `SyntaxError`. Pick one per file.

**Checkpoint:** open `exercises/server.js` and confirm the very first line is
`const http = require("http");` — that's CommonJS.

---

## Step 3 — Meet the built-in toolbox: `fs`, `path`, `os`
These three modules ship with Node — no `npm install` needed, just `require` them.
We'll look at each in isolation first, with tiny throwaway examples, before using them
for real in the big assignment below.

### 3a. `fs` — reading and writing files
**Definition:** `fs` ("file system") lets your code read from and write to files on
disk, the same way you'd open/save a file by hand — just done in code.

```js
const fs = require("fs");

// Synchronous — simplest, but blocks everything until the read finishes.
const data = fs.readFileSync("notes.txt", "utf-8");
console.log(data);

// Asynchronous — doesn't block. Use this inside a running server.
fs.readFile("notes.txt", "utf-8", (err, data) => {
  if (err) {
    console.error("Could not read file:", err.message);
    return;
  }
  console.log(data);
});
```
**Rule of thumb:** the `Sync` versions are fine for quick one-off scripts. Inside a
server, prefer the callback versions — `readFileSync` would freeze *every other
request* while it waits on the disk.

### 3b. `path` — building file paths that work on any computer
**Definition:** `path` builds file paths for you, so you never have to hand-type `/` or
`\` and worry about which operating system you're on.

```js
const path = require("path");

path.join("data", "students.json");
// -> "data/students.json" on Mac/Linux, "data\\students.json" on Windows
```
`path.join()` is the one you'll use constantly. Today's assignment uses it to build the
path to a data file that works no matter whose laptop runs the code.

### 3c. `os` — asking the computer about itself
**Definition:** `os` reports information about the machine Node is currently running
on — not your project, the actual physical (or virtual) computer.

```js
const os = require("os");

os.platform();      // "linux", "darwin" (Mac), or "win32"
os.cpus().length;    // how many CPU cores this machine has
os.totalmem();       // total RAM, in bytes
```

**Checkpoint:** in a scratch file (or the Node REPL — just type `node` in your
terminal), try `require("os").platform()` and see your own OS name print out.

---

## Step 4 — Your first raw server: "Hello, Server"
**Definition:** `http` is the module every Node web framework — including Express — is
built on top of. `http.createServer()` takes one function, and Node calls that function
for *every single request* that comes in.

Before touching `exercises/server.js`, type this into a **new, throwaway** file just to
see the shape:
```js
const http = require("http");

const server = http.createServer((req, res) => {
  res.end("Hello from a raw Node server!");
});

server.listen(3000, () => {
  console.log("Server running at http://localhost:3000");
});
```
Run it (`node yourfile.js`) and open `http://localhost:3000` in a browser. You should
see the plain text. That's it — that's a working web server, four lines of actual
logic. Stop it with `Ctrl+C` before moving on (only one program can use port 3000 at a
time).

### `req` and `res`, in one sentence each
- **`req`** ("request") — everything about what the visitor asked for:
  `req.method` (`"GET"`, `"POST"`, ...) and `req.url` (`"/health"`, `"/students"`, ...).
- **`res`** ("response") — what you build and send back. Nothing goes to the browser
  until you call `res.end(...)`.

**Checkpoint:** you just ran a real server and got a real response in your browser.
Everything from here is adding *more* to that same idea.

---

## Step 5 — Upgrading to JSON responses
Plain text is fine for a demo, but every real API responds with JSON. Two things
change from Step 4:

```js
const http = require("http");

const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ message: "Hello, JSON!" }));
});

server.listen(3000);
```
- **`res.writeHead(statusCode, headers)`** — sets the status code and headers. You must
  call this *before* `res.end()`, never after. `Content-Type: application/json` is what
  tells the browser (or Postman, or your frontend code) "the text I'm sending is JSON,
  parse it as such."
- **`JSON.stringify(...)`** — turns a JavaScript object into the text format JSON
  requires. `res.end()` can only send text, never a raw object.

Because you'll do these two steps on *every single route* today, `exercises/server.js`
already wraps them in one small helper for you:
```js
function sendJson(res, statusCode, data) {
  res.writeHead(statusCode, { "Content-Type": "application/json" });
  res.end(JSON.stringify(data));
}
```
From here on, every route is just: check `req.method`/`req.url`, then call
`sendJson(res, someStatusCode, someObject)`.

---

## Step 6 — Worked example: building `GET /health` together

This is the one route solved live, in the session — the shape every route you write
today reuses.

### Problem statement
Add a `GET /health` route that responds `200` with a JSON body reporting the server's
status and how long it's been running, in seconds.

### Thinking it through
1. One function runs for *every* request (Step 4) → check `req.method === "GET"` and
   `req.url === "/health"` *before* doing anything else, and only handle the request if
   both match.
2. "How long it's been running" needs a fixed starting point, captured **once**, when
   the server first starts — `const startedAt = Date.now()`, written outside the
   handler function, at the top of the file. Inside the route, `Date.now() - startedAt`
   gives the elapsed milliseconds; divide by 1000 and round down for seconds.
3. Respond using the `sendJson` helper from Step 5.
4. Anything that doesn't match *any* known route still needs *some* response — a `404`
   with a small JSON error body. Otherwise those requests just hang forever, which
   looks like the server crashed even though it didn't.

### Solution
See [`exercises/server.js`](./exercises/server.js) — this part is already written and
commented for you.

```js
const http = require("http");

const PORT = 3000;
const startedAt = Date.now();

function sendJson(res, statusCode, data) {
  res.writeHead(statusCode, { "Content-Type": "application/json" });
  res.end(JSON.stringify(data));
}

const server = http.createServer((req, res) => {
  if (req.method === "GET" && req.url === "/health") {
    const uptimeSeconds = Math.floor((Date.now() - startedAt) / 1000);
    sendJson(res, 200, { status: "ok", uptime: uptimeSeconds });
    return;
  }

  sendJson(res, 404, { error: "Not found" });
});

server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
```

Run it:
```bash
cd exercises
npm start
```
Then visit `http://localhost:3000/health` — you should see something like
`{"status":"ok","uptime":3}`. Try `http://localhost:3000/anything-else` too — you
should get the `404` instead.

### What to notice
- The `return` right after `sendJson` in the `/health` block matters. Without it,
  execution would keep going and *also* hit the `404` response below — two responses
  for one request, which crashes with an error.
- `startedAt` is captured once, at the top of the file — not inside the request
  handler. If it were inside `createServer`'s callback, it would reset on *every*
  request, and uptime would always read `0`.

### Common mistakes to watch for (today's whole session)
- **Forgetting `res.end()` anywhere** — the request just hangs, no error, no response.
- **Setting headers after calling `res.end()`** — `writeHead` must come *before* `end`.
- **Comparing `req.url` too loosely** — `/students` and `/students/` are different
  strings to `===`. Type URLs exactly when testing.
- **Mixing `require` and `import`** — see Step 2. This file is CommonJS throughout.

---

## Your turn — the big assignment

Now the real project: extend `exercises/server.js` one step at a time. Each TODO
comment in the file matches a numbered step below — do them **in order**, and test
each one in the browser (or `curl`) before starting the next. Don't try to write all
five at once.

### Step 1 — `GET /students`: list everyone
Respond `200` with `{ students }`, using the `students` array already declared near
the top of the file. Exact same shape as `/health`.
**Test:** `http://localhost:3000/students` → all three seed students.

### Step 2 — `GET /students/:id`: one student
There's no automatic route-parameter magic here like Express has — you split the URL
string yourself:
```js
const parts = req.url.split("/");   // "/students/2" -> ["", "students", "2"]
const id = Number(parts[2]);
```
Match only when `req.method` is `GET`, `parts[1] === "students"`, and there's a third
part (`parts.length === 3`) — that keeps it from also matching plain `/students`
above. Find the student whose `id` matches. Found → `200` with that student. Not
found → `404` with `{ error: "Student not found" }`.
**Test:** `/students/2` → Kofi. `/students/99` → the 404.

### Step 3 — Make it survive a restart (persistence with `fs` + `path`)
Right now, restarting the server resets everyone back to the seed data. Fix that:
1. At the top of the file, uncomment (or add) `const fs = require("fs");` and
   `const path = require("path");`.
2. Build two paths with `path.join`: the folder `data/` and the file
   `data/students.json`, both relative to `__dirname` (a variable Node gives every
   file — the folder that file lives in).
3. On startup: if `students.json` already exists (`fs.existsSync`), load it with
   `fs.readFileSync` + `JSON.parse` and use *that* instead of the seed array. If it
   doesn't exist, create the `data/` folder (`fs.mkdirSync(dataDir, { recursive: true
   })`) and write the seed array out with `fs.writeFileSync` + `JSON.stringify`.
4. Write one small `saveStudents()` function that repeats that same `writeFileSync`
   line, so Step 4 can call it whenever the list changes.

**Test:** run the server once, then stop it (`Ctrl+C`) and start it again — the same
students should still be there, now loaded from `data/students.json` instead of the
hardcoded array.

### Step 4 — `POST /students`: add a new student
This is the step that shows you the most of what Express normally hides. There's no
`express.json()` here — the request body arrives over time, in pieces, and you collect
it yourself:
```js
let body = "";
req.on("data", (chunk) => { body += chunk; });
req.on("end", () => {
  const newStudent = JSON.parse(body);   // expects { name, score }
  newStudent.id = students.length + 1;
  students.push(newStudent);
  saveStudents();
  sendJson(res, 201, newStudent);
});
return;
```
**The one thing that trips people up:** everything that responds to the request has to
happen *inside* the `req.on("end", ...)` callback — the body genuinely hasn't finished
arriving yet by the time the function reaches the line after `req.on(...)`.

**Test:** with the server running, in a second terminal:
```bash
curl -X POST http://localhost:3000/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Bruno","score":77}'
```
You should get back the new student with an `id`. Then check `/students` again — Bruno
should be in the list, and still there after a restart.

### Step 5 — `GET /system-info`: about this machine
Using what you learned in Step 3c, add `const os = require("os");` at the top, and
respond `200` with:
```json
{ "platform": "linux", "cpuCount": 8, "totalMemoryMB": 16384 }
```
using `os.platform()`, `os.cpus().length`, and
`Math.round(os.totalmem() / 1024 / 1024)`.

### Step 6 — write the `dev` npm script
Back in Step 1 you saw the `scripts` block in `package.json`. Now add to it yourself:
```bash
cd exercises
npm install --save-dev nodemon
```
Then add a `"dev"` entry to `"scripts"` that runs `server.js` with `nodemon` instead of
`node`. Run it with `npm run dev`, edit and save `server.js` while it's running, and
confirm the server restarts on its own — that's the whole benefit over plain `node`.

### Step 7 — double-check the `.gitignore`
One already exists in `exercises/`, ignoring `node_modules/` and `data/` (the folder
Step 3 generates — nobody else needs *your* local student list committed to git).
Before you push, run `git status` and confirm neither shows up as untracked. If one
does, figure out why before committing anything.

### Final checklist — every route should behave like this
| Route | Method | Expected result |
|---|---|---|
| `/health` | GET | `200` — `{ status: "ok", uptime: <number> }` |
| `/students` | GET | `200` — `{ students: [...] }` |
| `/students/2` | GET | `200` — Kofi's record |
| `/students/99` | GET | `404` — `{ error: "Student not found" }` |
| `/students` | POST | `201` — the new student, now with an `id` |
| `/system-info` | GET | `200` — `{ platform, cpuCount, totalMemoryMB }` |
| `/anything-else` | GET | `404` — `{ error: "Not found" }` |

### Stretch goal (optional, only if you finish early)
Add a `DELETE /students/:id` route that removes a student and saves the change. You'll
build the *real* version of this — with Express, properly — tomorrow, so don't worry if
you don't get to it today.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
