# Student Database Application System – Backend

Final-year internship project based on the EWB Trainer Instructions.

## Features
- Python + FastAPI modular backend
- Student CRUD APIs with validation and clear HTTP errors
- SQL database using SQLite + SQLAlchemy
- Automatic Swagger/OpenAPI documentation at `/docs`
- Gemini API integration for natural-language chatbot responses
- LangGraph workflow: question → retrieval → Gemini response
- Chroma local vector database for semantic retrieval of student records
- Docker / Docker Compose deployment
- Pytest API tests

## Architecture
```text
Client / Swagger
      |
   FastAPI
   /      \
Students   Chat
   |         |
SQLite   LangGraph
            |
         Chroma DB
            |
          Gemini
```

## Why Chroma?
Chroma is selected for this student project because it can run locally, integrates directly with Python, supports similarity search, and keeps setup simple for an internship-scale retrieval-augmented chatbot. The SQL database remains the source of structured student records; Chroma is used for semantic retrieval rather than replacing SQL CRUD.

## Setup
1. Install Python 3.12+.
2. Create a virtual environment: `python -m venv .venv`
3. Activate it.
4. Install: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env`.
6. Put your Gemini API key in `.env`.
7. Start: `uvicorn app.main:app --reload`
8. Open Swagger: `http://127.0.0.1:8000/docs`

## API Endpoints
- `GET /health` – health check
- `POST /api/students` – create student
- `GET /api/students` – list/filter students
- `GET /api/students/{id}` – read one student
- `PUT /api/students/{id}` – update student
- `DELETE /api/students/{id}` – delete student
- `POST /api/chat` – ask the AI student-database chatbot

### Example student
```json
{
  "name": "Rahul Kumar",
  "email": "rahul@example.com",
  "age": 21,
  "course": "BCA",
  "semester": 5,
  "department": "Computer Applications"
}
```

### Example chatbot request
```json
{"question":"Which students are in BCA?"}
```

## Docker
Create `.env`, then run:
```bash
docker compose up --build
```

## Tests
```bash
pytest -q
```

## Security
- `.env` is ignored by Git.
- API keys must never be committed.
- The chatbot is instructed to answer only from retrieved context and avoid secrets.
- Add authentication/authorization before using real sensitive student data in production.

## Internship submission checklist
- [x] Modular backend structure
- [x] Student database models/schema
- [x] CRUD API endpoints
- [x] Request validation and errors
- [x] Swagger/OpenAPI
- [x] Gemini integration
- [x] LangGraph workflow
- [x] Vector database selection and justification
- [x] Docker deployment
- [x] Tests
- [x] README and setup instructions
- [ ] Push repository to GitHub
- [ ] Submit GitHub URL in the management Google Form
