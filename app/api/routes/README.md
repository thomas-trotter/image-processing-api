# Routes Module

## Overview

The `routes` module contains all FastAPI endpoint definitions organized by functionality. Each route file handles a specific domain of operations and follows consistent patterns for documentation, error handling, and rate limiting.

## Architecture

Routes are organized into three main categories:

1. **Image Management Routes** (`image_routes.py`): CRUD operations
2. **Image Editing Routes** (`editing_routes.py`): Transformations and filters
3. **Detection Routes** (`detection_routes.py`): Object detection operations

Each route file:
- Defines a FastAPI router with a unique prefix
- Uses dependency injection for managers
- Applies rate limiting based on operation complexity
- Includes comprehensive docstrings for FastAPI's automatic documentation

## Components

### `image_routes.py` - Image Management

Handles all image CRUD operations:

- **POST `/images/upload`**: Upload new images
- **GET `/images/`**: List images with filtering and pagination
- **GET `/images/{image_name}/detail`**: Get detailed image metadata
- **GET `/images/{image_name}/metadata/dimensions`**: Get image dimensions
- **DELETE `/images/{image_name}/delete`**: Delete a specific image
- **POST `/images/{image_name}/move`**: Move image between folders
- **DELETE `/images/clear_all`**: Delete all images in a folder

**Rate Limits**: 10-60 requests/minute depending on operation

### `editing_routes.py` - Image Editing

Handles image transformations and filters:

- **POST `/images/edit/resize`**: Resize images
- **POST `/images/edit/grayscale`**: Convert to grayscale
- **POST `/images/edit/rotate`**: Rotate images
- **POST `/images/edit/blur`**: Apply blur filter
- **POST `/images/edit/sharpen`**: Apply sharpening filter
- **POST `/images/edit/brightness`**: Adjust brightness
- **POST `/images/edit/contrast`**: Adjust contrast

**Rate Limits**: 10-20 requests/minute depending on operation complexity

### `detection_routes.py` - Object Detection

Handles object detection operations:

- **POST `/images/detect/bounding_boxes/`**: Detect objects and draw bounding boxes
- **GET `/images/detect/detected_objects/`**: Get list of detected objects

**Rate Limits**: 5-10 requests/minute (lower due to ML model processing)

## Usage Patterns

### Standard Route Structure

All route handlers are **async functions** that wrap synchronous operations to prevent blocking:

```python
from fastapi import APIRouter, Depends, Request, Query
from app.core.rate_limiting import limiter
import asyncio

@router.post("/endpoint", response_model=ResponseModel)
@limiter.limit("10/minute")
async def endpoint_handler(
    request: Request,
    manager: ManagerDep,
    param: str = Query(...)
):
    """
    Endpoint description.
    
    Args:
        param: Parameter description
    
    Returns:
        ResponseModel: Response description
    """
    # Wrap sync manager/service calls in asyncio.to_thread()
    # This prevents blocking the event loop during I/O or CPU-intensive operations
    result = await asyncio.to_thread(manager.sync_operation, param)
    return ResponseModel(data=result)
```

### Async/Sync Pattern

The codebase follows a consistent pattern for handling async/sync operations:

1. **Route handlers are async**: All endpoints use `async def` for non-blocking request handling
2. **Sync operations are wrapped**: Synchronous manager/service methods are wrapped in `asyncio.to_thread()`
3. **Benefits**: 
   - Multiple requests can be processed concurrently
   - File I/O and CPU-intensive tasks don't block the event loop
   - Better resource utilization and scalability

### Error Handling

Routes use FastAPI's exception handling with async operations:

```python
try:
    # Async operation with sync wrapper
    result = await asyncio.to_thread(manager.operation, param)
except HTTPException:
    raise  # Re-raise HTTP exceptions
except Exception as e:
    logger.error(f"Error: {e}")
    raise HTTPException(status_code=500, detail=str(e))
```

### Logging

All routes log operations:

```python
logger.info(f"Operation started: {param}")
# ... operation ...
logger.info(f"Operation completed: {param}")
```

## Documentation

FastAPI automatically generates interactive API documentation from route docstrings. Docstrings use markdown formatting for better readability in the `/docs` endpoint.

## Dependencies

### Internal Dependencies
- **Managers**: Business logic coordination
  - `ImageManager` for image operations
  - `EditManager` for editing operations
  - `DetectionManager` for detection operations
- **Schemas**: Request/response models
- **Core**: Rate limiting, logging

### External Dependencies
- `fastapi`: Web framework
- `slowapi`: Rate limiting

## Related Documentation

- [API Module README](../README.md)
- [Managers](../../managers/README.md)
- [Main README](../../../README.md)



