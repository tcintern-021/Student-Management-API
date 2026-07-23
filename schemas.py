from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for data extracted from JWT token."""

    email: Optional[str] = None


class UserBase(BaseModel):
    """Base schema for User."""

    email: EmailStr = Field(..., json_schema_extra={"example": "admin@example.com"})


class UserCreate(UserBase):
    """Schema for user registration."""

    password: str = Field(..., min_length=6, json_schema_extra={"example": "secret123"})


class UserResponse(UserBase):
    """Schema for returning user data."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StudentBase(BaseModel):
    """Base schema with common attributes."""

    name: str = Field(..., min_length=2, max_length=100, json_schema_extra={"example": "Alex Johnson"})
    email: EmailStr = Field(..., json_schema_extra={"example": "alex@example.com"})
    age: int = Field(..., ge=5, le=100, json_schema_extra={"example": 21})
    course: str = Field(..., min_length=2, max_length=100, json_schema_extra={"example": "Computer Science"})


class StudentCreate(StudentBase):
    """Schema for creating a student, with optional manual ID assignment."""

    id: Optional[int] = Field(None, description="Optional explicit Student ID", json_schema_extra={"example": 1})


class StudentUpdate(StudentBase):
    """Schema for updating a student record."""

    pass


class StudentResponse(StudentBase):
    """Schema for returning student data with id and created_at timestamp."""

    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
