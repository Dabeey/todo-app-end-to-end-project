from fastapi import APIRouter, status
from ..database.core import DbSession
from . import schemas
from . import service
from ..auth.service import CurrentUser


router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/me', response_model=schemas.UserResponse)
def get_current_user(current_user: CurrentUser):
    return current_user


@router.put('/change-password', status_code=status.HTTP_200_OK)
def change_password(password_change: schemas.PasswordChange, current_user: CurrentUser, db=DbSession):
    service.change_password(db, current_user.id, password_change)

