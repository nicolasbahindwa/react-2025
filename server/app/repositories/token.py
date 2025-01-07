from datetime import datetime
from typing import Optional, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, and_
from fastapi import HTTPException, status
from app.core.logging import app_logger, log_operation
from app.models.users import User
from app.models.tokens import Token, ALLOWED_TOKEN_TYPES
from app.exceptions.database import (
    TokenExpiredError,
    InvalidTokenError,
    DatabaseCommitException,
    NotFoundException
)
from app.schemas.user import UserResponse
from app.core.config import Settings

class TokenRepository:
    """Repository pattern for Token-related database operations"""
    
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_active_token_with_user(
        self, 
        token_string: str, 
        token_type: str
    ) -> Optional[Tuple[Token, User]]:
        """Get active token with associated user using ORM relationships"""
        result = await self._session.execute(
            select(Token, User)
            .join(User)
            .options(selectinload(Token.user))
            .where(
                and_(
                    Token.token == token_string,
                    Token.token_type == token_type,
                    Token.is_revoked == False
                )
            )
        )
        return result.first()
