from fastapi import APIRouter, status
from typing import List
from uuid import UUID
from ..database.core import DbSession
from . import schemas
from . import service
from ..auth.service import CurrentUser


router = APIRouter(
    prefix='/todos',
    tags=['Todos']
)

@router.post('/', response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.TodoCreate, current_user: CurrentUser, db: DbSession):
    return service.create_todo(current_user, db, todo)

@router.get('/', response_model=List[schemas.TodoResponse])
def get_todos(current_user: CurrentUser, db: DbSession):
    return service.get_todos(current_user, db)


@router.get('/{todo_id}', response_model=schemas.TodoResponse)
def get_todo(todo_id: UUID, current_user: CurrentUser, db: DbSession):
    return service.get_todo_by_id(current_user, db, todo_id)

@router.put('/{todo_id}', response_model=schemas.TodoResponse)
def update_todo(todo_id: UUID, todo_update: schemas.TodoCreate, current_user: CurrentUser, db: DbSession):
    return service.update_todo(current_user, db, todo_id, todo_update)


@router.put('/{todo_id}/complete', response_model=schemas.TodoResponse)
def complete_todo(todo_id: UUID, current_user: CurrentUser, db: DbSession):
    return service.complete_todo(current_user, db, todo_id)


@router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: UUID, current_user: CurrentUser, db: DbSession):
    service.delete_todo(current_user, db, todo_id)
    