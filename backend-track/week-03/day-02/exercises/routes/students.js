// Students router — unchanged in shape from Day 8: routes stay thin, each one just
// points at a controller function. GET / and POST / are SOLVED. Uncomment the rest as
// you finish the matching controller function in controllers/students.js.

import express from "express";
import * as studentsController from "../controllers/students.js";

const router = express.Router();

// ----- SOLVED -----
router.get("/", studentsController.listStudents);
router.post("/", studentsController.createStudent);

// ----- TODO Step 2: GET /students/:id -----
// router.get("/:id", studentsController.getStudent);

// ----- TODO Step 3: PUT /students/:id -----
// router.put("/:id", studentsController.updateStudent);

// ----- TODO Step 4: DELETE /students/:id -----
// router.delete("/:id", studentsController.deleteStudent);

export default router;
