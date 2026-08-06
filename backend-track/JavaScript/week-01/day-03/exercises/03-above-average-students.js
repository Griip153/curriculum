// Exercise 3 — Above-average students
//
// Given the same students array, write a function aboveAverage(students) that
// returns a new array containing only the students whose score is above the
// average score of the whole group.
//
// Example:
//   aboveAverage(students)  ->  [{ name: "Ada", score: 91 }, { name: "Zara", score: 84 }]
//
// Hint: you already have an average() function from exercise 1 — reuse it here
// instead of recomputing the average by hand, then use .filter().
// Run: node exercises/03-above-average-students.js

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

function aboveAverage(students) {
  // TODO: your code here
}

console.log("Above average:", aboveAverage(students));
