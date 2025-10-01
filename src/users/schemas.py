from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    

class PasswordChange(BaseModel):
    current_pasword: str
    new_passwsord: str
    new_password_confirm: str