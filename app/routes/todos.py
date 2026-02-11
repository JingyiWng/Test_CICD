from fastapi import APIRouter, HTTPException
from app.models import Todo, TodoCreate
from app.database import todos_db
from uuid import uuid4

router = APIRouter()

@router.get("/todos")
def list_todos():
    return list(todos_db.values())

@router.post("/todos")
def create_todo(todo: TodoCreate):
    new_todo = Todo(id=uuid4().int, **todo.model_dump())
    todos_db[new_todo.id] = new_todo
    return new_todo

@router.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos_db[todo_id]

@router.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoCreate):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    updated = Todo(id=todo_id, **todo.model_dump())
    todos_db[todo_id] = updated
    return updated

@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos_db[todo_id]
    return {"message": "Todo deleted"}




####### THIS IS FOR TESTING ONLY
def create_todo_jenn(todo: TodoCreate):
    new_todo = Todo(id=uuid4().int, **todo.model_dump())
    todos_db[new_todo.id] = new_todo
    return new_todo
