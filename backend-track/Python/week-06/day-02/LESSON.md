# Day 22 — Teaching Lesson: Type Hints II — Enums, Literals & Deeper Types

> Companion to `README.md`. This is the material for the live session: a walkthrough
> of the concepts, then **`Enum` and `Literal` fully solved together**. `TypedDict`,
> `dataclass`, and the generic function are yours, using the same approach.

## Objective
Reach for the right precise type for the right job.

## 1. `Enum` — a fixed, named set of values

**Definition:** An `Enum` (enumeration) defines a small, fixed set of named
constants — used when a value should only ever be one of a *known, specific* set of
options, like a status field, and you want that constraint enforced and
self-documenting, rather than relying on everyone remembering to type the string
correctly.

```python
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

def describe_status(status: OrderStatus) -> str:
    if status == OrderStatus.DELIVERED:
        return "Your order has arrived!"
    return f"Order is {status.value}"
```
**Why `class OrderStatus(str, Enum)`, not just `class OrderStatus(Enum)`:**
inheriting from `str` as well means each member *is* a string (`OrderStatus.PENDING
== "pending"` is `True`), which makes it work seamlessly as a Pydantic field type and
serialise cleanly to JSON — this specific pattern (`str, Enum`) is what you'll use in
every FastAPI project from here on, any time a field should be one of a fixed set of
options.

**Compare to a plain string, and see what you gain:**
```python
def describe_status_unsafe(status: str) -> str:   # any string at all is "valid"
    ...

describe_status_unsafe("delivver")   # typo! runs fine, silently wrong
describe_status(OrderStatus.DELIVERED)   # the only way to get this exact value
```
A typo'd plain string sails through silently. An `Enum` value is checked by your
editor and `mypy` — there's no way to accidentally pass `"delivverd"` where an
`OrderStatus` is expected.

## 2. `Literal` — a fixed set of specific values, without an `Enum` class

**Definition:** `Literal[...]` restricts a type hint to one of a specific, listed set
of literal values — a lighter-weight alternative to `Enum` for when you don't need a
full class, just a constraint on the allowed values of, say, one function parameter.

```python
from typing import Literal

def sort_students(students: list[dict], order: Literal["asc", "desc"] = "asc") -> list[dict]:
    return sorted(students, key=lambda s: s["score"], reverse=(order == "desc"))
```
This is exactly the `sort_by`/`order` pattern from Week 5, Day 20 — formalised with a
type that documents (and lets `mypy` and FastAPI enforce) that `order` can *only*
ever be `"asc"` or `"desc"`, nothing else. Try `sort_students(data, order="ascending")`
and `mypy` catches the mistake immediately, the same way it caught
`average("hello")` on Day 21.

**When to reach for which:** use `Enum` when the set of values is meaningful on its
own and reused across several places in your codebase (like an order or student
status). Use `Literal` for a one-off constraint on a single parameter, like the sort
direction above.

---

## Worked example: `Enum` and `Literal`, together

### Problem statement
Model order statuses with an `Enum`, and write a function that accepts a status and a
`Literal["short", "long"]` format flag, returning a description matching the
requested length.

### Solution
See [`exercises/models.py`](./exercises/models.py) — fully solved and commented.

```python
from enum import Enum
from typing import Literal

class OrderStatus(str, Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

def describe_order(status: OrderStatus, style: Literal["short", "long"] = "short") -> str:
    if style == "short":
        return status.value
    messages = {
        OrderStatus.PENDING: "Your order is being prepared.",
        OrderStatus.SHIPPED: "Your order is on its way.",
        OrderStatus.DELIVERED: "Your order has arrived!",
        OrderStatus.CANCELLED: "Your order was cancelled.",
    }
    return messages[status]
```
Run a quick check:
```python
print(describe_order(OrderStatus.SHIPPED))              # "shipped"
print(describe_order(OrderStatus.SHIPPED, "long"))       # "Your order is on its way."
```

### What to notice
- `messages` is a `dict` keyed by `OrderStatus` members, not strings — this only
  works cleanly because `OrderStatus` inherits from `str`, so dictionary lookups
  behave predictably either way.
- Using an `Enum` directly as a FastAPI Pydantic field type (`status:
  OrderStatus`) automatically restricts what `/docs` shows as valid input for that
  field, and automatically rejects anything else with a `422` — no extra validation
  code needed, the same "for free" pattern you've seen from `Field()` since Day 11.

---

## 3. `TypedDict` — a dict with a known, fixed shape

**Definition:** A `TypedDict` describes a plain dictionary's expected keys and each
key's value type — unlike a Pydantic `BaseModel`, it does **not** validate anything
at runtime; it's purely a hint for `mypy` and your editor. Use it for data you're not
constructing yourself and don't need runtime validation for — most commonly, the
shape of a response from an external API you're consuming.

```python
from typing import TypedDict

class ExchangeRateResponse(TypedDict):
    base_code: str
    rates: dict[str, float]

def get_xaf_rate(data: ExchangeRateResponse) -> float:
    return data["rates"]["XAF"]
```
This documents exactly the shape you expect back from Week 2, Day 5's currency API,
without the runtime cost or ceremony of a full Pydantic model — appropriate because
you're not validating untrusted user input here, just documenting a shape you already
trust (or plan to check separately).

## 4. `dataclass` — a plain, typed value object

**Definition:** `@dataclass` is a decorator that generates `__init__`, `__repr__`,
and `__eq__` automatically for a class whose entire purpose is holding a fixed set of
typed fields — like a Pydantic `BaseModel`, but with **no validation at all**, and no
dependency on Pydantic.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

def distance(a: Point, b: Point) -> float:
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5

p1 = Point(0, 0)
p2 = Point(3, 4)
print(distance(p1, p2))   # 5.0
```
**Dataclass vs. Pydantic — when to use which:** a Pydantic `BaseModel` validates its
data at construction time and is what you use for anything crossing a boundary you
don't fully trust — a request body, a response you're shaping, data from a file. A
`dataclass` is for internal, already-trusted values passed around *inside* your own
code, where you want the convenience of a typed, structured object without the
overhead of validation you don't need. You'll use dataclasses occasionally for small
internal helper objects; you'll use Pydantic constantly, for anything touching the
outside world.

## 5. `TypeVar` and generics — a first look

**Definition:** A `TypeVar` lets you write one function that works correctly with
*any* type, while still preserving the specific type through to the return value —
`mypy` checks that if you pass in a `list[int]`, you get an `int | None` back, and if
you pass a `list[str]`, you get a `str | None` back, from the very same function.

```python
from typing import TypeVar

T = TypeVar("T")

def first_or_none(items: list[T]) -> T | None:
    return items[0] if items else None
```
```python
first_or_none([1, 2, 3])          # mypy knows this returns int | None
first_or_none(["a", "b"])          # mypy knows this returns str | None
```
Without `TypeVar`, you'd either write this once per type (`first_int_or_none`,
`first_str_or_none`, ...) or use a vague `Any` type that gives up type-checking
entirely. `TypeVar` gets you one function, fully type-safe for every type you call it
with.

---

## Your turn

1. In `exercises/models.py`, add a `PaymentInfo(TypedDict)` describing a payment
   webhook payload with `amount: float`, `currency: str`, and `status: str` — no
   runtime validation needed, this documents an external shape.
2. Add a `@dataclass` called `Money` with `amount: float` and `currency: str`
   fields, and a method `def formatted(self) -> str` returning something like
   `"1,500 XAF"` (reuse Day 21's `format_currency` idea).
3. Write `first_or_none` using `TypeVar`, exactly as in Section 5, in
   `exercises/generics.py`.
4. Check everything: `mypy exercises/`.

---

## Common mistakes to watch for
- **Reaching for `TypedDict` when you actually need validation** — if the data is
  coming from a user (a request body), you want Pydantic's runtime checking, not
  `TypedDict`'s compile-time-only hints. Reserve `TypedDict` for data you already
  trust.
- **Forgetting `(str, Enum)`** and just writing `(Enum)` — this still works, but loses
  the clean string comparison and JSON serialisation that makes `Enum` pleasant to
  use inside FastAPI/Pydantic models specifically.
- **Using `Any` as an escape hatch** whenever a type gets slightly annoying to write
  out — `Any` silently disables all type checking for that value, defeating the point
  of today entirely. Reach for `TypeVar` (Section 5) or a broader-but-still-real
  union type instead, and save `Any` for genuine "this really could be anything"
  cases.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
