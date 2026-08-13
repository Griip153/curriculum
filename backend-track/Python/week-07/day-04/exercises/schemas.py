# SOLVED: full response schemas, including the list wrapper from Step 2.

from pydantic import BaseModel

from models import UserRole


class StudentOut(BaseModel):
    id: int
    name: str
    score: int

    class Config:
        from_attributes = True


class CourseOut(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class CourseWithStudentsOut(BaseModel):
    id: int
    title: str
    students: list[StudentOut]

    class Config:
        from_attributes = True


class StudentWithCourseOut(BaseModel):
    id: int
    name: str
    score: int
    course: CourseOut | None

    class Config:
        from_attributes = True


class StudentListOut(BaseModel):
    total: int
    skip: int
    limit: int
    students: list[StudentOut]


class UserOut(BaseModel):
    id: int
    email: str
    role: UserRole

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str
