from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import Student, User
from schemas import StudentCreate, StudentResponse, StudentUpdate

router = APIRouter(prefix="/students", tags=["students"])


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new student",
)
def create_student(
    student_in: StudentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new student record in SQLite database. Validates duplicate ID and duplicate email."""
    # Check duplicate ID if manually provided
    if student_in.id is not None:
        existing_id = db.query(Student).filter(Student.id == student_in.id).first()
        if existing_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student with ID {student_in.id} already exists.",
            )

    # Check duplicate email
    existing_email = db.query(Student).filter(Student.email == student_in.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student with email '{student_in.email}' already exists.",
        )

    student_data = student_in.model_dump(exclude_unset=True)
    db_student = Student(**student_data, user_id=current_user.id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.get("", response_model=List[StudentResponse], summary="Get all students")
def get_students(
    name: Optional[str] = Query(None, min_length=1, description="Filter by partial name match"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all students, with optional partial name filter."""
    query = db.query(Student)
    if name:
        query = query.filter(Student.name.ilike(f"%{name}%"))
    return query.all()


@router.get("/search", response_model=List[StudentResponse], summary="Search students by name")
def search_students(
    name: Optional[str] = Query(None, min_length=1, description="Search query string"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search students by partial name match."""
    query = db.query(Student)
    if name:
        query = query.filter(Student.name.ilike(f"%{name}%"))
    return query.all()


@router.get("/{student_id}", response_model=StudentResponse, summary="Get a student by ID")
def get_student(
    student_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Return a student record given its ID."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found.",
        )
    return student


@router.put("/{student_id}", response_model=StudentResponse, summary="Update an existing student")
def update_student(
    student_id: int, 
    student_in: StudentUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a student record by ID."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found.",
        )

    # Check if user owns the student
    if student.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this student",
        )

    # Check email uniqueness against other students
    existing_email = (
        db.query(Student)
        .filter(Student.email == student_in.email, Student.id != student_id)
        .first()
    )
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student with email '{student_in.email}' already exists.",
        )

    student.name = student_in.name
    student.email = student_in.email
    student.age = student_in.age
    student.course = student_in.course

    db.commit()
    db.refresh(student)
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a student")
def delete_student(
    student_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a student record by ID."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found.",
        )

    # Check if user owns the student
    if student.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this student",
        )

    db.delete(student)
    db.commit()
    return
