from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

from todo_proj.database import Base


class TimestampMixin(object):
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, server_default=text("NULL ON UPDATE CURRENT_TIMESTAMP")
    )


class Todo(Base, TimestampMixin):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(String(500))
    priority = Column(Integer)
    isCompleted = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="todos")


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    username = Column(String(30), unique=True, index=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    hashed_password = Column(String(50))
    is_active = Column(Boolean, default=True)
    phone_number = Column(String(11))
    address_id = Column(Integer, ForeignKey("address.id"), nullable=True)

    todos = relationship("Todo", back_populates="owner")
    address = relationship("Address", back_populates="user")

    @validates("email")
    def validate_email(self, key, user):
        if "@" not in user:
            raise ValueError("failed simple email validation")
        return user


class Address(Base, TimestampMixin):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    address1 = Column(String(100))
    address2 = Column(String(100))
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(100))
    zipcode = Column(String(5))
    apt_num = Column(String(20))

    user = relationship("User", back_populates="address", uselist=False)
