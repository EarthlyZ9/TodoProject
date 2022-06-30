from sqlalchemy import TIMESTAMP, Column, text
from sqlalchemy.sql import func


class TimestampMixin(object):
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, server_default=text("NULL ON UPDATE CURRENT_TIMESTAMP")
    )
