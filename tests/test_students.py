from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get("/health").json()["status"] == "ok"

def test_create_and_read_student():
    email = "test.student@example.com"
    response = client.post("/api/students", json={"name":"Test Student","email":email,"age":21,"course":"BCA","semester":5,"department":"Computer Applications"})
    assert response.status_code == 201
    student_id = response.json()["id"]
    read = client.get(f"/api/students/{student_id}")
    assert read.status_code == 200
    assert read.json()["email"] == email
    client.delete(f"/api/students/{student_id}")
