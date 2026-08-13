# Day 22 — Type Hints II — Enums, Literals & Deeper Types

## Objective
Reach for the right precise type for the right job — not everything is a plain `str`
or `int`.

## Concepts
`Enum` for a fixed set of named values; `Literal` for a fixed set of literal values;
`TypedDict` for a dict with a known, fixed shape; `dataclasses` vs. Pydantic models;
`TypeVar` and generics (a first look).

## Watch before the session
- "Python Enums Explained" — mCoding
- "TypedDict vs dataclass vs Pydantic" — ArjanCodes
- Real Python — "Python's `Literal` Type" article

## Task of the day
Model a small "order status" system using `Enum`, a `TypedDict` for a raw API
response shape, a `dataclass` for an internal value object, and a generic
`first_or_none` function using `TypeVar`. Full step-by-step instructions and half the
task fully solved are in `LESSON.md`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
