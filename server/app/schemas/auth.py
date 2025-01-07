from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class LogoutResponse(BaseModel):
    message: str
    revoked_tokens: int

class UserBase(BaseModel):
    email: EmailStr
    is_active: bool
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RequestPasswordReset(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str