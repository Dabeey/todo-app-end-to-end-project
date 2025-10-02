from datetime import datetime, timezone
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import model
from src.auth.schemas import TokenData
from src.entities.todo import Todo
from src.exceptions 