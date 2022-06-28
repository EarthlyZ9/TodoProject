import sys

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from routers.auth import get_current_user
from schemas import user_schema
from todo_proj import models
from todo_proj.database import engine, SessionLocal
from todo_proj.dependencies import raise_404_error

sys.path.append("..")

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Cannot find user for the provided id"}},
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
    summary="Get all users. Only for administrators.",
    operation_id="get_all_users",
)
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get current user's data",
    response_model=user_schema.UserWithAddress,
    operation_id="get_user",
)
def get_user(
    current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return current_user


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get user by user id",
    operation_id="get_user_by_path",
    response_model=user_schema.UserBase,
)
def get_user_by_path(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise raise_404_error(detail="Cannot find user for the provided id.")
    return user


@router.patch(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Update current user's phone number",
    response_model=user_schema.UserOut,
    operation_id="update_phone_number",
)
def update_phone_number(
    new_data: user_schema.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    user_data = new_data.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Delete current user.",
    operation_id="delete_user",
    responses={200: {"description": "Successfully deleted user."}},
)
def delete_user(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    db.query(models.User).filter(models.User.id == current_user.id).delete()

    db.commit()

    return {"status": 200, "transaction": "Successful"}
