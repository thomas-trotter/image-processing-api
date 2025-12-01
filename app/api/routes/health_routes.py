"""
Health and root API routes.

This module defines system-level endpoints including the root endpoint
and health check endpoint for monitoring and Docker health checks.

For detailed documentation, see the module's README.md file.
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    tags=["System"]
)

@router.get("/")
async def root():
    """
    Root endpoint for the API.
    
    Returns:
        JSONResponse: Welcome message for the Image Processing API
    """
    return JSONResponse(
        status_code=200,
        content={"message": "Welcome to the Image Processing API"}
    )

@router.get("/health")
async def health():
    """
    Health check endpoint for monitoring and Docker health checks.
    
    Returns:
        JSONResponse: Status information indicating the API is healthy
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "Image Processing API",
            "version": "1.0.0"
        }
    )