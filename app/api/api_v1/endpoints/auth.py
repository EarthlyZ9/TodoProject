from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.dependencies import invalid_authentication_exception
from app.models.user import User
from app.schemas import user_schema

router = APIRouter(
    prefix="/auth", tags=["Auth"], responses={401: {"user": "Not authorized."}}
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def save_user(user: user_schema.UserCreate):
    hashed_password = hash_password(user.password)
    user_in_db = user_schema.UserInDB(**user.dict(), hashed_password=hashed_password)
    return user_in_db


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    username: str, user_id: int, expires_delta: Union[timedelta, None] = None
):
    to_encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


@router.post(
    "/signup",
    summary="Sign up",
    response_model=user_schema.UserOut,
    responses={
        201: {"description": "Created user."},
        409: {"description": "User email already exists."},
    },
)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    if db.query(exists().where(User.email == user.email)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User email already exists."
        )
    new_user = User(**save_user(user).dict())
    db.add(new_user)
    db.commit()
    return new_user


@router.post("/login", summary="Login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
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
    user = db.query(User).filter(User.id == current_user.id).first()

    if user_verification.username == user.username and verify_password(
        user_verification.password, user.hashed_password
    ):
        user.hashed_password = hash_password(user_verification.new_password)
        db.add(user)
        db.commit()

        return user
    raise invalid_authentication_exception()
