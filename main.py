from fastapi import FastAPI

import models
from database import engine
from student import router as student_router

# Create database tables automatically on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management API",
    description="A FastAPI application for managing student records with SQLite database persistence.",
    version="2.0.0",
)

app.include_router(student_router)


@app.get("/", summary="Root endpoint")
def root():
    """Welcome root endpoint."""
    return {
        "message": "Welcome to the Student Management API",
        "docs_url": "/docs",
    }
