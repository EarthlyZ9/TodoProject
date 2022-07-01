from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.dependencies import invalid_authentication_exception
from app.models.user import User
from app.schemas import user_schema
from app import crud
from app.core.security import create_access_token, verify_password

router = APIRouter(
    prefix="/auth", tags=["Auth"], responses={401: {"user": "Not authorized."}}
)


@router.post(
    "/signup",
    summary="Sign up",
    response_model=user_schema.UserOut,
    responses={
        201: {"description": "Created user."},
        409: {"description": "User email already exists."},
    },
)
def create_user(user_data: user_schema.UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User email already exists."
        )

    return crud.user.create(db, user_data)


@router.post("/login", summary="Login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = crud.user.authenticate(form_data.username, form_data.password, db)
    if not user:
        raise invalid_authentication_exception()
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user.username, user.id, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.patch(
    "/change-password",
    status_code=status.HTTP_200_OK,
    summary="Update current user's password with user verification.",
    operation_id="update_user_password",
    response_model=user_schema.UserOut,
    responses={200: {"description": "User password updated successfully."}},
)
def update_user_password(
    user_verification: user_schema.UserVerification,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if user_verification.username == current_user.username and verify_password(
        user_verification.password, current_user.hashed_password
    ):
        return crud.user.update_user_password(
            db, user_verification.new_password, current_user
        )
    raise invalid_authentication_exception()


@router.delete(
    "/leave",
    status_code=status.HTTP_200_OK,
    summary="Delete current user.",
    operation_id="delete_user",
    response_model=user_schema.UserOut,
    responses={200: {"description": "Successfully deleted user."}},
)
def delete_user(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return crud.user.deactivate(db, current_user)
