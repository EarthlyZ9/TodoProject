import copy
from typing import Optional

from pydantic import BaseModel, Field


class TodoIn(BaseModel):
    title: Optional[str]
    description: Optional[str]
    priority: Optional[int] = Field(
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


class TodoOut(TodoIn):
    id: int
    owner_id: int

    class Config(TodoIn.Config):
        schema_extra = copy.deepcopy(TodoIn.Config.schema_extra)
        schema_extra["example"]["id"] = 0
        schema_extra["example"]["owner_id"] = 1
