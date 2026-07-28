// Library queries — today's task, built one query at a time.
// Seed data + Query 1 are SOLVED — worked together in the session, see LESSON.md.
// Queries 2-10 are your TODO. Do them in order, running each one before starting the
// next, and keep every query in this file (that's what gets submitted).
//
// Run against your Atlas cluster:
//   mongosh "<your-connection-string>" exercises/library-queries.js
// Or paste each block into Compass's query bar / embedded shell one at a time.

// ----- Seed data: 10 books, deliberately varied so the queries below return
// different results (mix of genre, year, pages, and read status) -----
db.books.insertMany([
  {
    title: "Dune",
    author: "Frank Herbert",
    genre: "Science Fiction",
    year: 1965,
    pages: 412,
    read: false,
    tags: ["classic", "space"],
  },
  {
    title: "The Hobbit",
    author: "J.R.R. Tolkien",
    genre: "Fantasy",
    year: 1937,
    pages: 310,
    read: true,
    tags: ["classic"],
  },
  {
    title: "Neuromancer",
    author: "William Gibson",
    genre: "Science Fiction",
    year: 1984,
    pages: 271,
    read: false,
    tags: ["cyberpunk"],
  },
  {
    title: "A Game of Thrones",
    author: "George R.R. Martin",
    genre: "Fantasy",
    year: 1996,
    pages: 694,
    read: true,
    tags: ["epic"],
  },
  {
    title: "1984",
    author: "George Orwell",
    genre: "Dystopian",
    year: 1949,
    pages: 328,
    read: true,
    tags: ["classic", "political"],
  },
  {
    title: "Mistborn",
    author: "Brandon Sanderson",
    genre: "Fantasy",
    year: 2006,
    pages: 541,
    read: false,
    tags: ["magic"],
  },
  {
    title: "The Martian",
    author: "Andy Weir",
    genre: "Science Fiction",
    year: 2011,
    pages: 369,
    read: true,
    tags: ["space"],
  },
  {
    title: "Brave New World",
    author: "Aldous Huxley",
    genre: "Dystopian",
    year: 1932,
    pages: 288,
    read: false,
    tags: ["classic"],
  },
  {
    title: "The Name of the Wind",
    author: "Patrick Rothfuss",
    genre: "Fantasy",
    year: 2007,
    pages: 662,
    read: false,
    tags: ["magic"],
  },
  {
    title: "Foundation",
    author: "Isaac Asimov",
    genre: "Science Fiction",
    year: 1951,
    pages: 255,
    read: true,
    tags: ["classic", "space"],
  },
]);

// ----- Query 1 — all books in one genre (SOLVED) -----
db.books.find({ genre: "Fantasy" });

// ----- TODO Query 2 — books published after year 2000 -----
// Comparison operator: $gt. Filter shape: { year: { $gt: 2000 } }.

// ----- TODO Query 3 — books with fewer than 300 pages -----
// Comparison operator: $lt.

// ----- TODO Query 4 — books that are read: true -----
// Plain equality on a boolean field.

// ----- TODO Query 5 — books whose genre is one of two values -----
// Membership operator: $in. Filter shape: { genre: { $in: [...] } }.

// ----- TODO Query 6 — books published between two years (inclusive) -----
// Combine $gte and $lte on the same field: { year: { $gte: ..., $lte: ... } }.

// ----- TODO Query 7 — all books, only title and author returned -----
// Projection: second argument to find(). Remember _id: 0 to hide the id.

// ----- TODO Query 8 — all books sorted by year, newest first -----
// .sort({ year: -1 })

// ----- TODO Query 9 — the single oldest book -----
// .sort({ year: 1 }).limit(1)

// ----- TODO Query 10 — books in a genre AND under a page count -----
// Two conditions on one query: { genre: "...", pages: { $lt: ... } }.
