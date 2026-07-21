from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, status

from models import Student, StudentCreate, students

app = FastAPI(
    title="Student Management API",
    description="A simple FastAPI application for managing student records.",
    version="1.0.0",
)


@app.get("/students", response_model=List[Student], summary="Get all students")
def get_students():
    """Return a list of all students."""
    return students


@app.get("/students/search", response_model=List[Student], summary="Search students")
def search_students(name: Optional[str] = Query(None, min_length=1)):
    """Search students by partial name match."""
    if not name:
        return students
    return [student for student in students if name.lower() in student.name.lower()]


@app.get("/students/{student_id}", response_model=Student, summary="Get a student by ID")
def get_student(student_id: int):
    """Return a student record given its ID."""
    for student in students:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")


@app.post(
    "/students",
    response_model=Student,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new student",
)
def create_student(student_in: StudentCreate):
    """Add a new student to the in-memory store."""
    new_id = max((student.id for student in students), default=0) + 1
    student = Student(id=new_id, **student_in.model_dump())
    students.append(student)
    return student


@app.put("/students/{student_id}", response_model=Student, summary="Update an existing student")
def update_student(student_id: int, student_in: StudentCreate):
    """Update a student record by ID."""
    for index, student in enumerate(students):
        if student.id == student_id:
            updated_student = Student(id=student_id, **student_in.model_dump())
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
