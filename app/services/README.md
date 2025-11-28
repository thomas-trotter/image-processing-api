# Services Module

## Overview

The `services` module contains the core business logic of the application. Services are organized by domain (image processing, object detection) and provide reusable, testable implementations of business operations.

## Architecture

Services follow a **Service Layer Pattern**, separating business logic from API concerns:

```
Managers (orchestration)
    ↓
Services (business logic) - this module
    ↓
Utilities & External Libraries
```

Services are organized into submodules:
- **`image/`**: Image processing, storage, and metadata services
- **`detection/`**: Object detection using ML models

## Components

### `image/` - Image Services

Image-related business logic services.

#### `image_editor.py` - Image Editing Service
Performs image transformations using PIL:
- Resize, rotate, convert formats
- Apply filters (blur, sharpen)
- Adjust properties (brightness, contrast)

#### `crud_operations.py` - Image CRUD Service
Handles Create, Read, Update, Delete operations:
- List images with pagination
- Get image metadata
- Delete images
- Move images between folders

#### `metadata_handler.py` - Metadata Extraction
Extracts image metadata:
- Dimensions (width, height)
- Format, mode, file size
- File path information

#### `storage/` - Storage Services
- **`base_storage.py`**: Abstract storage interface
- **`local_storage.py`**: Local filesystem storage implementation

### `detection/` - Detection Services

#### `detection_service.py` - Object Detection Service
Uses DETR (DEtection TRansformer) model for object detection:
- Detect objects in images
- Generate bounding boxes
- Extract detection results with confidence scores

**Model**: `facebook/detr-resnet-50` from Hugging Face

## Usage

### Service Initialization

Services use dependency injection:

```python
from app.services.image.image_editor import ImageEditService, get_image_edit_service

@router.post("/edit")
async def edit_image(
    service: ImageEditService = Depends(get_image_edit_service)
):
    result = service.resize_image("image.jpg", 800, 600)
    return result
```

### Error Handling

Services raise appropriate exceptions:

```python
if not image_path.exists():
    raise HTTPException(status_code=404, detail="Image not found")
```

### Logging

Services log operations for debugging:

```python
logger.info(f"Processing image: {image_name}")
# ... operation ...
logger.info(f"Completed: {image_name}")
```

## Design Patterns

### Service Layer Pattern
Services encapsulate business logic, making it:
- Reusable across different entry points
- Testable in isolation
- Independent of API framework

### Dependency Injection
Services receive dependencies through constructor injection, enabling:
- Easy mocking for tests
- Flexible configuration
- Loose coupling

### Strategy Pattern
Storage services use a base interface (`BaseImageStorage`) allowing different storage implementations (local, cloud, etc.).

## Dependencies

### Internal Dependencies
- **Utils**: `app/utils/` - Utility functions
- **Core**: `app/core/` - Configuration

### External Dependencies
- `PIL/Pillow`: Image processing
- `transformers`: ML models for detection
- `torch`: Deep learning framework
- `fastapi`: Dependency injection

## Related Documentation

- [Image Services](image/README.md)
- [Detection Services](detection/README.md)
- [Managers](../managers/README.md)
- [Main README](../../README.md)



