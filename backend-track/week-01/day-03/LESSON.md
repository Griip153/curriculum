# Day 3 — Teaching Lesson: JavaScript Basics II — Functions, Arrays & Objects

> Companion to `README.md`. This is the material for the live session: a walkthrough of
> the concepts, then **the first part of the task of the day fully solved together**
> (the student data + the `average` function). The rest — `topStudent` and
> `aboveAverage` — is yours to build using the same approach.

## Objective
Organise code into functions and model real-world data — the bread and butter of
backend work.

## 1. Functions and parameters
**Definition:** A function is a named, reusable block of code. A parameter is a named
placeholder for an input value the function needs to do its job — you supply the real
value (the *argument*) when you call the function.

```js
function shout(message) {       // "message" is the parameter
  return message.toUpperCase() + "!";
}

shout("hello");                 // "hello" is the argument -> "HELLO!"
```
A function can take several parameters, and `return` is what sends a value back to
whoever called it — without `return`, the function produces `undefined`.

**Several parameters, in order:**
```js
function describeStudent(name, score) {
  return name + " scored " + score;
}

describeStudent("Ada", 91);   // "Ada scored 91"
```
Arguments are matched to parameters *by position*, not by name — `describeStudent(91, "Ada")`
would silently produce nonsense. This is one reason we'll switch to passing a single
object (`{ name, score }`) once functions take more than two or three related values.

**Default parameters** — a fallback value used only when the argument is omitted:
```js
function greet(name = "student") {
  return "Welcome, " + name;
}

greet();        // "Welcome, student" — no argument given, default kicks in
greet("Ada");   // "Welcome, Ada"
```

**Forgetting `return` is the single most common bug this week.** A function with no
`return` statement doesn't fail — it just quietly hands back `undefined`, and that
`undefined` then breaks whatever called the function:
```js
function average(students) {
  const scores = students.map(s => s.score);
  scores.reduce((sum, score) => sum + score, 0) / scores.length;   // BUG: no `return`
}

console.log(average(students));   // undefined — the math ran, but nothing came back
```
If you ever see `undefined` where you expected a number, check for a missing `return`
before you check anything else.

## 2. Arrays and key methods
**Definition:** An array is an ordered list of values, stored under one variable name
and accessed by position (starting at index 0).

```js
const scores = [72, 88, 91, 60];
scores[0];        // 72 — first element
scores.length;    // 4
scores.push(75);  // adds 75 to the end — mutates the array
```

Several methods you'll use constantly. Each one takes a small function (a "callback")
that runs once per element:

- **`.map()`** — transform every element, get back a **new array of the same length**.
  ```js
  scores.map(s => s * 2);   // [144, 176, 182, 120, 150]
  ```
- **`.filter()`** — keep only elements that pass a test, get back a shorter (or equal) array.
  ```js
  scores.filter(s => s >= 80);   // [88, 91]
  ```
- **`.find()`** — return the *first* element that passes a test, or `undefined` if none do.
  ```js
  scores.find(s => s > 90);   // 91
  ```
- **`.some()`** — does *at least one* element pass the test? Returns `true`/`false`.
  ```js
  scores.some(s => s < 60);   // false — nobody failed
  ```
- **`.every()`** — do *all* elements pass the test? Returns `true`/`false`.
  ```js
  scores.every(s => s >= 60);   // true — everybody passed
  ```
- **`.includes()`** — does the array contain this exact value?
  ```js
  scores.includes(91);   // true
  ```
- **`.forEach()`** — run a function on every element, but get **nothing back** (no new
  array). Use it only when you want a side effect (like printing), not a transformed value.
  ```js
  scores.forEach(s => console.log(s));   // prints each score, returns undefined
  ```
- **`.sort()`** — reorders the array **in place** (it mutates the original!). Without a
  comparator it sorts as strings, which breaks numbers — always pass one for numbers:
  ```js
  [10, 2, 33].sort();                       // [10, 2, 33] -> ["10","2","33"] as text -> WRONG: [10, 2, 33]
  [10, 2, 33].sort((a, b) => a - b);         // [2, 10, 33] -- ascending, correct
  ```

**Mutating vs. non-mutating.** `.push()` and `.sort()` change the original array.
`.map()`, `.filter()`, and `.concat()` return a **new** array and leave the original
untouched. Prefer the non-mutating ones by default — it's easier to reason about code
when data doesn't change underneath you unexpectedly.

**Chaining** — since `.map()`/`.filter()` return arrays, you can call another array
method right on the result:
```js
scores
  .filter(s => s >= 80)
  .map(s => s + 5);   // [93, 96] — first keep the high scorers, then bump their score
```

## 3. Objects and nesting
**Definition:** An object is a collection of `key: value` pairs used to represent one
real-world "thing" with several properties. Nesting means an object's value is itself
another object (or array) — modelling something with sub-parts.

```js
const student = {
  name: "Ada",
  score: 91,
  address: {              // nested object
    city: "Douala",
    country: "Cameroon",
  },
};

student.name;              // "Ada"
student.address.city;      // "Douala" — dot into the nested object
```

**Two ways to read a property:** dot notation (`student.name`) when you know the exact
property name ahead of time, or bracket notation (`student["name"]`) when the property
name is itself stored in a variable:
```js
const field = "score";
student[field];   // 91 — bracket notation lets the key be dynamic
student.field;     // undefined — this looks for a literal property called "field", which doesn't exist
```

**Checking whether a property exists** before reading it, so you don't accidentally
read from something that isn't there:
```js
"address" in student;        // true
student.address?.zip;        // undefined, not a crash — optional chaining stops safely
                              // if `address` (or any link in the chain) were missing
```

**Objects can hold functions too** — a function stored as a property is called a
*method*:
```js
const calculator = {
  add(a, b) { return a + b; },   // shorthand method syntax
};
calculator.add(2, 3);   // 5
```
We won't lean on this heavily yet (that's more of a Week 2/OOP topic), but you'll see
the shape constantly in libraries, so recognise it when you meet it.

## 4. Arrays of objects
**Definition:** Combining the two above — an array where every element is an object
with the same shape. This is the standard shape of real data (database rows, API
responses), so it's worth getting comfortable with it early.

```js
const students = [
  { name: "Ada", score: 91 },
  { name: "Kofi", score: 68 },
  { name: "Zara", score: 84 },
];

students.map(s => s.name);              // ["Ada", "Kofi", "Zara"]
students.filter(s => s.score >= 80);    // [{name: "Ada", ...}, {name: "Zara", ...}]
```

**Sorting an array of objects** needs a comparator that looks at the property you care
about, not the objects themselves:
```js
students.sort((a, b) => b.score - a.score);   // highest score first
```

**Chaining across an array of objects** is where `.filter()` and `.map()` start doing
real work together — filter down to who you want, then map to just the field you need:
```js
students
  .filter(s => s.score >= 80)
  .map(s => s.name);   // ["Ada", "Zara"]
```

### Common mistakes to watch for
- **Comparing objects with `===`** doesn't compare their contents — it checks whether
  they're *the exact same object in memory*. Two students with identical `name`/`score`
  built separately are **not** `===` equal. Compare specific fields instead
  (`a.score === b.score`), or use a library helper if you truly need deep equality.
- **`.map()` vs. `.forEach()`** — if you're building a new array, you want `.map()`.
  If you're just printing or logging, you want `.forEach()`. Using `.map()` purely for
  its side effects (and throwing away the returned array) is a common tell that
  `.forEach()` was the right tool.
- **Forgetting that `.push()` and `.sort()` mutate** — if you sort a students array in
  place and then reuse "the original order" elsewhere in the same function, it's gone.
- **Off-by-one on `undefined`** — `.find()` and array indexing (`students[10]` on a
  3-element array) return `undefined` instead of throwing. Always consider what happens
  downstream if nothing matched.

---

## Worked Exercise: student data + `average()`

This is the first part of today's task, solved together, live. The rest — `topStudent`
and `aboveAverage` — you build the same way, as stub files in `exercises/`.

### Problem statement
Model a small list of students (name + score) as an array of objects, then write a
function `average(students)` that returns the mean of all their scores.

### Thinking it through
1. Data shape first: each student is `{ name, score }` → an array of those is an
   **array of objects** (section 4 above).
2. "Average" = sum of all scores ÷ how many there are. Summing everything means
   visiting every element → `.map()` to pull out just the scores, or a loop with a
   running total.
3. Wrap it in a **function** so it's reusable for any array of students, not just this one.

### Solution
See [`exercises/01-student-average.js`](./exercises/01-student-average.js) — fully solved and commented.

```js
const students = [
  { name: "Ada", score: 91 },
  { name: "Kofi", score: 68 },
  { name: "Zara", score: 84 },
];

function average(students) {
  const scores = students.map(s => s.score);
  const total = scores.reduce((sum, score) => sum + score, 0);
  return total / scores.length;
}

console.log(average(students));   // 81
```

Run it:
```bash
node exercises/01-student-average.js
```

### What to notice
- `.reduce()` is new here — it walks the array and "reduces" it to one value, starting
  from `0` and adding each score. It's the array-method way to sum a list.
- `average` doesn't care about `name` at all — it only pulls out `score`. Functions
  that do one clear thing are easier to reuse and to test.
- The same `students` array will be reused, unchanged, by `topStudent` and `aboveAverage` below.

---

## Your turn — finish the task of the day

| # | Exercise | File | Concept practiced |
|---|----------|------|--------------------|
| 2 | Top student | `exercises/02-top-student.js` | functions, comparison, iterating an array |
| 3 | Above-average students | `exercises/03-above-average-students.js` | `.filter()`, calling one function from another |

Same process as the worked exercise: read the problem in the file's comment block,
say the plan out loud, then write it where it says `// TODO`.

Run each one the same way: `node exercises/0X-name.js`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
