import sys

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import raise_404_error, get_authorization_exception
from routers.auth import get_current_user
from schemas import todo_schema
from sql_app import models
from sql_app.database import engine, SessionLocal

sys.path.append("..")

router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
    responses={404: {"description": "Cannot find todo for the provided id."}},
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    tags=["Todos"],
    summary="Get all todos. Only for administrators.",
    operation_id="get_all_admin",
)
def get_all_admin(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=todo_schema.TodoOut,
    summary="Create new todo for the current user.",
    operation_id="create_todo",
)
def create_todo(
    todo: todo_schema.TodoIn,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_todo = models.Todo()
    new_todo.title = todo.title
    new_todo.description = todo.description
    new_todo.priority = todo.priority
    new_todo.complete = todo.complete
    new_todo.owner_id = current_user.id

    db.add(new_todo)
    db.commit()

    return new_todo


@router.get(
    "/", summary="Get all todos of current user.", status_code=status.HTTP_200_OK
)
def get_todos(
    current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    todos = db.query(models.Todo).filter(models.Todo.owner_id == current_user.id).all()
    return todos


@router.get(
    "/{todo_id}",
    status_code=status.HTTP_200_OK,
    response_model=todo_schema.TodoOut,
    summary="Get current user's todo by provided id.",
    operation_id="get_todo_by_id",
)
def get_todo_by_id(
    todo_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    todo_model = (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id)
        .filter(models.Todo.owner_id == current_user.id)
        .first()
    )
    if todo_model is not None:
        return todo_model
    raise raise_404_error(detail="Cannot find todo for the provided id.")


@router.patch(
    "/{todo_id}",
    status_code=status.HTTP_200_OK,
    summary="Update current user's todo by id.",
    operation_id="update_todo",
    response_model=todo_schema.TodoOut,
)
def update_todo(
    todo_id: int,
    todo: todo_schema.TodoIn,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    todo_by_id = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo_by_id is None:
        raise raise_404_error()
    else:
        todo_by_id = (
            db.query(models.Todo)
            .filter(models.Todo.id == todo_id)
            .filter(models.Todo.owner_id == current_user.id)
            .first()
        )
        if todo_by_id is None:
            raise get_authorization_exception()

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


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete current user's todo by id.",
    operation_id="delete_todo",
    responses={200: {"description": "Successfully deleted."}},
)
def delete_todo(
    todo_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise raise_404_error("Cannot find todo for the provided id.")
    else:
        todo = (
            db.query(models.Todo)
            .filter(models.Todo.id == todo_id)
            .filter(models.Todo.owner_id == current_user.id)
            .first()
        )
        if todo is None:
            raise get_authorization_exception()

    db.query(models.Todo).filter(models.Todo.id == todo_id).delete()

    db.commit()

    return {"status": 200, "transaction": "Successful"}
