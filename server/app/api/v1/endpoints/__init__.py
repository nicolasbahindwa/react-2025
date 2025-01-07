from fastapi import APIRouter
from app.api.v1.endpoints.posts import router as post_router
from app.api.v1.endpoints.users import router as user_router
from app.api.v1.endpoints.auth import router as auth_router
# from app.api.v1.endpoints.email import router as email_router


# Create main router
router = APIRouter()

# Add health check route to main router
@router.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}

# Include all route modules
router.include_router(post_router, prefix="/api/v1")
router.include_router(user_router, prefix="/api/v1")
router.include_router(auth_router, prefix="/api/v1")
# router.include_router(email_router, prefix="/api/v1")
# Add other routers as needed
# router.include_router(user_router, prefix="/api/v1")
# router.include_router(auth_router, prefix="/api/v1")
