from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class Todo(Base, TimestampMixin):
    title = Column(String(200))
    description = Column(String(500))
    priority = Column(Integer)
    isCompleted = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="todos")
