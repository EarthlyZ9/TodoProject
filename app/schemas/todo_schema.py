import copy
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str
    description: str
    priority: int = Field(
        gt=0, lt=6, description="The priority must be between 1 and 5."
    )
    isCompleted: Optional[bool] = Field(default=False)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Study FastAPI",
                "description": "Go to Udemy courses",
                "priority": 3,
                "isCompleted": False,
            }
        }


class TodoUpdate(TodoCreate):
    title: Optional[str]
    description: Optional[str]
    priority: Optional[int]

    class Config(TodoCreate.Config):
        pass


class TodoOut(TodoCreate):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Union[datetime, None] = None

    class Config(TodoCreate.Config):
        schema_extra = copy.deepcopy(TodoCreate.Config.schema_extra)
        schema_extra["example"]["id"] = 0
        schema_extra["example"]["owner_id"] = 1
        schema_extra["example"]["created_at"] = "2022-06-28 16:55:47"
        schema_extra["example"]["updated_at"] = "2022-06-29 17:00:42"
