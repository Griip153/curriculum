// Express entry point — Day 8
// ES Modules this time (package.json has "type": "module") — import/export instead
// of require/module.exports. Everything from Day 7 (the logger, express.json(), the
// students router) carries over as SOLVED. Today's new pieces — loading .env, the
// global 404 handler, and the central error-handling middleware — are your TODOs.
// See LESSON.md for the walkthrough.
//
// Run: npm run dev   (nodemon, auto-restarts on save)
//   or: npm start    (plain node, no auto-restart)

import "dotenv/config";
import express from "express";
import studentsRouter from "./routes/students.js";

const app = express();
const PORT = process.env.PORT || 3000;

// ----- SOLVED (carried over from Day 7): request logger -----
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} ${req.method} ${req.url}`);
  next();
});

// ----- SOLVED (carried over from Day 7): express.json() -----
app.use(express.json());

// ----- SOLVED: GET /health -----
app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

// ----- SOLVED: mounting the students router -----
// routes/students.js no longer holds any logic itself — see LESSON.md "Step 2".
app.use("/students", studentsRouter);

// ----- TODO Step 5: global 404 handler -----
// Goes AFTER every route/router above (if execution reaches here, nothing matched)
// and BEFORE the error handler below. See LESSON.md "Step 5".
//
// app.use((req, res) => {
//   res.status(404).json({ error: `Route ${req.method} ${req.originalUrl} not found` });
// });

// ----- TODO Step 4: central error-handling middleware -----
// Must be the LAST app.use() call, and its handler must take exactly FOUR
// arguments (err, req, res, next) — that's how Express recognises it as an error
// handler instead of regular middleware. See LESSON.md "Step 4".
//
// app.use((err, req, res, next) => {
//   console.error(err);
//   res.status(err.statusCode || 500).json({ error: err.message || "Something went wrong" });
// });

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
