from fastapi import APIRouter
from app.api.v1.endpoints.auth import router as auth_router


router = APIRouter()

@router.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "0.1.0"}

# Include all route modules
router.include_router(auth_router, prefix="/api/v1")