// Students controller — Day 8: this is where the actual logic lives now, moved out
// of routes/students.js. Every function has the shape (req, res, next) — same
// signature as middleware, which is why forwarding errors with next(err) works
// exactly the same way here as it does anywhere else.

let students = [
  { id: 1, name: "Ada", score: 91 },
  { id: 2, name: "Kofi", score: 68 },
  { id: 3, name: "Zara", score: 84 },
];
let nextId = 4;

// ----- SOLVED -----
export function listStudents(req, res) {
  res.json({ students });
}

// ----- SOLVED -----
export function createStudent(req, res) {
  const { name, score } = req.body;
  const newStudent = { id: nextId++, name, score };
  students.push(newStudent);
  res.status(201).json(newStudent);
}

// ----- TODO Step 6: getStudent -----
// Find by Number(req.params.id). Not found -> build an Error, set
// err.statusCode = 404, and call next(err) — do NOT res.status(404).json(...)
// yourself; let the central error handler in server.js format the response.
// Found -> res.json(student).
export function getStudent(req, res, next) {}

// ----- TODO Step 6: updateStudent -----
// Same not-found handling as getStudent (next(err) with statusCode 404). If
// found, overwrite name/score from req.body and respond 200 with the updated
// student.
export function updateStudent(req, res, next) {}

// ----- TODO Step 6: deleteStudent -----
// Same not-found handling. If found, splice it out of the array and respond 204
// with no body at all.
export function deleteStudent(req, res, next) {}
