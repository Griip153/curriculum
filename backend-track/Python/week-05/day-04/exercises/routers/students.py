# SOLVED: list_students is the full worked example from LESSON.md, combining
# pagination, sorting, search, and min_score in one route. The rest of the
# CRUD carries forward unchanged from Day 19.

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from database import get_db
from models import Student, User
from schemas import StudentWithCourseOut
from security import get_current_user
from services import students as students_service

router = APIRouter()

ALLOWED_SORT_FIELDS = {"name": Student.name, "score": Student.score, "id": Student.id}


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
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = "id",
    order: str = "asc",
    search: str | None = None,
    min_score: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Student)

    if search:
        query = query.filter(Student.name.ilike(f"%{search}%"))
    if min_score is not None:
        query = query.filter(Student.score >= min_score)

    total = query.count()

    column = ALLOWED_SORT_FIELDS.get(sort_by, Student.id)
    query = query.order_by(column.desc() if order == "desc" else column.asc())

    students = query.offset(skip).limit(limit).all()

    return {"total": total, "skip": skip, "limit": limit, "students": students}


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
