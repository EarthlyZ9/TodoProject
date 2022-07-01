from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.core import security
from app.db.session import SessionLocal
from app.dependencies import get_user_exception, get_authorization_exception
from app.models.user import User

oauth2_bearer = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=security.ALGORITHM)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return db.query(User).filter(User.id == user_id).first()
    except JWTError:
        raise get_user_exception()


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if not crud.user.is_admin(current_user):
        raise get_authorization_exception()
    return current_user
