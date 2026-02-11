from app.config import VERSION
from fastapi import FastAPI
from app.routes import health, todos


app = FastAPI(
    title="Todo API",
    version=VERSION,
    description="Simple todo list API with multi-env deployment"
)
#This app object is the central ASGI application; routers, middleware, exception handlers, and startup/shutdown events are attached to it.
# ASGI stands for Asynchronous Server Gateway Interface. An ASGI server is an application server that implements the ASGI protocol and 
# runs an ASGI-compatible application (like a FastAPI app). Uvicorn is a popular, high-performance ASGI server implementation.
# What the server actually does
    # - Imports your app object (for example app in app.main:app).
    # - Listens on a network socket for incoming connections (HTTP, WebSocket).
    # - Parses incoming requests and turns them into ASGI events/messages.
    # - Calls your application (the app object) following the ASGI interface (an async callable that receives scope/send/receive).
    # - Serializes the response back and writes it to the client.
    # - Manages concurrency and the event loop for async code.
app.include_router(health.router)
app.include_router(todos.router, prefix="/api")



### BELOW IS FOR TESTING ONLY
if __name__ == "__main__":
    from app.models import TodoCreate
    # Demo/test code: runs only when executing this file as a script
    todo_jenn = TodoCreate(title="Buy milk", description="2L", completed=False)
    print("todo_jenn is ", todo_jenn)
    # Pydantic v2 uses model_dump(); if you're on v1 use .dict()
    # print("todo_jenn.model_dump() is ", getattr(todo_jenn, "model_dump", todo_jenn.dict)())
    print("todo_jenn.model_dump() is ", todo_jenn.model_dump())
    # print("**todo_jenn.model_dump() is ", **todo_jenn.model_dump())
    # Call the create_todo function from the todos router module for a quick demo
    todo_jenn_final = todos.create_todo(todo_jenn)
    print("todo_jenn_final is", todo_jenn_final)