# Day 3 — Teaching Lesson: Functions, Lists & Dictionaries

> Companion to `README.md`. This is the material for the live session: a walkthrough
> of the concepts, then **the first part of the task of the day fully solved
> together** (the student data + the `average` function). The rest — `top_student`
> and `above_average` — is yours to build using the same approach.

## Objective
Organise code into functions and model real-world data — the bread and butter of
backend work.

## 1. Functions and parameters
**Definition:** A function is a named, reusable block of code. A parameter is a named
placeholder for an input value the function needs to do its job — you supply the real
value (the *argument*) when you call the function.

```python
def shout(message):             # "message" is the parameter
    return message.upper() + "!"

shout("hello")                  # "hello" is the argument -> "HELLO!"
```
`return` is what sends a value back to whoever called the function. Without
`return`, a function produces `None` — Python's "nothing" value.

**Several parameters, in order:**
```python
def describe_student(name, score):
    return f"{name} scored {score}"

describe_student("Ada", 91)   # "Ada scored 91"
```
Arguments are matched to parameters *by position* by default — `describe_student(91,
"Ada")` would silently produce nonsense. Python also lets you pass arguments *by
name*, which avoids this entirely and reads more clearly once a function has more
than two or three parameters:
```python
describe_student(name="Ada", score=91)   # order no longer matters
```

**Default parameters** — a fallback value used only when the argument is omitted:
```python
def greet(name="student"):
    return f"Welcome, {name}"

greet()          # "Welcome, student" — no argument given, default kicks in
greet("Ada")     # "Welcome, Ada"
```

**Forgetting `return` is the single most common bug this week.** A function with no
`return` statement doesn't fail — it just quietly hands back `None`, and that `None`
then breaks whatever called the function:
```python
def average(students):
    scores = [s["score"] for s in students]
    total = sum(scores)
    total / len(scores)   # BUG: no return statement

print(average(students))   # None — the math ran, but nothing came back
```
If you ever see `None` where you expected a number, check for a missing `return`
before you check anything else.

## 2. Lists and key methods
**Definition:** A list is an ordered collection of values, stored under one variable
name and accessed by position (starting at index 0).

```python
scores = [72, 88, 91, 60]
scores[0]          # 72 — first element
len(scores)         # 4
scores.append(75)   # adds 75 to the end — mutates the list in place
```

Several tools you'll use constantly:

- **List comprehension** — the Python way to build a new list by transforming or
  filtering another one, in a single readable line.
  ```python
  [s * 2 for s in scores]              # transform every element -> [144, 176, 182, 120]
  [s for s in scores if s >= 80]       # keep only elements that pass a test -> [88, 91]
  ```
  Read `[s * 2 for s in scores]` as "for each `s` in `scores`, give me `s * 2`." This
  single tool replaces what `.map()` and `.filter()` do in some other languages.
- **`sum()`, `max()`, `min()`, `len()`** — built-in functions that work on any list of
  numbers.
  ```python
  sum(scores)   # 316
  max(scores)   # 91
  min(scores)   # 60
  ```
- **`sorted()`** — returns a **new**, sorted list, leaving the original untouched.
  ```python
  sorted(scores)                  # [60, 72, 88, 91] — ascending by default
  sorted(scores, reverse=True)    # [91, 88, 72, 60] — descending
  ```
- **`.sort()`** — the list *method* version — sorts the list **in place** (mutates
  it, returns `None`). Prefer `sorted()` when you want to keep the original order
  available elsewhere.
- **`in`** — does the list contain this exact value?
  ```python
  91 in scores   # True
  ```
- **`any()` / `all()`** — combined with a comprehension, these answer "does at least
  one / do all elements pass this test?"
  ```python
  any(s < 60 for s in scores)    # False — nobody failed
  all(s >= 60 for s in scores)   # True — everybody passed
  ```

## 3. Dictionaries
**Definition:** A dictionary is a collection of `key: value` pairs used to represent
one real-world "thing" with several named properties — Python's equivalent of a JSON
object, which you'll meet formally on Day 4.

```python
student = {
    "name": "Ada",
    "score": 91,
    "address": {                # nested dictionary
        "city": "Douala",
        "country": "Cameroon",
    },
}

student["name"]              # "Ada" — square brackets, not dot notation
student["address"]["city"]   # "Douala" — chain into the nested dict
```

**Reading a key that might not exist safely** — `student["zip"]` would raise a
`KeyError` and crash your program. Use `.get()` instead, which returns `None` (or a
default you choose) if the key is missing:
```python
student.get("zip")            # None — no crash
student.get("zip", "N/A")     # "N/A" — your own fallback
```

**Checking whether a key exists** before reading it:
```python
"address" in student   # True
```

## 4. Lists of dictionaries
**Definition:** Combining the two above — a list where every element is a dictionary
with the same shape. This is the standard shape of real data (database rows, API
responses), so it's worth getting comfortable with it early — you'll live inside this
shape for the rest of the track.

```python
students = [
    {"name": "Ada", "score": 91},
    {"name": "Kofi", "score": 68},
    {"name": "Zara", "score": 84},
]

[s["name"] for s in students]                    # ["Ada", "Kofi", "Zara"]
[s for s in students if s["score"] >= 80]        # Ada's and Zara's dicts
```

**Sorting a list of dictionaries** needs a `key=` function that tells `sorted()`
which field to compare:
```python
sorted(students, key=lambda s: s["score"], reverse=True)   # highest score first
```
**Definition:** `lambda` creates a small, unnamed, one-line function — useful exactly
in places like this, where you need a tiny function just to hand to another function
and don't want to give it a full name with `def`.

### Common mistakes to watch for
- **Comparing dictionaries built separately with `==`** — this one *does* work in
  Python (unlike some other languages) for comparing contents, but comparing a
  dictionary to the *wrong* dictionary is still an easy typo to make. Compare specific
  fields (`a["score"] == b["score"]`) when in doubt.
- **`KeyError` from a missing dictionary key** — use `.get()` when a key might not be
  there.
- **Forgetting `sorted()` needs a `key=` for anything other than plain numbers or
  strings** — sorting a list of dictionaries with plain `sorted(students)` raises a
  `TypeError`, because Python doesn't know which field to compare.
- **Off-by-one / empty results** — filtering with a comprehension that matches
  nothing returns an empty list `[]`, not an error. Always consider what happens
  downstream if nothing matched.

---

## Worked Exercise: student data + `average()`

This is the first part of today's task, solved together, live. The rest —
`top_student` and `above_average` — you build the same way, as stub files in
`exercises/`.

### Problem statement
Model a small list of students (name + score) as a list of dictionaries, then write a
function `average(students)` that returns the mean of all their scores.

### Thinking it through
1. Data shape first: each student is `{"name": ..., "score": ...}` → a list of those
   is a **list of dictionaries** (section 4 above).
2. "Average" = sum of all scores ÷ how many there are. Summing everything means
   visiting every element → a list comprehension to pull out just the scores, then
   `sum()`.
3. Wrap it in a **function** so it's reusable for any list of students, not just this
   one.

### Solution
See [`exercises/01_student_average.py`](./exercises/01_student_average.py) — fully
solved and commented.

```python
students = [
    {"name": "Ada", "score": 91},
    {"name": "Kofi", "score": 68},
    {"name": "Zara", "score": 84},
]

def average(students):
    scores = [s["score"] for s in students]
    return sum(scores) / len(scores)

print(average(students))   # 81.0
```

Run it:
```bash
python3 exercises/01_student_average.py
```

### What to notice
- `average` doesn't care about `name` at all — it only pulls out `score`. Functions
  that do one clear thing are easier to reuse and to test.
- Dividing with `/` always gives a `float` in Python, even when the result is a whole
  number (`81.0`, not `81`) — that's expected here.
- The same `students` list will be reused, unchanged, by `top_student` and
  `above_average` below.

---

## Your turn — finish the task of the day

| # | Exercise | File | Concept practiced |
|---|----------|------|--------------------|
| 2 | Top student | `exercises/02_top_student.py` | functions, comparison, iterating a list |
| 3 | Above-average students | `exercises/03_above_average_students.py` | comprehensions, calling one function from another |

Same process as the worked exercise: read the problem in the file's comment block,
say the plan out loud, then write it where it says `# TODO`.

Run each one the same way: `python3 exercises/0X_name.py`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
