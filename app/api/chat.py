from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.chatbot.graph import build_graph

router = APIRouter(prefix="/api/chat", tags=["AI Chatbot"])

@router.post("", response_model=ChatResponse)
def chat(data: ChatRequest, db: Session = Depends(get_db)):
    graph = build_graph(db)
    result = graph.invoke({"question": data.question})
    return ChatResponse(answer=result["answer"])
