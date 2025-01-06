
from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.get("/me")
async def get_current_user_info():
    """Get current user's information"""
    return {"status": "healthy", "version": "0.1.0"}
