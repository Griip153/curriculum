// Exercise 1 — FizzBuzz (SOLVED — worked together in the session, see LESSON.md)
//
// Print the numbers from 1 to 20. But:
// - if divisible by 3, print "Fizz"
// - if divisible by 5, print "Buzz"
// - if divisible by both 3 and 5, print "FizzBuzz"
//
// Run: node exercises/01-fizzbuzz.js

for (let n = 1; n <= 20; n++) {
  if (n % 3 === 0 && n % 5 === 0) {
    console.log("FizzBuzz");
  } else if (n % 3 === 0) {
    console.log("Fizz");
  } else if (n % 5 === 0) {
    console.log("Buzz");
  } else {
    console.log(n);
  }
}
