# Day 2 — Teaching Lesson: Python Basics I — The Language

> Companion to `README.md`. This is the material for the live session: a walkthrough
> of the concepts, then **one exercise (FizzBuzz) fully solved together**. The
> remaining 9 exercises in `exercises/` are yours to solve using the same approach.

## Objective
Write your first real programs: store data, make decisions, repeat work.

## 0. Running Python and a critical rule: indentation

You already ran `python3 hello.py` on Day 1. That's how you'll run every file today.

**The one rule that trips up every beginner coming from other languages:** Python
uses **indentation** (spaces at the start of a line) to mark which lines belong
*inside* a block of code — there are no `{ }` curly braces like some other languages.
Use **4 spaces** per indent level, consistently. VS Code does this automatically when
you press Enter after a `:`.

```python
if True:
    print("this line is inside the if")   # 4 spaces in
print("this line is not")                  # back at column 0 — outside the if
```
Get the indentation wrong and Python will either misbehave silently or throw an
`IndentationError`. This is the single most common Day 2 bug.

## 1. Variables
**Definition:** A variable is a named container that stores a value in the computer's
memory, so you can refer to that value later by name instead of retyping it.

```python
pi = 3.14159
score = 0
score = score + 10   # reassigning — Python variables can always change
score += 10           # same thing, shorthand
```
Unlike some languages, Python doesn't need you to declare a variable's type up front
— you just assign a value and Python figures out the type. We'll meet a stricter,
more professional way to write this (type hints) in Week 6 — for now, focus on the
basics.

**Naming rules:** letters, numbers, and underscores only; can't start with a number;
`snake_case` (lowercase with underscores) is the Python convention — `student_score`,
not `studentScore`.

## 2. Data Types
**Definition:** A data type describes what *kind* of value something is (text, a
number, true/false, ...) — it determines what you're allowed to do with that value.

```python
name = "Ada"            # str (string) — text, in quotes
age = 25                 # int (integer) — whole number
gpa = 3.8                # float — decimal number
is_enrolled = True       # bool (boolean) — True or False, capitalised
nothing_yet = None       # None — Python's "intentional no value"
```
Check any value's type with the built-in `type()` function:
```python
type(age)   # <class 'int'>
```

## 3. Operators
**Definition:** An operator is a symbol that acts on one or more values (called
*operands*) to produce a result — for example `+` acts on two numbers to produce
their sum.

```python
# Arithmetic
10 + 3, 10 - 3, 10 * 3, 10 / 3, 10 // 3, 10 % 3
# / is "true division" -> always gives a float: 3.333...
# // is "floor division" -> whole number result: 3
# % is "modulo" -> the remainder: 1 — key for FizzBuzz!

# Comparison
5 == 5      # True — equality check (two equals signs, never one)
5 == "5"    # False — different types, Python doesn't silently convert them
5 != 4      # True — "not equal"

# Logical
True and False   # AND
True or False    # OR
not True          # NOT
```
**One equals sign (`=`) assigns a value. Two equals signs (`==`) compare two values.**
Mixing these up (`if score = 90:`) is a syntax error Python will catch for you — but
get used to the distinction now.

## 4. Conditionals
**Definition:** A conditional is a statement that runs one block of code if something
is true, and a different block (or nothing) if it's false — it's how a program makes
a decision. There are three shapes you'll use constantly:

**a) `if`** — run a block only when a condition is true, otherwise do nothing.
```python
if score >= 90:
    print("A")
```

**b) `if...else`** — run one block if true, a different block if false. Exactly two
paths.
```python
if is_enrolled:
    print("Welcome back!")
else:
    print("Please register first.")
```

**c) `if...elif...else`** — chain several conditions to pick one path out of many.
Checked top to bottom; the first one that's true wins, the rest are skipped. Notice
Python spells "else if" as one word: `elif`.
```python
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("Needs improvement")
```

**Bonus — the conditional expression** (`value_if_true if condition else value_if_false`):
a compact `if...else` used as an expression (it produces a value you can assign).
```python
status = "enrolled" if is_enrolled else "not enrolled"
```

## 5. Loops
**Definition:** A loop is a block of code that repeats automatically while a
condition holds true, so you don't have to write the same instruction over and over
by hand. There are two main loops in Python:

**a) `for`** — use when you're repeating a fixed number of times, or walking through
a known collection. `range(start, stop)` generates numbers from `start` up to (but
**not including**) `stop`.
```python
for i in range(1, 6):   # 1, 2, 3, 4, 5 — 6 is NOT included
    print(i)
```

**b) `while`** — use when you don't know the exact number of repeats in advance, only
the condition that should keep it going. Checks the condition *before* each pass — if
it's false from the start, the loop body never runs.
```python
n = 5
while n > 0:
    print(n)
    n -= 1   # without this, the loop never ends — an "infinite loop"
```

**`break`** exits a loop immediately. **`continue`** skips to the next iteration
without finishing the current one. Both work in either loop type.

---

## Worked Exercise (1 of 10): FizzBuzz

This is the one we solve together, live. The other 9 are listed at the bottom and
live as stub files in `exercises/` — same process, on your own.

### Problem statement
Print the numbers from 1 to 20. But:
- if the number is divisible by 3, print `"Fizz"` instead of the number
- if the number is divisible by 5, print `"Buzz"` instead of the number
- if the number is divisible by both 3 and 5, print `"FizzBuzz"`

### Thinking it through
1. We need to check every number from 1 to 20 → that's a `for` loop with `range(1, 21)`
   (remember, `range`'s stop value is exclusive, so we need `21` to include `20`).
2. For each number we need to make a decision → that's `if / elif / else`.
3. "Divisible by" → the modulo operator `%`. `n % 3 == 0` means "no remainder when
   divided by 3," i.e. divisible by 3.
4. **Order matters**: check "divisible by both" *first*. If we checked "divisible by
   3" first, a number like 15 would print `"Fizz"` and never reach the "both" check.

### Solution
See [`exercises/01_fizzbuzz.py`](./exercises/01_fizzbuzz.py) — fully solved and
commented.

```python
for n in range(1, 21):
    if n % 3 == 0 and n % 5 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)
```

Run it:
```bash
python3 exercises/01_fizzbuzz.py
```

### What to notice
- `n % 3 == 0 and n % 5 == 0` is equivalent to `n % 15 == 0` — either works, but the
  `and` version reads closer to the problem statement.
- The `elif`/`else` branches are what make this cheap: once one condition matches,
  the rest are skipped.
- This exact shape — loop + ordered conditionals + modulo — reappears in the grade
  calculator and the multiplication table below.

---

## Your turn — Exercises 2 to 10
Solve these the same way FizzBuzz was solved: read the problem, say the plan out
loud, then write it. Stub files are in `exercises/`, each with the problem statement
and expected sample output in a comment block — write your code where it says
`# TODO`.

| # | Exercise | File | Concept practiced |
|---|----------|------|--------------------|
| 2 | Grade calculator | `exercises/02_grade_calculator.py` | conditionals |
| 3 | XAF currency formatter | `exercises/03_xaf_currency_formatter.py` | operators, strings |
| 4 | Biggest of three | `exercises/04_biggest_of_three.py` | conditionals |
| 5 | Even or odd | `exercises/05_even_or_odd.py` | modulo |
| 6 | Sum of digits | `exercises/06_sum_of_digits.py` | loops |
| 7 | Reverse a string | `exercises/07_reverse_string.py` | loops |
| 8 | Simple calculator | `exercises/08_simple_calculator.py` | conditionals |
| 9 | Temperature converter | `exercises/09_temperature_converter.py` | operators |
| 10 | Multiplication table | `exercises/10_multiplication_table.py` | loops |

Run each one the same way: `python3 exercises/0X_name.py`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*