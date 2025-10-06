from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from src.entities.todo import Priority


class TodoBase(BaseModel):
    description: str
    due_date: Optional[datetime] = None
    priority: Priority = Priority.Medium


class TodoCreate(TodoBase):
    description: str


class TodoResponse(TodoBase):
    id: UUID
    is_completed: bool
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)