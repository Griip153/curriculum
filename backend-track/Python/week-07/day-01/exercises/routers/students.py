# SOLVED: upload_photo is the full worked example from LESSON.md Steps 1-3.
# The rest of the CRUD carries forward unchanged from Day 23.

import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from database import get_db
from models import User, UserRole
from schemas import StudentListOut, StudentOut, StudentWithCourseOut
from security import get_current_user
from services import students as students_service

router = APIRouter()

UPLOAD_DIR = "uploads"
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB


class StudentIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    score: int = Field(..., ge=0, le=100)
    course_id: int | None = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name must not be blank")
        return value.strip()


@router.get("/", response_model=StudentListOut)
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = "id",
    order: str = "asc",
    search: str | None = None,
    min_score: int | None = None,
    db: Session = Depends(get_db),
):
    students, total = students_service.get_all(
        db, min_score, search, skip, limit, sort_by, order
    )
    return {"total": total, "skip": skip, "limit": limit, "students": students}


@router.get("/{student_id}", response_model=StudentWithCourseOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = students_service.get_by_id(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/", status_code=201, response_model=StudentOut)
def create_student(
    student: StudentIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return students_service.create(
        db, student.name, student.score, current_user.id, student.course_id
    )


@router.put("/{student_id}", response_model=StudentOut)
def update_student(
    student_id: int,
    student: StudentIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = students_service.get_by_id(db, student_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if existing.created_by != current_user.id and current_user.role != UserRole.ADMIN:
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
    if existing.created_by != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="You do not own this student record")
    students_service.delete(db, student_id)
    return None


@router.post("/{student_id}/photo", response_model=StudentOut)
async def upload_photo(
    student_id: int,
    db: Session = Depends(get_db),
    photo: UploadFile = File(...),
):
    student = students_service.get_by_id(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    if photo.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG or PNG images are allowed")

    contents = await photo.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 2 MB)")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    extension = (photo.filename or "upload").split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as f:
        f.write(contents)

    student.photo_path = file_path
    db.commit()
    db.refresh(student)
    return student
