from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_current_user, get_db, get_current_admin
from app.dependencies import raise_404_error, get_authorization_exception
from app.models.user import User
from app.schemas import todo_schema

router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
    responses={404: {"description": "Cannot find todo for the provided id."}},
)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    tags=["Todos"],
    summary="Get all todos. Only for administrators.",
    operation_id="read_all",
)
def read_all(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)
):
    if current_user:
        return crud.todo.get_multi(db)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=todo_schema.TodoOut,
    summary="Create new todo for the current user.",
    operation_id="create_todo",
)
def create_todo(
    todo: todo_schema.TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.todo.create_with_owner(db=db, obj_in=todo, owner_id=current_user.id)


@router.get(
    "/",
    summary="Get all todos of current user.",
    status_code=status.HTTP_200_OK,
    operation_id="read_todos",
    response_model=List[todo_schema.TodoOut],
)
def read_todos(current_user: User = Depends(get_current_user)):
    if current_user.todos is None:
        return HTTPException(status_code=status.HTTP_200_OK, detail="No todos created.")
    return current_user.todos


@router.get(
    "/{todo_id}",
    status_code=status.HTTP_200_OK,
    response_model=todo_schema.TodoOut,
    summary="Get current user's todo by provided id.",
    operation_id="get_todo_by_id",
)
def get_todo_by_id(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = crud.todo.get(db=db, id=todo_id)
    if todo is None:
        raise raise_404_error(detail="Cannot find todo for the provided id.")
    if todo.owner_id == current_user.id:
        return todo
    raise get_authorization_exception()


@router.patch(
    "/{todo_id}",
    status_code=status.HTTP_200_OK,
    summary="Update current user's todo by id.",
    operation_id="update_todo",
    response_model=todo_schema.TodoOut,
    responses={200: {"description": "Successfully updated."}},
)
def update_todo(
    todo_id: int,
    todo: todo_schema.TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo_by_id = crud.todo.get(db=db, id=todo_id)
    if todo_by_id is None:
        raise raise_404_error(detail="Cannot find todo for the provided id.")
    if todo_by_id.owner_id == current_user.id:
        return crud.todo.update(db=db, db_obj=todo_by_id, obj_in=todo)
    raise get_authorization_exception()


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete current user's todo by id.",
    operation_id="delete_todo",
    responses={200: {"description": "Successfully deleted."}},
    response_model=todo_schema.TodoOut,
)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = crud.todo.get(db=db, id=todo_id)
    if todo is None:
        raise raise_404_error("Cannot find todo for the provided id.")
    if todo.owner_id == current_user.id:
        return crud.todo.remove(db=db, id=todo_id)
    raise get_authorization_exception()
