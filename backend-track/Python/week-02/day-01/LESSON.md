# Day 5 — Teaching Lesson: Asynchronous Python

> Companion to `README.md`. This is the material for the live session: a walkthrough
> of the concepts, then **fetching one exchange rate with async/await, fully solved
> together** (`exercises/01_get_rate.py`). Today's task is picking ONE of three stub
> files in `exercises/` (currency dashboard, weather checker, or GitHub profile card)
> and finishing it the same way.

## Objective
Master the concept every backend developer lives inside: code that waits — on a
network, a timer, a disk — without blocking everything else.

## 0. Setting up a virtual environment (properly, for the first time)

**Definition:** A virtual environment is an isolated copy of Python and its installed
packages, kept inside one project folder. Day 1 explained *why* this matters — today
you actually create one, because today is the first day you `pip install` anything.

```bash
python3 -m venv venv          # creates a "venv" folder — your isolated Python
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```
Your terminal prompt now shows `(venv)` at the start — that means every `pip install`
from here on only affects *this* project, not your whole computer. Do this at the
start of every coding session from today onward. To leave it: `deactivate`.

Install today's one package:
```bash
pip install httpx
```
**Definition:** `httpx` is a library for making HTTP requests from Python — it's what
lets your program act as a *client*, the same role your browser plays, but from a
script.

## 1. Why today is different: synchronous vs. asynchronous

**Definition:** Synchronous code runs one line at a time, each line waiting for the
previous one to finish before it starts. Asynchronous code lets a *slow* operation (a
network request, a timer, reading a big file) run in the background, so the rest of
the program isn't stuck waiting for it.

Everything you've written so far has been synchronous — line 2 never started before
line 1 finished. That breaks down the moment a line takes 300ms to talk to a server:
```python
data = fetch_from_server()   # if this blocked for 300ms, EVERYTHING pauses —
print("done")                 # including code that has nothing to do with the network
```
A backend server that blocks like this can only serve one visitor at a time. Today is
about the tools Python gives you to avoid that.

## 2. `async` and `await`

**Definition:** `async def` declares a function as a **coroutine** — a function that
can be paused and resumed. `await` pauses execution inside that coroutine until
whatever it's waiting on finishes — without blocking anything else in the program.

```python
import asyncio

async def wait_a_second():
    await asyncio.sleep(1)
    print("1 second later")

asyncio.run(wait_a_second())
```
**Definition:** `asyncio` is Python's built-in library for writing and running
asynchronous code. `asyncio.run(...)` is how you start the whole async machine from
ordinary, synchronous code — you'll use it once, at the very bottom of your script.

**The one hard rule:** `await` only works inside a function declared `async def`.
Using it anywhere else is a `SyntaxError`. This mirrors Day 1's indentation rule —
it's a rule the language enforces for you, not a style choice.

## 3. Running things one after another vs. at the same time

Two `await`s in a row still run one after another — that alone doesn't make things
faster, just non-blocking:
```python
async def steps():
    await asyncio.sleep(1)
    print("step 1")
    await asyncio.sleep(1)
    print("step 2")

asyncio.run(steps())   # takes about 2 seconds total, printed in order
```
To actually run several things **at the same time**, use `asyncio.gather`:
```python
async def steps_together():
    await asyncio.gather(
        asyncio.sleep(1),
        asyncio.sleep(1),
    )
    print("both done")

asyncio.run(steps_together())   # takes about 1 second total, not 2
```
You won't need `gather` heavily today, but recognise it — it's how you'll fetch
several things from an API at once later in the track, instead of one at a time.

## 4. The event loop (conceptually)

**Definition:** The event loop is the mechanism that lets your program run one thing
at a time (like a single cashier) while still handling background work — like
waiting on a network response — by holding finished background work in a queue and
only picking it up once the currently running code is done.

You don't need the full internals today — just this mental model: **an `await` never
freezes your whole program, only the one coroutine it's inside of.** That's the whole
reason this style of code exists — it lets one Python program serve many users at
once, each one's slow network wait happening in the background while others are
handled.

## 5. Fetching real data: `httpx` with `async`/`await`

**Definition:** An HTTP client sends a request and gives you back a response object
once it arrives. `httpx.AsyncClient` is the async version — it doesn't block your
program while it waits for the network.

```python
import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://open.er-api.com/v6/latest/USD")
        data = response.json()
        print(data["rates"]["XAF"])

asyncio.run(main())
```
**Definition:** `async with` is the async version of Python's `with` statement — it
opens a resource (here, an HTTP connection pool) and guarantees it gets cleanly
closed afterward, even if an error happens in between.

`response.json()` here is *not* async in `httpx` (unlike some JS equivalents) — it
just parses the already-downloaded response body as JSON and gives you back a Python
dictionary.

## 6. Error handling with `try`/`except`

**Definition:** A `try`/`except` block lets you attempt something that might fail,
and handle the failure gracefully instead of letting your whole program crash.

```python
try:
    response = await client.get(url)
    response.raise_for_status()   # raises an exception if status is 4xx or 5xx
    data = response.json()
except httpx.RequestError:
    print("Network problem — couldn't reach the server.")
except httpx.HTTPStatusError as error:
    print(f"Server responded with an error: {error.response.status_code}")
```
**Definition:** `response.raise_for_status()` checks the response's status code and
raises an exception if it's an error code (`4xx` or `5xx`) — a clean way to turn "the
server said something went wrong" into a `try`/`except`-able error, instead of
silently continuing with bad data.

---

## Worked Exercise: fetch one exchange rate

### Problem statement
Write an async function that fetches the current USD-to-XAF exchange rate from a free
public API and prints it in a friendly format, handling the case where the network
request fails.

### Thinking it through
1. We need an `async def` function, since we're making a network call (Section 2).
2. Inside it, open an `httpx.AsyncClient` and `await client.get(url)` (Section 5).
3. Wrap the call in `try`/`except` so a dropped connection doesn't crash the whole
   script (Section 6).
4. Pull the specific number we want out of the parsed JSON dictionary, and format it
   for a human to read.

### Solution
See [`exercises/01_get_rate.py`](./exercises/01_get_rate.py) — fully solved and
commented.

```python
import asyncio
import httpx

async def get_usd_to_xaf_rate():
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            rate = data["rates"]["XAF"]
            print(f"1 USD = {rate} XAF")
    except httpx.RequestError:
        print("Network problem — could not reach the exchange rate service.")
    except httpx.HTTPStatusError as error:
        print(f"Exchange rate service returned an error: {error.response.status_code}")

asyncio.run(get_usd_to_xaf_rate())
```

Run it:
```bash
python3 exercises/01_get_rate.py
```

### What to notice
- `timeout=10` caps how long we'll wait before giving up — without it, a stalled
  network connection could hang forever.
- Two separate `except` blocks catch two genuinely different failures — "couldn't
  reach the server at all" vs. "reached it, but it said something's wrong" — and give
  the user a different, useful message for each.
- This exact shape — async function, `try`/`except` around an `httpx` call, pull a
  value out of the parsed JSON — is what every remaining stub file below reuses.

---

## Your turn — pick ONE stub and finish it

All three live in `exercises/`. Pick the one that interests you most; they all
practice the same skills.

| File | What it does |
|---|---|
| `exercises/02_currency_dashboard.py` | Fetch and display several exchange rates (USD, EUR, GBP → XAF) in one formatted table |
| `exercises/03_weather_checker.py` | Fetch and display the current weather for a city using a free weather API |
| `exercises/04_github_profile_card.py` | Fetch and display a GitHub user's public profile info (name, bio, follower count) |

Each stub file has the problem statement, the free API to use, and `# TODO` markers
in a comment block. Run yours the same way: `python3 exercises/0X_name.py`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
