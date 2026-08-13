# Day 9 — Teaching Lesson: SQL & Relational Databases

> Companion to `README.md`. This lesson assumes zero prior SQL knowledge. Today has
> **no Python at all** — just the database and its own language, SQL, so you can
> think clearly about queries before FastAPI is in the mix tomorrow.

## Objective
Learn to think in tables and rows, and get comfortable writing SQL by hand.

## 0. Why a real database, and why SQL

Every list you've stored so far — in a Python list, then a JSON file — has one
problem: to find, say, "every book borrowed by Ada," you'd have to load *everything*
into memory and loop through it by hand in Python. A **relational database** stores
data in **tables** and lets you ask precise questions about it directly, using a
dedicated query language: **SQL** (Structured Query Language). It's dramatically
faster at scale, and it's the standard tool for exactly this job.

**Definition:** A relational database organises data into **tables** (like a
spreadsheet: rows and columns), where relationships *between* tables (a book has one
borrower; a borrower can have many books) are expressed with shared identifiers,
rather than nesting one JSON object inside another.

## 1. SQLite — a database with zero setup

**Definition:** SQLite is a complete relational database that lives in a single file
on disk, with no separate server process to install or run — perfect for learning,
and genuinely used in production for small-to-medium apps. Python has it built into
the standard library.

Open a Python shell and try it directly:
```bash
python3
```
```python
import sqlite3
conn = sqlite3.connect("library.db")   # creates library.db if it doesn't exist
cursor = conn.cursor()
```
**Definition:** A **connection** is a live link to the database file. A **cursor** is
the object you use to actually run SQL commands and read results back through that
connection.

You'll use the free **DB Browser for SQLite** app (download from
sqlitebrowser.org) alongside the terminal today — it lets you see your tables and run
queries visually, which helps a lot while you're still building a mental model of
what SQL is doing.

## 2. Creating a table

**Definition:** `CREATE TABLE` defines a table's shape — its columns and each
column's data type — before any data can be inserted into it.

```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER,
    available INTEGER DEFAULT 1
);
```
**Reading each piece:**
- `id INTEGER PRIMARY KEY AUTOINCREMENT` — every table needs a **primary key**: a
  column that uniquely identifies each row. `AUTOINCREMENT` means SQLite assigns the
  next number automatically — you never set `id` yourself, the same rule as the `id`
  fields you've been auto-assigning in Python all track.
- `TEXT`, `INTEGER` — SQLite's basic column types (also `REAL` for decimals, `BLOB`
  for binary data).
- `NOT NULL` — a **constraint**: this column can never be left empty. The database
  itself rejects an `INSERT` that violates this — not your application code.
- `DEFAULT 1` — if not provided, this column gets this value automatically.

Run it from Python:
```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER,
        available INTEGER DEFAULT 1
    )
""")
conn.commit()
```
**Definition:** `conn.commit()` saves your changes permanently to the file. Without
it, changes only exist in memory for that connection and can be lost. `IF NOT EXISTS`
avoids an error if you accidentally run the `CREATE TABLE` twice.

## 3. Inserting rows

**Definition:** `INSERT INTO` adds a new row to a table.

```sql
INSERT INTO books (title, author, year) VALUES ('Dune', 'Frank Herbert', 1965);
```
From Python, **always** use `?` placeholders instead of building the SQL string with
Python's own string formatting — this is not a style preference, it prevents a
serious security hole called **SQL injection** (you'll cover this properly in Week 7,
Day 1, but the habit starts today):
```python
cursor.execute(
    "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
    ("Dune", "Frank Herbert", 1965),
)
conn.commit()
```

## 4. Reading rows: `SELECT`, `WHERE`, `ORDER BY`

**Definition:** `SELECT` retrieves rows. `WHERE` filters which rows come back. `ORDER
BY` controls the order they come back in.

```sql
SELECT * FROM books;                              -- every column, every row
SELECT title, author FROM books;                   -- only these two columns
SELECT * FROM books WHERE year > 1960;              -- only matching rows
SELECT * FROM books WHERE available = 1;
SELECT * FROM books ORDER BY year DESC;             -- newest first
SELECT * FROM books ORDER BY year DESC LIMIT 3;     -- only the top 3
```
From Python, `.fetchall()` gets every matching row back as a list of tuples;
`.fetchone()` gets just the first:
```python
cursor.execute("SELECT * FROM books WHERE year > ?", (1960,))
rows = cursor.fetchall()
for row in rows:
    print(row)
```

## 5. Updating and deleting

**Definition:** `UPDATE` changes existing rows; `DELETE` removes them. **Both are
dangerous without a `WHERE` clause** — without one, they apply to *every row in the
table*. Always write and check your `WHERE` clause before running either.

```sql
UPDATE books SET available = 0 WHERE id = 1;
DELETE FROM books WHERE id = 5;
```

## 6. A second table and `JOIN`

**Definition:** A `JOIN` combines rows from two tables based on a shared column,
letting you ask questions that span both — the entire reason data gets split across
multiple tables instead of one giant one.

```sql
CREATE TABLE borrowers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    book_id INTEGER,
    FOREIGN KEY (book_id) REFERENCES books(id)
);
```
**Definition:** A **foreign key** is a column in one table that stores the primary
key of a row in another table — this is *the* mechanism relational databases use to
express "this row relates to that row," the SQL equivalent of nesting an object
inside another in JSON, but without duplicating the data.

```sql
INSERT INTO borrowers (name, book_id) VALUES ('Ada', 1);

SELECT borrowers.name, books.title
FROM borrowers
JOIN books ON borrowers.book_id = books.id;
```
This returns each borrower's name next to the title of the book they borrowed —
data assembled from two separate tables in one query.

---

## Worked example: 3 queries against the library

### Problem statement
Given the `books` table above with a handful of rows, write queries to: (1) find
every book published after 1970, sorted newest-first; (2) count how many books are
currently available; (3) find the title of the book borrowed by "Ada."

### Solution
See [`exercises/library_queries.py`](./exercises/library_queries.py) — a complete,
runnable script that creates the tables, inserts sample data, and answers these three
queries, fully commented.

```python
# Query 1 — books after 1970, newest first
cursor.execute("SELECT * FROM books WHERE year > ? ORDER BY year DESC", (1970,))

# Query 2 — count available books
cursor.execute("SELECT COUNT(*) FROM books WHERE available = 1")
count = cursor.fetchone()[0]

# Query 3 — Ada's borrowed book title, via JOIN
cursor.execute("""
    SELECT books.title FROM borrowers
    JOIN books ON borrowers.book_id = books.id
    WHERE borrowers.name = ?
""", ("Ada",))
```
Run it:
```bash
python3 exercises/library_queries.py
```

### What to notice
- `COUNT(*)` is an **aggregate function** — it computes one summary value across many
  rows, instead of returning the rows themselves. You'll meet more of these
  (`SUM`, `AVG`, `GROUP BY`) properly in Week 7, Day 3.
- `.fetchone()[0]` — `fetchone()` still returns a tuple even for one value, so `[0]`
  grabs the first (only) item out of it.
- The `JOIN` query never repeats book data anywhere — that's the entire benefit of
  splitting related data into separate tables with foreign keys, instead of copying a
  book's title into every borrower's row.

---

## Your turn — 10 query exercises

Open [`exercises/library_queries.py`](./exercises/library_queries.py) and complete
the 10 numbered `# TODO` queries at the bottom, using the `books` and `borrowers`
tables already set up for you at the top of the file. Each one has a comment
describing what it should return. Run the file after each one to check your work —
it prints results as you go.

Topics covered across the 10: filtering with `WHERE`, sorting with `ORDER BY`,
limiting with `LIMIT`, counting with `COUNT(*)`, updating a row, deleting a row, and
two more `JOIN` queries.

---

## Common mistakes to watch for
- **`UPDATE`/`DELETE` without a `WHERE` clause** — always double-check this before
  running either. In DB Browser, you can inspect the affected rows visually first.
- **Building SQL strings with f-strings/`+` instead of `?` placeholders** — never do
  this with any value that came from a user, ever. It's the #1 cause of SQL
  injection vulnerabilities in real applications.
- **Forgetting `conn.commit()`** after an `INSERT`/`UPDATE`/`DELETE` — your changes
  silently don't persist.
- **Confusing `WHERE` with `HAVING`** — you'll meet `HAVING` in Week 7; for now just
  know `WHERE` filters individual rows, before any grouping happens.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
