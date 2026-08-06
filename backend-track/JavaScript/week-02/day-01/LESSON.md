# Day 5 — Teaching Lesson: Asynchronous JavaScript

> Companion to `README.md`. This is the material for the live session: a walkthrough of
> the concepts, then **fetching one exchange rate with async/await, fully solved
> together** (`exercises/01-get-rate.js`). Today's task is picking ONE of three stub
> files in `exercises/` (currency dashboard, weather checker, or GitHub profile card)
> and finishing it the same way — all backend Node scripts, no browser involved.

## Objective
Master the concept every backend developer lives inside: code that waits — on a
network, a timer, a disk — without blocking everything else.

## 0. Why today is different: synchronous vs. asynchronous
**Definition:** Synchronous code runs one line at a time, each line waiting for the
previous one to finish before it starts. Asynchronous code lets a *slow* operation
(a network request, a timer, reading a big file) run in the background, so the rest of
the program isn't stuck waiting for it.

Everything you've written so far has been synchronous — line 2 never started before
line 1 finished. That breaks down the moment a line takes 300ms to talk to a server:
```js
const data = fetchFromServer();   // if this blocked for 300ms, EVERYTHING pauses —
console.log("done");              // including code that has nothing to do with the network
```
A backend server that blocks like this can only serve one visitor at a time. Today is
about the tools JavaScript gives you to avoid that.

## 1. Callbacks
**Definition:** A callback is a function you hand to another function, to be called
*later*, once some work finishes — instead of returning a value right away.

```js
setTimeout(() => {
  console.log("2 seconds passed");
}, 2000);

console.log("This logs FIRST");
```
`setTimeout` doesn't block — it schedules the callback and immediately lets the next
line run. So `"This logs FIRST"` prints before `"2 seconds passed"`, even though it's
written second. This is your first real look at asynchronous behaviour.

**Callback hell.** The problem shows up once one async step depends on another —
callbacks nest inside callbacks:
```js
setTimeout(() => {
  console.log("step 1");
  setTimeout(() => {
    console.log("step 2");
    setTimeout(() => {
      console.log("step 3");
    }, 1000);
  }, 1000);
}, 1000);
```
It works, but it grows sideways instead of downward, and error handling gets messy fast.
Promises exist to fix exactly this.

## 2. Promises
**Definition:** A promise is an object representing a value that isn't ready yet, but
will be — either successfully (**fulfilled**) or with an error (**rejected**) — at some
point in the future. Every promise starts **pending** and settles into exactly one of
those two outcomes, exactly once.

```js
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

wait(1000).then(() => console.log("1 second later"));
```
`.then()` runs once the promise fulfills. `.catch()` runs if it rejects. Chaining
`.then()` calls flattens the "sideways" callback hell shape back into a straight line:
```js
wait(1000)
  .then(() => { console.log("step 1"); return wait(1000); })
  .then(() => { console.log("step 2"); return wait(1000); })
  .then(() => console.log("step 3"))
  .catch((error) => console.error("something failed:", error));
```
Better than nested callbacks — but `async`/`await` below reads even closer to the
synchronous code you already know.

## 3. async/await
**Definition:** `async`/`await` is syntax that lets you write promise-based code that
*reads* top-to-bottom like ordinary synchronous code. `await` pauses execution inside
an `async` function until the promise it's waiting on settles — without blocking
anything else in the program.

```js
async function main() {
  console.log("start");
  await wait(1000);           // pauses here, but only this function — nothing else stalls
  console.log("1 second later");
}

main();
```
**The one hard rule:** `await` only works inside a function declared `async` (or at the
top level of a `.mjs`/ES module file). Using it anywhere else is a `SyntaxError`.

Rewriting the callback-hell example one more time — this is the version you'll actually
write from today on:
```js
async function steps() {
  await wait(1000);
  console.log("step 1");
  await wait(1000);
  console.log("step 2");
  await wait(1000);
  console.log("step 3");
}

steps();
```
Same behaviour as the nested-callback version, but it reads like a list of instructions.

## 4. The event loop (conceptually)
**Definition:** The event loop is the mechanism that lets JavaScript run one thing at a
time (the "call stack") while still handling background work like timers and network
responses — by holding finished background work in a queue and only running it once the
call stack is empty.

You don't need the full internals today — just this mental model, and the one behaviour
it explains:

**All synchronous code finishes first, no matter what.** A background task's callback,
even a promise that's already resolved, waits in a queue until the current stack is
empty.
```js
console.log("1");
setTimeout(() => console.log("2"), 0);
console.log("3");

// prints: 1, 3, 2  — even with a 0ms delay!
```
`setTimeout(..., 0)` doesn't mean "run immediately" — it means "run as soon as
everything currently running is done." This is why an `await` never freezes your whole
program: it only pauses the one `async` function it's inside of.

## 5. Fetching real data: `fetch()` in Node
**Definition:** `fetch(url)` sends an HTTP request and returns a promise that resolves
to a `Response` object once the response *headers* arrive. The body isn't parsed yet —
you call `.json()` (itself async — it also returns a promise) to read and parse it.

```js
const response = await fetch("https://open.er-api.com/v6/latest/USD");
const data = await response.json();
console.log(data.rates.XAF);
```
Node 18+ has `fetch` built in globally — no `import`, no package to install.

## 6. Error handling with try/catch
**Definition:** `try`/`catch` lets you run code that might throw, and handle the failure
in one place instead of letting it crash the program. With `async`/`await`, a rejected
promise behaves exactly like a thrown error — `await` "throws" it into the nearest
`catch`.

**Two different kinds of failure to watch for with `fetch`:**
- **Network failure** (no internet, DNS lookup fails, request times out) — the `fetch`
  promise itself *rejects*. `await fetch(...)` throws, and `catch` catches it.
- **HTTP error status** (404, 500, ...) — `fetch` still *fulfills* normally! It doesn't
  throw just because the server said "not found." You have to check `response.ok`
  yourself and throw if it's false.

```js
try {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`API responded with status ${response.status}`);
  }
  const data = await response.json();
  console.log(data);
} catch (error) {
  console.error("Could not fetch data:", error.message);
}
```

### Common mistakes to watch for
- **Forgetting `await`** — you get the `Promise` object itself in your variable, not
  the value inside it, and `console.log` prints something like `Promise { <pending> }`.
- **Forgetting `async` on the function** — `await` outside an `async` function (or
  outside a module's top level) is a `SyntaxError`, not a runtime bug.
- **Assuming `fetch` throws on 404/500** — it doesn't. Always check `response.ok`
  before trusting the body.
- **Forgetting `.json()` is also async** — `const data = response.json();` (no
  `await`) hands you a `Promise`, not your data.
- **An unhandled rejected promise crashes the script.** Any `await` on something that
  can fail (a network call, always) belongs inside a `try`/`catch`.
- **Mixing `.then()` chains inside an `async` function** — if you're already using
  `async`/`await`, stay consistent; reaching for `.then()` in the middle is usually a
  sign you meant to just `await` that line.

---

## Worked Exercise: fetch one exchange rate with async/await

This is the core building block behind Option A of today's task, solved together, live.
The `try`/`catch` + `response.ok` shape here is exactly what all three task options
reuse. Finishing whichever option you pick is yours to build the same way.

### Problem statement
Write an `async` function `getRate(base, target)` that fetches live exchange rates from
a free public API and returns the numeric rate from `base` to `target` (e.g. USD to
XAF) — returning `null` and logging a clear message instead of crashing if the network
request fails.

### Thinking it through
1. This is one network call → one `await fetch(...)`, wrapped in an `async` function
   (rule from section 3).
2. The API returns JSON with a `rates` object keyed by currency code → `await
   response.json()`, then index into `data.rates[target]`.
3. Two things can go wrong (section 6): the request itself can fail (no internet), or
   the API can respond with a non-OK status. Both need to end up in the same `catch`,
   with a message that says *what* failed, not just "error."
4. The caller shouldn't have to guess whether it worked — return `null` on failure so
   calling code can check for that explicitly.

### Solution
See [`exercises/01-get-rate.js`](./exercises/01-get-rate.js) — fully solved and commented.

```js
async function getRate(base, target) {
  const url = `https://open.er-api.com/v6/latest/${base}`;

  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`API responded with status ${response.status}`);
    }

    const data = await response.json();
    return data.rates[target];
  } catch (error) {
    console.error(`Could not fetch rate ${base} -> ${target}:`, error.message);
    return null;
  }
}

async function main() {
  const rate = await getRate("USD", "XAF");

  if (rate !== null) {
    console.log(`1 USD = ${rate} XAF`);
  }
}

main();
```

Run it:
```bash
node exercises/01-get-rate.js
```

### What to notice
- `main()` doesn't need its own `try`/`catch` — `getRate` already swallowed the error
  and returned `null`. `main` just checks for that, the same "quiet failure" shape as
  `.find()` returning `undefined` back in Day 3.
- Nothing here uses `.then()` — every asynchronous step is a plain `await`, read
  top-to-bottom.
- `base` and `target` are parameters, not hardcoded — this function is already reusable
  for any currency pair, which is exactly what a dashboard needs to loop over.

---

## Your turn — today's task

Pick **one** of the three (all pure backend: Node scripts that print to the terminal —
no browser, no HTML involved anywhere). Stub files with the fetch/error-handling half
already wired up are in `exercises/`, each with the problem statement and expected
sample output in a comment block — write your code where it says `// TODO`.

| # | Task | File | API used |
|---|------|------|----------|
| A | Currency dashboard | `exercises/02-currency-dashboard.js` | open.er-api.com (exchange rates) |
| B | Weather checker | `exercises/03-weather-checker.js` | api.open-meteo.com (weather) |
| C | GitHub profile card | `exercises/04-github-profile-card.js` | api.github.com (profiles) |

Option C deliberately exercises the `response.ok` gotcha from section 6: a made-up
username doesn't fail the network call — GitHub responds with a normal 404, and your
code has to notice that itself instead of crashing on `undefined` fields.

Whichever you pick must have:
- **Only `async`/`await`** — no `.then()` chains.
- **Formatted output** — aligned columns or a clear labelled summary, not a raw
  `console.log(data)` dump.
- **Graceful network-error handling** — if the request fails (bad connection, API
  down), the program prints a friendly message and exits cleanly. It must never crash
  with an unhandled promise rejection.

Same process as the worked exercise: read the problem in the file's comment block, say
the plan out loud, then write it. Run it the same way:
`node exercises/0X-name.js`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
