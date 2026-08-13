# SOLVED: list, get, and create are worked together in the session - create
# now requires a valid token (Depends(get_current_user)) and sets created_by
# from it. update_student and delete_student are today's "Your turn"
# assignment - marked with # TODO, and need an ownership + admin-override
# check (see LESSON.md Step 5-6).

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from database import get_db
from models import User
from security import get_current_user
from services import students as students_service

router = APIRouter()


class StudentIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    score: int = Field(..., ge=0, le=100)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value):
        if not value.strip():
            raise ValueError("name must not be blank")
        return value.strip()


@router.get("/")
def list_students(min_score: int | None = None, db: Session = Depends(get_db)):
    return {"students": students_service.get_all(db, min_score)}


@router.get("/{student_id}")
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
    return students_service.create(db, student.name, student.score, current_user.id)


@router.put("/{student_id}")
def update_student(
    student_id: int,
    student: StudentIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # TODO:
    # 1. existing = students_service.get_by_id(db, student_id)
    # 2. if existing is None: raise HTTPException(404, detail="Student not found")
    # 3. if existing.created_by != current_user.id and current_user.role != "admin":
    #        raise HTTPException(403, detail="You do not own this student record")
    # 4. return students_service.update(db, student_id, student.name, student.score)
    pass


@router.delete("/{student_id}", status_code=204)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # TODO: same existence + ownership/admin check as update_student above,
    # then students_service.delete(db, student_id) and return None.
    pass
