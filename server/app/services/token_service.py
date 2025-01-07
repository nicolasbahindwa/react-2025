from datetime import datetime, timedelta
import secrets
import uuid
from typing import Optional, Tuple
import pytz
from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.tokens import Token, ALLOWED_TOKEN_TYPES
from app.models.users import User
from app.utils.security import JWTHandler
from app.exceptions.database import (
    TokenCreationError,
    TokenExpiredError,
    InvalidTokenError,
    NotFoundException
)
from app.config import settings
from app.core.logging import app_logger, log_operation

class TokenService:
    def __init__(self, session: AsyncSession, jwt_handler: Optional[JWTHandler] = None):
        self._session = session
        self.jwt_handler = jwt_handler or JWTHandler()

    @log_operation("create_activation_token")
    async def create_activation_token(self, user_id: str) -> Token:
        """Create and save a new activation token."""
        try:
            token_string = secrets.token_urlsafe(32)
            expires_at = datetime.now(pytz.UTC) + timedelta(hours=settings.account_activation_expires)
            
            token = Token(
                user_id=user_id,
                token=token_string,
                token_type='activation',
                expires_at=expires_at
            )
            
            self._session.add(token)
            await self._session.commit()
            return token
        except Exception as e:
            await self._session.rollback()
            app_logger.log_error(
                "Failed to create activation token",
                error=e,
                extra={"user_id": str(user_id)}
            )
            raise TokenCreationError(detail=str(e))

    @log_operation("create_password_reset_token")
    async def create_password_reset_token(self, user_id: str) -> Token:
        """Create and save a password reset token."""
        try:
            # Generate a secure token string
            token_string = secrets.token_urlsafe(32)
            expires_at = datetime.now(pytz.UTC) + timedelta(hours=settings.password_reset_token_expire_hours)
            
            # Revoke any existing password reset tokens for this user
            await self.revoke_user_tokens_by_type(user_id, 'password_reset')
            
            token = Token(
                user_id=user_id,
                token=token_string,
                token_type='password_reset',
                expires_at=expires_at
            )
            
            self._session.add(token)
            await self._session.commit()
            return token
        except Exception as e:
            await self._session.rollback()
            app_logger.log_error(
                "Failed to create password reset token",
                error=e,
                extra={"user_id": str(user_id)}
            )
            raise TokenCreationError(detail=str(e))

    async def verify_token(self, token_string: str, token_type: str, user_id: Optional[str] = None) -> bool:
        """Verify if a given token is valid and not expired."""
        try:
            query = select(Token).where(
                and_(
                    Token.token == token_string,
                    Token.token_type == token_type,
                    Token.is_revoked == False,
                    Token.expires_at > datetime.now(pytz.UTC)
                )
            )
            
            if user_id:
                query = query.where(Token.user_id == user_id)
                
            result = await self._session.execute(query)
            token = result.scalar_one_or_none()
            
            if not token:
                return False
                
            if token.expires_at < datetime.now(pytz.UTC):
                raise TokenExpiredError("Token has expired")
                
            return True
        except TokenExpiredError:
            raise
        except Exception as e:
            app_logger.log_error(
                "Token verification failed",
                error=e,
                extra={"token_type": token_type}
            )
            raise
    
    async def get_valid_reset_token(self, token_string: str) -> Token:
        """
        Get and validate a password reset token.
        
        Args:
            token_string: The token string to validate
            
        Returns:
            Token: Valid token object
            
        Raises:
            InvalidTokenError: If token is invalid or not found
            TokenExpiredError: If token is expired
        """
        # Get the token with its associated user
         
        token = await self._session.scalar(
            select(Token).where(
                Token.token == token_string,
                Token.token_type == 'password_reset',
                Token.is_revoked == False
            )
        )
        
        if not token:
            raise InvalidTokenError("Invalid or expired reset token")

        # Check if token is expired
        if token.is_expired():
            # Revoke expired token
            token.is_revoked = True
            await self._session.commit()
            raise TokenExpiredError("Reset token has expired")

        return token

    async def get_active_token_with_user(self, token_string: str, token_type: str) -> Optional[Tuple[Token, User]]:
        """Get active token with associated user using ORM relationships"""
        result = await self._session.execute(
            select(Token, User)
            .join(User)
            .options(selectinload(Token.user))
            .where(
                and_(
                    Token.token == token_string,
                    Token.token_type == token_type,
                    Token.is_revoked == False,
                    Token.expires_at > datetime.now(pytz.UTC)
                )
            )
        )
        return result.first()

    async def revoke_token(self, token: Token) -> None:
        """Revoke a specific token"""
        try:
            query = update(Token).where(Token.id == token.id).values(is_revoked=True)
            await self._session.execute(query)
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise TokenCreationError(detail=f"Failed to revoke token: {str(e)}")

    async def revoke_all_user_tokens(self, user_id: str) -> None:
        """Revoke all tokens for a specific user"""
        try:
            query = update(Token).where(Token.user_id == user_id).values(is_revoked=True)
            await self._session.execute(query)
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise TokenCreationError(detail=f"Failed to revoke user tokens: {str(e)}")

    async def revoke_user_tokens_by_type(self, user_id: str, token_type: str) -> None:
        """Revoke all tokens of a specific type for a user"""
        try:
            query = update(Token).where(
                and_(
                    Token.user_id == user_id,
                    Token.token_type == token_type
                )
            ).values(is_revoked=True)
            await self._session.execute(query)
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise TokenCreationError(detail=f"Failed to revoke user tokens by type: {str(e)}")

    async def create_token_pair(self, user_id: str) -> Tuple[str, str]:
        """Create a new access/refresh token pair"""
        try:
            access_jwt = self.jwt_handler.create_access_token(subject=user_id)
            refresh_jwt = self.jwt_handler.create_refresh_token(subject=user_id)

            access_token = Token(
                user_id=user_id,
                token=access_jwt,
                token_type='access',
                expires_at=datetime.now(pytz.UTC) + timedelta(minutes=settings.access_token_expire_minutes)
            )

            refresh_token = Token(
                user_id=user_id,
                token=refresh_jwt,
                token_type='refresh',
                expires_at=datetime.now(pytz.UTC) + timedelta(days=settings.refresh_token_expire_days)
            )

            self._session.add(access_token)
            self._session.add(refresh_token)
            await self._session.commit()
            
            return access_jwt, refresh_jwt
        except Exception as e:
            await self._session.rollback()
            raise TokenCreationError(detail=str(e))

    async def verify_refresh_token(self, refresh_token: str) -> uuid.UUID:
        """Verify the refresh token and return the user_id"""
        try:
            payload = self.jwt_handler.decode_token(refresh_token)
            
            if payload.get("type") != "refresh_token":
                raise InvalidTokenError(detail="Invalid token type", status_code=401)
            
            try:
                user_id = uuid.UUID(payload.get("sub"))
            except (ValueError, TypeError):
                raise InvalidTokenError(detail="Invalid user ID format in token", status_code=401)
            
            result = await self._session.execute(
                select(Token).where(
                    and_(
                        Token.token == refresh_token,
                        Token.token_type == "refresh",
                        Token.is_revoked == False,
                        Token.expires_at > datetime.now(pytz.UTC)
                    )
                )
            )
            token = result.scalar_one_or_none()
            
            if not token:
                raise InvalidTokenError(detail="Refresh token not found or revoked", status_code=401)
                
            return user_id
        except Exception as e:
            if hasattr(e, 'status_code'):
                raise InvalidTokenError(detail=str(e), status_code=e.status_code)
            raise InvalidTokenError(detail=f"Error verifying refresh token: {str(e)}", status_code=401)

    async def refresh_access_token(self, refresh_token: str) -> Tuple[str, Token]:
        """Create a new access token using a valid refresh token."""
        try:
            user_id = await self.verify_refresh_token(refresh_token)
            access_jwt = self.jwt_handler.create_access_token(subject=str(user_id))
            
            access_token = Token(
                user_id=user_id,
                token=access_jwt,
                token_type='access',
                expires_at=datetime.now(pytz.UTC) + timedelta(minutes=settings.access_token_expire_minutes)
            )
            
            self._session.add(access_token)
            await self._session.commit()
            
            return access_jwt, access_token
        except Exception as e:
            await self._session.rollback()
            if isinstance(e, InvalidTokenError):
                raise
            raise TokenCreationError(detail=str(e))