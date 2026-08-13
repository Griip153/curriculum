# SOLVED: create/update/delete now include the ownership + admin check from
# Day 18. StudentIn gained an optional course_id (Step: "Your turn" item 2 -
# already wired here). get_student now uses response_model=StudentWithCourseOut
# (Step: "Your turn" item 3) so it shows the nested course.

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import StudentWithCourseOut
from security import get_current_user
from services import students as students_service

router = APIRouter()


class StudentIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    score: int = Field(..., ge=0, le=100)
    course_id: int | None = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value):
        if not value.strip():
            raise ValueError("name must not be blank")
        return value.strip()


@router.get("/")
def list_students(min_score: int | None = None, db: Session = Depends(get_db)):
    return {"students": students_service.get_all(db, min_score)}


@router.get("/{student_id}", response_model=StudentWithCourseOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = students_service.get_by_id(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/", status_code=201)
def create_student(
    student: StudentIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return students_service.create(
        db, student.name, student.score, current_user.id, student.course_id
    )


@router.put("/{student_id}")
def update_student(
    student_id: int,
    student: StudentIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = students_service.get_by_id(db, student_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if existing.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You do not own this student record")
    return students_service.update(db, student_id, student.name, student.score)


@router.delete("/{student_id}", status_code=204)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = students_service.get_by_id(db, student_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if existing.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You do not own this student record")
    students_service.delete(db, student_id)
    return None
