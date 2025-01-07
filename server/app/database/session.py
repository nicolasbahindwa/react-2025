# from typing import AsyncGenerator
# from fastapi import Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
# from app.config import settings
# from contextlib import asynccontextmanager
# from app.exceptions.database import DatabaseError


# # Create SQLAlchemy engine
# engine = create_async_engine(
#     url = settings.database_url,
#     echo=True,  # Enable SQLAlchemy logging
#     pool_pre_ping=True,  # Enable connection pool "pre-ping" feature
#     pool_size=5,  # Set initial pool size
#     max_overflow=10  # Allow up to 10 connections beyond pool_size
# )
# # Create sessionmaker
# AsyncSessionLocal = async_sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False
# )

# @asynccontextmanager
# async def managed_transaction(session:AsyncSession):
#     """Async context manager for handling database transactions.
#     Automatically handles commit and rollback.
#     """
#     try:
#         yield
#         await session.commit()
#     except Exception as e:
#         await session.rollback()
#         raise DatabaseError(f"Transaction faild: {str(e)}")

# async def get_db() -> AsyncGenerator[AsyncSession, None]:
#     """Async database session dependency."""
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#         finally:
#             await session.close()

# async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
#     """
#     Create a new async database session and ensure it's closed after use.
    
#     Yields:
#         AsyncSession: SQLAlchemy async database session
#     """
#     async for session in get_db():
#         yield session

# async def get_session(session: AsyncSession = Depends(get_db_session)) -> AsyncSession:
#     """
#     Dependency to get async database session.
    
#     Args:
#         session: AsyncSession from get_db_session dependency
        
#     Returns:
#         AsyncSession: Active database session
#     """
#     return session

from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config import get_settings
from contextlib import asynccontextmanager
from app.exceptions.database import DatabaseError
import logging

logger = logging.getLogger(__name__)

# Get settings instance
settings = get_settings()

# Debug: Print DATABASE_URL
print(f"DATABASE_URL: {settings.DATABASE_URL}")

# Create SQLAlchemy engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Enable SQLAlchemy logging
    pool_pre_ping=True,  # Enable connection pool "pre-ping" feature
    pool_size=5,  # Set initial pool size
    max_overflow=10,  # Allow up to 10 connections beyond pool_size
)

# Create sessionmaker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

@asynccontextmanager
async def managed_transaction():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Transaction failed: {str(e)}")
            raise DatabaseError(f"Transaction failed: {str(e)}")
        finally:
            await session.close()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {str(e)}")
            raise DatabaseError(f"Database session error: {str(e)}")
        finally:
            await session.close()

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db():
        yield session

async def get_session(db: AsyncSession = Depends(get_db)) -> AsyncSession:
    return db
