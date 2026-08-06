// Student model — unchanged from your completed Day 10 assignment.
// Schema validation is still the last line of defense — request validation
// (validators/students.js) is what catches most bad input before it gets here.

import mongoose from "mongoose";

const studentSchema = new mongoose.Schema({
  name: { type: String, required: true, trim: true },
  score: { type: Number, required: true, min: 0, max: 100 },
});

export default mongoose.model("Student", studentSchema);
