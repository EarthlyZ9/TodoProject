from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, get_current_admin
from app.dependencies import raise_404_error, get_authorization_exception
from app.models.user import User
from app.schemas import user_schema
from app import crud

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Cannot find user for the provided id"}},
)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    summary="Get all users. Only for administrators.",
    operation_id="get_all_users",
    response_model=List[user_schema.UserWithAddress],
)
def get_all_users(
    db: Session = Depends(get_db), admin: User = Depends(get_current_admin)
):
    return crud.user.get_multi(db)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get current user's data",
    response_model=user_schema.UserWithAddress,
    operation_id="get_user",
)
def get_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get user by user id",
    operation_id="get_user_by_id",
    response_model=user_schema.UserWithAddress,
)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = crud.user.get(db, user_id)
    if user is None:
        raise raise_404_error(detail="Cannot find user for the provided id.")

    if current_user.id == user.id:
        return user
    if not crud.user.is_admin(current_user):
        raise get_authorization_exception()
    return user


@router.patch(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Update current user's phone number",
    response_model=user_schema.UserOut,
    operation_id="update_user",
)
def update_user(
    new_data: user_schema.UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = crud.user.update(db, db_obj=current_user, obj_in=new_data)
    return user
