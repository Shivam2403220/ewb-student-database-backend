from typing import TypedDict
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.student import Student
from app.vector.store import StudentVectorStore

class ChatState(TypedDict, total=False):
    question: str
    context: str
    answer: str


def retrieve(state: ChatState, db: Session, vector_store: StudentVectorStore):
    question = state["question"]
    rows = list(db.scalars(select(Student).limit(100)).all())
    vector_store.upsert_students(rows)
    docs = vector_store.search(question, 5)
    if docs:
        context = "\n".join(docs)
    else:
        context = "\n".join(f"ID {s.id}: {s.name}, {s.email}, {s.course}, semester {s.semester}, {s.department}, age {s.age}" for s in rows)
    return {"context": context[:12000]}


def generate(state: ChatState):
    if not settings.gemini_api_key:
        return {"answer": "Gemini API key is not configured. I retrieved the relevant student context, but cannot generate the AI response yet. Add GEMINI_API_KEY to .env."}
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage
    llm = ChatGoogleGenerativeAI(model=settings.gemini_model, google_api_key=settings.gemini_api_key, temperature=0)
    prompt = f"""You are a student database assistant. Answer only from the supplied context. Do not invent student information. If the context is insufficient, say so. Avoid revealing secrets.\n\nContext:\n{state['context']}\n\nQuestion: {state['question']}"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"answer": response.content}


def build_graph(db: Session):
    from langgraph.graph import StateGraph, START, END
    vector_store = StudentVectorStore()
    graph = StateGraph(ChatState)
    graph.add_node("retrieve", lambda state: retrieve(state, db, vector_store))
    graph.add_node("generate", generate)
    graph.add_edge(START, "retrieve"); graph.add_edge("retrieve", "generate"); graph.add_edge("generate", END)
    return graph.compile()
