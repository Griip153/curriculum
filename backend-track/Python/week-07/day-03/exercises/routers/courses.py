# SOLVED: course_stats is the full worked example from LESSON.md.
# "Your turn" item 3 (the ?min_students= HAVING variant) is marked # TODO.

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
from models import Course, Student
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
    new_course = Course(title=course.title)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@router.get("/stats")
def course_stats(min_students: int | None = None, db: Session = Depends(get_db)):
    query = (
        db.query(
            Course.id,
            Course.title,
            func.count(Student.id).label("student_count"),
            func.avg(Student.score).label("average_score"),
        )
        .join(Student, Student.course_id == Course.id, isouter=True)
        .group_by(Course.id)
    )

    # TODO: if min_students is not None, add
    # .having(func.count(Student.id) >= min_students) to the query above
    # before .all() is called.

    results = query.all()
    return [
        {
            "id": r.id,
            "title": r.title,
            "student_count": r.student_count,
            "average_score": round(r.average_score, 1) if r.average_score is not None else None,
        }
        for r in results
    ]
