from typing import Optional, Union

from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from sql_app import models
from sql_app.database import engine, SessionLocal

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
        "description": "Operations with todo items.",
    },
    {
        "name": "Users",
        "description": "Manage users.",
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


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Todo(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str]
    priority: int = Field(
        gt=0, lt=6, description="The priority must be between 1 and 5."
    )
    complete: bool = Field(default=False)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "1",
                "title": "Study FastAPI",
                "description": "Go to Udemy courses",
                "priority": 3,
                "complete": False,
            }
        }


def raise_404_error(detail="Todo not found."):
    return HTTPException(status_code=404, detail=detail)


@app.get("/todos", status_code=status.HTTP_200_OK, tags=["Todos"])
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()


@app.post(
    "/todos/", status_code=status.HTTP_201_CREATED, tags=["Todos"], response_model=Todo
)
def create_todo(todo: Todo, db: Session = Depends(get_db)):
    new_todo = models.Todo()
    new_todo.title = todo.title
    new_todo.description = todo.description
    new_todo.priority = todo.priority
    new_todo.complete = todo.complete

    db.add(new_todo)
    db.commit()

    return new_todo


@app.get(
    "/todos/{todo_id}",
    status_code=status.HTTP_200_OK,
    tags=["Todos"],
    response_model=Todo,
)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise raise_404_error()


@app.patch(
    "/todos/{todo_id}",
    status_code=status.HTTP_200_OK,
    tags=["Todos"],
    response_model=Todo,
)
def update_todo(
    todo_id: int,
    new_title: Union[str, None] = None,
    new_description: Union[str, None] = None,
    new_priority: Union[str, None] = None,
    new_complete: Union[str, None] = None,
    db: Session = Depends(get_db),
):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise raise_404_error()

    if new_title:
        todo.title = new_title
    if new_description:
        todo.description = new_description
    if new_priority:
        todo.priority = new_priority
    if new_complete:
        todo.complete = new_complete

    db.commit()

    return {"status": 200, "transaction": "Successful"}


@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_200_OK,
    tags=["Todos"],
    responses={200: {"description": "Successfully deleted."}},
)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise raise_404_error()

    db.query(models.Todo).filter(models.Todo.id == todo_id).delete()

    db.commit()

    return {"status": 200, "transaction": "Successful"}
