# SOLVED: get_all and create use SQLAlchemy already (worked together in the
# session). get_by_id, update, and delete are the "Your turn" assignment -
# marked with # TODO.

from sqlalchemy.orm import Session

from models import Student


def get_all(db: Session, min_score: int | None = None):
    query = db.query(Student)
    if min_score is not None:
        query = query.filter(Student.score >= min_score)
    return query.all()


def create(db: Session, name: str, score: int):
    if not name or not name.strip():
        raise ValueError("name must not be empty")
    new_student = Student(name=name, score=score)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


def get_by_id(db: Session, student_id: int):
    # TODO: return db.get(Student, student_id)
    pass


def update(db: Session, student_id: int, name: str, score: int):
    # TODO: look the student up with get_by_id(db, student_id).
    # If None, return None. Otherwise set .name and .score, db.commit(),
    # db.refresh(student), and return it.
    pass


def delete(db: Session, student_id: int):
    # TODO: look the student up with get_by_id(db, student_id).
    # If None, return False. Otherwise db.delete(student), db.commit(),
    # and return True.
    pass
