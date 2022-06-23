from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from sql_app.database import Base


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

    todos = relationship("Todo", back_populates="owner")
