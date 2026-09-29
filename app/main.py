from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import Base, engine
from app.models import Student
from app.api.students import router as students_router
from app.api.chat import router as chat_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.app_name, version="1.0.0", description="Modular Student Database API with Gemini + LangGraph chatbot and Chroma vector retrieval.")
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins.split(","), allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(students_router)
app.include_router(chat_router)

@app.get("/", tags=["Health"])
def root(): return {"message": "Student Database Backend is running", "docs": "/docs", "redoc": "/redoc"}

@app.get("/health", tags=["Health"])
def health(): return {"status": "ok"}
