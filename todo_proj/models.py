from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from todo_proj.database import Base


# TODO: How am I going to return resources including every related nested object (serialization)?


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(String(500))
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="todos")


class User(Base):
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
    address = relationship("Address", back_populates="user", uselist=False)


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    address1 = Column(String(100))
    address2 = Column(String(100))
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(100))
    zipcode = Column(String(5))
    apt_num = Column(String(20))
    # user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="address", uselist=False)
