# Day 21 — Teaching Lesson: Python Type Hints I — The Type System

> Companion to `README.md`. This is the material for the live session: a walkthrough
> of the concepts, then **the first 3 of 15 utility functions typed together**. The
> remaining 12 are yours, using the same approach, checked automatically by `mypy`.

## Objective
Write Python the way a professional team does: every function's inputs and outputs
declared, checked automatically, and self-documenting.

## 1. Why type hints exist

You've been writing Python for five weeks without ever declaring a type up front —
and everything still ran. That's real: Python doesn't *require* type hints to run
code. Type hints exist for a different reason: **catching mistakes before you run the
code at all**, and **making a function's contract obvious without reading its whole
body**.

```python
def average(numbers):
    return sum(numbers) / len(numbers)

average("hello")   # runs! then crashes deep inside sum(), with a confusing error
```
```python
def average(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)

average("hello")   # your editor (and mypy) flags this BEFORE you ever run it
```
Nothing about `list[float]` changes what the code *does* — Python still doesn't
enforce it at runtime. What changes is that your editor, and a tool called `mypy`
(Section 6), can now catch the mistake statically — by reading the code, not running
it — and VS Code can show you a function's expected inputs the instant you hover over
it.

## 2. Basic types, formally

You've used all of these informally since Week 1 — today you write them explicitly,
on every function signature from here on:
```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def add(a: int, b: int) -> int:
    return a + b

def average(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)

def is_passing(score: int) -> bool:
    return score >= 50
```
**Reading the syntax:** `name: str` means "the parameter `name` must be a `str`."
`-> str` (after the closing parenthesis) means "this function returns a `str`." A
function with no `-> ...` implicitly returns `None` — write `-> None` explicitly when
that's genuinely the intent, so it's clear it wasn't just forgotten.

## 3. Collection types: `list[...]`, `dict[...]`, `tuple[...]`

**Definition:** These generic types describe not just *that* something is a list or
dict, but *what's inside it* — `list[str]` is a list where every element is a `str`,
not just any list.

```python
def get_names(students: list[dict[str, int | str]]) -> list[str]:
    return [s["name"] for s in students]

def get_score_range(scores: list[int]) -> tuple[int, int]:
    return min(scores), max(scores)

student_scores: dict[str, int] = {"Ada": 91, "Kofi": 68}
```
`tuple[int, int]` is specific about *how many* elements and each one's type, in
order — different from `list[int]`, which says "any number of ints." Use `tuple` when
the shape is fixed (like "a min and a max," always exactly two, always in that
order); use `list` when the length varies.

## 4. Optional values: `| None`

**Definition:** A value that might legitimately be `None` needs that reflected in its
type — `int | None` means "an `int`, or `None`." You met this briefly on Day 7
(`min_score: int | None = None`) — today it's formalised as a general pattern, used
constantly.

```python
def find_student(students: list[dict], name: str) -> dict | None:
    for student in students:
        if student["name"] == name:
            return student
    return None
```
**Why this matters:** without `| None` in the return type, calling code has no signal
that it needs to handle a missing result — `find_student(...)["score"]` would look
completely reasonable to write, and then crash at runtime on a `None`. With
`dict | None` declared, your editor (and `mypy`) will flag exactly that mistake
before you run anything.

(You may see `Optional[int]` in older code or tutorials — it means exactly the same
thing as `int | None`. The `|` syntax, used throughout this track, is the modern,
preferred style, available from Python 3.10 onward.)

## 5. Typing functions with several parameters, defaults, and `*args`/`**kwargs`

```python
def create_student(name: str, score: int, course_id: int | None = None) -> dict:
    return {"name": name, "score": score, "course_id": course_id}

def total(*numbers: int) -> int:
    return sum(numbers)

def build_student(**fields: str) -> dict[str, str]:
    return fields
```
**Reading `*numbers: int`:** the type hint applies to *each individual* argument
collected into the tuple, not to the tuple itself — `total(1, 2, 3)` collects
`numbers` as `(1, 2, 3)`, and the hint says each of those is an `int`. Same idea for
`**fields: str` with keyword arguments collected into a dict.

## 6. `mypy` — checking your types without running your code

```bash
pip install mypy
mypy exercises/
```
**Definition:** `mypy` reads your code and its type hints, and reports every place
where a type hint is violated — a function called with the wrong argument type, a
return value that doesn't match the declared return type — all without executing a
single line. This is exactly the tool that would have caught `average("hello")` from
Section 1, instantly, before you ever ran it.

```
exercises/utils.py:12: error: Argument 1 to "average" has incompatible type "str"; expected "list[float]"
Found 1 error in 1 file
```
**Today's goal:** every function in `exercises/utils.py` fully typed, and
`mypy exercises/` reporting `Success: no issues found`.

---

## Worked example: typing the first 3 functions

### Problem statement
Given untyped versions of `average`, `find_student`, and `format_currency`, add
correct, complete type hints to each.

### Thinking it through, function by function
1. **`average(numbers)`** — takes a list of numbers, returns one number. Following
   Section 3-2: `numbers: list[float]`, `-> float`. (Using `float` rather than `int`
   here is deliberate — an average is very often not a whole number, and `float`
   safely accepts `int` values passed in too.)
2. **`find_student(students, name)`** — a list of dicts, a string, and a result that
   might not exist. Following Section 4: `students: list[dict]`, `name: str`,
   `-> dict | None`.
3. **`format_currency(amount)`** — a number in, a formatted string out — no
   surprises: `amount: float`, `-> str`.

### Solution
See [`exercises/utils.py`](./exercises/utils.py) — the first 3 functions are fully
typed and commented; the remaining 12 are stubs for you.

```python
def average(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)

def find_student(students: list[dict], name: str) -> dict | None:
    for student in students:
        if student["name"] == name:
            return student
    return None

def format_currency(amount: float) -> str:
    return f"{amount:,.0f} XAF"
```

Check it:
```bash
mypy exercises/utils.py
```

### What to notice
- None of the three function *bodies* changed at all from how you'd have written
  them in Week 1 — type hints are purely additive, describing what was already true,
  not changing behaviour.
- `dict` on its own (Section 3) is a valid but imprecise hint — `dict[str, int |
  str]` (as in Section 3's `get_names` example) is more precise when you know the key
  and value types. Use the more precise form when you reasonably can; a plain `dict`
  is an acceptable starting point when the shape is genuinely mixed or complex, as
  it is for a "student" dict.

---

## Your turn — type the remaining 12 functions

Open [`exercises/utils.py`](./exercises/utils.py). Each of the remaining 12 functions
has a docstring describing its parameters and return value — read it, decide the
right type hints using Sections 2-5 above, and add them to the function signature
(the function bodies are already complete and correct; you're only adding hints).

Run `mypy exercises/utils.py` after every few functions — fix each error as it
appears rather than typing all 12 blind and debugging at the end.

**Final checkpoint:** `mypy exercises/utils.py` reports `Success: no issues found in
1 source file`.

---

## Common mistakes to watch for
- **Hinting a mutable default argument's *type* correctly while still using a
  mutable default value**, e.g. `def f(items: list[int] = []):` — this is a
  well-known Python trap unrelated to typing itself (the same empty list is reused
  across every call!). Prefer `items: list[int] | None = None`, then
  `items = items or []` inside the function.
- **Forgetting `| None` on a return type that can genuinely return `None`** — this is
  the single most valuable habit from today; it's what turns a whole category of
  `NoneType has no attribute...` runtime crashes into an error caught before you run
  anything.
- **Over-precise types where a simpler one is genuinely fine** — `dict` instead of
  `dict[str, str | int | list]` for a genuinely mixed-shape dictionary is a
  reasonable, honest choice; forcing false precision is worse than a slightly loose
  but accurate hint. (Week 6, Day 2's Pydantic models are the *precise*, validated
  version of exactly these "mixed dict" shapes.)

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
