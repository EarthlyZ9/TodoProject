import sys
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from todo_proj.dependencies import get_user_exception, invalid_authentication_exception
from schemas import user_schema
from todo_proj import models
from todo_proj.database import SessionLocal, engine
from todo_proj.database import secrets

sys.path.append("..")

JWT_SECRET_KEY = secrets["JWT_SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/auth", tags=["Auth"], responses={401: {"user": "Not authorized."}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def hash_password(password: str):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def save_user(user: user_schema.UserIn):
    hashed_password = hash_password(user.password)
    user_in_db = user_schema.UserInDB(**user.dict(), hashed_password=hashed_password)
    return user_in_db


def authenticate_user(username: str, password: str, db):
    user = db.query(models.User).filter(models.User.username == username).first()
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
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return db.query(models.User).filter(models.User.id == user_id).first()
    except JWTError:
        raise get_user_exception()


@router.post(
    "/signup",
    summary="Sign up",
    response_model=user_schema.UserOut,
    responses={201: {"description": "Created user."}},
)
def create_user(user: user_schema.UserIn, db: Session = Depends(get_db)):
    new_user = models.User(**save_user(user).dict())
    db.add(new_user)
    db.commit()
    return new_user


@router.post("/token", summary="Login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise invalid_authentication_exception()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user.username, user.id, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
