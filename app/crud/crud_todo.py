from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.todo import Todo
from app.schemas.todo_schema import TodoCreate, TodoUpdate


class CRUDTodo(CRUDBase[Todo, TodoCreate, TodoUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: TodoCreate, owner_id: int
    ) -> Todo:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # def read_todo_by_user(self, db: Session, *, user_id: int) -> List[Todo]:
    #     return db.query(self.model).filter(self.model.owner_id == user_id).all()


todo = CRUDTodo(Todo)
