# Day 6 — Node.js In Depth

## Objective
Understand the platform itself — npm, modules, and what Node gives you beyond the language.

## Concepts
npm and package.json (scripts, dependencies); CommonJS vs ES modules; fs, path, os modules; building a raw HTTP server once to see what Express saves you.

## Watch before the session
- "Node.js Crash Course" — Traversy Media
- Net Ninja — Node.js Crash Course playlist
- freeCodeCamp — Node.js and Express course (Node sections)

## Task of the day
Build a raw HTTP server (no Express) with several JSON routes: a health check, a list-all-students route, a get-one-student-by-id route, and a create-student route — with the student list saved to a JSON file on disk so it survives a restart. Add one more route that reports info about your machine using the `os` module. Then write an npm script to run the server with nodemon. Push with a proper .gitignore (node_modules! and the generated data file!). Full step-by-step instructions are in `LESSON.md`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
