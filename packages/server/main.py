"""FastAPI application main entry point."""

from contextlib import asynccontextmanager

from core.config import settings
from core.logging_config import setup_logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from presentation.middleware import SecurityHeadersMiddleware
from presentation.routers import download, files, search
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    setup_logging(level=settings.log_level, json_format=settings.json_logging)
    yield
    # Shutdown
    pass


# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.rate_limit_default],
    enabled=settings.rate_limit_enabled,
)

# Create FastAPI application
app = FastAPI(
    title="YouTube Music Downloader API",
    description="REST API for downloading and converting YouTube videos to MP3",
    version="0.2.0",
    lifespan=lifespan,
)

# Add rate limiter state and exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
if settings.cors_enabled:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Include routers
app.include_router(search.router)
app.include_router(download.router)
app.include_router(files.router)

# Mount static files if available
if settings.static_dir and settings.static_dir.exists():
    app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "0.2.0"}


@app.get("/")
async def root():
    """Root endpoint - serve index.html or API info."""
    return {
        "message": "YouTube Music Downloader API",
        "version": "0.2.0",
        "docs": "/docs",
    }
