from pathlib import Path
from app.core.config import settings

class StudentVectorStore:
    """Chroma-backed semantic retrieval for student records.

    Chroma is used as a local vector database. It is useful when the chatbot
    needs semantic retrieval rather than simple SQL filtering.
    """
    def __init__(self):
        self._collection = None
        try:
            import chromadb
            Path(settings.chroma_path).mkdir(parents=True, exist_ok=True)
            client = chromadb.PersistentClient(path=settings.chroma_path)
            self._collection = client.get_or_create_collection("students")
        except Exception:
            self._collection = None

    def upsert_students(self, students):
        if not self._collection: return
        ids, docs, metas = [], [], []
        for s in students:
            ids.append(str(s.id))
            docs.append(f"{s.name}, {s.email}, {s.course}, semester {s.semester}, {s.department}, age {s.age}")
            metas.append({"student_id": s.id, "department": s.department, "course": s.course})
        if ids: self._collection.upsert(ids=ids, documents=docs, metadatas=metas)

    def search(self, query: str, n_results: int = 5):
        if not self._collection or self._collection.count() == 0: return []
        result = self._collection.query(query_texts=[query], n_results=n_results)
        return result.get("documents", [[]])[0]
