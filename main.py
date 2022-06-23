import copy
from typing import Optional

from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from auth import get_current_user
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


class TodoIn(BaseModel):
    title: Optional[str]
    description: Optional[str]
    priority: Optional[int] = Field(
        gt=0, lt=6, description="The priority must be between 1 and 5."
    )
    complete: Optional[bool] = Field(default=False)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Study FastAPI",
                "description": "Go to Udemy courses",
                "priority": 3,
                "complete": False,
            }
        }


class TodoOut(TodoIn):
    id: int
    owner_id: int

    class Config(TodoIn.Config):
        schema_extra = copy.deepcopy(TodoIn.Config.schema_extra)
        schema_extra["example"]["id"] = 0
        schema_extra["example"]["owner_id"] = 1


def raise_404_error(detail="Todo not found."):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def get_todo_authorization_exception():
    authorization_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
    )
    return authorization_exception


@app.get(
    "/todos",
    status_code=status.HTTP_200_OK,
    tags=["Todos"],
    description="Get all todos. Only for administrators.",
    operation_id="get_all_admin",
)
def get_all_admin(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()


@app.post(
    "/todos/",
    status_code=status.HTTP_201_CREATED,
    tags=["Todos"],
    response_model=TodoOut,
    description="Create new todo for the current user.",
    operation_id="create_todo",
)
def create_todo(
    todo: TodoIn, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    new_todo = models.Todo()
    new_todo.title = todo.title
    new_todo.description = todo.description
    new_todo.priority = todo.priority
    new_todo.complete = todo.complete
    new_todo.owner_id = user.get("user_id")

    db.add(new_todo)
    db.commit()

    return new_todo


@app.get(
    "/todos/{todo_id}",
    status_code=status.HTTP_200_OK,
    tags=["Todos"],
    response_model=TodoOut,
    description="Get current user's todo by provided id.",
    operation_id="get_todo",
)
def get_todo(
    todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    todo_model = (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id)
        .filter(models.Todo.owner_id == user.get("user_id"))
        .first()
    )
    if todo_model is not None:
        return todo_model
    raise raise_404_error()


@app.patch(
    "/todos/{todo_id}",
    status_code=status.HTTP_200_OK,
    tags=["Todos"],
    description="Update current user's todo by id.",
    operation_id="update_todo",
    response_model=TodoOut,
)
def update_todo(
    todo_id: int,
    todo: TodoIn,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    todo_by_id = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo_by_id is None:
        raise raise_404_error()
    else:
        todo_by_id = (
            db.query(models.Todo)
            .filter(models.Todo.id == todo_id)
            .filter(models.Todo.owner_id == user.get("user_id"))
            .first()
        )
        if todo_by_id is None:
            raise get_todo_authorization_exception()

    if todo.title:
        todo_by_id.title = todo.title
    if todo.description:
        todo_by_id.description = todo.description
    if todo.priority:
        todo_by_id.priority = todo.priority
    if todo.complete:
        todo_by_id.complete = todo.complete

    db.commit()

    return todo_by_id


@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_200_OK,
    tags=["Todos"],
    description="Delete current user's todo by id.",
    operation_id="delete_todo",
    responses={200: {"description": "Successfully deleted."}},
)
def delete_todo(
    todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise raise_404_error()
    else:
        todo = (
            db.query(models.Todo)
            .filter(models.Todo.id == todo_id)
            .filter(models.Todo.owner_id == user.get("user_id"))
            .first()
        )
        if todo is None:
            raise get_todo_authorization_exception()

    db.query(models.Todo).filter(models.Todo.id == todo_id).delete()

    db.commit()

    return {"status": 200, "transaction": "Successful"}
