from typing import Union

from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas import user_schema
from app.schemas.user_schema import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, obj_in: UserCreate):
        hashed_password = hash_password(obj_in.password)
        user_in_db = user_schema.UserInDB(
            **obj_in.dict(), hashed_password=hashed_password
        )
        new_user = User(**user_in_db.dict())
        db.add(new_user)
        db.commit()

        return new_user

    def update_user_password(self, db: Session, obj_in: str, u: User) -> User:
        u.hashed_password = hash_password(obj_in)
        db.add(u)
        db.commit()
        return u

    def authenticate(
        self, username: str, password: str, db: Session
    ) -> Union[User, bool]:
        u = db.query(self.model).filter(User.username == username).first()
        if not user:
            return False
        if not verify_password(password, u.hashed_password):
            return False
        return u

    def deactivate(self, db: Session, u: User):
        u.is_active = False
        db.add(user)
        db.commit()

        return u

    def is_admin(self, u: User) -> bool:
        return u.is_admin


user = CRUDUser(User)
