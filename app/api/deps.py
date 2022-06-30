from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.dependencies import get_user_exception
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
):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=settings.ALGORITHM
        )
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return db.query(User).filter(User.id == user_id).first()
    except JWTError:
        raise get_user_exception()
