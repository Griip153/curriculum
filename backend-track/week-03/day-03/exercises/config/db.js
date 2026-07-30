// MongoDB connection — unchanged from your completed Day 10 assignment.
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
