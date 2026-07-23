// Express entry point — Day 7
// The logger middleware, express.json(), GET /health, and mounting the students
// router are all SOLVED — worked together in the session, see LESSON.md.
// The actual CRUD logic lives in routes/students.js — that's where your TODOs are.
//
// Run: npm run dev   (nodemon, auto-restarts on save)
//   or: npm start    (plain node, no auto-restart)

const express = require("express");
const studentsRouter = require("./routes/students");

const app = express();
const PORT = 3000;

// ----- SOLVED: a custom middleware — logs every request -----
// A middleware is just a function of (req, res, next). Whatever it does, it must
// call next() to hand control to the next middleware/route — forgetting next()
// leaves every request hanging forever, same failure shape as forgetting res.end()
// on the raw server yesterday.
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} ${req.method} ${req.url}`);
  next();
});

// ----- SOLVED: express.json() — built-in middleware that parses a JSON request
// body into req.body for you. Compare to yesterday's manual req.on("data"/"end").
app.use(express.json());

// ----- SOLVED: GET /health -----
app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

// ----- SOLVED: mounting the students router -----
// Every route defined inside routes/students.js is automatically prefixed with
// "/students" — a route written as router.get("/") really answers GET /students.
app.use("/students", studentsRouter);

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
