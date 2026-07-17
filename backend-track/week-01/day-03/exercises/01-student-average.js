// Exercise 1 — Student average (SOLVED — worked together in the session, see LESSON.md)
//
// Model a list of students as an array of objects, then compute the average score.
//
// Run: node exercises/01-student-average.js

const students = [
  { name: "Ada", score: 91 },
  { name: "Kofi", score: 68 },
  { name: "Zara", score: 84 },
];

function average(students) {
  const scores = students.map((s) => s.score);
  const total = scores.reduce((sum, score) => sum + score, 0);
  return total / scores.length;
}

console.log("Average score:", average(students));
