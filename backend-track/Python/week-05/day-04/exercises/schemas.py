# Pydantic response ("out") shapes. See LESSON.md Step 5.
# Note: CourseOut is defined WITHOUT students to avoid infinite nesting
# (Course -> students -> course -> students -> ...). Only
# CourseWithStudentsOut includes the nested list, for the one route that
# needs it.

from pydantic import BaseModel


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
