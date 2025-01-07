from datetime import datetime
from typing import Optional
from pydantic import BaseModel, IPvAnyAddress

class BlockedIPBase(BaseModel):
    ip: IPvAnyAddress
    blocked_at: datetime
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True
        orm_mode = True

class BlockedIPCreate(BlockedIPBase):
    pass

class BlockedIPResponse(BlockedIPBase):
    blocked_at: datetime