# Day 3 — Teaching Lesson: CSS Fundamentals

> Companion to `README.md`. This is the material for the live session: a walkthrough of
> the concepts, then **a small business card styled together, fully solved**. Styling
> yesterday's profile page, and recreating the full business card design from class, is
> yours to build in `exercises/`.

## Objective
Control how everything looks: colors, spacing, text, and the box model that governs
all layout.

## 1. What is CSS?
**Definition:** CSS (Cascading Style Sheets) is the language that describes how HTML
should *look* — colors, fonts, spacing, layout — without touching what it *is* or what
it *does*. HTML gives the browser a structure; CSS tells it how to paint that structure
on screen.

**Where it fits with HTML and JavaScript:**
- **HTML** — structure and meaning ("what is this thing") — Day 2
- **CSS** — presentation ("how should it look") — today
- **JavaScript** — behavior ("what happens when you interact with it") — later weeks

**"Cascading" is the important word.** Styles can come from multiple places — the
browser's defaults, a stylesheet, an inline `style` attribute — and multiple rules can
target the same element at once. CSS has to decide which one wins. That's the cascade,
and specificity (section 3) is the main rule it uses to resolve conflicts.

**Three ways to attach CSS to a page**, in order of what you should actually reach for:
```html
<!-- 1. External — a separate .css file, linked in <head>. Use this. -->
<link rel="stylesheet" href="styles.css" />

<!-- 2. Internal — a <style> block inside the HTML file. OK for a quick demo. -->
<style>
  p { color: navy; }
</style>

<!-- 3. Inline — a style attribute on one element. Avoid — it can't be reused,
     and it wins over almost everything else in the cascade, which makes bugs
     hard to track down later. -->
<p style="color: navy;">Hello</p>
```
**Gotcha:** the `<link>` tag goes in `<head>`, not `<body>` — same reasoning as `<title>`:
it's metadata about the page, not visible content itself.

## 2. Selectors and specificity
**Definition:** A **selector** picks which element(s) a rule applies to. A CSS rule is
`selector { property: value; }`.

```css
/* Element selector — every <p> on the page */
p { line-height: 1.5; }

/* Class selector — any element with class="card" (reusable, the one you'll use most) */
.card { padding: 16px; }

/* ID selector — the one element with id="hero" (use sparingly — see specificity below) */
#hero { text-align: center; }

/* Descendant selector — <a> tags, but only inside something with class="nav" */
.nav a { text-decoration: none; }
```

**Specificity** is how the browser decides which rule wins when two rules target the
same element. Roughly, from weakest to strongest:
1. Element selectors (`p`, `div`) — weakest
2. Class selectors (`.card`), attribute selectors, pseudo-classes (`:hover`)
3. ID selectors (`#hero`) — strong
4. Inline `style="..."` — stronger than any selector in a stylesheet
5. `!important` — overrides everything; treat it as a last resort, not a tool

**Gotcha:** when two rules have equal specificity, the one that appears **later** in the
stylesheet wins. This is why "I changed the color but nothing happened" is so often a
specificity or ordering problem, not a typo. Check DevTools (right-click → Inspect) —
it shows every matching rule and which one actually won.

**Rule of thumb:** style with classes by default. Reach for an ID only when you're
certain the element is genuinely unique on the page (and even then, prefer a class —
IDs are hard to override later because of their weight above).

## 3. Colors and units
**Colors** — three common formats, all valid:
```css
.a { color: navy; }              /* named color — 147 of these exist, limited palette */
.b { color: #1e3a8a; }           /* hex — most common in real projects */
.c { color: rgb(30, 58, 138); }  /* rgb() — same color, easier to tweak one channel */
.d { color: rgba(30, 58, 138, 0.5); } /* rgba() — same, with 50% opacity */
```

**Units** — the ones you'll use constantly:
| Unit | What it means | When to use it |
|---|---|---|
| `px` | Fixed pixels | Borders, small precise values (1px, 2px) |
| `%` | Relative to the parent element | Widths that should flex with their container |
| `rem` | Relative to the root (`<html>`) font size — default 16px, so `1rem` = 16px | Font sizes, spacing — **default choice** |
| `em` | Relative to the *current* element's font size | Rarely — it compounds when nested, which surprises people |
| `vh` / `vw` | % of the viewport height/width | Full-screen sections |

**Why `rem` over `px` for text:** if a user increases their browser's default font size
for accessibility, `rem`-based text scales with it. `px`-based text ignores that setting
entirely.

## 4. The box model
**Definition:** every element on a page is a rectangular box made of four layers, from
the inside out:

```
┌─────────────────────────────┐
│           margin             │  ← space outside the border, between elements
│  ┌─────────────────────┐    │
│  │        border         │   │  ← the visible edge
│  │  ┌───────────────┐   │   │
│  │  │    padding      │   │   │  ← space inside the border, around the content
│  │  │  ┌─────────┐   │   │   │
│  │  │  │ content │   │   │   │  ← the actual text/image
│  │  │  └─────────┘   │   │   │
│  │  └───────────────┘   │   │
│  └─────────────────────┘    │
└─────────────────────────────┘
```

```css
.card {
  width: 300px;
  padding: 20px;
  border: 1px solid #ccc;
  margin: 16px;
}
```

**Gotcha — the box-sizing trap:** by default, `width: 300px` sets the width of the
*content only*. Padding and border get added **on top**, so this box actually renders
at `300 + 20 + 20 + 1 + 1 = 342px` wide. This trips up almost everyone at first.

**Fix — set this once, at the top of every stylesheet:**
```css
* {
  box-sizing: border-box;
}
```
With `border-box`, `width: 300px` means the *whole box* — padding and border are
squeezed inside that 300px instead of added to it. Padding and border no longer break
your layout math.

**Shorthand values** — `margin`/`padding` accept 1, 2, or 4 values:
```css
margin: 10px;              /* all four sides */
margin: 10px 20px;         /* top/bottom, left/right */
margin: 10px 20px 5px 0;   /* top, right, bottom, left — clockwise from top */
```

**Margin collapsing:** vertical margins between two stacked block elements don't add —
the larger one wins. If one has `margin-bottom: 20px` and the next has
`margin-top: 10px`, the gap between them is 20px, not 30px. This only happens
vertically, and only for regular block flow — it's a common source of "why isn't my
spacing what I calculated" confusion.

## 5. Typography
```css
body {
  font-family: "Helvetica Neue", Arial, sans-serif; /* fallback list, left to right */
  font-size: 1rem;
  font-weight: 400;   /* 400 = normal, 700 = bold */
  line-height: 1.5;   /* unitless = multiple of the font size — preferred */
  text-align: left;
}

h1 {
  font-weight: 700;
  letter-spacing: -0.02em; /* tightens large headings slightly */
}
```
**Gotcha:** always list a generic fallback (`sans-serif`, `serif`, `monospace`) last in
`font-family` — if every named font fails to load, the browser still picks *something*
sane instead of falling back to its own arbitrary default.

**`line-height`:** prefer a unitless value (`1.5`) over `24px`. Unitless scales with the
element's own font size; a fixed pixel value doesn't adjust if you later change the
font size and forget to update it too.

## 6. Backgrounds
```css
.card {
  background-color: #f9fafb;
  background-image: url("pattern.svg");
  background-size: cover;      /* fills the box, cropping if needed */
  background-position: center;
  background-repeat: no-repeat;
}
```
**Gotcha:** `background-image` needs `background-repeat: no-repeat` almost every time
you're using it as a single photo/illustration rather than a tiling pattern — otherwise
small images tile across the whole box by default, which rarely looks intentional.

## 7. Display types
**Definition:** `display` controls how an element behaves in the page's flow.

| Value | Behavior |
|---|---|
| `block` | Takes the full width available; starts on a new line (`div`, `p`, `section`) |
| `inline` | Only as wide as its content; sits in the middle of text, **ignores `width`/`height`/vertical margin** (`span`, `a`) |
| `inline-block` | Sits in line like `inline`, but **respects** `width`/`height`/margin like `block` |
| `none` | Removed from the page entirely — takes up no space (different from `visibility: hidden`, which hides it but keeps its space) |

**Gotcha:** trying to set `width`/`height` on an `inline` element (like a bare `<a>` or
`<span>`) and seeing nothing happen is one of the most common early CSS confusions —
switch it to `inline-block` or `block` first.

**Not covered today:** `display: flex` and `display: grid` — real layout tools for
arranging multiple boxes together. That's Day 4. Today's display types are about how a
*single* element behaves in normal document flow.

### Common mistakes to watch for
- **Forgetting `box-sizing: border-box`** — padding/border silently blow past your
  intended width. Set it globally, once, at the top of the file.
- **Using `px` for every font size** — ignores the user's accessibility font-size
  preference. Default to `rem` for text.
- **Reaching for an ID selector out of habit** — makes the rule hard to override later.
  Use a class unless the element is truly one-of-a-kind.
- **Forgetting `background-repeat: no-repeat`** on a single background image.
- **Setting `width`/`height` on an `inline` element** and not understanding why it's
  ignored — check `display` first.
- **Not opening DevTools** when a style "isn't working" — the Elements/Inspector panel
  shows every rule targeting an element and which one the cascade picked.

---

## Worked Exercise: a business card, built together

This is a small slice of today's task, solved together, live. Styling the full profile
page, and recreating the complete business card design from class, you build the same
way, as stub files in `exercises/`.

### Problem statement
Style a simple business card: a name, a title, and one line of contact info, in a
bordered box with a background color, comfortable spacing, and readable type.

### Thinking it through
1. The card is one rectangular box → the box model: padding for breathing room inside,
   a border to define its edge, margin to keep it clear of the page edge.
2. `box-sizing: border-box` first, so the width I pick is the width I actually get.
3. Name is the most important line → largest, boldest text (`h2`, not `h1` — this isn't
   the page's main heading). Title and contact info are supporting text → smaller,
   lighter weight, a muted color.
4. Spacing between the three lines uses `margin`, not manual line breaks.

### Solution
See [`exercises/example.html`](./exercises/example.html) and
[`exercises/example.css`](./exercises/example.css) — fully solved and commented.

```css
* {
  box-sizing: border-box;
}

.business-card {
  width: 320px;
  padding: 24px;
  margin: 40px auto;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background-color: #ffffff;
  font-family: Arial, Helvetica, sans-serif;
  text-align: center;
}

.business-card h2 {
  margin: 0 0 4px;
  font-size: 1.5rem;
  color: #111827;
}

.business-card .title {
  margin: 0 0 12px;
  font-size: 1rem;
  color: #6b7280;
}

.business-card .contact {
  margin: 0;
  font-size: 0.875rem;
  color: #374151;
}
```

Open it directly in a browser to check it renders — no server needed for a static
HTML file:
```bash
open exercises/example.html      # macOS
xdg-open exercises/example.html  # Linux
```

### What to notice
- Every spacing value came from the box model, not trial and error — padding for the
  card's interior, margin to center it and separate its lines.
- The visual hierarchy (name > title > contact) is built entirely with `font-size`,
  `font-weight`, and `color` — no change to the HTML structure at all. That's the point
  of separating structure (HTML) from presentation (CSS).

---

## Your turn — finish the task of the day

| # | Exercise | Files | Concept practiced |
|---|----------|-------|--------------------|
| 1 | Style yesterday's profile page | `exercises/profile.css` (link it from your Day 2 `exercises/profile.html`) | selectors, box model, typography, backgrounds, applied to a real page |
| 2 | Recreate the business card design from class | `exercises/business-card.html`, `exercises/business-card.css` | full styling pass on a fresh structure: colors, spacing, box model |

**Exercise 1 — style the profile page:**
1. Open your completed `../day-02/exercises/profile.html`.
2. Add a stylesheet link in its `<head>`: `<link rel="stylesheet" href="../../day-03/exercises/profile.css" />`.
3. Fill in `exercises/profile.css` — a color scheme (pick 2-3 colors and stay
   consistent), a custom `font-family` on `body`, and proper spacing (padding/margin)
   around each `<section>`. Use classes, not IDs, for anything you might reuse.
4. Re-open `profile.html` in the browser after every change to check your work.

**Exercise 2 — the business card:**
`exercises/business-card.html` is a stub with the structure already in place (see the
comment block at the top of the file for what it contains). Style it in
`exercises/business-card.css` to match the design shown in class — same process as the
worked exercise above: box model first, then typography, then color.

Once both are done, push your changes to your `seed-internship` repo.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
