from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
import re
from app.schemas.role import RoleResponse

class PasswordValidator:
    @staticmethod
    def validate_password(password: str) -> bool:
        """Validates password complexity."""
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character.")
        return True

class UserBase(BaseModel):
    username: str = Field(..., min_length=4, max_length=20, description="The user's username.")
    email: EmailStr = Field(..., description="The user's email address.")

    model_config = ConfigDict(from_attributes=True)
    
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User's password with required complexity.")

    @field_validator('password')
    def validate_password_complexity(cls, v):
        PasswordValidator.validate_password(v)
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=4, max_length=20, description="Optional username update.")
    email: Optional[EmailStr] = Field(None, description="Optional email update.")
    password: Optional[str] = Field(None, min_length=8, description="Optional password update with complexity checks.")
    is_active: Optional[bool] = Field(None, description="User active status.")
    role: Optional[str] = Field(None, description="Optional role update for the user.")

    model_config = ConfigDict(from_attributes=True)

    @field_validator('password')
    def validate_password_complexity(cls, v):
        if v is not None:
            PasswordValidator.validate_password(v)
        return v

class UserPatch(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=32, description="Optional patch for username.")
    email: Optional[EmailStr] = Field(None, description="Optional patch for email.")
    is_active: Optional[bool] = Field(None, description="Patch to update user's active status.")
    password: Optional[str] = Field(None, min_length=8, max_length=64, description="Optional patch for password with complexity checks.")
    role: Optional[str] = Field(None, description="Optional patch for user's role.")

    model_config = ConfigDict(from_attributes=True)

    @field_validator('password')
    def validate_password_complexity(cls, v):
        if v is not None:
            PasswordValidator.validate_password(v)
        return v

class UserResponse(UserBase):
    id: UUID = Field(default_factory=uuid4, description="Unique identifier for the user.")
    slug: str = Field(..., description="URL-friendly user identifier.")
    is_active: bool = Field(..., description="User's active status.")
    last_login: Optional[datetime] = Field(None, description="The last login timestamp.")
    created_at: datetime = Field(..., description="Account creation timestamp.")
    updated_at: datetime = Field(..., description="Timestamp for last update to the user's information.")
    roles: List[RoleResponse] = Field(..., description="List of roles assigned to the user.")  # Added roles field

    model_config = ConfigDict(from_attributes=True)
    
    
