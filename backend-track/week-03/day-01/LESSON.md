# Day 9 — Teaching Lesson: MongoDB — Documents & Atlas

> Companion to `README.md`. This is a **step-by-step walkthrough** — each numbered step
> builds on the one before it. By the end you'll have a real cloud database running,
> a `library` collection seeded with books, and one query solved live to copy the shape
> of the other nine you write yourself in `exercises/library-queries.js`.

## Objective
Learn to think in documents instead of tables/rows, and get a real cloud database
running on MongoDB Atlas.

## What you're doing today
- Create a free Atlas cluster and connect to it with Compass.
- Create a `library` database with a `books` collection, and insert 10 documents.
- Write 10 queries against that collection — filters, comparisons, membership,
  projection, and sorting.

No Node code today — everything runs as a query, either clicked together in Compass or
typed as a `mongosh` script. Tomorrow's Mongoose lesson is where this connects to Express.

---

## Step 1 — SQL vs NoSQL
**Definition:** SQL databases (Postgres, MySQL) store data in tables with a fixed
schema — every row has the same columns — and relate tables to each other with foreign
keys and JOINs. MongoDB stores data in **collections** of **documents** — JSON-like
objects with no fixed shape — and related data can live embedded inside a document or
be referenced by id, your choice per case.

```json
{
  "title": "Dune",
  "author": "Frank Herbert",
  "genre": "Science Fiction",
  "year": 1965,
  "pages": 412,
  "read": false,
  "tags": ["classic", "space"]
}
```
That whole object is one document. No separate "tags table" needed for a small array
like this — it just lives on the book.

**Checkpoint:** could you draw this same book as a row in a spreadsheet? Everything
except `tags` fits fine in a column — `tags` is the first hint of why a flexible
document shape is sometimes easier than a rigid table.

---

## Step 2 — Vocabulary
| MongoDB term | Rough SQL equivalent |
|---|---|
| Database | Database |
| Collection | Table |
| Document | Row |
| Field | Column |
| `_id` | Primary key (auto-generated `ObjectId` unless you set your own) |

**Checkpoint:** in today's exercise, `library` is the database, `books` is the
collection, and each book you insert is one document.

---

## Step 3 — Create your Atlas cluster (click-by-click)
1. Go to the MongoDB Atlas site and register for a free account (email or Google
   sign-in both work).
2. You land on **"Deploy your database"**. Pick the **M0 Free** tier, leave the
   default cloud provider/region (or pick one close to you), optionally rename the
   cluster (default `Cluster0` is fine), then click **Create Deployment**.
3. A **"Security Quickstart"** panel pops up automatically:
   - **Username/password:** type a username and password for a database user, then
     click **Create Database User**. Write these down — you'll paste them into the
     connection string in a moment.
   - **Where would you like to connect from?**: click **Add My Current IP Address**
     (or, for class purposes only, add `0.0.0.0/0` to allow any IP — never do this on
     a real project). Click **Finish and Close**.
4. Wait for the cluster card to show a green **active** status — provisioning takes a
   minute or two. Grab a coffee, don't refresh anxiously.
5. Click the **Connect** button on the cluster card, choose **Compass** from the list
   of connection methods, and copy the full connection string it shows you (it already
   has your username baked in — you just need to swap in the password from step 3).
6. If you don't have Compass installed yet, download it from the MongoDB Compass page
   and install it now.
7. Open Compass, paste the connection string into the **New Connection** field,
   replace `<password>` with your actual password, and click **Connect**.

**Checkpoint:** Compass's left sidebar now lists your cluster's databases (just the
built-in `admin`, `local`, `config` for now — nothing custom yet). If you see that,
the cluster and the connection both work.

---

## Step 4 — Create the `library` database and `books` collection
Atlas doesn't let you create an empty database — Mongo only creates a database (and a
collection) the first time you actually put a collection in it, so Compass asks for
both names at once.

1. In Compass's left sidebar, click the **Create database** button (a `+` icon next to
   the list of databases, or the green **"Create database"** button on the main
   Databases view).
2. In the dialog: **Database Name** → `library`, **Collection Name** → `books`.
3. Click **Create Database**.

**Checkpoint:** `library` now appears in the sidebar, and expanding it shows one
collection, `books`, currently reporting "This collection has no documents."

---

## Step 5 — CRUD, one operation at a time
**Definition:** CRUD is Create, Read, Update, Delete — the four things you do to data,
whichever database you're using.

```js
// Create
db.books.insertOne({ title: "Dune", author: "Frank Herbert" });
db.books.insertMany([ /* array of book objects */ ]);

// Read
db.books.find({ genre: "Fantasy" });

// Update
db.books.updateOne({ title: "Dune" }, { $set: { read: true } });

// Delete
db.books.deleteOne({ title: "Dune" });
```

### Inserting through Compass, step by step
You have two options for getting documents in — both are valid, use whichever feels
more natural:

**Option A — the GUI, one document (or a pasted array) at a time:**
1. Open the `books` collection, click the green **Add Data** button, then
   **Insert Document**.
2. A dialog opens in a form view by default — click the `{}` icon top-right to switch
   to **JSON view**, which lets you paste a full object (or even an array of objects —
   Compass inserts every item in the array).
3. Paste a book object (see Step 1's example, or the seed list in
   `exercises/library-queries.js`), then click **Insert**.
4. Repeat, or paste all 10 at once as a JSON array `[ {...}, {...}, ... ]` in the same
   dialog.

**Option B — the embedded shell, all 10 at once:**
1. In Compass, open the **`_MONGOSH`** tab at the bottom of the window (the built-in
   shell — no separate install needed).
2. Type or paste `db.books.insertMany([ ... ])` with your 10 book objects and press
   Enter. All 10 land in one command, exactly like running the same line from a
   terminal.

Either way, the query bar (Read), the pencil icon on a document (Update), and the
trash icon (Delete) cover the rest of CRUD without typing anything.

**Checkpoint:** insert one throwaway document with **Insert Document**, confirm it
appears in the document list below, then delete it with the trash icon. That round
trip is three of the four CRUD verbs — Update is the pencil icon on any document.

---

## Step 6 — Query filters
**Definition:** a filter is the object you pass to `find()` describing which documents
you want back. An empty filter `{}` means "all of them."

```js
db.books.find({ genre: "Fantasy" });              // equality
db.books.find({ year: { $gt: 2000 } });           // comparison: $gt $gte $lt $lte $ne
db.books.find({ genre: { $in: ["Fantasy", "Horror"] } }); // membership
db.books.find({ read: true, pages: { $lt: 300 } }); // implicit AND (multiple fields)
db.books.find({}, { title: 1, author: 1, _id: 0 }); // projection: only these fields
db.books.find().sort({ year: -1 });               // sort descending
db.books.find().sort({ year: 1 }).limit(1);        // oldest book only
```
**Checkpoint:** run `db.books.find({ genre: "Fantasy" })` right now against whatever's
in your collection (even if it's empty) — an empty array back is a correct result, not
an error.

---

## Step 7 — Embedding vs referencing (first pass)
**Definition:** embedding puts related data directly inside the parent document.
Referencing stores just the other document's `_id` and looks it up separately when
needed.

- **Embed** when the data is always read together with its parent and doesn't grow
  unbounded — a book's `tags` array.
- **Reference** when the data is large, shared across many documents, or updated
  independently — an `author` document that many books point to by `_id`.

Today you'll only embed (tags on a book). Referencing comes back once relationships get
more complex, later in the track.

**Checkpoint:** if you added a `reviews` array with hundreds of entries per book, would
you still embed it? (No — that's exactly the "grows unbounded" case referencing exists
for.)

---

## Worked Exercise: seed the collection and run the first query together

This is solved live, in the session — the shape every one of today's 10 queries reuses.

### Problem statement
Insert 10 book documents into `library.books`, then write a query that returns every
book in one specific genre.

### Thinking it through
1. Ten related documents going in at once → `insertMany`, not ten separate
   `insertOne` calls (Step 5).
2. Vary `genre`, `year`, `pages`, and `read` across the 10 books — otherwise every query
   you write today returns either everything or nothing, and you can't tell if the
   filter is actually working.
3. "All books in one genre" is a plain equality filter (Step 6) — no operators needed
   yet, just `{ genre: "Fantasy" }`.

### Solution
See [`exercises/library-queries.js`](./exercises/library-queries.js) — the seed data and
Query 1 are fully solved and commented.

```js
db.books.insertMany([
  { title: "Dune", author: "Frank Herbert", genre: "Science Fiction", year: 1965, pages: 412, read: false, tags: ["classic", "space"] },
  { title: "The Hobbit", author: "J.R.R. Tolkien", genre: "Fantasy", year: 1937, pages: 310, read: true, tags: ["classic"] },
  // ... 8 more, see the file
]);

// Query 1 — all books in one genre
db.books.find({ genre: "Fantasy" });
```

Run it (from the Atlas connection string):
```bash
mongosh "<your-connection-string>" exercises/library-queries.js
```
Or paste the same lines straight into Compass's query bar / the embedded shell.

### What to notice
- `insertMany` takes an array — one `{...}` per book, comma-separated, exactly like the
  arrays of objects you built back in Week 1.
- The filter `{ genre: "Fantasy" }` matches on exact value — case and spelling have to
  line up exactly with what you inserted.
- Nothing here needed an operator (`$gt`, `$in`, ...) — plain equality is still the most
  common filter shape you'll write.

---

## Your turn — today's task

Open `exercises/library-queries.js` — the seed data (10 books) and Query 1 are already
solved. Write queries 2–10 where it says `// TODO`, running each one the same way as the
worked exercise before moving to the next.

| # | Query | Concept exercised |
|---|-------|--------------------|
| 1 | All books in one genre | equality — **solved** |
| 2 | Books published after year 2000 | `$gt` |
| 3 | Books with fewer than 300 pages | `$lt` |
| 4 | Books that are `read: true` | equality on a boolean |
| 5 | Books whose genre is one of two values | `$in` |
| 6 | Books published between two years | `$gte` + `$lte` on the same field |
| 7 | All books, only `title` and `author` returned | projection |
| 8 | All books sorted by year, newest first | `.sort({ year: -1 })` |
| 9 | The single oldest book | `.sort()` + `.limit(1)` |
| 10 | Books in a genre AND under a page count | combining two filters on one query |

Whichever tool you use (Compass query bar or `mongosh`), keep a copy of every query you
ran in the file — that's what gets submitted.

### Common mistakes to watch for
- **Comparing strings without matching case/spelling exactly** — `"fantasy"` won't match
  documents stored as `"Fantasy"`.
- **Forgetting `insertMany` takes an array** — a bare object without the surrounding
  `[ ]` throws, since `insertMany` always expects a list, even of one.
- **Mixing up `$gt`/`$lt` direction** — `$gt` means *greater than*, so "after year 2000"
  is `{ year: { $gt: 2000 } }`, not `$lt`.
- **Forgetting projection needs `_id: 0` to actually hide the id** — `_id` is included by
  default even when you only ask for other fields.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
