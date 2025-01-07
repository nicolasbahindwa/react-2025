from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.models.users import User
from app.repositories.base import BaseRepository
from app.core.logging import app_logger
from app.exceptions.database import DatabaseError
from app.utils.security import JWTHandler
from sqlalchemy.exc import SQLAlchemyError
from app.database.session import get_db_session, managed_transaction

class AuthRepository(BaseRepository):
    """
    Repository class for handling authentication-related database operations.
    Uses managed transactions for database operations.
    """
    
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        """
        Initialize with injected database session using FastAPI dependency.
        
        Args:
            session: AsyncSession from get_db_session dependency
        """
        super().__init__(session, User)
        self._session = session

    async def get_user_by_token(self, token: str) -> User:
        """
        Verify token and retrieve the associated user.
        Uses managed transaction for database operations.
        
        Args:
            token: JWT token string
            
        Returns:
            User: The authenticated user
            
        Raises:
            HTTPException: If token is invalid or user not found
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            # Decode the JWT token
            payload = JWTHandler.decode_token(token)
            
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception

            async with managed_transaction(self._session):
                # Get user from database
                query = select(User).filter(User.id == user_id)
                result = await self._session.execute(query)
                user = result.scalar_one_or_none()
                
                if user is None or not user.is_active:
                    raise credentials_exception
                    
                return user
                
        except Exception as e:
            app_logger.log_error(
                "Token validation failed",
                error=str(e),
                extra={"token": token[:10]}  # Log only first 10 chars of token
            )
            raise credentials_exception

    async def verify_active_user(self, user: User) -> User:
        """
        Verify if user is active.
        
        Args:
            user: User to verify
            
        Returns:
            User: The verified active user
            
        Raises:
            HTTPException: If user is inactive
        """
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )
        return user

    async def verify_admin_user(self, user: User) -> User:
        """
        Verify if user has admin privileges.
        
        Args:
            user: User to verify
            
        Returns:
            User: The verified admin user
            
        Raises:
            HTTPException: If user is not an admin
        """
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can perform this action"
            )
        return user

    async def get_all_users(self) -> List[User]:
        """
        Get all users from the database.
        Uses managed transaction for database operations.
        
        Returns:
            List[User]: List of all users
            
        Raises:
            DatabaseError: If database query fails
        """
        try:
            async with managed_transaction(self._session):
                query = select(User)
                result = await self._session.execute(query)
                return result.scalars().all()
        except SQLAlchemyError as e:
            app_logger.log_error(
                "Database error retrieving all users",
                error=str(e)
            )
            raise DatabaseError(f"Error retrieving users: {str(e)}")

# Dependency function to get repository instance
async def get_auth_repository(
    session: AsyncSession = Depends(get_db_session)
) -> AuthRepository:
    """
    Dependency to get AuthRepository instance with managed session.
    
    Args:
        session: AsyncSession from get_db_session dependency
        
    Returns:
        AuthRepository: Repository instance with active session
    """
    return AuthRepository(session)