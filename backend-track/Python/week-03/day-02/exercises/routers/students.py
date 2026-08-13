# SOLVED: list and create already pass db: Session = Depends(get_db) through
# to the service layer. get_student, update_student, and delete_student are
# the "Your turn" assignment - marked with # TODO.

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from services import students as students_service

router = APIRouter()


class StudentIn(BaseModel):
    name: str
    score: int


@router.get("/")
def list_students(min_score: int | None = None, db: Session = Depends(get_db)):
    return {"students": students_service.get_all(db, min_score)}


@router.post("/", status_code=201)
def create_student(student: StudentIn, db: Session = Depends(get_db)):
    return students_service.create(db, student.name, student.score)


@router.get("/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    # TODO: call students_service.get_by_id(db, student_id).
    # If None, raise HTTPException(404, detail="Student not found").
    pass


@router.put("/{student_id}")
def update_student(student_id: int, student: StudentIn, db: Session = Depends(get_db)):
    # TODO: call students_service.update(...). If None, 404. Else return it.
    pass


@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    # TODO: call students_service.delete(...). If False, 404. Else return None.
    pass
