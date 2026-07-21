from typing import List

from pydantic import BaseModel, EmailStr, Field


class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, json_schema_extra={"example": "Alex Johnson"})
    email: EmailStr = Field(..., json_schema_extra={"example": "alex@example.com"})
    age: int = Field(..., ge=5, le=100, json_schema_extra={"example": 21})
    course: str = Field(..., min_length=2, max_length=100, json_schema_extra={"example": "Computer Science"})


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int = Field(..., json_schema_extra={"example": 1})


students: List[Student] = [
    Student(
        id=1,
        name="Ayesha Khan",
        email="ayesha.khan@example.com",
        age=20,
        course="Data Science",
    ),
    Student(
        id=2,
        name="Ali Raza",
        email="ali.raza@example.com",
        age=22,
        course="Software Engineering",
    ),
]
