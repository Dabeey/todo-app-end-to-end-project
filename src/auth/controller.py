from typing import Annotated
from fastapi import APIRouter, status, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..database.core import DbSession
from ..rate_limiter import limiter
from . import schemas
from . import service
from ..users.schemas import UserResponse


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
@limiter.limit('5/minute')
async def register_user(request: Request, register_user_request: schemas.RegisterUserRequest, db: DbSession):
    return service.register_user(db, register_user_request)


@router.post('/login', response_model=schemas.Token)
async def login(login_request: schemas.LoginRequest, db: DbSession):
    """Login with email and password - works well with /docs"""
    return service.login_for_access_token(login_request, db)


@router.post('/token', response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    """OAuth2 compatible login for external clients"""
    return service.login_for_access_token_oauth2(form_data, db)