// Students controller — unchanged from your completed Day 10 assignment.
// Validation now happens before any of these functions run (see routes/students.js
// and validators/students.js) — nothing in here needs to change today.

import Student from "../models/Student.js";

export async function listStudents(req, res, next) {
  try {
    const students = await Student.find();
    res.json({ students });
  } catch (error) {
    next(error);
  }
}

export async function getStudent(req, res, next) {
  try {
    const student = await Student.findById(req.params.id);
    if (!student) {
      const err = new Error("Student not found");
      err.statusCode = 404;
      return next(err);
    }
    res.json(student);
  } catch (error) {
    next(error);
  }
}

export async function createStudent(req, res, next) {
  try {
    const newStudent = await Student.create(req.body);
    res.status(201).json(newStudent);
  } catch (error) {
    next(error);
  }
}

export async function updateStudent(req, res, next) {
  try {
    const updatedStudent = await Student.findByIdAndUpdate(req.params.id, req.body, {
      new: true,
      runValidators: true,
    });
    if (!updatedStudent) {
      const err = new Error("Student not found");
      err.statusCode = 404;
      return next(err);
    }
    res.json(updatedStudent);
  } catch (error) {
    next(error);
  }
}

export async function deleteStudent(req, res, next) {
  try {
    const deletedStudent = await Student.findByIdAndDelete(req.params.id);
    if (!deletedStudent) {
      const err = new Error("Student not found");
      err.statusCode = 404;
      return next(err);
    }
    res.status(204).end();
  } catch (error) {
    next(error);
  }
}
