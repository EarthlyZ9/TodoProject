import sys
from fastapi import APIRouter, status, Depends

from dependencies import raise_404_error, invalid_authentication_exception
from routers.auth import get_current_user, hash_password, verify_password
from schemas import user_schema

from sql_app import models
from sql_app.database import engine, SessionLocal
from sqlalchemy.orm import Session

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
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get user by user id (path).",
    operation_id="get_user_by_path",
    response_model=user_schema.UserOut,
)
def get_user_by_path(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise raise_404_error(detail="Cannot find user for the provided id.")
    return user


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get user by user id (query params).",
    operation_id="get_user_by_query_params",
    response_model=user_schema.UserOut,
)
def get_user_by_query_params(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise raise_404_error(detail="Cannot find user for the provided id.")
    return user


@router.patch(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Update current user's password with user verification.",
    operation_id="update_user_password",
    response_model=user_schema.UserOut,
    responses={200: {"description": "User password updated successfully."}},
)
def update_user_password(
    user_verification: user_schema.UserVerification,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.id == current_user.get("user_id"))
        .first()
    )

    if user_verification.username == user.username and verify_password(
        user_verification.password, user.hashed_password
    ):
        hashed_password = hash_password(user_verification.new_password)
        user.hashed_password = hashed_password

        db.commit()

        return user
    raise invalid_authentication_exception()


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Delete current user.",
    operation_id="delete_user",
    responses={200: {"description": "Successfully deleted user."}},
)
def delete_user(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    db.query(models.User).filter(models.User.id == current_user.get("user_id")).delete()

    db.commit()

    return {"status": 200, "transaction": "Successful"}
