from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.v1.endpoints import router
from app.database import init_db
# from app.config import Settings
from app.config import get_settings
from app.middleware.ip_address_middleware import IPAddressMiddleware
 

 

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
     
    # await init_db()
    yield
    # Shutdown
    # Add cleanup code here if needed

def create_application() -> FastAPI:
    """
    Factory function to create FastAPI application with all configurations
    """
    settings = get_settings()
    
    app = FastAPI(
        title=settings.API_TITLE,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION,
        lifespan=lifespan,
        docs_url=None if settings.is_production else "/docs",
        redoc_url=None if settings.is_production else "/redoc"
    )

    # Configure middlewares
    app.add_middleware(IPAddressMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routes
    app.include_router(router, prefix="/api/v1")

    return app

app = create_application()