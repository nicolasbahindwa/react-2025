from datetime import datetime
from pydantic import BaseModel, UUID4

class TokenBase(BaseModel):
    token: str
    expires_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True

class TokenCreate(TokenBase):
    user_id: UUID4

# class TokenResponse(TokenBase):
#     id: UUID4
#     user_id: UUID4

class RefreshTokenRequest(BaseModel):
    refresh_token: str
    
    
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"