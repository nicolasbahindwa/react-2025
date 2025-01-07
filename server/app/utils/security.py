from datetime import datetime, timedelta
from typing import Optional, Union
from jose import jwt, JWTError
from fastapi import HTTPException
from uuid import UUID
from app.config import settings
import pytz
from app.exceptions.database import TokenCreationError, TokenExpiredError, InvalidTokenError

class JWTHandler:
    @staticmethod
    def _current_utc_time() -> datetime:
        """Utility method to get current UTC time."""
        return datetime.now(pytz.UTC)

    @staticmethod
    def create_access_token(
        subject: Union[str, UUID],
        expires_delta: Optional[timedelta] = None,
        claims: dict = None
    ) -> str:
        """Creates an access token."""
        expires_delta = expires_delta or timedelta(minutes=settings.access_token_expire_minutes)

        jwt_claims = {
            "type": "access_token",
            "exp": int(JWTHandler._current_utc_time().timestamp() + expires_delta.total_seconds()),
            "iat": int(JWTHandler._current_utc_time().timestamp()),
            "sub": str(subject)
        }

        if claims:
            jwt_claims.update(claims)

        try:
            return jwt.encode(
                jwt_claims,
                settings.jwt_secret_key,
                algorithm=settings.jwt_algorithm
            )
        except Exception as e:
            raise TokenCreationError(detail=str(e))

    @staticmethod
    def create_refresh_token(
        subject: Union[str, UUID],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Creates a refresh token."""
        expires_delta = expires_delta or timedelta(days=settings.refresh_token_expire_days)

        jwt_claims = {
            "type": "refresh_token",
            "exp": int(JWTHandler._current_utc_time().timestamp() + expires_delta.total_seconds()),
            "iat": int(JWTHandler._current_utc_time().timestamp()),
            "sub": str(subject)
        }

        try:
            return jwt.encode(
                jwt_claims,
                settings.jwt_refresh_secret_key,  # Using refresh secret key
                algorithm=settings.jwt_algorithm
            )
        except Exception as e:
            raise TokenCreationError(detail=str(e))

    @staticmethod
    def decode_token(token: str, is_refresh: bool = False) -> dict:
        """Decodes a JWT token and verifies it."""
        try:
            # Use appropriate secret key based on token type
            secret_key = settings.jwt_refresh_secret_key if is_refresh else settings.jwt_secret_key
            payload = jwt.decode(token, secret_key, algorithms=[settings.jwt_algorithm])
            
            # Verify token type
            expected_type = "refresh_token" if is_refresh else "access_token"
            if payload.get("type") != expected_type:
                raise InvalidTokenError(f"Invalid token type. Expected {expected_type}")
                
            return payload
        except JWTError as e:
            if "expired" in str(e).lower():
                raise TokenExpiredError()
            raise InvalidTokenError(str(e))
