// Students router — Day 11: the write routes now run validation middleware before
// the controller ever sees the request. GET routes are unchanged from Day 10. POST is
// SOLVED — createStudentValidator wired in as the worked example. PUT is your TODO —
// see LESSON.md "Your Turn" Step 1.

import express from "express";
import * as studentsController from "../controllers/students.js";
import {
  createStudentValidator,
  updateStudentValidator,
  handleValidationErrors,
} from "../validators/students.js";

const router = express.Router();

router.get("/", studentsController.listStudents);
router.get("/:id", studentsController.getStudent);

// ----- SOLVED -----
router.post(
  "/",
  createStudentValidator,
  handleValidationErrors,
  studentsController.createStudent
);

// ----- TODO Step 1: wire updateStudentValidator + handleValidationErrors in here,
// the same way POST / does it above -----
router.put("/:id", studentsController.updateStudent);

router.delete("/:id", studentsController.deleteStudent);

export default router;
