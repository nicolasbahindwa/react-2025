from sqlalchemy import Column, String, DateTime
from datetime import datetime, timezone
from sqlalchemy.sql import func
from app.database.base_model import BaseModel


class BlockedIP(BaseModel):
    __tablename__ = "blocked_ips"

    ip = Column(String, primary_key=True)
    blocked_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    class Config:
        orm_mode = True

    def is_blocked(self)-> bool:
        if not self.expires_at:
            return True
        return self.expires_at > datetime.now(timezone.utc)