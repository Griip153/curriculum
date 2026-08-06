# Exercise 1 - Student average (SOLVED - worked together in the session, see LESSON.md)
#
# Model a list of students as a list of dictionaries, then write average(students)
# which returns the mean of all their scores.
#
# Run: python3 exercises/01_student_average.py

students = [
    {"name": "Ada", "score": 91},
    {"name": "Kofi", "score": 68},
    {"name": "Zara", "score": 84},
]

def average(students):
    scores = [s["score"] for s in students]
    return sum(scores) / len(scores)

print(average(students))
