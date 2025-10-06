from datetime import timedelta, datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
import jwt
from jwt import PyJWTError
from sqlalchemy.orm import Session
from src.entities.user import User
from . import schemas
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ..exceptions import AuthenticationError
import logging
import os
from ..database.core import get_db
from sqlalchemy.orm.util


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')



""" Password: Authenticate user """

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def authenticate_user(email:str, password:str, db:Session) -> User | bool:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        logging.warning(f'Failed to authenticate email for {email}')
        return False
    return user


""" Access Token"""

def create_access_token(email:str, user_id: UUID, expires_delta: timedelta) -> str:
    encode = {
        'sub': email,
        'id': str(user_id),
        'exp': datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> schemas.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get('id')
        return schemas.TokenData(user_id=user_id)
    except PyJWTError as e:
        logging.warning(f'Token verification failed: {str(e)}')
        raise AuthenticationError()
    

"""" Fetch Current User using access token"""


def register_user(db, register_user_request: schemas.RegisterUserRequest):
    try:
        # 1️⃣ Check if user already exists
        existing_user = db.query(User).filter(User.email == register_user_request.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # 2️⃣ Create new user
        hashed_password = get_password_hash(register_user_request.password)
        new_user = User(
            id=uuid4(),
            email=register_user_request.email,
            first_name=register_user_request.first_name,
            last_name=register_user_request.last_name,
            password_hash=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logging.info(f"✅ User {new_user.email} registered successfully.")
        return new_user  # Returning model (works fine if response_model handles it)

    except IntegrityError as e:
        db.rollback()
        logging.error(f"IntegrityError: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists."
        )
    except Exception as e:
        db.rollback()
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while creating the user."
        )
    

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> schemas.TokenData:
    return verify_token(token)

CurrentUser = Annotated[schemas.TokenData, Depends(get_current_user)]


""" Login User using access token schemas"""

def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]) -> schemas.Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise AuthenticationError()
    
    token = create_access_token(user.email, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return schemas.Token(access_token=token, token_type='bearer')