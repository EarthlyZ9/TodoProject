import copy
from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from sql_app import models
from sql_app.database import SessionLocal, engine
from sql_app.database import secrets

JWT_SECRET_KEY = secrets["JWT_SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: Optional[bool] = Field(default=True)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "linda2927",
                "email": "linda2927@naver.com",
                "first_name": "Jisoo",
                "last_name": "Lee",
            }
        }


class UserIn(UserBase):
    password: str

    class Config(UserBase.Config):
        schema_extra = copy.deepcopy(UserBase.Config.schema_extra)
        schema_extra["example"]["password"] = "linda2927"


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    id: Optional[int]
    hashed_password: str

    class Config(UserBase.Config):
        schema_extra = copy.deepcopy(UserBase.Config.schema_extra)
        schema_extra["example"]["id"] = 0
        schema_extra["example"]["hashed_password"] = ""


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


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


def save_user(user: UserIn):
    hashed_password = hash_password(user.password)
    user_in_db = UserInDB(**user.dict(), hashed_password=hashed_password)
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


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "user_id": user_id}
    except JWTError:
        raise get_user_exception()


@app.post(
    "/users",
    tags=["Users"],
    response_model=UserOut,
    responses={201: {"description": "Created user."}},
)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    new_user = models.User(**save_user(user).dict())
    db.add(new_user)
    db.commit()
    return new_user


@app.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user.username, user.id, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# Exceptions
def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception


def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response
