import copy
from typing import Optional

from pydantic import BaseModel, Field


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
    id: Optional[int]

    class Config(UserBase.Config):
        schema_extra = copy.deepcopy(UserBase.Config.schema_extra)
        schema_extra["example"]["id"] = 0


class UserInDB(UserOut):
    hashed_password: str

    class Config(UserBase.Config):
        schema_extra = copy.deepcopy(UserBase.Config.schema_extra)
        schema_extra["example"]["hashed_password"] = ""


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "linda2927",
                "password": "password",
                "new_password": "password2",
            }
        }
