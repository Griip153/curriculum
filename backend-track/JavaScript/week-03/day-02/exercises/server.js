// Express entry point — Day 10.
// Everything from Day 8 (the logger, express.json(), the students router, the 404 and
// error-handling middleware) carries over as SOLVED. The new piece today is
// connectDB() — see config/db.js and LESSON.md "Step 2" — awaited before the server
// starts listening, so the very first request never races an unfinished connection.
//
// Run: npm run dev   (nodemon, auto-restarts on save)
//   or: npm start    (plain node, no auto-restart)

import "dotenv/config";
import express from "express";
import { connectDB } from "./config/db.js";
import studentsRouter from "./routes/students.js";

const app = express();
const PORT = process.env.PORT || 3000;

app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} ${req.method} ${req.url}`);
  next();
});

app.use(express.json());

app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

app.use("/students", studentsRouter);

app.use((req, res) => {
  res.status(404).json({ error: `Route ${req.method} ${req.originalUrl} not found` });
});

// ----- STRETCH GOAL: add an `error.name === "CastError"` check here, before the
// generic fallback, and respond 400 with "Invalid student id" — see LESSON.md.
app.use((err, req, res, next) => {
  console.error(err);
  res.status(err.statusCode || 500).json({ error: err.message || "Something went wrong" });
});

async function start() {
  await connectDB();
  app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
  });
}

start();
