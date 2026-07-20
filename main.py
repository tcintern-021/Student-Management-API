from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import List

app = FastAPI(
    title="Student Management API",
    description="A simple FastAPI application for managing student records.",
    version="1.0.0",
)

class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Alex Johnson")
    email: EmailStr = Field(..., example="alex@example.com")
    age: int = Field(..., ge=5, le=100, example=21)
    course: str = Field(..., min_length=2, max_length=100, example="Computer Science")

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int = Field(..., example=1)

students: List[Student] = [
    Student(id=1, name="Ayesha Khan", email="ayesha.khan@example.com", age=20, course="Data Science"),
    Student(id=2, name="Ali Raza", email="ali.raza@example.com", age=22, course="Software Engineering"),
]

@app.get("/students", response_model=List[Student], summary="Get all students")
def get_students():
    """Return a list of all students."""
    return students

@app.get("/students/{student_id}", response_model=Student, summary="Get a student by ID")
def get_student(student_id: int):
    """Return a student record given its ID."""
    for student in students:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED, summary="Create a new student")
def create_student(student_in: StudentCreate):
    """Add a new student to the in-memory store."""
    new_id = max((student.id for student in students), default=0) + 1
    student = Student(id=new_id, **student_in.dict())
    students.append(student)
    return student

@app.put("/students/{student_id}", response_model=Student, summary="Update an existing student")
def update_student(student_id: int, student_in: StudentCreate):
    """Update a student record by ID."""
    for index, student in enumerate(students):
        if student.id == student_id:
            updated_student = Student(id=student_id, **student_in.dict())
            students[index] = updated_student
            return updated_student
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a student")
def delete_student(student_id: int):
    """Remove a student record by ID."""
    for index, student in enumerate(students):
        if student.id == student_id:
            students.pop(index)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
