# SOLVED: get_course_with_students is worked together in the session.
# create_course is today's "Your turn" item 1 - marked with # TODO.

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import get_db
from models import Course
from schemas import CourseWithStudentsOut

router = APIRouter()


class CourseIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)


@router.get("/{course_id}/students", response_model=CourseWithStudentsOut)
def get_course_with_students(course_id: int, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/", status_code=201)
def create_course(course: CourseIn, db: Session = Depends(get_db)):
    # TODO: build a Course(title=course.title), db.add/commit/refresh it,
    # then return it (same pattern as create_student in services/students.py).
    pass
