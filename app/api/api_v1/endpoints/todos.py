from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.dependencies import raise_404_error, get_authorization_exception
from app.models.todo import Todo
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
    operation_id="get_all_admin",
)
def get_all_admin(db: Session = Depends(get_db)):
    return db.query(Todo).all()


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
    new_todo = Todo(**todo.dict(), owner_id=current_user.id)
    db.add(new_todo)
    db.commit()

    return new_todo


@router.get(
    "/", summary="Get all todos of current user.", status_code=status.HTTP_200_OK
)
def get_todos(current_user: User = Depends(get_current_user)):
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
    todo_model = (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .filter(Todo.owner_id == current_user.id)
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
    todo: todo_schema.TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo_by_id = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_by_id is None:
        raise raise_404_error()
    else:
        todo_by_id = (
            db.query(Todo)
            .filter(Todo.id == todo_id)
            .filter(Todo.owner_id == current_user.id)
            .first()
        )
        if todo_by_id is None:
            raise get_authorization_exception()

    todo_data = todo.dict(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(todo_by_id, key, value)
    db.add(todo_by_id)
    db.commit()
    db.refresh(todo_by_id)

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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise raise_404_error("Cannot find todo for the provided id.")
    else:
        todo = (
            db.query(Todo)
            .filter(Todo.id == todo_id)
            .filter(Todo.owner_id == current_user.id)
            .first()
        )
        if todo is None:
            raise get_authorization_exception()

    db.query(Todo).filter(Todo.id == todo_id).delete()

    db.commit()

    return {"status": 200, "transaction": "Successful"}
