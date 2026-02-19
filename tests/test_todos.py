from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_todos_empty():
    response = client.get("/api/todos")
    assert response.status_code == 200
    assert response.json() == []

def test_create_todo():
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "completed": False
    }
    response = client.post("/api/todos", json=todo_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert "id" in data

def test_get_todo():
    # Create a todo first
    create_response = client.post("/api/todos", json={
        "title": "Get Test",
        "completed": False
    })
    todo_id = create_response.json()["id"]
    
    # Get the todo
    response = client.get(f"/api/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Get Test"

def test_get_nonexistent_todo():
    response = client.get("/api/todos/9999")
    assert response.status_code == 404