from datetime import datetime, timezone
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import schemas
from src.auth.schemas import TokenData
from src.entities.todo import Todo
from src.exceptions import TodoCreationError, TodoNotFoundError
import logging


def create_todo(current_user: TokenData, db: Session,  todo: schemas.TodoCreate) -> Todo:
    try:
        new_todo = Todo(**todo.model_dump())
        new_todo.user_id = current_user.get_uuid()
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        logging.info(f'Created new todo for user: {current_user.get_uuid()}')
        return new_todo
        
    except Exception as e:
        logging.error(f'Failed to create todo for user {current_user.get_uuid()}')
        raise TodoCreationError(str(e))


