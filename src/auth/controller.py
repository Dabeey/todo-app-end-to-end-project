from typing import Annotated
from fastapi import APIRouter, status, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..database.core import DbSession
from ..rate_limiter import limiter
from . import schemas
from . import service

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
@limiter.limit('5/hour')
async def register_user(request: Request, db: DbSession, register_user_request: schemas.RegisterUserRequest):
    service.register_user(db, register_user_request)


@router.post('/token', response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends() ], db: DbSession):
    return service.login_for_access_token(form_data, db)