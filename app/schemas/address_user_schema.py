import copy

from app.schemas.address_schema import AddressOut
from app.schemas.user_schema import UserOut


class AddressWithUser(AddressOut):
    user: UserOut

    class Config(AddressOut.Config):
        schema_extra = copy.deepcopy(AddressOut.Config.schema_extra)
        schema_extra["example"]["user"] = UserOut.Config.schema_extra["example"]
