from sqlalchemy.orm import Session

from models import Student


def get_all(db: Session, min_score: int | None = None):
    query = db.query(Student)
    if min_score is not None:
        query = query.filter(Student.score >= min_score)
    return query.all()


def get_by_id(db: Session, student_id: int):
    return db.get(Student, student_id)


def create(db: Session, name: str, score: int, created_by: int, course_id: int | None = None):
    new_student = Student(name=name, score=score, created_by=created_by, course_id=course_id)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


def update(db: Session, student_id: int, name: str, score: int):
    student = get_by_id(db, student_id)
    if student is None:
        return None
    student.name = name
    student.score = score
    db.commit()
    db.refresh(student)
    return student


def delete(db: Session, student_id: int):
    student = get_by_id(db, student_id)
    if student is None:
        return False
    db.delete(student)
    db.commit()
    return True
