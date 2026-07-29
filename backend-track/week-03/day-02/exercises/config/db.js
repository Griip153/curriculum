// MongoDB connection — Day 10.
// SOLVED — worked together in the session, see LESSON.md "Step 2".
// Called once from server.js, before the server starts accepting requests.

import mongoose from "mongoose";

export async function connectDB() {
  try {
    await mongoose.connect(process.env.DATABASE_URL);
    console.log("MongoDB connected");
  } catch (error) {
    console.error("MongoDB connection failed:", error.message);
    process.exit(1);
  }
}
