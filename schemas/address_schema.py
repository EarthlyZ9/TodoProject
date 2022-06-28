import copy
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


class AddressIn(BaseModel):
    address1: str
    address2: Union[str, None] = None
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
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config(AddressIn.Config):
        schema_extra = copy.deepcopy(AddressIn.Config.schema_extra)
        schema_extra["example"]["id"] = 0
        schema_extra["example"]["created_at"] = "2022-06-28 16:55:47"
        schema_extra["example"]["updated_at"] = "2022-06-29 17:00:42"


class AddressUpdate(BaseModel):
    address1: Optional[str]
    address2: Union[str, None] = None
    apt_num: Union[str, None] = None
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    zipcode: Optional[str]

    class Config(AddressIn.Config):
        pass
