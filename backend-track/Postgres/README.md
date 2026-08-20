# PostgreSQL — A Complete Beginner's Lesson

## Objective
Understand PostgreSQL itself, deeply — not just enough SQL to pass a query, but a
real working knowledge of how it stores data, enforces rules, connects to
applications, and stays fast as it grows.

## Who this is for
Someone who has never used a real database before, or who has only used SQLite/a
JSON file and wants to understand what a "real," production-grade relational
database adds on top.

## Concepts covered
What PostgreSQL is and how it differs from SQLite; installing it and connecting with
`psql`; databases, schemas, tables; data types; constraints (`NOT NULL`, `UNIQUE`,
`CHECK`, foreign keys); `SELECT`/`WHERE`/`ORDER BY`/`LIMIT` in depth; `JOIN`s (inner,
left, right, full); `GROUP BY`/`HAVING`/aggregate functions; subqueries and CTEs;
indexes and `EXPLAIN`; transactions and `ACID`; users, roles, and permissions;
connecting from Python with `psycopg2` and SQLAlchemy; backups with `pg_dump`; a
common-mistakes and troubleshooting reference.

## Watch before reading
- "PostgreSQL Tutorial for Beginners" — freeCodeCamp
- "PostgreSQL in 100 Seconds" — Fireship
- "SQL Joins Explained" — any short visual explainer (Joins are easiest to
  understand visually first, then in SQL)

## How to use this lesson
Read `LESSON.md` top to bottom, in order — later sections build on earlier ones.
Every SQL example is written to be typed and run yourself in `psql` (or a GUI like
pgAdmin/DBeaver) as you go. There is no separate "task of the day" — the worked
examples throughout **are** the exercises; type every one of them yourself rather
than only reading them.

---
*This lesson is a standalone deep-dive — it doesn't require any of the FastAPI
material to follow along, though it directly supports Week 3, Day 9-10 of the
`backend-python` track if you're using it alongside that.*
