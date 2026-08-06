# Exercise 1 - FizzBuzz (SOLVED - worked together in the session, see LESSON.md)
#
# Print the numbers from 1 to 20. But:
# - if divisible by 3, print "Fizz"
# - if divisible by 5, print "Buzz"
# - if divisible by both 3 and 5, print "FizzBuzz"
#
# Run: python3 exercises/01_fizzbuzz.py

for n in range(1, 21):
    if n % 3 == 0 and n % 5 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)
