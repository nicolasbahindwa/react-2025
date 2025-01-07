from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime, timezone

ALLOWED_TOKEN_TYPES = {
    'access': 'access',
    'refresh': 'refresh',
    "password_reset": "password_reset",
    "activation": "activation",
    "password_reset": "password_reset",
    
}

class Token(BaseModel):
    __tablename__ = "tokens"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    token = Column(String(255), nullable=False, unique=True, index=True)
    token_type = Column(String(50), nullable=False)  # Use string for token_type
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # relationship
    user = relationship('User', back_populates="tokens")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.token_type not in ALLOWED_TOKEN_TYPES.values():
            raise ValueError(f"Invalid token_type: {self.token_type}. Must be one of {ALLOWED_TOKEN_TYPES.values()}")

    def is_expired(self) -> bool:
        return self.expires_at < datetime.now(timezone.utc)

    def is_valid(self) -> bool:
        return not (self.is_expired() or self.is_revoked)
