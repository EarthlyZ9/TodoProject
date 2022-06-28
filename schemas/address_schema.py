import copy
from typing import Optional, Union

from pydantic import BaseModel

from schemas.user_schema import UserOut


class AddressIn(BaseModel):
    address1: str
    address2: Optional[str]
    apt_num: Optional[str]
    city: str
    state: str
    country: str
    zipcode: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "address1": "1  Washington Cir, NW",
                "address2": "",
                "city": "Washington",
                "state": "District of Columbia",
                "country": "United States",
                "zipcode": "20037",
                "apt_num": "307",
            }
        }


class AddressOut(AddressIn):
    id: int
    # resident: Union[UserOut, None] = None

    class Config(AddressIn.Config):
        schema_extra = copy.deepcopy(AddressIn.Config.schema_extra)
        schema_extra["example"]["id"] = 0
        # schema_extra["example"]["resident"] = {
        #     "id": 0,
        #     "username": "linda2927",
        #     "email": "linda2927@naver.com",
        #     "first_name": "Jisoo",
        #     "last_name": "Lee",
        # }
