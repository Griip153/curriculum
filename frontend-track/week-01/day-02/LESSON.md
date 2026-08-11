# Day 2 — Teaching Lesson: HTML & Semantic HTML

> Companion to `README.md`. This is the material for the live session: a walkthrough of
> the concepts, then **a small "about me" section built together, fully solved**. The
> full profile page — with a photo, more sections, and a form — is yours to build in
> `exercises/profile.html`.

## Objective
Structure a real web page the way professionals do — with meaning, not just `<div>`
everywhere.

## 1. What is HTML?
**Definition:** HTML (HyperText Markup Language) is not a programming language — it has
no logic, no variables, no loops. It's a **markup language**: plain text with tags
wrapped around it to describe the *structure and meaning* of content, so a browser
knows "this is a heading," "this is a list," "this is a link to another page."

**Where it fits with CSS and JavaScript:**
- **HTML** — structure and meaning ("what is this thing")
- **CSS** — presentation ("how should it look") — Day 3
- **JavaScript** — behavior ("what happens when you interact with it") — later weeks

A page can exist as HTML alone (it'll just look plain — default browser styling, no
colors or custom layout) but CSS and JavaScript can't exist without it: they both
operate *on* the structure HTML provides. That's why it's day one of building anything
on the web.

**How a browser uses it:** when you open a page, the browser reads the HTML top to
bottom and builds the **DOM** (Document Object Model) — an in-memory tree of every
element, which is what actually gets rendered on screen and what CSS/JavaScript later
reach into. Getting the structure right here is what everything downstream builds on.

## 2. Tags, elements, and attributes
**Definition:** A **tag** is the markup itself (`<p>`, `</p>`). An **element** is the
tag plus everything between the opening and closing tag. An **attribute** is extra
information added inside the opening tag.

```html
<p class="intro">Hello there</p>
```
- `<p>` and `</p>` — the opening and closing **tags**
- `<p class="intro">Hello there</p>` — the whole **element**
- `class="intro"` — an **attribute** (name="value")

**Self-closing tags** — some elements never wrap content, so they have no closing tag:
`<img>`, `<br>`, `<input>`, `<hr>`.

**Every page starts with the same skeleton:**
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Page title</title>
  </head>
  <body>
    <!-- everything visible goes here -->
  </body>
</html>
```
**Gotcha:** `<head>` holds metadata (title, charset, linked CSS) — nothing in there is
visible on the page. Content you actually want to see goes in `<body>`.

## 3. Headings and paragraphs
**Definition:** `<h1>`–`<h6>` are headings, in order of importance; `<p>` is a block of
text.

```html
<h1>Ada Lovelace</h1>
<h2>About me</h2>
<p>I'm a frontend developer learning to build for the web.</p>
```
**Rule: one `<h1>` per page.** It's the page's main title — screen readers and search
engines use it to understand what the page is about. Everything below nests logically:
`h2` for major sections, `h3` for subsections within those, and so on. Don't pick a
heading level because of how big the text looks — that's what CSS is for.

## 4. Lists
**Definition:** `<ul>` (unordered, bullets) and `<ol>` (ordered, numbers) group related
items; each item is an `<li>`.

```html
<h2>My goals</h2>
<ul>
  <li>Finish the frontend track</li>
  <li>Build three real projects</li>
  <li>Get comfortable with Git</li>
</ul>
```
**Common mistake:** putting text directly inside `<ul>` instead of wrapping every item
in its own `<li>` — a list can only directly contain `<li>` elements.

## 5. Links and images
**Links (`<a>`):** `href` is where it goes; the text between the tags is what's clickable.
```html
<a href="https://github.com/yourname">My GitHub</a>
```
**Opening in a new tab** — add `target="_blank"`, and pair it with
`rel="noopener noreferrer"` (prevents the new tab from getting a handle back on your page):
```html
<a href="https://github.com/yourname" target="_blank" rel="noopener noreferrer">My GitHub</a>
```

**Images (`<img>`):** self-closing, needs `src` (the file path or URL) and `alt`
(text shown if the image fails to load, and read aloud by screen readers).
```html
<img src="profile.jpg" alt="Ada smiling at a laptop" />
```
**Gotcha:** `alt=""` is only acceptable for a purely decorative image. For anything
meaningful — like a profile photo — describe what's actually in it. A missing `alt`
attribute entirely is a bigger problem: screen readers fall back to reading the file
name out loud (`"IMG dash 4 2 0 1 dot jpg"`).

## 6. Tables
**Definition:** For genuinely tabular data (rows and columns of related values) — not
for page layout, that's what Flexbox/Grid are for (Day 4).

```html
<table>
  <thead>
    <tr>
      <th>Skill</th>
      <th>Level</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTML</td>
      <td>Learning</td>
    </tr>
  </tbody>
</table>
```
- `<tr>` = table row, `<th>` = header cell, `<td>` = data cell.
- `<thead>`/`<tbody>` aren't required to make a table work, but they separate the
  header row from the data — use them.

## 7. Forms
**Definition:** How a page collects input from a user — text, choices, files — and
sends it somewhere.

```html
<form action="/submit" method="post">
  <label for="name">Your name</label>
  <input type="text" id="name" name="name" required />

  <label for="message">Message</label>
  <textarea id="message" name="message"></textarea>

  <button type="submit">Send</button>
</form>
```
- `<label for="...">` must match the input's `id` — this is what lets clicking the
  label focus the input, and what a screen reader announces before reading the field.
- `name="..."` is what identifies the field's value when the form is submitted — not
  the same thing as `id`, though they're often given matching values for clarity.
- `type="text"`, `type="email"`, `type="checkbox"`, `type="radio"` — the browser
  validates and renders each differently. `required` blocks submission if empty, no
  JavaScript needed.

**Common mistake:** an `<input>` with no matching `<label>` — it might look fine
visually, but it's unusable for anyone relying on a screen reader, and clicking the
text next to it won't focus the field.

## 8. Semantic tags
**Definition:** Elements that describe *what a section of the page means*, not just how
it looks. `<div>` and `<span>` mean nothing — a screen reader or search engine crawler
can't tell them apart from any other `<div>`. Semantic tags can.

| Tag | Meaning |
|---|---|
| `<header>` | Introductory content — usually a title, logo, nav |
| `<nav>` | A block of navigation links |
| `<main>` | The page's primary content (one per page) |
| `<section>` | A themed group of content, usually with its own heading |
| `<article>` | Self-contained content that could stand on its own (a post, a card) |
| `<aside>` | Tangential content — a sidebar, a pull quote |
| `<footer>` | Closing content — copyright, contact info |

```html
<body>
  <header>
    <h1>Ada Lovelace</h1>
    <nav>
      <a href="#about">About</a>
      <a href="#goals">Goals</a>
    </nav>
  </header>

  <main>
    <section id="about">
      <h2>About me</h2>
      <p>...</p>
    </section>
  </main>

  <footer>
    <p>&copy; 2026 Ada Lovelace</p>
  </footer>
</body>
```

**Why it matters:**
- **Accessibility** — screen readers let users jump straight to `<nav>` or `<main>`,
  skipping repeated boilerplate. A page built entirely from `<div>`s offers no such
  shortcuts.
- **SEO** — search engines weigh content inside `<article>`/`<main>` differently than
  content in a `<div>`, and use `<h1>`/`<h2>` structure to understand what a page is
  about.
- **Readability** — six months from now, `<section id="about">` tells you what's inside
  before you read a single line; `<div class="wrapper2">` doesn't.

**Rule of thumb:** reach for a semantic tag first; fall back to `<div>` only when
nothing in the table above actually describes the content (a generic styling wrapper,
a layout container).

### Common mistakes to watch for
- **Skipping heading levels** (`h1` straight to `h3`) — breaks the outline screen
  readers and SEO crawlers rely on.
- **`alt`-less or meaninglessly-`alt`ed images** — see the gotcha in section 5.
- **`<label>` not linked to its `<input>` via matching `for`/`id`** — the form still
  submits, but it's unusable with a keyboard or screen reader.
- **Using `<div>` where a semantic tag fits** — it'll look identical in the browser and
  fail every accessibility/SEO check.
- **Multiple `<h1>`s or `<main>`s on one page** — each should appear exactly once.

---

## Worked Exercise: an "About me" section, built together

This is a small slice of today's task, solved together, live. The full profile page —
photo, goals list, links, and a contact form — you build the same way, as a stub file
in `exercises/profile.html`.

### Problem statement
Build a self-contained "About me" section using a heading, a paragraph, and a list —
wrapped in the semantic tag that actually describes it.

### Thinking it through
1. A themed chunk of content with its own heading → `<section>`, not `<div>`.
2. The section's title → `<h2>` (it lives *inside* the page, under the page's one `<h1>`).
3. Free text → `<p>`. A set of related, unordered points → `<ul>` of `<li>`.

### Solution
See [`exercises/example.html`](./exercises/example.html) — fully solved and commented.

```html
<section id="about">
  <h2>About me</h2>
  <p>I'm learning to build for the web, one project at a time.</p>
  <ul>
    <li>Based in Douala, Cameroon</li>
    <li>Currently: frontend track, week 1</li>
    <li>Interested in accessible, semantic HTML</li>
  </ul>
</section>
```

Open it directly in a browser to check it renders — no server needed for a static
HTML file:
```bash
open exercises/example.html      # macOS
xdg-open exercises/example.html  # Linux
```

### What to notice
- Nothing here is a `<div>`. Every tag was picked because it describes what the content
  *is*, not because it renders in a particular way.
- This same section, dropped into the full profile page, still makes sense read on its
  own — that's the test for whether `<section>` (or `<article>`) was the right call.

---

## Your turn — finish the task of the day

| # | Exercise | File | Concept practiced |
|---|----------|------|--------------------|
| 1 | Full personal profile page | `exercises/profile.html` | semantic layout, images, lists, links, a form |

Goal: a complete page — `<header>`, `<nav>`, `<main>` with at least two `<section>`s
(About, Goals), a photo, links to your GitHub/socials, and a contact `<form>` — using
**at least 8 semantic tags** and **one form**, matching today's task in `README.md`.

Same process as the worked exercise: read the problem in the file's comment block, say
the plan out loud, then fill in where it says `<!-- TODO -->`.

Open it the same way: `open exercises/profile.html` (or `xdg-open` on Linux), and
re-open after every change to check your work.

Once it's done, push it to your `seed-internship` repo.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
