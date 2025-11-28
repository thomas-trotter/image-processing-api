# Managers Module

## Overview

The `managers` module provides a coordination layer between API routes and service classes. Managers orchestrate business logic by combining multiple services and handling cross-cutting concerns like error handling and logging.

## Architecture

Managers follow the **Facade Pattern**, providing a simplified interface to complex service interactions:

```
API Routes
    ↓
Managers (this module) - Coordination & Orchestration
    ↓
Services - Business Logic
```

Each manager:
- Coordinates multiple service calls
- Handles business logic flow
- Provides a clean interface for routes
- Manages error handling and logging

## Components

### `image_manager.py` - Image Management

Orchestrates image storage, retrieval, and metadata operations.

**Responsibilities:**
- Save uploaded images
- Retrieve image paths and metadata
- List images with filtering
- Delete and move images
- Extract image dimensions and metadata

**Dependencies:**
- `DirectoryManager`: Directory path management
- `LocalImageStorage`: File storage operations
- `ImageCRUDService`: CRUD operations
- `ImageMetadataExtractor`: Metadata extraction

### `edit_manager.py` - Image Editing

Orchestrates image transformation operations.

**Responsibilities:**
- Apply image transformations (resize, rotate, filters)
- Coordinate editing service calls
- Handle bulk edit operations
- Process individual edit requests

**Dependencies:**
- `ImageEditService`: Image transformation operations

**Methods:**
- `apply_resize()`, `apply_grayscale()`, `apply_rotation()`
- `apply_blur()`, `apply_sharpen()`
- `apply_brightness()`, `apply_contrast()`
- `apply_bulk_edits()`: Apply multiple edits in sequence
- `process_image_edit()`: Generic edit processing with error handling

### `detection_manager.py` - Object Detection

Orchestrates object detection operations using ML models.

**Responsibilities:**
- Process images for object detection
- Generate bounding box visualizations
- Extract detected object summaries
- Handle detection errors

**Dependencies:**
- `ObjectDetectionService`: ML model operations

**Methods:**
- `process_image_for_detection()`: Full detection with bounding boxes
- `get_detected_objects_summary()`: Get detection results only

## Usage

### Dependency Injection

Managers are injected into routes via FastAPI's dependency system:

```python
from app.managers.image_manager import ImageManager, get_image_manager

@router.get("/images")
async def list_images(manager: ImageManager = Depends(get_image_manager)):
    return manager.list_images()
```

### Error Handling

Managers handle errors and convert them to appropriate HTTP exceptions:

```python
try:
    result = self.service.operation()
except Exception as e:
    logger.error(f"Operation failed: {e}")
    raise HTTPException(status_code=500, detail=str(e))
```

### Logging

All manager operations are logged:

```python
logger.info(f"Starting operation: {param}")
result = self.service.operation()
logger.info(f"Operation completed: {param}")
```

## Design Patterns

### Facade Pattern
Managers provide a simplified interface to complex service interactions, hiding implementation details from routes.

### Dependency Injection
All managers use FastAPI's dependency injection for services, enabling:
- Easy testing with mock services
- Loose coupling between layers
- Centralized service configuration

## Dependencies

### Internal Dependencies
- **Services**: `app/services/` - Business logic implementation
- **Core**: `app/core/` - Configuration and utilities

### External Dependencies
- `fastapi`: Dependency injection framework

## Related Documentation

- [Services](../services/README.md)
- [API Routes](../api/README.md)
- [Main README](../../README.md)



