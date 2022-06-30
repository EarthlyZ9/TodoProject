from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class User(Base, TimestampMixin):
    email = Column(String(100), unique=True, index=True)
    username = Column(String(30), unique=True, index=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    hashed_password = Column(String(50))
    is_active = Column(Boolean, default=True)
    phone_number = Column(String(11))
    address_id = Column(Integer, ForeignKey("address.id"), nullable=True)
    is_admin = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    todos = relationship("Todo", back_populates="owner")
    address = relationship("Address", back_populates="user")

    @validates("email")
    def validate_email(self, key, user):
        if "@" not in user:
            raise ValueError("failed simple email validation")
        return user
