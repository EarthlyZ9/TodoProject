from fastapi import FastAPI

from routers import auth, todos, users, address
from todo_proj import models
from todo_proj.database import engine, SessionLocal

description = """
    TODO Project API 🚀
    
    ## Todos
    
    You can **CRUD Todos**.
    
    ## Users
    
    This includes:
    
    * **Authentication** (_not implemented_).
    * **Authorization** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "Todos",
        "description": "Operations with todo items",
    },
    {
        "name": "Auth",
        "description": "Authentication and authorization",
    },
    {
        "name": "Users",
        "description": "User management",
    },
    {
        "name": "Address",
        "description": "Address information for users",
    },
]

app = FastAPI(
    title="Todo Project API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Earthly Jisoo",
        "url": "https://github.com/linda2927",
        "email": "linda2927@naver.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
)

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(address.router)
