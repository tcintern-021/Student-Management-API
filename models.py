from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from database import Base


class Student(Base):
    """SQLAlchemy model representing a student in the database."""

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    course = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
