# Students router - SOLVED: list (Step 1 TODO below) and create are worked
# together in the session. Steps 2-4 (get one, update, delete) are the
# assignment - marked with # TODO.

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class StudentIn(BaseModel):
    name: str
    score: int


students_db = [
    {"id": 1, "name": "Ada", "score": 91},
    {"id": 2, "name": "Kofi", "score": 68},
    {"id": 3, "name": "Zara", "score": 84},
]
next_id = 4


@router.get("/")
def list_students(min_score: int | None = None):
    # TODO (Step 1): if min_score is given, only return students with
    # score >= min_score. Right now it always returns everyone.
    return {"students": students_db}


@router.post("/", status_code=201)
def create_student(student: StudentIn):
    global next_id
    new_student = {"id": next_id, "name": student.name, "score": student.score}
    students_db.append(new_student)
    next_id += 1
    return new_student


# TODO (Step 2): GET /{student_id} - find the student with this id in
# students_db. Found -> return it. Not found -> raise HTTPException(404,
# detail="Student not found").


# TODO (Step 3): PUT /{student_id} - same lookup as Step 2, but on success
# overwrite the matching dict's "name" and "score" from the request body
# (a StudentIn, just like create_student) and return the updated student.


# TODO (Step 4): DELETE /{student_id}, status_code=204 - find the student's
# position in students_db (e.g. with enumerate()), remove it with
# students_db.pop(index), and return None. Not found -> 404, same as above.
