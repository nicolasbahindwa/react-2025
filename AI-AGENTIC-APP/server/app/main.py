from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import router
from app.config.settings import get_settings
from app.middleware.ip_address_middleware import IPAddressMiddleware
from contextlib import asynccontextmanager
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load any global configurations or resources
    settings = get_settings()
    logger.info("Application starting up...")
    yield
    # Shutdown: Clean up any resources
    logger.info("Application shutting down...")

# Initialize FastAPI with lifespan
app = FastAPI(
    lifespan=lifespan,
    title=get_settings().api_title,
    description=get_settings().api_description,
    version=get_settings().api_version,
    # Disable docs in development for faster reload
    # docs_url=None if get_settings().is_development else "/docs",
    # redoc_url=None if get_settings().is_development else "/redoc"
)

# Middleware configuration
middleware_config = [
    (IPAddressMiddleware, {}),
    (
        CORSMiddleware,
        {
            "allow_origins": (
                get_settings().allow_origins.split(",")
                if get_settings().allow_origins
                else ["*"]
            ),
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        },
    ),
]

# Add middleware efficiently
for middleware_class, config in middleware_config:
    app.add_middleware(middleware_class, **config)

# Performance monitoring middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.debug(f"Request processed in {process_time:.4f} seconds")
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Include routes
app.include_router(router)

# Optional: Add startup logging
@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application is ready")