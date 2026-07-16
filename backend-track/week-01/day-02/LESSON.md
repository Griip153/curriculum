# Day 2 — Teaching Lesson: JavaScript Basics I — The Language

> Companion to `README.md`. This is the material for the live session: a walkthrough of
> the concepts, then **one exercise (FizzBuzz) fully solved together**. The remaining 9
> exercises in `exercises/` are yours to solve using the same approach.

## Objective
Write your first real programs: store data, make decisions, repeat work — and get
comfortable running JavaScript outside the browser, with `node`.

## 0. Running JavaScript with Node
**Definition:** Node.js ("Node") is a program that runs JavaScript *outside* a browser —
directly on your computer, from the terminal, like any other command-line program.

Up to now JS has lived in `<script>` tags in a browser. From today, we run it directly:

```bash
node filename.js
```

Create a file, put JS in it, run that command. No HTML, no browser — just the language.
Try it now:

```js
// hello.js
console.log("Hello, backend track!");
```

```bash
node hello.js
```

## 1. Variables — `let` and `const`
**Definition:** A variable is a named container that stores a value in the computer's
memory, so you can refer to that value later by name instead of retyping it.

- `const` — the value never gets reassigned. **Default to this.**
- `let` — the value will change (a counter, a running total, a toggle).
- Avoid `var` — it has confusing scoping rules we don't need.

```js
const pi = 3.14159;   // never reassigned
let score = 0;        // will change as the program runs
score = score + 10;
```

## 2. Data Types
**Definition:** A data type describes what *kind* of value something is (text, a
number, true/false, ...) — it determines what you're allowed to do with that value.

```js
const name = "Ada";        // string
const age = 25;            // number
const isEnrolled = true;   // boolean
const nothingYet = null;   // intentional "no value"
let notSet;                // undefined — declared, no value assigned
```
Check any value's type with `typeof x`.

## 3. Operators
**Definition:** An operator is a symbol that acts on one or more values (called
*operands*) to produce a result — for example `+` acts on two numbers to produce their sum.

```js
// Arithmetic
10 + 3, 10 - 3, 10 * 3, 10 / 3, 10 % 3   // % = remainder (modulo) — key for FizzBuzz!

// Comparison
5 === 5     // true  — always use === / !== (strict), not == / !=
5 === "5"   // false — different types, no coercion with ===

// Logical
true && false   // AND
true || false   // OR
!true           // NOT
```

## 4. Conditionals
**Definition:** A conditional is a statement that runs one block of code if something
is true, and a different block (or nothing) if it's false — it's how a program makes a decision.
There are four types you'll use constantly:

**a) `if`** — run a block only when a condition is true, otherwise do nothing.
```js
if (score >= 90) {
  console.log("A");
}
```

**b) `if...else`** — run one block if true, a different block if false. Exactly two paths.
```js
if (isEnrolled) {
  console.log("Welcome back!");
} else {
  console.log("Please register first.");
}
```

**c) `if...else if...else`** — chain several conditions to pick one path out of many.
Checked top to bottom; the first one that's true wins, the rest are skipped.
```js
if (score >= 90) {
  console.log("A");
} else if (score >= 80) {
  console.log("B");
} else if (score >= 70) {
  console.log("C");
} else {
  console.log("Needs improvement");
}
```

**d) `switch`** — compare one value against many exact possibilities. Good alternative
to a long `else if` chain when you're checking one variable against fixed options.
Don't forget `break`, or execution "falls through" into the next case.
```js
switch (operator) {
  case "+":
    console.log(a + b);
    break;
  case "-":
    console.log(a - b);
    break;
  default:
    console.log("Unknown operator");
}
```

**Bonus — the ternary operator** (`condition ? ifTrue : ifFalse`): a compact `if...else`
for simple cases, used as an expression (it produces a value).
```js
const status = isEnrolled ? "enrolled" : "not enrolled";
```

## 5. Loops
**Definition:** A loop is a block of code that repeats automatically while a condition
holds true, so you don't have to write the same instruction over and over by hand.
There are three main loops:

**a) `for`** — use when you know how many times to repeat (or you're counting 1..N).
The three parts are: start value, condition to keep going, and what happens after each pass.
```js
for (let i = 1; i <= 5; i++) {
  console.log(i);
}
```

**b) `while`** — use when you don't know the exact number of repeats in advance, only
the condition that should keep it going. Checks the condition *before* each pass — if
it's false from the start, the loop body never runs.
```js
let n = 5;
while (n > 0) {
  console.log(n);
  n--;
}
```

**c) `do...while`** — like `while`, but checks the condition *after* each pass, so the
body always runs at least once, even if the condition is false from the start.
```js
let attempts = 0;
do {
  console.log("Attempt", attempts + 1);
  attempts++;
} while (attempts < 3);
```

---

## Worked Exercise (1 of 10): FizzBuzz

This is the one we solve together, live. The other 9 are listed at the bottom and live
as stub files in `exercises/` — same process, on your own.

### Problem statement
Print the numbers from 1 to 20. But:
- if the number is divisible by 3, print `"Fizz"` instead of the number
- if the number is divisible by 5, print `"Buzz"` instead of the number
- if the number is divisible by both 3 and 5, print `"FizzBuzz"`

### Thinking it through
1. We need to check every number from 1 to 20 → that's a `for` loop.
2. For each number we need to make a decision → that's `if / else if / else`.
3. "Divisible by" → the modulo operator `%`. `n % 3 === 0` means "no remainder when
   divided by 3", i.e. divisible by 3.
4. **Order matters**: check "divisible by both" *first*. If we checked "divisible by 3"
   first, a number like 15 would print `"Fizz"` and never reach the "both" check.

### Solution
See [`exercises/01-fizzbuzz.js`](./exercises/01-fizzbuzz.js) — fully solved and commented.

```js
for (let n = 1; n <= 20; n++) {
  if (n % 3 === 0 && n % 5 === 0) {
    console.log("FizzBuzz");
  } else if (n % 3 === 0) {
    console.log("Fizz");
  } else if (n % 5 === 0) {
    console.log("Buzz");
  } else {
    console.log(n);
  }
}
```

Run it:
```bash
node exercises/01-fizzbuzz.js
```

### What to notice
- `n % 3 === 0 && n % 5 === 0` is equivalent to `n % 15 === 0` — either works, but the
  `&&` version reads closer to the problem statement.
- The `else` branches are what make this cheap: once one condition matches, the rest
  are skipped.
- This exact shape — loop + ordered conditionals + modulo — reappears in the grade
  calculator and the multiplication table below.

---

## Your turn — Exercises 2 to 10
Solve these the same way FizzBuzz was solved: read the problem, say the plan out loud,
then write it. Stub files are in `exercises/`, each with the problem statement and
expected sample output in a comment block — write your code where it says `// TODO`.

| # | Exercise | File | Concept practiced |
|---|----------|------|--------------------|
| 2 | Grade calculator | `exercises/02-grade-calculator.js` | conditionals |
| 3 | XAF currency formatter | `exercises/03-xaf-currency-formatter.js` | operators, strings |
| 4 | Biggest of three | `exercises/04-biggest-of-three.js` | conditionals |
| 5 | Even or odd | `exercises/05-even-or-odd.js` | modulo |
| 6 | Sum of digits | `exercises/06-sum-of-digits.js` | loops |
| 7 | Reverse a string | `exercises/07-reverse-string.js` | loops |
| 8 | Simple calculator | `exercises/08-simple-calculator.js` | conditionals / switch |
| 9 | Temperature converter | `exercises/09-temperature-converter.js` | operators |
| 10 | Multiplication table | `exercises/10-multiplication-table.js` | loops |

Run each one the same way: `node exercises/0X-name.js`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
