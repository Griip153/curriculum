# Thin router - reads the request, calls the service layer, shapes the
# response. No business logic lives here.

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services import students as students_service

router = APIRouter()


class StudentIn(BaseModel):
    name: str
    score: int


@router.get("/")
def list_students(min_score: int | None = None):
    return {"students": students_service.get_all(min_score)}


@router.get("/{student_id}")
def get_student(student_id: int):
    student = students_service.get_by_id(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/", status_code=201)
def create_student(student: StudentIn):
    # A bad name raises a plain ValueError - caught by main.py's global
    # exception handler, not a try/except here.
    return students_service.create(student.name, student.score)


@router.put("/{student_id}")
def update_student(student_id: int, student: StudentIn):
    updated = students_service.update(student_id, student.name, student.score)
    if updated is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated


@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int):
    deleted = students_service.delete(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return None
