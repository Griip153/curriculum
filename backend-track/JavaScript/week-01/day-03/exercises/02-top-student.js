// Exercise 2 — Top student
//
// Given the same students array, write a function topStudent(students) that
// returns the student object with the highest score.
//
// Example:
//   topStudent(students)  ->  { name: "Ada", score: 91 }
//
// Hint: no built-in "max of objects" — loop through, or use .reduce(), keeping
// track of whichever student has the highest score seen so far.
// Run: node exercises/02-top-student.js

const students = [
  { name: "Ada", score: 91 },
  { name: "Kofi", score: 68 },
  { name: "Zara", score: 84 },
];

function topStudent(students) {
  // TODO: your code here
}

console.log("Top student:", topStudent(students));
