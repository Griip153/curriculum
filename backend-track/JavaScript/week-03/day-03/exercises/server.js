// Express entry point — Day 11.
// Everything here is unchanged from Day 10 except the error handler at the bottom,
// which today learns to recognize Mongoose's own error types instead of reporting
// every failure as a generic 500. See LESSON.md "Your Turn" Steps 2-3.

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

app.use((err, req, res, next) => {
  // ----- TODO Step 2: if (err.name === "ValidationError") { ... } -----
  // A Mongoose ValidationError (e.g. from a runValidators failure on update) carries
  // an err.errors object keyed by field name — pull the first message out of it and
  // respond 400. Must come BEFORE the generic fallback below, and must `return`.

  // ----- TODO Step 3: if (err.name === "CastError") { ... } -----
  // A malformed :id (not a 24-character hex ObjectId) throws this before your
  // controller's findById/findByIdAndUpdate/findByIdAndDelete ever runs. Respond 400
  // with a message like "Invalid student id" — a client mistake, not a server one.

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
