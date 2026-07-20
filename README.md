# Student Management API

A simple FastAPI application for managing student records.

## Endpoints

- `GET /students` - Return all students
- `GET /students/{id}` - Return a student by ID
- `POST /students` - Add a new student
- `PUT /students/{id}` - Update an existing student
- `DELETE /students/{id}` - Delete a student

## Run locally

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the environment:

```bash
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the app:

```bash
uvicorn main:app --reload
```

5. Open the API docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Notes

- Data is stored in-memory for demonstration purposes.
- Input validation is handled with Pydantic models.
- Proper HTTP status codes are returned for create, update, delete, and not found conditions.
