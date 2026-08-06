// Students router — Day 8: routes are now THIN. Each one just points at a
// controller function; the actual logic moved to controllers/students.js.
// GET / and POST / are SOLVED — worked together in the session, see LESSON.md.
// Everything else is your TODO, in order — see LESSON.md "Your Turn".

import express from "express";
import * as studentsController from "../controllers/students.js";

const router = express.Router();

// ----- SOLVED -----
router.get("/", studentsController.listStudents);
router.post("/", studentsController.createStudent);

// ----- TODO Step 6: GET /students/:id -----
// router.get("/:id", studentsController.getStudent);

// ----- TODO Step 6: PUT /students/:id -----
// router.put("/:id", studentsController.updateStudent);

// ----- TODO Step 6: DELETE /students/:id -----
// router.delete("/:id", studentsController.deleteStudent);

export default router;
