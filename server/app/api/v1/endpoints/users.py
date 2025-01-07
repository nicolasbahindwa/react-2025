from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserUpdate, UserPatch, UserResponse
from app.schemas.common import PaginatedResponse
from app.repositories.user import UserRepository
from app.database.session import get_db
from uuid import UUID
from app.services.token_service import TokenService
from app.services.auth_service import AuthService
from app.models.users import User

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: Request,
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new user"""
    repo = UserRepository(db)
    client_ip = request.state.client_ip
    return await repo.create(user_in, client_ip)

@router.get("/", response_model=PaginatedResponse[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    order_by: Optional[List[str]] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """List users with pagination"""
    repo = UserRepository(db)
    return await repo.get_all(skip=skip, limit=limit, order_by=order_by)

@router.get("/search", response_model=PaginatedResponse[UserResponse])
async def search_users(
    q: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Search users by any field"""
    repo = UserRepository(db)
    return await repo.get_by_any_field(q, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific user by ID"""
    repo = UserRepository(db)
    return await repo.get_by_id(user_id)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a user"""
    repo = UserRepository(db)
    return await repo.update(id=user_id, schema=user_in)

@router.patch("/{user_id}", response_model=UserResponse)
async def patch_user(
    user_id: UUID,
    user_in: UserPatch,
    db: AsyncSession = Depends(get_db)
):
    """Partially update a user"""
    repo = UserRepository(db)
    return await repo.patch(id=user_id, schema=user_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete a user"""
    repo = UserRepository(db)
    await repo.delete(user_id)
    


