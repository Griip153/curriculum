# Exercise 3 - Above-average students
#
# Write a function above_average(students) that returns a list of the names
# of every student who scored above the average of the whole group.
#
# Example (using the same `students` list):
#   above_average(students)  ->  ["Ada", "Zara"]
#
# Hint: reuse the average() function from 01_student_average.py (you can just
# copy its definition in here), then filter with a list comprehension.
# Run: python3 exercises/03_above_average_students.py

students = [
    {"name": "Ada", "score": 91},
    {"name": "Kofi", "score": 68},
    {"name": "Zara", "score": 84},
]

def average(students):
    scores = [s["score"] for s in students]
    return sum(scores) / len(scores)

def above_average(students):
    # TODO: your code here
    pass

print(above_average(students))
