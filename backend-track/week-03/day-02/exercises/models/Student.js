// Student model — Day 10.
// The schema shape (name, score) is SOLVED. TODO Step 1 (LESSON.md "Your Turn"):
// add the validation rules — min/max on score, trim on name — so bad input actually
// gets rejected before it reaches the database.

import mongoose from "mongoose";

const studentSchema = new mongoose.Schema({
  name: { type: String, required: true /* TODO Step 1: , trim: true */ },
  score: { type: Number, required: true /* TODO Step 1: , min: 0, max: 100 */ },
});

export default mongoose.model("Student", studentSchema);
