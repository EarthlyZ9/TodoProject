import copy
from typing import Union

from schemas.address_schema import AddressIn
from schemas.user_schema import UserOut


# class UserBase(BaseModel):
#     username: str
#     email: str
#     first_name: str
#     last_name: str
#     phone_number: Optional[str]
#     is_active: bool = Field(default=True)
#
#     class Config:
#         orm_mode = True
#         schema_extra = {
#             "example": {
#                 "username": "linda2927",
#                 "email": "linda2927@naver.com",
#                 "first_name": "Jisoo",
#                 "last_name": "Lee",
#                 "phone_number": "01029277729",
#                 "is_active": True
#             }
#         }


class AddressWithUser(AddressIn):
    id: int
    user: Union[UserOut, None] = None

    class Config(AddressIn.Config):
        schema_extra = copy.deepcopy(AddressIn.Config.schema_extra)
        schema_extra["example"]["id"] = 0
        # schema_extra["example"]["user"] = {
        #     "id": 0,
        #     "username": "linda2927",
        #     "email": "linda2927@naver.com",
        #     "first_name": "Jisoo",
        #     "last_name": "Lee",
        # }
