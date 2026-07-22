# Student Management API (FastAPI + SQLite + SQLAlchemy)

A complete CRUD RESTful API for managing student records with SQLite persistent database storage, SQLAlchemy ORM, dynamic validation, and timestamps.

## Project Structure

```
Student-Management-API/
├── database.py    # Database connection setup, session factory, Base & get_db dependency
├── models.py      # SQLAlchemy ORM models (Student DB model)
├── schemas.py     # Pydantic schemas for request validation & DTO serialization
├── student.py     # FastAPI APIRouter containing all /students CRUD endpoints
├── main.py        # Application entry point & router registration
├── requirements.txt # Project dependencies
└── README.md      # Project documentation
```

## Endpoints

- `GET /` - Root welcome endpoint
- `GET /students` - View all students (Supports name filter: `/students?name=Ayesha`)
- `GET /students/search?name=Ayesha` - Search students by name
- `GET /students/{id}` - View a single student by ID
- `POST /students` - Create a new student (validates duplicate ID & duplicate email)
- `PUT /students/{id}` - Update an existing student by ID
- `DELETE /students/{id}` - Delete a student by ID

## Features & Bonus Implementations

- **SQLite Persistence**: Data is stored persistently in `students.db`.
- **SQLAlchemy ORM**: Clean model definitions and session handling via FastAPI dependencies.
- **Duplicate Validation**: Rejects duplicate student IDs (if manually provided) and duplicate email addresses with HTTP `400 Bad Request`.
- **Timestamps**: Every student record automatically tracks `created_at` timestamp.
- **Modular Design**: Code is cleanly separated into database, models, schemas, and router modules.

## Setup & Running Locally

1. **Activate virtual environment**:
   ```bash
   .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the API server**:
   ```bash
   uvicorn main:app --reload
   ```

4. **Interactive Documentation**:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`
