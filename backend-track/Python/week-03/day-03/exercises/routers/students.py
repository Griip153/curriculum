# StudentIn now has real constraints (Field) - worked together in the
# session. The @field_validator for "name must not be blank after
# stripping whitespace" is today's "Your turn" - marked with # TODO.

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from database import get_db
from services import students as students_service

router = APIRouter()


class StudentIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    score: int = Field(..., ge=0, le=100)

    # TODO: add a @field_validator("name") @classmethod method that strips
    # whitespace and raises ValueError("name must not be blank") if the
    # stripped result is empty. See LESSON.md Step 3 for the exact pattern.


@router.get("/")
def list_students(min_score: int | None = None, db: Session = Depends(get_db)):
    return {"students": students_service.get_all(db, min_score)}


@router.post("/", status_code=201)
def create_student(student: StudentIn, db: Session = Depends(get_db)):
    return students_service.create(db, student.name, student.score)


@router.get("/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = students_service.get_by_id(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}")
def update_student(student_id: int, student: StudentIn, db: Session = Depends(get_db)):
    updated = students_service.update(db, student_id, student.name, student.score)
    if updated is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated


@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    deleted = students_service.delete(db, student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return None
