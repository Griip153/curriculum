# Plain Python - the actual business logic, with no FastAPI imports at all.
# This is what makes it independently testable (see Week 3, Day 4).

students_db = [
    {"id": 1, "name": "Ada", "score": 91},
    {"id": 2, "name": "Kofi", "score": 68},
    {"id": 3, "name": "Zara", "score": 84},
]
next_id = 4


def get_all(min_score=None):
    if min_score is None:
        return students_db
    return [s for s in students_db if s["score"] >= min_score]


def get_by_id(student_id):
    return next((s for s in students_db if s["id"] == student_id), None)


def create(name, score):
    global next_id
    if not name or not name.strip():
        raise ValueError("name must not be empty")
    new_student = {"id": next_id, "name": name, "score": score}
    students_db.append(new_student)
    next_id += 1
    return new_student


def update(student_id, name, score):
    student = get_by_id(student_id)
    if student is None:
        return None
    student["name"] = name
    student["score"] = score
    return student


def delete(student_id):
    for index, s in enumerate(students_db):
        if s["id"] == student_id:
            students_db.pop(index)
            return True
    return False
