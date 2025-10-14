from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.orm import Session
from . import schemas
from src.entities.user import User
from src.entities.todo import Todo
from src.exceptions import TodoCreationError, TodoNotFoundError
import logging


def create_todo(current_user: User, db: Session, todo: schemas.TodoCreate) -> Todo:
    try:
        new_todo = Todo(**todo.model_dump())
        new_todo.user_id = current_user.id
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        logging.info(f'Created new todo for user: {current_user.id}')
        return new_todo
        
    except Exception as e:
        logging.error(f'Failed to create todo for user {current_user.id}: {e}')
        raise TodoCreationError(str(e))


def get_todos(current_user: User, db: Session) -> list[Todo]:
    todos = db.query(Todo).filter(Todo.user_id == current_user.id).all()
    logging.info(f'Retrieved {len(todos)} todos for user: {current_user.id}')
    return todos


def get_todo_by_id(current_user: User, db: Session, todo_id: UUID) -> Todo:
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .filter(Todo.user_id == current_user.id)
        .first()
    )
    if not todo:
        logging.warning(f'Todo {todo_id} not found for user {current_user.id}')
        raise TodoNotFoundError(todo_id)
    logging.info(f'Retrieved todo {todo_id} for user: {current_user.id}')
    return todo


def update_todo(current_user: User, db: Session, todo_id: UUID, todo_update: schemas.TodoCreate) -> Todo:
    todo = get_todo_by_id(current_user, db, todo_id)
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    logging.info(f'Successfully updated todo {todo_id} for user: {current_user.id}')
    return todo


def complete_todo(current_user: User, db: Session, todo_id: UUID) -> Todo:
    todo = get_todo_by_id(current_user, db, todo_id)
    if todo.is_completed:
        logging.debug(f'Todo {todo_id} is already complete')
        return todo

    todo.is_completed = True
    todo.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(todo)
    logging.info(f'Todo {todo_id} marked as complete by user {current_user.id}')
    return todo


def delete_todo(current_user: User, db: Session, todo_id: UUID) -> None:
    todo = get_todo_by_id(current_user, db, todo_id)
    db.delete(todo)
    db.commit()
    logging.info(f'Todo {todo_id} deleted by user {current_user.id}')