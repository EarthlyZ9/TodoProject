from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class Address(Base, TimestampMixin):
    address1 = Column(String(100))
    address2 = Column(String(100))
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(100))
    zipcode = Column(String(5))
    apt_num = Column(String(20))

    user = relationship("User", back_populates="address", uselist=False)
