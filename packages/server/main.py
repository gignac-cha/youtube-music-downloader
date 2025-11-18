"""FastAPI application main entry point."""

from contextlib import asynccontextmanager

from core.config import settings
from core.logging_config import setup_logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from presentation.routers import download, files, search


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    setup_logging(level=settings.log_level, json_format=settings.json_logging)
    yield
    # Shutdown
    pass


# Create FastAPI application
app = FastAPI(
    title="YouTube Music Downloader API",
    description="REST API for downloading and converting YouTube videos to MP3",
    version="0.2.0",
    lifespan=lifespan,
)

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
