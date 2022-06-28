import copy
from typing import Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field

from schemas.address_schema import AddressOut


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    phone_number: Optional[str]
    is_active: bool = Field(default=True)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "linda2927",
                "email": "linda2927@naver.com",
                "first_name": "Jisoo",
                "last_name": "Lee",
                "phone_number": "01029277729",
                "is_active": True,
            }
        }


class UserIn(UserBase):
    password: str

    class Config(UserBase.Config):
        schema_extra = copy.deepcopy(UserBase.Config.schema_extra)
        schema_extra["example"]["password"] = "linda2927"


class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config(UserBase.Config):
        schema_extra = copy.deepcopy(UserBase.Config.schema_extra)
        schema_extra["example"]["id"] = 0
        schema_extra["example"]["created_at"] = "2022-06-28 16:55:47"
        schema_extra["example"]["updated_at"] = "2022-06-29 17:00:42"


class UserWithAddress(UserOut):
    address: AddressOut

    class Config(UserOut.Config):
        schema_extra = copy.deepcopy(UserOut.Config.schema_extra)
        schema_extra["example"]["address"] = {
            "address1": "1  Washington Cir, NW",
            "address2": "",
            "city": "Washington",
            "state": "District of Columbia",
            "country": "United States",
            "zipcode": "20037",
            "apt_num": "307",
        }


class UserInDB(UserOut):
    hashed_password: str

    class Config(UserOut.Config):
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
