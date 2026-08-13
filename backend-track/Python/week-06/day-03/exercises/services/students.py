# SOLVED: fully typed, per LESSON.md Step 4.

from sqlalchemy.orm import Session

from models import Student


def get_all(
    db: Session,
    min_score: int | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 20,
    sort_by: str = "id",
    order: str = "asc",
) -> tuple[list[Student], int]:
    allowed_sort_fields = {"name": Student.name, "score": Student.score, "id": Student.id}
    query = db.query(Student)

    if search:
        query = query.filter(Student.name.ilike(f"%{search}%"))
    if min_score is not None:
        query = query.filter(Student.score >= min_score)

    total = query.count()

    column = allowed_sort_fields.get(sort_by, Student.id)
    query = query.order_by(column.desc() if order == "desc" else column.asc())

    students = query.offset(skip).limit(limit).all()
    return students, total


def get_by_id(db: Session, student_id: int) -> Student | None:
    return db.get(Student, student_id)


def create(
    db: Session,
    name: str,
    score: int,
    created_by: int,
    course_id: int | None = None,
) -> Student:
    new_student = Student(name=name, score=score, created_by=created_by, course_id=course_id)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


def update(db: Session, student_id: int, name: str, score: int) -> Student | None:
    student = get_by_id(db, student_id)
    if student is None:
        return None
    student.name = name
    student.score = score
    db.commit()
    db.refresh(student)
    return student


def delete(db: Session, student_id: int) -> bool:
    student = get_by_id(db, student_id)
    if student is None:
        return False
    db.delete(student)
    db.commit()
    return True
