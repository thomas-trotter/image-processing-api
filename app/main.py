"""
Main FastAPI application entry point.

This module initializes the FastAPI application and registers all route
handlers. It also configures the application lifespan for startup and
shutdown operations.

For detailed documentation, see the main README.md file.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.routes import detection_routes, image_routes, editing_routes
from app.utils.system.lifespan import lifespan

description = """
This API allows users to upload, manage, and process images.

## The following directories are used:
By default, images are stored in the following folders:
1. **Uploaded** - Folder for uploaded images.
2. **Edited** - Folder for edited images.
3. **Detected** - Folder for detected image outputs.

## Features:
- Image upload and management
- Image editing and transformations
- Object detection using DETR model
- Comprehensive API documentation at /docs
"""

app = FastAPI(
    title="Image Processing API",
    description=description,
    lifespan=lifespan
)

@app.get("/health", tags=["Health"])
async def health_check():
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

# Register all route handlers
app.include_router(image_routes.router)
app.include_router(editing_routes.router)
app.include_router(detection_routes.router)



