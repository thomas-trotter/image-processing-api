"""
Main FastAPI application entry point.

This module initializes the FastAPI application and registers all route
handlers. It also configures the application lifespan for startup and
shutdown operations.

For detailed documentation, see the main README.md file.
"""

from fastapi import FastAPI

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

# Register all route handlers
app.include_router(image_routes.router)
app.include_router(editing_routes.router)
app.include_router(detection_routes.router)



