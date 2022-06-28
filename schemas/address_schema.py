import copy
from typing import Optional

from pydantic import BaseModel


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

    class Config(AddressIn.Config):
        schema_extra = copy.deepcopy(AddressIn.Config.schema_extra)
        schema_extra["example"]["id"] = 0
