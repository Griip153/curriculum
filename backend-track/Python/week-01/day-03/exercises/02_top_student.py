# Exercise 2 - Top student
#
# Write a function top_student(students) that returns the dictionary of the
# student with the highest score.
#
# Example (using the same `students` list as 01_student_average.py):
#   top_student(students)  ->  {"name": "Ada", "score": 91}
#
# Hint: you can loop and track the best one seen so far, or use the built-in
# max() function with a key= argument (same idea as sorted(..., key=...) from
# LESSON.md). Try the loop version first.
# Run: python3 exercises/02_top_student.py

students = [
    {"name": "Ada", "score": 91},
    {"name": "Kofi", "score": 68},
    {"name": "Zara", "score": 84},
]

def top_student(students):
    # TODO: your code here
    pass

print(top_student(students))
