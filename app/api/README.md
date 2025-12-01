# API Module

## Overview

The `api` module contains all FastAPI route definitions and endpoint handlers. It serves as the entry point for all HTTP requests and orchestrates interactions between clients and the application's business logic through managers and services.

## Architecture

The API module follows a layered architecture:

```
Client Request
    ↓
API Routes (this module)
    ↓
Managers (coordination layer)
    ↓
Services (business logic)
```

Routes are organized by functionality:
- **Image Routes**: CRUD operations for images
- **Editing Routes**: Image transformation endpoints
- **Detection Routes**: Object detection endpoints

## Components

### `routes/` - Route Handlers
- **image_routes.py**: Image management endpoints (upload, list, get, delete, move)
- **editing_routes.py**: Image editing endpoints (resize, rotate, filters, adjustments)
- **detection_routes.py**: Object detection endpoints (bounding boxes, detected objects)

Each route file:
- Defines FastAPI routers with appropriate prefixes and tags
- Uses **async route handlers** (`async def`) for non-blocking request processing
- Wraps synchronous operations in `asyncio.to_thread()` to prevent event loop blocking
- Applies rate limiting via decorators
- Uses dependency injection for managers
- Handles request validation and error responses
- Logs operations for debugging and monitoring

## Usage

### Route Organization

Routes are registered in `app/main.py`:

```python
from app.api.routes import image_routes, editing_routes, detection_routes

app.include_router(image_routes.router)
app.include_router(editing_routes.router)
app.include_router(detection_routes.router)
```

### Adding New Routes

1. Create route handler in appropriate `routes/` file
2. Apply rate limiting decorator
3. Use dependency injection for managers
4. Register router in `main.py`

Example:

```python
from fastapi import APIRouter, Depends, Request
from app.core.rate_limiting import limiter
import asyncio

router = APIRouter(prefix="/example", tags=["Example"])

@router.get("/")
@limiter.limit("10/minute")
async def example_endpoint(request: Request, manager: ManagerDep):
    # Wrap sync operations in asyncio.to_thread() to avoid blocking
    result = await asyncio.to_thread(manager.sync_operation, param)
    return {"message": "Success", "data": result}
```

## Endpoint Patterns

### Rate Limiting
All endpoints use rate limiting with different limits based on operation complexity:
- Simple operations: 20-60 requests/minute
- Complex operations (detection): 5-10 requests/minute
- Destructive operations (delete): 2-10 requests/minute

### Error Handling
- 400: Bad Request (validation errors)
- 404: Not Found (resource doesn't exist)
- 500: Internal Server Error (processing failures)

### Response Models
All endpoints use Pydantic response models defined in `schemas/` for consistent API responses.

## Dependencies

### Internal Dependencies
- **Managers**: `app/managers/` - Business logic coordination
- **Schemas**: `app/schemas/` - Request/response models
- **Core**: `app/core/` - Configuration, logging, rate limiting

### External Dependencies
- `fastapi`: Web framework
- `slowapi`: Rate limiting

## Related Documentation

- [Routes README](routes/README.md)
- [Managers](../managers/README.md)
- [Schemas](../schemas/README.md)
- [Main README](../../README.md)



