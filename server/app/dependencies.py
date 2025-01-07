from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db_session
from app.repositories.base import BaseRepository
from app.repositories.post import PostRepository
from app.models.post import Post

# Type alias for dependency injection
DbSession = Annotated[Session, Depends(get_db_session)]

def get_post_repository(db: DbSession) -> PostRepository:
    """
    Get Post repository instance with database session.
    
    Args:
        db: Database session dependency
    
    Returns:
        PostRepository: Repository instance for Post model
    """
    return PostRepository(Post, db)

 

# Generic repository factory function
def get_repository(
    model: type,
    create_schema: type,
    update_schema: type,
    patch_schema: type,
) -> callable:
    """
    Factory function to create repository dependency functions.
    
    Args:
        model: SQLAlchemy model class
        create_schema: Pydantic create schema
        update_schema: Pydantic update schema
        patch_schema: Pydantic patch schema
    
    Returns:
        callable: Dependency function that returns a repository instance
    """
    def get_repo(db: DbSession) -> BaseRepository:
        return BaseRepository[model, create_schema, update_schema, patch_schema](model, db)
    return get_repo