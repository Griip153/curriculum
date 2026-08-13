# Day 9 - SQL practice against a small SQLite "library" database.
# The setup (tables + sample data) and the 3 worked queries are SOLVED.
# Exercises 4-13 below are the "10 query exercises" from the task of the day
# - each is a # TODO. Run this file after each one to check your work.
#
# Run: python3 exercises/library_queries.py

import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# --- Setup: tables -----------------------------------------------------
cursor.execute("DROP TABLE IF EXISTS borrowers")
cursor.execute("DROP TABLE IF EXISTS books")

cursor.execute("""
    CREATE TABLE books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER,
        available INTEGER DEFAULT 1
    )
""")

cursor.execute("""
    CREATE TABLE borrowers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        book_id INTEGER,
        FOREIGN KEY (book_id) REFERENCES books(id)
    )
""")

# --- Setup: sample data --------------------------------------------------
books = [
    ("Dune", "Frank Herbert", 1965, 1),
    ("Neuromancer", "William Gibson", 1984, 1),
    ("Foundation", "Isaac Asimov", 1951, 1),
    ("Snow Crash", "Neal Stephenson", 1992, 1),
    ("The Left Hand of Darkness", "Ursula K. Le Guin", 1969, 1),
    ("1984", "George Orwell", 1949, 1),
    ("Brave New World", "Aldous Huxley", 1932, 1),
    ("Fahrenheit 451", "Ray Bradbury", 1953, 1),
    ("The Martian", "Andy Weir", 2011, 1),
    ("Project Hail Mary", "Andy Weir", 2021, 1),
]
cursor.executemany(
    "INSERT INTO books (title, author, year, available) VALUES (?, ?, ?, ?)",
    books,
)
cursor.execute("INSERT INTO borrowers (name, book_id) VALUES (?, ?)", ("Ada", 1))
cursor.execute("INSERT INTO borrowers (name, book_id) VALUES (?, ?)", ("Kofi", 4))
conn.commit()

print("=== Worked queries ===")

# Query 1 - books after 1970, newest first
cursor.execute("SELECT title, year FROM books WHERE year > ? ORDER BY year DESC", (1970,))
print("After 1970:", cursor.fetchall())

# Query 2 - count available books
cursor.execute("SELECT COUNT(*) FROM books WHERE available = 1")
print("Available count:", cursor.fetchone()[0])

# Query 3 - Ada's borrowed book title, via JOIN
cursor.execute("""
    SELECT books.title FROM borrowers
    JOIN books ON borrowers.book_id = books.id
    WHERE borrowers.name = ?
""", ("Ada",))
print("Ada is reading:", cursor.fetchone()[0])

print("\n=== Your turn (exercises 4-13) ===")

# TODO 4: select every book title and author, no filtering (SELECT title, author FROM books)

# TODO 5: select all books by "Andy Weir"

# TODO 6: select the 3 oldest books (ORDER BY year ASC LIMIT 3)

# TODO 7: select all books published between 1950 and 1970 (WHERE year BETWEEN ? AND ?)

# TODO 8: select all book titles that contain the word "The" (hint: WHERE title LIKE '%The%')

# TODO 9: mark "Dune" as unavailable (UPDATE books SET available = 0 WHERE title = ?)

# TODO 10: count how many books are now unavailable (should be 1, after exercise 9)

# TODO 11: delete "1984" from the books table

# TODO 12: select every borrower's name next to the title AND year of the book they borrowed (JOIN, 3 columns)

# TODO 13: select the titles of every book that has NOT been borrowed by anyone
#          (hint: look up "SQL NOT IN subquery", or "LEFT JOIN ... WHERE ... IS NULL")

conn.close()
